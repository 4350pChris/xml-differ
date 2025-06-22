from logging import getLogger
from pathlib import Path
from typing import Generator, Tuple
from datetime import datetime
import xml.etree.ElementTree as ET

from git import Repo, TagReference

from ..db.models import Law

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
    if not blob:
        raise FileNotFoundError(f"File {file_path} not found in tag {tag.name}")
    return blob.data_stream.read().decode("utf-8")


def iter_file_contents(file_path: str) -> Generator[Tuple[str, datetime]]:
    for prev, tag in get_all_tags_with_previous():
        diff = tag.commit.diff(prev.commit, paths=file_path) if prev else None
        if prev and not diff:
            continue

        logger.info(f"Processing file {file_path} in tag {tag.name}")
        content = get_file_content(tag, file_path)
        yield content, datetime.strptime(tag.name, "%Y-%m-%d")


def get_all_file_paths() -> list[str]:
    repo = Repo(local_path)
    return [
        item.path
        for item in repo.tree()["data/items"].traverse()
        if item.path.endswith(".xml")
    ]


def law_from_file(content: str, date: datetime) -> Law:
    law_metadata = ET.fromstring(content).find("norm").find("metadaten")
    if law_metadata is None:
        raise ValueError("Invalid law content: missing metadata")
    name = law_metadata.find("jurabk").text
    short_title_el = law_metadata.find("kurzue")
    short_title = short_title_el.text if short_title_el is not None else None
    long_title_el = law_metadata.find("langue")
    long_title = long_title_el.text if long_title_el is not None else None
    return Law(
        name=name,
        short_title=short_title,
        long_title=long_title,
        content=content,
        date=date,
    )


def iter_laws(path: str) -> Generator[Law]:
    for content, date in iter_file_contents(path):
        yield law_from_file(content, date)
