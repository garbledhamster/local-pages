from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase


class EngineSmokeTest(TestCase):
    def setUp(self):
        self.reader = get_user_model().objects.create_user(
            username="reader", password="reader-test-password"
        )

    def test_reader_opens_directory_and_protected_example(self):
        for host in (settings.BASE_HOST, settings.PAGE_HOST):
            with self.subTest(host=host):
                response = self.client.get("/", HTTP_HOST=host)
                self.assertRedirects(response, "/accounts/login/?next=/", fetch_redirect_response=False)

        login = self.client.post(
            "/accounts/login/",
            {"username": "reader", "password": "reader-test-password"},
            HTTP_HOST=settings.BASE_HOST,
        )
        self.assertRedirects(login, "/", fetch_redirect_response=False)
        directory = self.client.get("/", HTTP_HOST=settings.BASE_HOST)
        self.assertContains(directory, f"http://{settings.PAGE_HOST}/")

        # Each hostname has its own session cookie. Use a separate client to model that.
        page_client = self.client_class()
        self.assertEqual(page_client.get("/", HTTP_HOST=settings.PAGE_HOST).status_code, 302)
        login = page_client.post(
            "/accounts/login/",
            {"username": "reader", "password": "reader-test-password", "next": "/"},
            HTTP_HOST=settings.PAGE_HOST,
        )
        self.assertRedirects(login, "/", fetch_redirect_response=False)
        self.assertEqual(login.cookies[settings.SESSION_COOKIE_NAME]["domain"], "")
        page = page_client.get("/", HTTP_HOST=settings.PAGE_HOST)
        self.assertContains(page, "Welcome to Local Pages")
        self.reader.is_active = False
        self.reader.save(update_fields=["is_active"])
        response = page_client.get("/", HTTP_HOST=settings.PAGE_HOST)
        self.assertEqual(response.status_code, 302)


class AdminPublishingTest(TestCase):
    def test_operator_publishes_a_page_and_bad_update_keeps_live_files(self):
        import subprocess
        from pathlib import Path
        from tempfile import TemporaryDirectory

        operator = get_user_model().objects.create_user(username="operator", is_staff=True)
        self.client.force_login(operator)
        with TemporaryDirectory() as folder:
            repo = Path(folder) / "source"
            repo.mkdir()

            def git(*args):
                subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)

            git("init", "-b", "main")
            git("config", "user.name", "Local Pages test")
            git("config", "user.email", "test@example.com")
            (repo / "site").mkdir()
            (repo / "site" / "reader").mkdir()
            entry = repo / "site" / "reader" / "index.html"
            entry.write_text("<h1>Published from Git</h1>")
            (entry.parent / "app.js").write_text("console.log('ready')")
            (repo / "site" / "notes.md").write_text("# Raw notes")
            (repo / "private.txt").write_text("outside publish folder")
            git("add", ".")
            git("commit", "-m", "Add test site")
            with self.settings(PUBLISH_ROOT=Path(folder) / "published", ALLOW_FILE_REPOSITORIES=True):
                response = self.client.post("/admin/add/", {
                    "action": "publish",
                    "title": "Test Bible",
                    "slug": "test-bible",
                    "provider": "gitea",
                    "repository": repo.as_uri(),
                    "branch": "main",
                    "folder": "site",
                    "entry": "reader/index.html",
                }, HTTP_HOST=settings.BASE_HOST)
                self.assertEqual(response.status_code, 302)
                self.assertContains(self.client.get("/", HTTP_HOST=settings.BASE_HOST), "Test Bible")
                host = f"test-bible.{settings.BASE_HOST}"
                self.assertRedirects(self.client.get("/", HTTP_HOST=host), "/reader/index.html",
                                     fetch_redirect_response=False)
                self.assertContains(self.client.get("/reader/index.html", HTTP_HOST=host), "Published from Git")
                self.assertContains(self.client.get("/reader/app.js", HTTP_HOST=host), "ready")
                raw = self.client.get("/notes.md", HTTP_HOST=host)
                self.assertEqual(raw["Content-Type"], "text/plain; charset=utf-8")
                self.assertContains(raw, "# Raw notes")
                self.assertEqual(self.client.get("/private.txt", HTTP_HOST=host).status_code, 404)

                from io import StringIO

                from django.core.management import call_command

                entry.write_text("<h1>Updated by the scheduled command</h1>")
                git("add", "-u")
                git("commit", "-m", "Update entry")
                output = StringIO()
                call_command("refresh_pages", stdout=output)
                self.assertIn("test-bible: published", output.getvalue())
                self.assertContains(self.client.get("/reader/index.html", HTTP_HOST=host),
                                    "Updated by the scheduled command")

                entry.unlink()
                git("add", "-u")
                git("commit", "-m", "Remove entry")
                response = self.client.post("/admin/test-bible/refresh/", HTTP_HOST=settings.BASE_HOST)
                self.assertContains(response, "Entry file")
                self.assertContains(self.client.get("/reader/index.html", HTTP_HOST=host),
                                    "Updated by the scheduled command")

                operator.is_staff = False
                operator.save(update_fields=["is_staff"])
                self.assertEqual(self.client.get("/admin/add/", HTTP_HOST=settings.BASE_HOST).status_code, 403)
                self.assertEqual(self.client_class().get("/reader/app.js", HTTP_HOST=host).status_code, 302)
