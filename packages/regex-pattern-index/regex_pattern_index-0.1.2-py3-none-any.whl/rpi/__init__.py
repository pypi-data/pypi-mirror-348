"""
NOTE: Pattern Compilation on Import
    Calling `re.compile` is surprisingly fast (~100ns).
    We'd need millions of regex patterns in a module to
    even reach an import time of 1 second, which would
    still be faster than importing pandas. Accordingly,
    no caching, or fancy tricks for only compiling patterns
    when needed are attempted.
"""

import re

name_chain = re.compile(
    r"^([A-za-z]\w*)(\.?[A-za-z]\w*)+$",
)
""""""

name_chain_lp = re.compile(
    r"^(\.)?([A-za-z]\w*)(\.?[A-za-z]\w*)+$",
)
""""""

definition_locator = re.compile(
    r"^(([A-za-z]\w*)(\.?[A-za-z]\w*)*)\:(([A-za-z]\w*)(\.?[A-za-z]\w*)*)$"
)
""""""
