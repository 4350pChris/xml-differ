from pathlib import Path

from xmldiff import formatting
from xmldiff import main as xmldiff_main
import lxml.etree as ET

from diff.types import DiffStrategy


class HTMLFormatter(formatting.XMLFormatter):
    def render(self, result):
        with (Path(__file__).parent / "htmlformatter.xslt").open() as f:
            xslt_template = ET.fromstring(f.read())
            transform = ET.XSLT(xslt_template)
            return super(HTMLFormatter, self).render(transform(result))


class XmlToHtmlDiffStrategy(DiffStrategy):
    def __call__(self, left: ET._Element, right: ET._Element) -> str:
        formatter = HTMLFormatter()
        edits = xmldiff_main.diff_trees(left, right, formatter=formatter)
        return edits.__str__()
