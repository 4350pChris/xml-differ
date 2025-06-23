from beanie import WriteRules

from .parser import law_data_from_file, paragraphs_from_elements
from .repo import iter_tag_contents
from ..db.models import Law, LawVersion

import logging

logger = logging.getLogger(__name__)


async def get_or_create_law(
    name: str, short_title: str | None = None, long_title: str | None = None
) -> Law:
    law = await Law.find_one(Law.name == name)
    if law is None:
        law = Law(
            name=name, short_title=short_title, long_title=long_title, versions=[]
        )
        await law.insert(link_rule=WriteRules.WRITE)
    return law


async def import_files():
    logger.info("Starting import of law files")
    for content, date in iter_tag_contents():
        metadata, paragraphEls = law_data_from_file(content)
        existing_law = await get_or_create_law(**metadata)
        # skip if this version exists
        if any(version.date == date for version in existing_law.versions):
            continue
        version = LawVersion(
            date=date, paragraphs=paragraphs_from_elements(paragraphEls)
        )
        await version.insert(link_rule=WriteRules.WRITE)
        existing_law.versions.append(version)
        await existing_law.save(link_rule=WriteRules.WRITE)
