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
