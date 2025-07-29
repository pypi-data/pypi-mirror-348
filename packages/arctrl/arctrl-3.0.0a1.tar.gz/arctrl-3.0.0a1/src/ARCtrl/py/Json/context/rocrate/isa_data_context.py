from __future__ import annotations
from dataclasses import dataclass
from typing import (Any, TypeVar)
from ....fable_modules.fable_library.reflection import (TypeInfo, string_type, record_type)
from ....fable_modules.fable_library.seq import map
from ....fable_modules.fable_library.types import Record
from ....fable_modules.fable_library.util import (to_enumerable, IEnumerable_1)
from ....fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1)

__A_ = TypeVar("__A_")

def _expr1644() -> TypeInfo:
    return record_type("ARCtrl.Json.ROCrateContext.Data.IContext", [], IContext, lambda: [("sdo", string_type), ("arc", string_type), ("Data", string_type), ("ArcData", string_type), ("type", string_type), ("name", string_type), ("comments", string_type)])


@dataclass(eq = False, repr = False, slots = True)
class IContext(Record):
    sdo: str
    arc: str
    Data: str
    ArcData: str
    type: str
    name: str
    comments: str

IContext_reflection = _expr1644

def _arrow1653(__unit: None=None) -> IEncodable:
    class ObjectExpr1645(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
            return helpers.encode_string("http://schema.org/")

    class ObjectExpr1646(IEncodable):
        def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
            return helpers_1.encode_string("sdo:MediaObject")

    class ObjectExpr1647(IEncodable):
        def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
            return helpers_2.encode_string("sdo:disambiguatingDescription")

    class ObjectExpr1648(IEncodable):
        def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
            return helpers_3.encode_string("sdo:encodingFormat")

    class ObjectExpr1649(IEncodable):
        def Encode(self, helpers_4: IEncoderHelpers_1[Any]) -> Any:
            return helpers_4.encode_string("sdo:usageInfo")

    class ObjectExpr1650(IEncodable):
        def Encode(self, helpers_5: IEncoderHelpers_1[Any]) -> Any:
            return helpers_5.encode_string("sdo:name")

    class ObjectExpr1651(IEncodable):
        def Encode(self, helpers_6: IEncoderHelpers_1[Any]) -> Any:
            return helpers_6.encode_string("sdo:comment")

    values: IEnumerable_1[tuple[str, IEncodable]] = to_enumerable([("sdo", ObjectExpr1645()), ("Data", ObjectExpr1646()), ("type", ObjectExpr1647()), ("encodingFormat", ObjectExpr1648()), ("usageInfo", ObjectExpr1649()), ("name", ObjectExpr1650()), ("comments", ObjectExpr1651())])
    class ObjectExpr1652(IEncodable):
        def Encode(self, helpers_7: IEncoderHelpers_1[Any]) -> Any:
            def mapping(tupled_arg: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg[0], tupled_arg[1].Encode(helpers_7))

            arg: IEnumerable_1[tuple[str, __A_]] = map(mapping, values)
            return helpers_7.encode_object(arg)

    return ObjectExpr1652()


context_jsonvalue: IEncodable = _arrow1653()

context_str: str = "\r\n{\r\n  \"@context\": {\r\n    \"sdo\": \"http://schema.org/\",\r\n    \"arc\": \"http://purl.org/nfdi4plants/ontology/\",\r\n\r\n    \"Data\": \"sdo:MediaObject\",\r\n    \"ArcData\": \"arc:ARC#ARC_00000076\",\r\n\r\n    \"type\": \"arc:ARC#ARC_00000107\",\r\n\r\n    \"name\": \"sdo:name\",\r\n    \"comments\": \"sdo:disambiguatingDescription\"\r\n  }\r\n}\r\n    "

__all__ = ["IContext_reflection", "context_jsonvalue", "context_str"]

