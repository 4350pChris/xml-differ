from collections.abc import AsyncGenerator, Generator

from lxml import etree

from .types import Diff, DiffStrategy


def match_paragraphs(
    left: etree._Element, right: etree._Element
) -> Generator[tuple[tuple[int, etree._Element], tuple[int, etree._Element]]]:
    """Match paragraphs in two XML trees."""
    left_paragraphs = left.xpath("//norm")
    right_paragraphs = right.xpath("//norm")

    for left_index, lp in enumerate(left_paragraphs):
        # A Norm matches another if their `metadaten/enbez` child elements are equal
        left_enbez = lp.find("./metadaten/enbez")
        if left_enbez is None:
            continue
        for right_index, rp in enumerate(right_paragraphs):
            right_enbez = rp.find("./metadaten/enbez")
            if right_enbez is not None:
                if left_enbez.text == right_enbez.text:
                    yield ((left_index, lp), (right_index, rp))
                    break


async def diff_files(
    diff_strategy: DiffStrategy, left: bytes, right: bytes
) -> AsyncGenerator[Diff]:
    # TODO: how to handle large files?
    parser = etree.XMLParser(remove_blank_text=True)

    left_tree = etree.fromstring(left, parser)
    right_tree = etree.fromstring(right, parser)

    matches = match_paragraphs(left_tree, right_tree)

    # Create diff for each match
    for (left_index, left_paragraph), (right_index, right_paragraph) in matches:
        edits = list(diff_strategy(left_paragraph, right_paragraph))
        yield Diff(left_index=left_index, right_index=right_index, edits=edits)
