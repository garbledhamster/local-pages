# Project Bible

Local Pages

- Current stage: Chapter 1, Vision & Scope.
- Next decision: Confirm the first operator, supported host environment, and first-release access boundary.

## Vision & Scope

### Project folder and Git

The standalone [Local Pages repository](https://github.com/garbledhamster/local-pages) is the public home for the project. The [README](../README.md) maps the files. The shared Project Bible guide is pinned under `docs/bible-upstream`.

### What the operator should be able to do

Sign in to the admin, pick a Git provider, repository, branch, and source, then publish to a site address. The root directory lists published Pages so people can find the one they need. The intended sources include HTML, a rendered Markdown entry file, and static build output. The first deployment is internal. Local Pages runs alongside Gitea so operators can update Gitea through its official channels.

### Similar projects

- [GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site) offers branch and workflow publishing. Use its source setup to evaluate how much an operator needs to configure for a first Page.
- [Codeberg Pages](https://docs.codeberg.org/codeberg-pages/) publishes static sites using Git and supports custom domains. Compare its branch and URL setup when defining how Local Pages maps sources to addresses.
- [Coolify](https://coolify.io/docs/applications/) deploys applications from Git. Compare its setup with the narrower workflow for publishing a folder of already-built files.

### First playable milestone and release scope

A proposed first check is to add one Page from a private Gitea repo through the admin, open it from the directory, then push a content change and see it at the same URL. Confirm the audience, host environment, access boundary, and whether GitHub is part of that first milestone before treating this as release scope.

### Open decisions

- Who should be able to install and operate the first release?
- Which host environment will the first release document and verify?
- Who can view the directory and published Pages?
- Which sources, providers, and addresses belong in the first release?
- What proves that the first release is ready for another operator to try?

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
