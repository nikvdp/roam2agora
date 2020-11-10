""" Type classes for roam json from app.quicktype.io """
# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = welcome_from_dict(json.loads(json_string))

from enum import Enum
from dataclasses import dataclass
from typing import Optional, List, Any, TypeVar, Callable, Type, cast


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


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


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


class Email(Enum):
    ROAM_NIKVDP_COM = "roam@nikvdp.com"


@dataclass
class FriskyChild:
    string: Optional[str] = None
    children: Optional[List["FriskyChild"]] = None
    uid: Optional[str] = None
    edit_time: Optional[int] = None
    edit_email: Optional[Email] = None

    @staticmethod
    def from_dict(obj: Any) -> "FriskyChild":
        assert isinstance(obj, dict)
        string = from_union([from_str, from_none], obj.get("string"))
        children = from_union(
            [lambda x: from_list(FriskyChild.from_dict, x), from_none],
            obj.get("children"),
        )
        uid = from_union([from_str, from_none], obj.get("uid"))
        edit_time = from_union([from_int, from_none], obj.get("edit-time"))
        edit_email = from_union([Email, from_none], obj.get("edit-email"))
        return FriskyChild(string, children, uid, edit_time, edit_email)

    def to_dict(self) -> dict:
        result: dict = {}
        result["string"] = from_union([from_str, from_none], self.string)
        result["children"] = from_union(
            [
                lambda x: from_list(lambda x: to_class(FriskyChild, x), x),
                from_none,
            ],
            self.children,
        )
        result["uid"] = from_union([from_str, from_none], self.uid)
        result["edit-time"] = from_union([from_int, from_none], self.edit_time)
        result["edit-email"] = from_union(
            [lambda x: to_enum(Email, x), from_none], self.edit_email
        )
        return result


