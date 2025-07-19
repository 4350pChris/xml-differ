from pathlib import Path

from xmldiff import formatting
import lxml.etree as ET
from xmldiff.formatting import WS_BOTH


class HTMLFormatter(formatting.XMLFormatter):
    def __init__(self):
        # text_tags=None
        formatting_tags = (
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
        )
        formatting_condition = " or ".join(f"self::{tag}" for tag in formatting_tags)
        text_tags = [
            f"{tag}[not(*) or not(*[not({formatting_condition})])]"
            for tag in ("SPAN", "ENTRY", "DT", "LA", "P")
        ]
        super().__init__(
            text_tags=text_tags,
            formatting_tags=formatting_tags,
            normalize=WS_BOTH,
        )

    def render(self, result):
        with (Path(__file__).parent / "htmlformatter.xslt").open() as f:
            xslt_template = ET.fromstring(f.read())
            transform = ET.XSLT(xslt_template)
            transformed = transform(result)
            return super(HTMLFormatter, self).render(transformed)
