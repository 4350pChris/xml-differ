import logging
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Generator

from ..db.models import Paragraph, Law
from ..laws.repo import iter_file_contents

logger = logging.getLogger("laws.parser")


def get_law_metadata(el: ET.Element) -> dict[str, str | None]:
    law_metadata = el.find("metadaten")
    if law_metadata is None:
        raise ValueError("Invalid law content: missing metadata")
    name = law_metadata.find("jurabk").text
    short_title_el = law_metadata.find("kurzue")
    short_title = short_title_el.text if short_title_el is not None else None
    long_title_el = law_metadata.find("langue")
    long_title = long_title_el.text if long_title_el is not None else None
    return {
        "name": name,
        "short_title": short_title,
        "long_title": long_title,
    }


def paragraph_from_element(index: int, el: ET.Element) -> Paragraph | None:
    titleEl = el.find("metadaten").find("enbez")
    if titleEl is None:
        return None
    content = ET.tostring(el, encoding="unicode")
    return Paragraph(index=index, title=titleEl.text, content=content)


def law_from_file(content: str, date: datetime) -> Law:
    tree = ET.ElementTree(ET.fromstring(content))
    [metadataEl, *paragraphEls] = tree.findall("norm")

    metadata = get_law_metadata(metadataEl)
    paragraphs = [paragraph_from_element(i, el) for i, el in enumerate(paragraphEls)]

    return Law(
        date=date, paragraphs=[p for p in paragraphs if p is not None], **metadata
    )


def iter_laws(path: str) -> Generator[Law]:
    for content, date in iter_file_contents(path):
        try:
            yield law_from_file(content, date)
        except ValueError as e:
            logger.error(f"Error parsing law from file {path} on date {date}: {e}")
            continue