@dataclass
class MagentaChild:
    string: Optional[str] = None
    create_email: Optional[Email] = None
    create_time: Optional[int] = None
    uid: Optional[str] = None
    edit_time: Optional[int] = None
    edit_email: Optional[Email] = None
    children: Optional[List[FriskyChild]] = None

    @staticmethod
    def from_dict(obj: Any) -> "MagentaChild":
        assert isinstance(obj, dict)
        string = from_union([from_str, from_none], obj.get("string"))
        create_email = from_union([Email, from_none], obj.get("create-email"))
        create_time = from_union([from_int, from_none], obj.get("create-time"))
        uid = from_union([from_str, from_none], obj.get("uid"))
        edit_time = from_union([from_int, from_none], obj.get("edit-time"))
        edit_email = from_union([Email, from_none], obj.get("edit-email"))
        children = from_union(
            [lambda x: from_list(FriskyChild.from_dict, x), from_none],
            obj.get("children"),
        )
        return MagentaChild(
            string,
            create_email,
            create_time,
            uid,
            edit_time,
            edit_email,
            children,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["string"] = from_union([from_str, from_none], self.string)
        result["create-email"] = from_union(
            [lambda x: to_enum(Email, x), from_none], self.create_email
        )
        result["create-time"] = from_union(
            [from_int, from_none], self.create_time
        )
        result["uid"] = from_union([from_str, from_none], self.uid)
        result["edit-time"] = from_union([from_int, from_none], self.edit_time)
        result["edit-email"] = from_union(
            [lambda x: to_enum(Email, x), from_none], self.edit_email
        )
        result["children"] = from_union(
            [
                lambda x: from_list(lambda x: to_class(FriskyChild, x), x),
                from_none,
            ],
            self.children,
        )
        return result


@dataclass
class CunningChild:
    string: Optional[str] = None
    create_email: Optional[Email] = None
    create_time: Optional[int] = None
    children: Optional[List[MagentaChild]] = None
    uid: Optional[str] = None
    edit_time: Optional[int] = None
    edit_email: Optional[Email] = None

    @staticmethod
    def from_dict(obj: Any) -> "CunningChild":
        assert isinstance(obj, dict)
        string = from_union([from_str, from_none], obj.get("string"))
        create_email = from_union([Email, from_none], obj.get("create-email"))
        create_time = from_union([from_int, from_none], obj.get("create-time"))
        children = from_union(
            [lambda x: from_list(MagentaChild.from_dict, x), from_none],
            obj.get("children"),
        )
        uid = from_union([from_str, from_none], obj.get("uid"))
        edit_time = from_union([from_int, from_none], obj.get("edit-time"))
        edit_email = from_union([Email, from_none], obj.get("edit-email"))
        return CunningChild(
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
            [lambda x: to_enum(Email, x), from_none], self.create_email
        )
        result["create-time"] = from_union(
            [from_int, from_none], self.create_time
        )
        result["children"] = from_union(
            [
                lambda x: from_list(lambda x: to_class(MagentaChild, x), x),
                from_none,
            ],
            self.children,
        )
        result["uid"] = from_union([from_str, from_none], self.uid)
        result["edit-time"] = from_union([from_int, from_none], self.edit_time)
        result["edit-email"] = from_union(
            [lambda x: to_enum(Email, x), from_none], self.edit_email
        )
        return result


@dataclass
class AmbitiousChild:
    string: Optional[str] = None
    create_email: Optional[Email] = None
    create_time: Optional[int] = None
    uid: Optional[str] = None
    edit_time: Optional[int] = None
    edit_email: Optional[Email] = None
    children: Optional[List[CunningChild]] = None

    @staticmethod
    def from_dict(obj: Any) -> "AmbitiousChild":
        assert isinstance(obj, dict)
        string = from_union([from_str, from_none], obj.get("string"))
        create_email = from_union([Email, from_none], obj.get("create-email"))
        create_time = from_union([from_int, from_none], obj.get("create-time"))
        uid = from_union([from_str, from_none], obj.get("uid"))
        edit_time = from_union([from_int, from_none], obj.get("edit-time"))
        edit_email = from_union([Email, from_none], obj.get("edit-email"))
        children = from_union(
            [lambda x: from_list(CunningChild.from_dict, x), from_none],
            obj.get("children"),
        )
        return AmbitiousChild(
            string,
            create_email,
            create_time,
            uid,
            edit_time,
            edit_email,
            children,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["string"] = from_union([from_str, from_none], self.string)
        result["create-email"] = from_union(
            [lambda x: to_enum(Email, x), from_none], self.create_email
        )
        result["create-time"] = from_union(
            [from_int, from_none], self.create_time
        )
        result["uid"] = from_union([from_str, from_none], self.uid)
        result["edit-time"] = from_union([from_int, from_none], self.edit_time)
        result["edit-email"] = from_union(
            [lambda x: to_enum(Email, x), from_none], self.edit_email
        )
        result["children"] = from_union(
            [
                lambda x: from_list(lambda x: to_class(CunningChild, x), x),
                from_none,
            ],
            self.children,
        )
        return result


@dataclass
class HilariousChild:
    string: Optional[str] = None
    create_email: Optional[Email] = None
    create_time: Optional[int] = None
    uid: Optional[str] = None
    edit_time: Optional[int] = None
    edit_email: Optional[Email] = None
    children: Optional[List[AmbitiousChild]] = None

    @staticmethod
    def from_dict(obj: Any) -> "HilariousChild":
        assert isinstance(obj, dict)
        string = from_union([from_str, from_none], obj.get("string"))
        create_email = from_union([Email, from_none], obj.get("create-email"))
        create_time = from_union([from_int, from_none], obj.get("create-time"))
        uid = from_union([from_str, from_none], obj.get("uid"))
        edit_time = from_union([from_int, from_none], obj.get("edit-time"))
        edit_email = from_union([Email, from_none], obj.get("edit-email"))
        children = from_union(
            [lambda x: from_list(AmbitiousChild.from_dict, x), from_none],
            obj.get("children"),
        )
        return HilariousChild(
            string,
            create_email,
            create_time,
            uid,
            edit_time,
            edit_email,
            children,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["string"] = from_union([from_str, from_none], self.string)
        result["create-email"] = from_union(
            [lambda x: to_enum(Email, x), from_none], self.create_email
        )
        result["create-time"] = from_union(
            [from_int, from_none], self.create_time
        )
        result["uid"] = from_union([from_str, from_none], self.uid)
        result["edit-time"] = from_union([from_int, from_none], self.edit_time)
        result["edit-email"] = from_union(
            [lambda x: to_enum(Email, x), from_none], self.edit_email
        )
        result["children"] = from_union(
            [
                lambda x: from_list(lambda x: to_class(AmbitiousChild, x), x),
                from_none,
            ],
            self.children,
        )
        return result


@dataclass
class IndecentChild:
    string: Optional[str] = None
    create_email: Optional[Email] = None
    create_time: Optional[int] = None
    uid: Optional[str] = None
    edit_time: Optional[int] = None
    edit_email: Optional[Email] = None
    children: Optional[List[HilariousChild]] = None

    @staticmethod
    def from_dict(obj: Any) -> "IndecentChild":
        assert isinstance(obj, dict)
        string = from_union([from_str, from_none], obj.get("string"))
        create_email = from_union([Email, from_none], obj.get("create-email"))
        create_time = from_union([from_int, from_none], obj.get("create-time"))
        uid = from_union([from_str, from_none], obj.get("uid"))
        edit_time = from_union([from_int, from_none], obj.get("edit-time"))
        edit_email = from_union([Email, from_none], obj.get("edit-email"))
        children = from_union(
            [lambda x: from_list(HilariousChild.from_dict, x), from_none],
            obj.get("children"),
        )
        return IndecentChild(
            string,
            create_email,
            create_time,
            uid,
            edit_time,
            edit_email,
            children,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["string"] = from_union([from_str, from_none], self.string)
        result["create-email"] = from_union(
            [lambda x: to_enum(Email, x), from_none], self.create_email
        )
        result["create-time"] = from_union(
            [from_int, from_none], self.create_time
        )
        result["uid"] = from_union([from_str, from_none], self.uid)
        result["edit-time"] = from_union([from_int, from_none], self.edit_time)
        result["edit-email"] = from_union(
            [lambda x: to_enum(Email, x), from_none], self.edit_email
        )
        result["children"] = from_union(
            [
                lambda x: from_list(lambda x: to_class(HilariousChild, x), x),
                from_none,
            ],
            self.children,
        )
        return result


@dataclass
class IndigoChild:
    string: Optional[str] = None
    create_email: Optional[Email] = None
    create_time: Optional[int] = None
    children: Optional[List[IndecentChild]] = None
    uid: Optional[str] = None
    edit_time: Optional[int] = None
    edit_email: Optional[Email] = None

    @staticmethod
    def from_dict(obj: Any) -> "IndigoChild":
        assert isinstance(obj, dict)
        string = from_union([from_str, from_none], obj.get("string"))
        create_email = from_union([Email, from_none], obj.get("create-email"))
        create_time = from_union([from_int, from_none], obj.get("create-time"))
        children = from_union(
            [lambda x: from_list(IndecentChild.from_dict, x), from_none],
            obj.get("children"),
        )
        uid = from_union([from_str, from_none], obj.get("uid"))
        edit_time = from_union([from_int, from_none], obj.get("edit-time"))
        edit_email = from_union([Email, from_none], obj.get("edit-email"))
        return IndigoChild(
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
            [lambda x: to_enum(Email, x), from_none], self.create_email
        )
        result["create-time"] = from_union(
            [from_int, from_none], self.create_time
        )
        result["children"] = from_union(
            [
                lambda x: from_list(lambda x: to_class(IndecentChild, x), x),
                from_none,
            ],
            self.children,
        )
        result["uid"] = from_union([from_str, from_none], self.uid)
        result["edit-time"] = from_union([from_int, from_none], self.edit_time)
        result["edit-email"] = from_union(
            [lambda x: to_enum(Email, x), from_none], self.edit_email
        )
        return result


@dataclass
class StickyChild:
    string: Optional[str] = None
    create_email: Optional[Email] = None
    create_time: Optional[int] = None
    uid: Optional[str] = None
    edit_time: Optional[int] = None
    edit_email: Optional[Email] = None
    children: Optional[List[IndigoChild]] = None

    @staticmethod
    def from_dict(obj: Any) -> "StickyChild":
        assert isinstance(obj, dict)
        string = from_union([from_str, from_none], obj.get("string"))
        create_email = from_union([Email, from_none], obj.get("create-email"))
        create_time = from_union([from_int, from_none], obj.get("create-time"))
        uid = from_union([from_str, from_none], obj.get("uid"))
        edit_time = from_union([from_int, from_none], obj.get("edit-time"))
        edit_email = from_union([Email, from_none], obj.get("edit-email"))
        children = from_union(
            [lambda x: from_list(IndigoChild.from_dict, x), from_none],
            obj.get("children"),
        )
        return StickyChild(
            string,
            create_email,
            create_time,
            uid,
            edit_time,
            edit_email,
            children,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["string"] = from_union([from_str, from_none], self.string)
        result["create-email"] = from_union(
            [lambda x: to_enum(Email, x), from_none], self.create_email
        )
        result["create-time"] = from_union(
            [from_int, from_none], self.create_time
        )
        result["uid"] = from_union([from_str, from_none], self.uid)
        result["edit-time"] = from_union([from_int, from_none], self.edit_time)
        result["edit-email"] = from_union(
            [lambda x: to_enum(Email, x), from_none], self.edit_email
        )
        result["children"] = from_union(
            [
                lambda x: from_list(lambda x: to_class(IndigoChild, x), x),
                from_none,
            ],
            self.children,
        )
        return result


@dataclass
class TentacledChild:
    string: Optional[str] = None
    create_email: Optional[Email] = None
    create_time: Optional[int] = None
    uid: Optional[str] = None
    edit_time: Optional[int] = None
    edit_email: Optional[Email] = None
    children: Optional[List[StickyChild]] = None
    text_align: Optional[str] = None
    heading: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> "TentacledChild":
        assert isinstance(obj, dict)
        string = from_union([from_str, from_none], obj.get("string"))
        create_email = from_union([Email, from_none], obj.get("create-email"))
        create_time = from_union([from_int, from_none], obj.get("create-time"))
        uid = from_union([from_str, from_none], obj.get("uid"))
        edit_time = from_union([from_int, from_none], obj.get("edit-time"))
        edit_email = from_union([Email, from_none], obj.get("edit-email"))
        children = from_union(
            [lambda x: from_list(StickyChild.from_dict, x), from_none],
            obj.get("children"),
        )
        text_align = from_union([from_str, from_none], obj.get("text-align"))
        heading = from_union([from_int, from_none], obj.get("heading"))
        return TentacledChild(
            string,
            create_email,
            create_time,
            uid,
            edit_time,
            edit_email,
            children,
            text_align,
            heading,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["string"] = from_union([from_str, from_none], self.string)
        result["create-email"] = from_union(
            [lambda x: to_enum(Email, x), from_none], self.create_email
        )
        result["create-time"] = from_union(
            [from_int, from_none], self.create_time
        )
        result["uid"] = from_union([from_str, from_none], self.uid)
        result["edit-time"] = from_union([from_int, from_none], self.edit_time)
        result["edit-email"] = from_union(
            [lambda x: to_enum(Email, x), from_none], self.edit_email
        )
        result["children"] = from_union(
            [
                lambda x: from_list(lambda x: to_class(StickyChild, x), x),
                from_none,
            ],
            self.children,
        )
        result["text-align"] = from_union(
            [from_str, from_none], self.text_align
        )
        result["heading"] = from_union([from_int, from_none], self.heading)
        return result


@dataclass
class FluffyChild:
    string: Optional[str] = None
    create_email: Optional[Email] = None
    create_time: Optional[int] = None
    uid: Optional[str] = None
    edit_time: Optional[int] = None
    edit_email: Optional[Email] = None
    children: Optional[List[TentacledChild]] = None
    heading: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> "FluffyChild":
        assert isinstance(obj, dict)
        string = from_union([from_str, from_none], obj.get("string"))
        create_email = from_union([Email, from_none], obj.get("create-email"))
        create_time = from_union([from_int, from_none], obj.get("create-time"))
        uid = from_union([from_str, from_none], obj.get("uid"))
        edit_time = from_union([from_int, from_none], obj.get("edit-time"))
        edit_email = from_union([Email, from_none], obj.get("edit-email"))
        children = from_union(
            [lambda x: from_list(TentacledChild.from_dict, x), from_none],
            obj.get("children"),
        )
        heading = from_union([from_int, from_none], obj.get("heading"))
        return FluffyChild(
            string,
            create_email,
            create_time,
            uid,
            edit_time,
            edit_email,
            children,
            heading,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["string"] = from_union([from_str, from_none], self.string)
        result["create-email"] = from_union(
            [lambda x: to_enum(Email, x), from_none], self.create_email
        )
        result["create-time"] = from_union(
            [from_int, from_none], self.create_time
        )
        result["uid"] = from_union([from_str, from_none], self.uid)
        result["edit-time"] = from_union([from_int, from_none], self.edit_time)
        result["edit-email"] = from_union(
            [lambda x: to_enum(Email, x), from_none], self.edit_email
        )
        result["children"] = from_union(
            [
                lambda x: from_list(lambda x: to_class(TentacledChild, x), x),
                from_none,
            ],
            self.children,
        )
        result["heading"] = from_union([from_int, from_none], self.heading)
        return result


@dataclass
class PurpleChild:
    string: Optional[str] = None
    create_email: Optional[Email] = None
    create_time: Optional[int] = None
    uid: Optional[str] = None
    edit_time: Optional[int] = None
    edit_email: Optional[Email] = None
    children: Optional[List[FluffyChild]] = None
    text_align: Optional[str] = None
    heading: Optional[int] = None
    emojis: Optional[List[Any]] = None

    @staticmethod
    def from_dict(obj: Any) -> "PurpleChild":
        assert isinstance(obj, dict)
        string = from_union([from_str, from_none], obj.get("string"))
        create_email = from_union([Email, from_none], obj.get("create-email"))
        create_time = from_union([from_int, from_none], obj.get("create-time"))
        uid = from_union([from_str, from_none], obj.get("uid"))
        edit_time = from_union([from_int, from_none], obj.get("edit-time"))
        edit_email = from_union([Email, from_none], obj.get("edit-email"))
        children = from_union(
            [lambda x: from_list(FluffyChild.from_dict, x), from_none],
            obj.get("children"),
        )
        text_align = from_union([from_str, from_none], obj.get("text-align"))
        heading = from_union([from_int, from_none], obj.get("heading"))
        emojis = from_union(
            [lambda x: from_list(lambda x: x, x), from_none], obj.get("emojis")
        )
        return PurpleChild(
            string,
            create_email,
            create_time,
            uid,
            edit_time,
            edit_email,
            children,
            text_align,
            heading,
            emojis,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["string"] = from_union([from_str, from_none], self.string)
        result["create-email"] = from_union(
            [lambda x: to_enum(Email, x), from_none], self.create_email
        )
        result["create-time"] = from_union(
            [from_int, from_none], self.create_time
        )
        result["uid"] = from_union([from_str, from_none], self.uid)
        result["edit-time"] = from_union([from_int, from_none], self.edit_time)
        result["edit-email"] = from_union(
            [lambda x: to_enum(Email, x), from_none], self.edit_email
        )
        result["children"] = from_union(
            [
                lambda x: from_list(lambda x: to_class(FluffyChild, x), x),
                from_none,
            ],
            self.children,
        )
        result["text-align"] = from_union(
            [from_str, from_none], self.text_align
        )
        result["heading"] = from_union([from_int, from_none], self.heading)
        result["emojis"] = from_union(
            [lambda x: from_list(lambda x: x, x), from_none], self.emojis
        )
        return result


@dataclass
class Encryption:
    hint: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> "Encryption":
        assert isinstance(obj, dict)
        hint = from_union([from_str, from_none], obj.get("hint"))
        return Encryption(hint)

    def to_dict(self) -> dict:
        result: dict = {}
        result["hint"] = from_union([from_str, from_none], self.hint)
        return result


@dataclass
class Line:
    color: Optional[str] = None
    width: Optional[int] = None
    points: Optional[List[List[int]]] = None

    @staticmethod
    def from_dict(obj: Any) -> "Line":
        assert isinstance(obj, dict)
        color = from_union([from_str, from_none], obj.get("color"))
        width = from_union([from_int, from_none], obj.get("width"))
        points = from_union(
            [
                lambda x: from_list(lambda x: from_list(from_int, x), x),
                from_none,
            ],
            obj.get("points"),
        )
        return Line(color, width, points)

    def to_dict(self) -> dict:
        result: dict = {}
        result["color"] = from_union([from_str, from_none], self.color)
        result["width"] = from_union([from_int, from_none], self.width)
        result["points"] = from_union(
            [
                lambda x: from_list(lambda x: from_list(from_int, x), x),
                from_none,
            ],
            self.points,
        )
        return result


@dataclass
class Props:
    encryption: Optional[Encryption] = None
    lines: Optional[List[Line]] = None

    @staticmethod
    def from_dict(obj: Any) -> "Props":
        assert isinstance(obj, dict)
        encryption = from_union(
            [Encryption.from_dict, from_none], obj.get("encryption")
        )
        lines = from_union(
            [lambda x: from_list(Line.from_dict, x), from_none],
            obj.get("lines"),
        )
        return Props(encryption, lines)

    def to_dict(self) -> dict:
        result: dict = {}
        result["encryption"] = from_union(
            [lambda x: to_class(Encryption, x), from_none], self.encryption
        )
        result["lines"] = from_union(
            [lambda x: from_list(lambda x: to_class(Line, x), x), from_none],
            self.lines,
        )
        return result


@dataclass
class WelcomeChild:
    string: Optional[str] = None
    create_email: Optional[Email] = None
    create_time: Optional[int] = None
    children: Optional[List[PurpleChild]] = None
    uid: Optional[str] = None
    edit_time: Optional[int] = None
    edit_email: Optional[Email] = None
    heading: Optional[int] = None
    props: Optional[Props] = None

    @staticmethod
    def from_dict(obj: Any) -> "WelcomeChild":
        assert isinstance(obj, dict)
        string = from_union([from_str, from_none], obj.get("string"))
        create_email = from_union([Email, from_none], obj.get("create-email"))
        create_time = from_union([from_int, from_none], obj.get("create-time"))
        children = from_union(
            [lambda x: from_list(PurpleChild.from_dict, x), from_none],
            obj.get("children"),
        )
        uid = from_union([from_str, from_none], obj.get("uid"))
        edit_time = from_union([from_int, from_none], obj.get("edit-time"))
        edit_email = from_union([Email, from_none], obj.get("edit-email"))
        heading = from_union([from_int, from_none], obj.get("heading"))
        props = from_union([Props.from_dict, from_none], obj.get("props"))
        return WelcomeChild(
            string,
            create_email,
            create_time,
            children,
            uid,
            edit_time,
            edit_email,
            heading,
            props,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["string"] = from_union([from_str, from_none], self.string)
        result["create-email"] = from_union(
            [lambda x: to_enum(Email, x), from_none], self.create_email
        )
        result["create-time"] = from_union(
            [from_int, from_none], self.create_time
        )
        result["children"] = from_union(
            [
                lambda x: from_list(lambda x: to_class(PurpleChild, x), x),
                from_none,
            ],
            self.children,
        )
        result["uid"] = from_union([from_str, from_none], self.uid)
        result["edit-time"] = from_union([from_int, from_none], self.edit_time)
        result["edit-email"] = from_union(
            [lambda x: to_enum(Email, x), from_none], self.edit_email
        )
        result["heading"] = from_union([from_int, from_none], self.heading)
        result["props"] = from_union(
            [lambda x: to_class(Props, x), from_none], self.props
        )
        return result


@dataclass
class WelcomeElement:
    title: Optional[str] = None
    children: Optional[List[WelcomeChild]] = None
    edit_time: Optional[int] = None
    edit_email: Optional[Email] = None
    create_email: Optional[Email] = None
    create_time: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> "WelcomeElement":
        assert isinstance(obj, dict)
        title = from_union([from_str, from_none], obj.get("title"))
        children = from_union(
            [lambda x: from_list(WelcomeChild.from_dict, x), from_none],
            obj.get("children"),
        )
        edit_time = from_union([from_int, from_none], obj.get("edit-time"))
        edit_email = from_union([Email, from_none], obj.get("edit-email"))
        create_email = from_union([Email, from_none], obj.get("create-email"))
        create_time = from_union([from_int, from_none], obj.get("create-time"))
        return WelcomeElement(
            title, children, edit_time, edit_email, create_email, create_time
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["title"] = from_union([from_str, from_none], self.title)
        result["children"] = from_union(
            [
                lambda x: from_list(lambda x: to_class(WelcomeChild, x), x),
                from_none,
            ],
            self.children,
        )
        result["edit-time"] = from_union([from_int, from_none], self.edit_time)
        result["edit-email"] = from_union(
            [lambda x: to_enum(Email, x), from_none], self.edit_email
        )
        result["create-email"] = from_union(
            [lambda x: to_enum(Email, x), from_none], self.create_email
        )
        result["create-time"] = from_union(
            [from_int, from_none], self.create_time
        )
        return result


def welcome_from_dict(s: Any) -> List[WelcomeElement]:
    return from_list(WelcomeElement.from_dict, s)


def welcome_to_dict(x: List[WelcomeElement]) -> Any:
    return from_list(lambda x: to_class(WelcomeElement, x), x)
