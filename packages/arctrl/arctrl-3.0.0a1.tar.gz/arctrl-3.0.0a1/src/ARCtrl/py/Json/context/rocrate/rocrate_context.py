from __future__ import annotations
from dataclasses import dataclass
from typing import (Any, TypeVar)
from ....fable_modules.fable_library.reflection import (TypeInfo, string_type, record_type)
from ....fable_modules.fable_library.seq import map
from ....fable_modules.fable_library.types import Record
from ....fable_modules.fable_library.util import (to_enumerable, IEnumerable_1)
from ....fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1)

__A_ = TypeVar("__A_")

def _expr1864() -> TypeInfo:
    return record_type("ARCtrl.Json.ROCrateContext.ROCrate.IContext", [], IContext, lambda: [("sdo", string_type), ("arc", string_type), ("CreativeWork", string_type), ("about", string_type), ("conforms_to", string_type)])


@dataclass(eq = False, repr = False, slots = True)
class IContext(Record):
    sdo: str
    arc: str
    CreativeWork: str
    about: str
    conforms_to: str

IContext_reflection = _expr1864

def _arrow1867(__unit: None=None) -> IEncodable:
    class ObjectExpr1865(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
            return helpers.encode_string("https://w3id.org/ro/crate/1.1")

    values: IEnumerable_1[tuple[str, IEncodable]] = to_enumerable([("@id", ObjectExpr1865())])
    class ObjectExpr1866(IEncodable):
        def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
            def mapping(tupled_arg: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg[0], tupled_arg[1].Encode(helpers_1))

            arg: IEnumerable_1[tuple[str, __A_]] = map(mapping, values)
            return helpers_1.encode_object(arg)

    return ObjectExpr1866()


conforms_to_jsonvalue: IEncodable = _arrow1867()

def _arrow1875(__unit: None=None) -> IEncodable:
    class ObjectExpr1868(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
            return helpers.encode_string("http://schema.org/")

    class ObjectExpr1869(IEncodable):
        def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
            return helpers_1.encode_string("http://purl.org/nfdi4plants/ontology/")

    class ObjectExpr1870(IEncodable):
        def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
            return helpers_2.encode_string("sdo:CreativeWork")

    class ObjectExpr1871(IEncodable):
        def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
            return helpers_3.encode_string("sdo:about")

    class ObjectExpr1873(IEncodable):
        def Encode(self, helpers_4: IEncoderHelpers_1[Any]) -> Any:
            return helpers_4.encode_string("http://purl.org/dc/terms/conformsTo")

    values: IEnumerable_1[tuple[str, IEncodable]] = to_enumerable([("sdo", ObjectExpr1868()), ("arc", ObjectExpr1869()), ("CreativeWork", ObjectExpr1870()), ("about", ObjectExpr1871()), ("conformsTo", ObjectExpr1873())])
    class ObjectExpr1874(IEncodable):
        def Encode(self, helpers_5: IEncoderHelpers_1[Any]) -> Any:
            def mapping(tupled_arg: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg[0], tupled_arg[1].Encode(helpers_5))

            arg: IEnumerable_1[tuple[str, __A_]] = map(mapping, values)
            return helpers_5.encode_object(arg)

    return ObjectExpr1874()


context_jsonvalue: IEncodable = _arrow1875()

__all__ = ["IContext_reflection", "conforms_to_jsonvalue", "context_jsonvalue"]

