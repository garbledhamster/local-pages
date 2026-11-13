import base64
import hashlib
import json
import os
import shutil
import subprocess
import tarfile
from pathlib import Path, PurePosixPath
from tempfile import TemporaryDirectory
from urllib.parse import urlsplit
from uuid import uuid4

from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings


class PublishError(Exception):
    pass


def credential_box():
    key = hashlib.sha256(("local-pages-git:" + settings.SECRET_KEY).encode()).digest()
    return Fernet(base64.urlsafe_b64encode(key))


def git(args, *, cwd=None, repository="", username="", token="", output=None):
    env = {
        **os.environ,
        "GIT_TERMINAL_PROMPT": "0",
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_CONFIG_COUNT": "0",
    }
    if token:
        auth = base64.b64encode(f"{username}:{token}".encode()).decode()
        env.update(GIT_CONFIG_COUNT="1", GIT_CONFIG_KEY_0=f"http.{repository}.extraHeader",
                   GIT_CONFIG_VALUE_0=f"Authorization: Basic {auth}")
    protocols = "http:https:file" if settings.ALLOW_FILE_REPOSITORIES else "http:https"
    env["GIT_ALLOW_PROTOCOL"] = protocols
    try:
        result = subprocess.run(
            ["git", "-c", "http.followRedirects=false", *args], cwd=cwd, env=env,
            stdin=subprocess.DEVNULL, stdout=output if output is not None else subprocess.PIPE,
            stderr=subprocess.DEVNULL, check=True, timeout=45,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        raise PublishError("Git could not read this repository or branch. Check the address and read access.") from exc
    return result.stdout.decode().strip() if result.stdout is not None else ""


def branches(repository, username, token):
    result = git(["ls-remote", "--heads", "--", repository], repository=repository,
                 username=username, token=token)
    return [line.split("\trefs/heads/", 1)[1] for line in result.splitlines()
            if "\trefs/heads/" in line]


def relative_path(value):
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or "\\" in value:
        raise PublishError("Choose a path inside the publish folder.")
    return str(path)


def validate_repository(value):
    url = urlsplit(value)
    if settings.ALLOW_FILE_REPOSITORIES and url.scheme == "file":
        return
    if (url.scheme not in {"https", "http"} or not url.hostname or not url.path.strip("/")
            or url.username is not None or url.password is not None or url.query or url.fragment):
        raise PublishError("Enter a Git clone URL without credentials in the address.")
    if url.scheme == "http" and url.hostname not in settings.INSECURE_GIT_HOSTS:
        raise PublishError("Use HTTPS or an internal Git host configured by your operator.")


def snapshot(page, username, token):
    validate_repository(page.repository)
    if not page.branch or page.branch.startswith("-"):
        raise PublishError("Choose a branch.")
    ref = f"refs/heads/{page.branch}"
    git(["check-ref-format", ref])
    root = settings.PUBLISH_ROOT
    root.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(dir=root, prefix=".publishing-") as folder:
        work = Path(folder)
        repo = work / "git"
        git(["init", "--bare", str(repo)])
        git(["fetch", "--depth=1", "--no-tags", "--", page.repository, ref], cwd=repo,
            repository=page.repository, username=username, token=token)
        revision = git(["rev-parse", "FETCH_HEAD"], cwd=repo)
        if revision == page.revision:
            return
        tree = "FETCH_HEAD" if page.folder == "." else f"FETCH_HEAD:{page.folder}"
        archive = work / "site.tar"
        with archive.open("wb") as output:
            git(["archive", "--format=tar", tree], cwd=repo, output=output)
        site = work / "site"
        site.mkdir()
        with tarfile.open(archive) as source:
            for member in source:
                if not (member.isfile() or member.isdir()):
                    raise PublishError("The publish folder contains a link. Commit the linked files directly.")
                source.extract(member, site, filter="data")
        if not (site / page.entry).is_file():
            raise PublishError("Entry file was not found in the publish folder.")
        snapshot_id = uuid4()
        shutil.move(site, root / str(snapshot_id))
        page.snapshot = snapshot_id
        page.revision = revision


def refresh(page):
    previous = page.snapshot
    username, token = "", ""
    if page.credential:
        try:
            username, token = json.loads(credential_box().decrypt(page.credential.encode()))
        except InvalidToken as exc:
            raise PublishError("The saved Git credential cannot be read. Check the installation secret.") from exc

    snapshot(page, username, token)
    if page.snapshot == previous:
        return False

    updated = type(page).objects.filter(pk=page.pk, snapshot=previous).update(
        snapshot=page.snapshot, revision=page.revision,
    )
    old_snapshot = previous if updated else page.snapshot
    shutil.rmtree(settings.PUBLISH_ROOT / str(old_snapshot), ignore_errors=True)
    return bool(updated)
