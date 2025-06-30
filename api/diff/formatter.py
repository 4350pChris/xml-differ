from pathlib import Path

from xmldiff import formatting
import lxml.etree as ET


class HTMLFormatter(formatting.XMLFormatter):
    def __init__(self):
        super().__init__(
            text_tags=("entry", "LA"),
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
        )

    def render(self, result):
        with (Path(__file__).parent / "htmlformatter.xslt").open() as f:
            xslt_template = ET.fromstring(f.read())
            transform = ET.XSLT(xslt_template)
            return super(HTMLFormatter, self).render(transform(result))
