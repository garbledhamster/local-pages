# Local Pages

Local Pages is a planned self-hosted service for publishing project documentation and browser builds from Git repositories. You choose what to publish in a browser and open the published sites from a directory on your network. The first release will support Gitea, GitHub, and GitLab on Linux with Docker Compose.

The project is in Chapter 4, Development Sandbox.

## Try the first runnable example

The example opens a sample HTML Page from a signed-in directory and lets an operator publish a Page from Git. Use a local Docker Compose installation and a browser that resolves `.localhost` names to your computer.

```sh
python3 -c 'import secrets; print("LOCAL_PAGES_SECRET_KEY=" + secrets.token_hex(32))' > .env
docker compose build
docker compose run --rm app python manage.py migrate
docker compose run --rm app python manage.py createsuperuser
docker compose up
```

Open [the directory](http://pages.localhost:8000/) and sign in with the account you created. Open **Welcome** and sign in on that hostname to view the sample Page. Use this setup on loopback for development. The Blackbox pilot uses HTTPS.

To publish a Page, open **Manage Pages → Add Page**. Paste the Git clone URL and enter a Git username and read-only token for a private repository. Check the available branches, then choose the branch, publish folder, and entry file. Enter `.` for the branch root. Use `index.html` or a Markdown file such as `README.md` as the entry. Use **Publish now** to refresh a published Page.

Run `docker compose exec -T app python manage.py refresh_pages` to check all published Pages. For automatic refresh, run that command every five minutes using the host scheduler. Run it from the directory containing `compose.yaml` and `.env`.

Keep `LOCAL_PAGES_SECRET_KEY` with your database backup. Local Pages uses it to encrypt saved Git credentials. Use HTTPS for repository URLs. To allow a trusted internal Git server over HTTP, set `LOCAL_PAGES_INSECURE_GIT_HOSTS` to its hostname or IP address. Use `LOCAL_PAGES_HTTPS=1` behind a trusted HTTPS reverse proxy that sets `X-Forwarded-Proto` and keeps the app port private.

To run the Django checks with Python 3.12, create a virtual environment, install `requirements.txt`, and run `python manage.py test`.

## Project files

- [Project Bible](docs/game-bible.md) records the release scope, evidence, and open decisions.
- [Glossary](CONTEXT.md) defines the terms used in Local Pages.
- `docs/bible-upstream/` contains the shared Project Bible guide and templates as a Git submodule. After cloning, run `git submodule update --init -- docs/bible-upstream`.
