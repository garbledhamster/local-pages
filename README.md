# Local Pages

Local Pages is a planned self-hosted service for publishing project documentation and browser builds from Git repositories. You choose what to publish in a browser and open the published sites from a directory on your network. The first release will support Gitea, GitHub, and GitLab on Linux with Docker Compose.

The project is in Chapter 3, Engine & Assets.

## Project files

- [Project Bible](docs/game-bible.md) records the release scope, evidence, and open decisions.
- [Glossary](CONTEXT.md) defines the terms used in Local Pages.
- `docs/bible-upstream/` contains the shared Project Bible guide and templates as a Git submodule. After cloning, run `git submodule update --init -- docs/bible-upstream`.
