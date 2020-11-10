import json
from typing import List
from lark import Lark

from roam_types import from_roam_export, Page, Block

parser = Lark(open("./GRAMMAR").read())


def load_roam_import(
    roam_json_file="/Users/nik/Downloads/nikvdp.json",
) -> List[Page]:
    with open(roam_json_file) as f:
        return from_roam_export(json.load(f))


def extract_children(thing):
    res = []
    if thing.children:
        for child in thing.children:
            res.append((child.uid, child))
            if child.children:
                res += extract_children(child)
    return res


def parse_block_text(block: Block):
    return parser.parse(block.string)


def build_flattened_blocklist(roam_pages: List[Page]):
    blocks = {}
    for page in roam_pages:
        children = extract_children(page)
        for block_tuple in children:
            blocks[block_tuple[0]] = block_tuple[1]

    return blocks
blocks_by_id = build_flattened_blocklist([load_roam_import()[0]])
