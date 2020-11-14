""" Type classes for roam json from app.quicktype.io """

import json

from dataclasses import dataclass
from typing import Optional, List, Any, TypeVar, Callable, Type, cast


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Block:
    string: Optional[str] = None
    create_email: Optional[str] = None
    create_time: Optional[int] = None
    children: Optional[List["Block"]] = None
    uid: Optional[str] = None
    edit_time: Optional[int] = None
    edit_email: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> "Block":
        assert isinstance(obj, dict)
        string = from_union([from_str, from_none], obj.get("string"))
        create_email = from_union(
            [from_str, from_none], obj.get("create-email")
        )
        create_time = from_union([from_int, from_none], obj.get("create-time"))
        children = from_union(
            [lambda x: from_list(Block.from_dict, x), from_none],
            obj.get("children"),
        )
        uid = from_union([from_str, from_none], obj.get("uid"))
        edit_time = from_union([from_int, from_none], obj.get("edit-time"))
        edit_email = from_union([from_str, from_none], obj.get("edit-email"))
        return Block(
            string,
            create_email,
            create_time,
            children,
            uid,
            edit_time,
            edit_email,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["string"] = from_union([from_str, from_none], self.string)
        result["create-email"] = from_union(
            [from_str, from_none], self.create_email
        )
        result["create-time"] = from_union(
            [from_int, from_none], self.create_time
        )
        result["children"] = from_union(
            [lambda x: from_list(lambda x: to_class(Block, x), x), from_none],
            self.children,
        )
        result["uid"] = from_union([from_str, from_none], self.uid)
        result["edit-time"] = from_union([from_int, from_none], self.edit_time)
        result["edit-email"] = from_union(
            [from_str, from_none], self.edit_email
        )
        return result


@dataclass
class Page:
    title: Optional[str] = None
    children: Optional[List[Block]] = None

    @staticmethod
    def from_dict(obj: Any) -> "Page":
        assert isinstance(obj, dict)
        title = from_union([from_str, from_none], obj.get("title"))
        children = from_union(
            [lambda x: from_list(Block.from_dict, x), from_none],
            obj.get("children"),
        )
        return Page(title, children)

    def to_dict(self) -> dict:
        result: dict = {}
        result["title"] = from_union([from_str, from_none], self.title)
        result["children"] = from_union(
            [lambda x: from_list(lambda x: to_class(Block, x), x), from_none],
            self.children,
        )
        return result


def from_roam_export(roam_export: List[dict]) -> List[Page]:
    return [Page.from_dict(p) for p in roam_export]
