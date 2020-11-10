import json
from typing import List

from roam_types import from_roam_export, Page


def load_roam_import(
    roam_json_file="/Users/nik/Downloads/nikvdp.json",
) -> List[Page]:
    with open(roam_json_file) as f:
        return from_roam_export(json.load(f))


print([x.string for x in load_roam_import()[0].children])
