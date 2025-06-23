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


def iter_tag_contents() -> Generator[Tuple[str, datetime]]:
    for previous, tag in get_all_tags_with_previous():
        logger.info(f"Processing {tag.name}")
        prev_commit = previous.commit if previous else tag.commit.parents[0]
        diff = prev_commit.diff(tag.commit, paths="data/items")
        for change in diff:
            if change.deleted_file:
                continue

            file_path = change.b_path
            if not file_path.endswith(".xml"):
                continue

            try:
                content = get_file_content(tag, file_path)
                yield content, datetime.strptime(tag.name, "%Y-%m-%d")
            except KeyError:
                logger.warning(f"File {file_path} not found in tag {tag.name}")
                continue
