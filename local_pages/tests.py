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
