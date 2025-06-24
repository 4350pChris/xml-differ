from .diff.differ import diff_files
from .diff.xmldiff_strat import XmldiffStrategy
from functools import partial


def get_diff_strategy():
    return partial(diff_files, XmldiffStrategy())
