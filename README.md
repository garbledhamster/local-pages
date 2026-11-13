# Local Pages

Local Pages is a planned self-hosted service for publishing project documentation and browser builds from Git repositories. You choose what to publish in a browser and open the published sites from a directory on your network. The first release will support Gitea, GitHub, and GitLab on Linux with Docker Compose.

The project is in Chapter 3, Engine & Assets.

## Try the first runnable example

The example opens a sample HTML Page from a signed-in directory. Use a local Docker Compose installation and a browser that resolves `.localhost` names to your computer.

```sh
python3 -c 'import secrets; print("LOCAL_PAGES_SECRET_KEY=" + secrets.token_hex(32))' > .env
docker compose build
docker compose run --rm app python manage.py migrate
docker compose run --rm app python manage.py createsuperuser
docker compose up
```

Open [the directory](http://pages.localhost:8000/) and sign in with the account you created. Open **Welcome** and sign in on that hostname to view the sample Page. Use this setup on loopback for development. The Blackbox pilot uses HTTPS.

To run the Django checks with Python 3.12, create a virtual environment, install `requirements.txt`, and run `python manage.py test`.

## Project files

- [Project Bible](docs/game-bible.md) records the release scope, evidence, and open decisions.
- [Glossary](CONTEXT.md) defines the terms used in Local Pages.
- `docs/bible-upstream/` contains the shared Project Bible guide and templates as a Git submodule. After cloning, run `git submodule update --init -- docs/bible-upstream`.
