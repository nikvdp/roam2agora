import json
from typing import List
from dataclasses import dataclass
from collections import defaultdict
import re

from ipdb import set_trace
from pprint import pprint

from roam_types import from_roam_export, Page, Block

INLINE_TAG_RE: re.Pattern = re.compile(r"#([A-Za-z0-9_-]+)")
BACKLINK_TAG_RE: re.Pattern = re.compile(r"#\[\[([^\]]+)]\]")

PUBLIC_PAGE_TAG = "public_page"
PRIVATE_PAGE_TAG = "private_page"
PUBLIC_TAG = "public"
PRIVATE_TAG = "private"


def load_roam_import(
    roam_json_file="./nikvdp-public-private.json",
) -> List[Page]:
    with open(roam_json_file) as f:
        return from_roam_export(json.load(f))


def extract_children(block_or_page):
    res = []
    if block_or_page.children:
        for child in block_or_page.children:
            res.append(child)
            if child.children:
                res += extract_children(child)
    return res


def delete_child_blocks(root_block, block_id):
    if not root_block.children or len(root_block.children) < 1:
        return

    for idx, block in enumerate(root_block.children):
        if block.uid == block_id:
            del root_block.children[idx]
        if block.children and len(block.children) > 0:
            delete_child_blocks(block, block_id)


@dataclass
class BlockMap:
    by_block_id: dict
    block_to_page: dict
    pages: dict


def build_flattened_blocklist(roam_pages: List[Page]):
    block_to_page_map = {}
    blocks = {}
    pages = {}

    for page in roam_pages:
        pages[page.title] = page
        children = extract_children(page)
        for block in children:
            blocks[block.uid] = block
            block_to_page_map[block.uid] = page

    return BlockMap(
        by_block_id=blocks, block_to_page=block_to_page_map, pages=pages
    )


def collect_relevant_tags(block):
    return [
        tag
        for tag in (
            INLINE_TAG_RE.findall(block) + BACKLINK_TAG_RE.findall(block)
        )
        if tag in [PUBLIC_TAG, PUBLIC_PAGE_TAG, PRIVATE_TAG, PRIVATE_PAGE_TAG]
    ]


def format_block_recursive(block, indent=2, indent_step=4):
    indent_str = " " * indent
    out = f"{indent_str}- {block.string}\n"
    if block.children and len(block.children) > 0:
        for child in block.children:
            out += format_block_recursive(
                child, indent=indent + indent_step, indent_step=indent_step
            )
    return out


roam_import = load_roam_import()

flattened_import = build_flattened_blocklist(roam_import)
blocks_by_id = flattened_import.by_block_id

output_pages = defaultdict(list)

for block_id, block in blocks_by_id.items():
    tags = collect_relevant_tags(block.string)

    if PUBLIC_PAGE_TAG in tags:
        page = flattened_import.block_to_page[block_id]
        output_pages[
            flattened_import.block_to_page[block_id].title
        ] += page.children

    if PUBLIC_TAG in tags:
        try:
            output_pages[
                flattened_import.block_to_page[block_id].title
            ].append(block)
        except Exception as e:
            raise e

# do a second pass to remove anything that was marked private
for block_id, block in blocks_by_id.items():
    tags = collect_relevant_tags(block.string)
    page = flattened_import.block_to_page[block_id]

    if PRIVATE_PAGE_TAG in tags:
        print(
            f"Got #private_page tag on block {block_id} of page '{page.title}'"
        )
        if output_pages.get(page.title):
            print(f"Deleting page {page.title}")
            del output_pages[page.title]

    if PRIVATE_TAG in tags:
        print(f"Got #private tag on block {block_id} of page '{page.title}'")
        output_pages[page.title] = [
            b for b in output_pages[page.title] if b.uid != block_id
        ]

        # recursively iterate through and make sure the privat block isn't
        # nested
        for block in output_pages[page.title]:
            delete_child_blocks(page, block_id)


print("----\n")

for page_title, blocks in output_pages.items():
    print(f"{page_title}:")
    for block in blocks:
        print(format_block_recursive(block))
