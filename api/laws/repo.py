from logging import getLogger
from pathlib import Path
from typing import Generator, Tuple
from datetime import datetime

from git import Repo, TagReference


logger = getLogger(__name__)

repo_url = "https://github.com/QuantLaw/gesetze-im-internet.git"
local_path = Path(__file__).resolve().parent / "data"


def clone_repo() -> Repo:
    logger.info(f"cloning repo: {repo_url} to {local_path}")
    return Repo.clone_from(repo_url, local_path, branch="2019-06-10")


def repo_exists() -> bool:
    return local_path.exists() and local_path.is_dir()


def get_all_tags_with_previous() -> Generator[Tuple[None | TagReference, TagReference]]:
    repo = Repo(local_path)
    prev_tag = None
    for tag in repo.tags:
        yield prev_tag, tag
        prev_tag = tag


def get_file_content(tag: TagReference, file_path: str) -> str:
    repo = Repo(local_path)
    commit = repo.commit(tag.commit)
    blob = commit.tree[file_path]
    return blob.data_stream.read().decode("utf-8")


def iter_file_contents(file_path: str) -> Generator[Tuple[str, datetime]]:
    for prev, tag in get_all_tags_with_previous():
        diff = tag.commit.diff(prev.commit, paths=file_path) if prev else None
        if prev and not diff or diff and diff[0].deleted_file:
            continue

        logger.info(f"Processing file {file_path} in tag {tag.name}")
        try:
            content = get_file_content(tag, file_path)
        except KeyError:
            logger.warning(f"File {file_path} not found in tag {tag.name}")
            continue
        yield content, datetime.strptime(tag.name, "%Y-%m-%d")


def get_all_file_paths() -> list[str]:
    repo = Repo(local_path)
    return [
        item.path
        for item in repo.tree()["data/items"].traverse()
        if item.path.endswith(".xml")
    ]
