from fastapi import UploadFile
from xmldiff import main as xmldiff_main
from lxml import etree


def match_paragraphs(left: etree._Element, right: etree._Element) -> list[tuple[tuple[int, etree._Element], tuple[int, etree._Element]]]:
    """Match paragraphs in two XML trees."""
    left_paragraphs = left.xpath("//norm")
    right_paragraphs = right.xpath("//norm")

    matches = []
    for left_index, lp in enumerate(left_paragraphs):
        # A Norm matches another if their `metadaten/enbez` child elements are equal
        left_enbez = lp.find("./metadaten/enbez")
        if left_enbez is None:
            continue
        for right_index, rp in enumerate(right_paragraphs):
            right_enbez = rp.find("./metadaten/enbez")
            if right_enbez is not None:
                if left_enbez.text == right_enbez.text:
                    matches.append((
                        (left_index, lp),
                        (right_index, rp)
                    ))
                    break
    return matches


async def diff_files(left: UploadFile, right: UploadFile) -> list[dict]:
    left_content = await left.read()
    right_content = await right.read()

    parser = etree.XMLParser(remove_blank_text=True)

    left_tree = etree.fromstring(left_content, parser)
    right_tree = etree.fromstring(right_content, parser)

    matches = match_paragraphs(left_tree, right_tree)

    diffs = []
    # Create diff for each match
    for (left_index, l), (right_index, r) in matches:
        diff = xmldiff_main.diff_trees(l, r)
        diffs.append({
            'left_index': left_index,
            'right_index': right_index,
            'diff': diff
        })

    return diffs
