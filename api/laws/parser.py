import logging
import xml.etree.ElementTree as ET
from typing import List

from ..db.models import Paragraph

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


def paragraphs_from_elements(elements: List[ET.Element]) -> List[Paragraph]:
    paragraphs = []
    for i, el in enumerate(elements):
        paragraph = paragraph_from_element(i, el)
        if paragraph is not None:
            paragraphs.append(paragraph)
    return paragraphs


def law_data_from_file(content: str) -> tuple[dict[str, str | None], List[ET.Element]]:
    tree = ET.ElementTree(ET.fromstring(content))
    [metadataEl, *paragraphEls] = tree.findall("norm")

    metadata = get_law_metadata(metadataEl)

    return metadata, paragraphEls
