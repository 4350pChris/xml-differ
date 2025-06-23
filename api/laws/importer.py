from beanie import WriteRules

from .parser import law_from_file, paragraphs_from_elements
from .repo import iter_tag_contents
from ..db.models import Law

import logging

logger = logging.getLogger(__name__)


async def import_files():
    for content, date in iter_tag_contents():
        law, paragraphEls = law_from_file(content, date)
        existing_law = await Law.find_one(Law.name == law.name, Law.date == law.date)
        if existing_law is not None:
            continue
        law.paragraphs = paragraphs_from_elements(paragraphEls)
        await law.insert(link_rule=WriteRules.WRITE)
