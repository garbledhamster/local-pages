# Project Bible

Local Pages

- Current stage: Chapter 1, Vision & Scope.
- Next decisions: Confirm the Page address, refresh behavior, and first-release verification.

## Vision & Scope

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

### Open decisions

- What address should a new Page get, and when can the operator choose another?
- How soon should a push show up on a Page?
- What does another operator need to prove before the first shareable release?
- How should the admin present source choices and publishing status? Carry this into the Design Document.

## Design Document
- Core workflow and intended experience:
- For each rule or interaction: input, rule, feedback, success, failure, and recovery:
- Screens or scenes and their dependencies:
- Open design decisions:

## Engine and Assets
- Engine and launch instructions:
- Maps, characters, objects, interface, art, and sound:
- Asset locations and readiness:

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
