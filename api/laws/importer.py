from beanie import WriteRules
from beanie.operators import In

from .parser import law_data_from_file, paragraphs_from_elements
from .repo import iter_tag_contents
from ..db.models import Law, LawVersion, Paragraph

import logging

logger = logging.getLogger(__name__)


async def get_or_create_law(
    name: str, short_title: str | None = None, long_title: str | None = None
) -> Law:
    law = await Law.find_one(Law.name == name, fetch_links=True, nesting_depth=1)
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
        paragraphs = paragraphs_from_elements(paragraphEls)
        if not paragraphs:
            logger.warning(f"No paragraphs found for law {existing_law.name} on {date}")
            if not existing_law.versions:
                logger.warning(
                    f"Law {existing_law.name} has no versions left, deleting"
                )
                await existing_law.delete(link_rule=WriteRules.WRITE)
            continue
        insert_result = await Paragraph.insert_many(paragraphs)
        paragraphs = await Paragraph.find(
            In(Paragraph.id, insert_result.inserted_ids)
        ).to_list()
        version = LawVersion(date=date, paragraphs=paragraphs)
        await version.create()
        existing_law.versions.append(version)
        await existing_law.save(link_rule=WriteRules.WRITE)
