# Project Bible

Local Pages

- Current stage: Chapter 3, Engine & Assets.
- Next check: Run the Compose example from a clean Linux checkout, then prove publishing through the admin.

## Vision & Scope

Scope confirmed on November 13, 2026.

### Project folder and Git

The standalone [Local Pages repository](https://github.com/garbledhamster/local-pages) is the public home for the project. The [README](../README.md) maps the files. The shared Project Bible guide is pinned under `docs/bible-upstream`.

### What the operator should be able to do

Sign in to the admin, pick a Git provider, repository, branch, and source, then publish to a site address. The root directory lists published Pages so people can find the one they need. The intended sources include HTML, a rendered Markdown entry file, and static build output. The first deployment is internal. Local Pages runs alongside Gitea so operators can update Gitea through its official channels.

### Similar projects

- [GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site) offers branch and workflow publishing. Use its source setup to evaluate how much an operator needs to configure for a first Page.
- [Codeberg Pages](https://docs.codeberg.org/codeberg-pages/) publishes static sites using Git and supports custom domains. Compare its branch and URL setup when defining how Local Pages maps sources to addresses.
- [Coolify](https://coolify.io/docs/applications/) deploys applications from Git. Compare its setup with the narrower workflow for publishing a folder of already-built files.

### Who we’re building for

Joe is the first operator. The first release should make his publishing workflow simple and give other self-hosters a setup they can repeat. Linux with Docker Compose is the supported installation target. Readers sign in to open the directory and published Pages.

### Product and interface direction

Keep the service straightforward to install, use, and maintain. Add components when the publishing workflow needs them. Give the directory and admin each a clear purpose. Use spacing, borders, and text hierarchy to show where to go, what is live, and what needs attention. Check both views at the screen sizes operators and readers will use.

### First milestone and release scope

Use Island Post to prove the first installation. In the admin, publish its Project Bible reader and an already-built playable browser preview. Open both from the directory, push an update, and check that the same addresses serve the new versions. This check covers publishing prebuilt files.

The first shareable release supports Gitea, GitHub, GitLab.com, and self-managed GitLab. Prove the Gitea workflow on the first deployment, then verify the remaining connections before release.

Ship a Codex plugin, MCP setup, and repo-level agent instructions. An agent can install, update, check status, and diagnose the service, then hand over the admin URL. The operator connects repositories and creates, publishes, and disables Pages in the web admin.

### Page addresses and updates

The directory lives at the configured base hostname. When you add a Page, the admin suggests a subdomain you can edit before publishing, such as `island-post.pages.example.com`. The operator sets up the directory hostname and a wildcard DNS entry for the project sites. See [the address decision](adr/0001-use-a-subdomain-for-each-page.md).

Local Pages checks the selected branches every few minutes across all supported providers. Use **Publish now** in the admin to request a refresh without waiting for the next check.

### How we’ll verify the release

- Start with a fresh Linux host and install with Docker Compose using the public repo instructions.
- Verify that an agent using the Codex plugin and MCP setup can get the service running and hand over the admin URL.
- Sign in, connect private repositories, and publish one Page from Gitea, GitHub, GitLab.com, and self-managed GitLab. Open each Page from the directory. Verify that signed-out visitors cannot open the directory or published Pages.
- On the Island Post pilot, open the Bible and play the browser preview. Push an update and verify that both existing addresses serve the expected versions after refresh. Check **Publish now** as well.

### Decisions for the Design Document

Work through how operators connect a provider, choose an HTML or Markdown entry or build folder, and see the result of a publish. Use the Island Post reader and browser preview to check that the flow makes sense for both sources.

## Design Document

Workflow confirmed on November 13, 2026.

### Core workflow

The operator opens the admin URL from the installation handoff, signs in, and chooses **Add Page**.

1. Choose Gitea, GitHub, or GitLab, paste the repository URL, and provide a read-only credential. The admin checks access and loads the branches. If the connection fails, explain what to check and let the operator retry.
2. Select a branch and a publish folder. Choose the entry file inside that folder. Suggest `index.html` for an HTML site or `README.md` for Markdown. The operator can choose a nested entry, such as `docs/reader/index.html`, while keeping the files it links to inside the publish folder.
3. Review the suggested subdomain and publish. The Bible reader and playable preview can each have a Page sourced from the same repository. Open each address to check the result.

A reader signs in with an individual account. Each active account can open the directory and every published Page, including through direct links. The operator creates reader accounts and removes access from the admin.

### Preparing files for a Page

Each project commits its finished files to a branch or folder. Local Pages serves those files. For the Island Post pilot, prepare a publish folder for the Bible with its shared guide files, linked assets, and evidence. Prepare another folder for the finished browser build. Set up each folder as a separate Page.

### Screens

- **Directory.** Show published Pages by name with a link to each site. Keep the focus on finding and opening a Page.
- **Admin.** Show the Page name, live address, and publish status. Give the operator a place to add a Page, edit its settings, publish now, and disable it.
- **Page setup.** Bring the source, editable subdomain, and publish action together. Show where the Page will open before the operator publishes.
- **Readers.** Let the operator create individual reader accounts and remove access.

### Proposed behavior to verify

| Situation | What the operator or reader sees |
| --- | --- |
| First publish succeeds | The Page has a working link in the admin and appears in the directory. |
| The service finds a new commit on the selected branch | The same address serves the new version after publishing succeeds. **Publish now** checks immediately. |
| An update fails after the Page has gone live | The previous version stays available. The admin shows what failed and lets the operator retry. |
| The operator disables a Page | The directory stops listing it and the site address stops serving its content. |
| A signed-out reader opens the directory or a Page directly | The reader must sign in before viewing the content. |
| The operator removes a reader account | The reader loses access to the directory and all published Pages, including in an existing session. |

### Checks for the Island Post pilot

- Add both Pages from the admin and open them from the directory. Check that the Bible entry opens and that its styles, scripts, and linked files load. Play the browser preview from its own address.
- Push updated files for both Pages and check that the same addresses serve the new versions. Try **Publish now**, then try an update with a missing entry file and check that the previous version stays available and the admin shows the failure.
- Create a reader account, sign in, and open both Pages. Remove the account and check that the directory and direct Page links require access again, including in the same browser session.

## Engine & Assets

### Application stack

Use Django 5.2 LTS, SQLite, server-rendered HTML, and Docker Compose. Django supplies user accounts, sessions, and permissions. Local Pages uses its own directory and publishing screens. Keep the database and published snapshots on persistent storage. One application handles publishing and account access for the first release. See [Django authentication](https://docs.djangoproject.com/en/5.2/topics/auth/) and [Django's SQLite notes](https://docs.djangoproject.com/en/5.2/ref/databases/#sqlite-notes).

### HTTPS on the pilot host

The directory hostname and wildcard Page hostnames need HTTPS. Use Caddy with Cloudflare DNS validation to issue a browser-trusted certificate for the pilot. The network's DNS resolver points both hostnames to the private server. Other operators can bring an HTTPS reverse proxy they already run. See [Caddy's DNS challenge documentation](https://caddyserver.com/docs/automatic-https#dns-challenge).

### What the first running example needs

- **Directory.** A simple list of published Pages with clear names and links. Check the layout on desktop and phone.
- **Admin and Page setup.** A list of Pages with their live addresses and publish status, plus a form for the repository, branch, publish folder, entry file, and subdomain. Give a failed publish enough room to show what happened and how to retry.
- **Pilot content.** Use the Island Post reader, including the shared guide files and linked assets, and a prebuilt playable preview. Verify that both run at their own subdomains.

### Clean checkout check

The [README](../README.md#try-the-first-runnable-example) shows how to launch the sample with Docker Compose. It includes a signed-in directory and a checked-in HTML Page on its own hostname. The sample signs in on each hostname separately.

On November 13, 2026, the Django test verified anonymous redirects, protected content, and loss of access after deactivating an account. Chrome opened the directory and sample at 1280 and 390 pixels. The Compose configuration parsed on Blackbox. Running the container from a clean Linux checkout, configuring pilot HTTPS, and publishing an HTML Page from the admin remain to be verified.

## Development Sandbox
- Dedicated development scene to build before player-scene assembly:
- Release mechanics, assets, controls, objects, and outcomes reachable from that scene:
- Development entry point or test-build shortcut:
- NPC roster picker and dialogue branches to exercise, including the states that change each conversation:
- Playable cases for every release mechanic and the other applicable checks from the Development Sandbox chapter:
- For each case, record the named starting state, the object or control to use in the scene, what the player should see, and how to reset:
- Record build, platform, observed result, and evidence:
- Open failures and next checks:

## Scene Scripts and Playtests
- For each scene: entry, player objective, actions, dialogue, outcomes, and transitions:
- Mechanics and assets used:
- Playtest criteria, observations, fixes, and result:

## Build and Play the Game
- Startup scene, build targets, source revision, and build or export steps:
- Versioned installer, app package, or staged browser build:
- Clean install or fresh launch, core playthrough, and results by target:

## Player Manual and Wiki
- In-game How to Play outline:
- Wiki topics and screenshots:
- Published references:

## Release Pricing and Marketing
- Release scope, delivery platform, price, and payment:
- Readiness checks and release evidence:
- Store copy, screenshots, pitch scripts, and distribution links:

## Contributor Training
- Setup, first task, and verification instructions:
- Decisions and references a contributor needs:

## Updates and DLC
- Proposed changes, affected players, and release approach:
- Sandbox, scene, and compatibility checks:
- Manual, wiki, and release note updates:

## Intake and Feedback
- Who we want to hear from, including prospects, current players, and customers:
- Where feedback comes in and how we ask for it:
- Who reads each channel, replies, and follows up:
- What people said or did, with the source, date, and context:
- What came up repeatedly, what needs attention now, and what needs another conversation:
- What evidence goes back to Chapter 1, what we’ll change, and how we’ll check it:
