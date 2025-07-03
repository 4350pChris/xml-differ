from pathlib import Path

from xmldiff import formatting
import lxml.etree as ET
from xmldiff.formatting import WS_BOTH


class HTMLFormatter(formatting.XMLFormatter):
    def __init__(self):
        super().__init__(
            formatting_tags=(
                "BR",
                "B",
                "U",
                "I",
                "F",
                "SP",
                "small",
                "SUP",
                "SUB",
                "FnR",
                "NB",
                "noindex",
            ),
            normalize=WS_BOTH,
        )

    def render(self, result):
        with (Path(__file__).parent / "htmlformatter.xslt").open() as f:
            xslt_template = ET.fromstring(f.read())
            transform = ET.XSLT(xslt_template)
            return super(HTMLFormatter, self).render(transform(result))
