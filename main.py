#!/usr/bin/env python3
import os
import sys
import json
from typing import List
from dataclasses import dataclass
from collections import defaultdict
import re

try:
    # TODO: for debugging only, delete soon
    from ipdb import set_trace
except:
    pass
from pprint import pprint

import click

from roam_types import from_roam_export, Page, Block


INLINE_TAG_RE: re.Pattern = re.compile(r"#([A-Za-z0-9_-]+)")
BACKLINK_TAG_RE: re.Pattern = re.compile(r"#\[\[([^\]]+)]\]")

PUBLIC_PAGE_TAG = "public_page"
PRIVATE_PAGE_TAG = "private_page"
PUBLIC_TAG = "public"
PRIVATE_TAG = "private"


def load_roam_import(roam_json_file) -> List[Page]:
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


def process_roam_export(roam_import: List[Page]) -> defaultdict:
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
            print(
                f"Got #private tag on block {block_id} of page '{page.title}'"
            )
            output_pages[page.title] = [
                b for b in output_pages[page.title] if b.uid != block_id
            ]

            # recursively iterate through and make sure the private block isn't
            # nested
            for block in output_pages[page.title]:
                delete_child_blocks(page, block_id)

    return output_pages


def sanitize_filename(filename) -> str:
    # stolen from agora code here:
    # https://github.com/flancian/agora-server/blob/39453d8b0758a6276face99fc7b78576e48136a0/app/db.py#L42
    # TODO: probably should replace slashes too lest roam namespace pages screw up dir structure
    return filename.lower().replace(" ", "-").replace("'", "").replace(",", "")


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option(
    "--roam-export-file",
    "-i",
    type=click.Path(file_okay=True, dir_okay=False, exists=True),
    prompt="Path to your roam export json file",
)
@click.option(
    "--output-folder",
    "-o",
    default="./agora",
    type=click.Path(file_okay=False, dir_okay=True),
    prompt="Path to save garden files to",
)
def main(roam_export_file, output_folder="./agora"):
    roam_import = load_roam_import(roam_export_file)

    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    output_pages = process_roam_export(roam_import)

    for page_title, blocks in output_pages.items():
        filename = f"{sanitize_filename(page_title)}.md"

        sys.stdout.write(
            f"Writing page '{page_title}' to '{filename}'... ",
        )

        with open(os.path.join(output_folder, filename), "w") as out_file:
            out_file.write(f"# {page_title}\n\n")

            for block in blocks:
                out_file.write(format_block_recursive(block))

        print(f"DONE!")


if __name__ == "__main__":
    main()
