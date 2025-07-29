from __future__ import annotations
from dataclasses import dataclass
from typing import (Any, TypeVar)
from ....fable_modules.fable_library.reflection import (TypeInfo, string_type, record_type)
from ....fable_modules.fable_library.seq import map
from ....fable_modules.fable_library.types import Record
from ....fable_modules.fable_library.util import (to_enumerable, IEnumerable_1)
from ....fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1)

__A_ = TypeVar("__A_")

def _expr1810() -> TypeInfo:
    return record_type("ARCtrl.Json.ROCrateContext.ProtocolParameter.IContext", [], IContext, lambda: [("sdo", string_type), ("arc", string_type), ("ProtocolParamter", string_type), ("ArcProtocolParameter", string_type), ("parameter_name", string_type)])


@dataclass(eq = False, repr = False, slots = True)
class IContext(Record):
    sdo: str
    arc: str
    ProtocolParamter: str
    ArcProtocolParameter: str
    parameter_name: str

IContext_reflection = _expr1810

def _arrow1817(__unit: None=None) -> IEncodable:
    class ObjectExpr1811(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
            return helpers.encode_string("http://schema.org/")

    class ObjectExpr1812(IEncodable):
        def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
            return helpers_1.encode_string("http://purl.org/nfdi4plants/ontology/")

    class ObjectExpr1813(IEncodable):
        def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
            return helpers_2.encode_string("sdo:Thing")

    class ObjectExpr1814(IEncodable):
        def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
            return helpers_3.encode_string("arc:ARC#ARC_00000063")

    class ObjectExpr1815(IEncodable):
        def Encode(self, helpers_4: IEncoderHelpers_1[Any]) -> Any:
            return helpers_4.encode_string("arc:ARC#ARC_00000100")

    values: IEnumerable_1[tuple[str, IEncodable]] = to_enumerable([("sdo", ObjectExpr1811()), ("arc", ObjectExpr1812()), ("ProtocolParameter", ObjectExpr1813()), ("ArcProtocolParameter", ObjectExpr1814()), ("parameterName", ObjectExpr1815())])
    class ObjectExpr1816(IEncodable):
        def Encode(self, helpers_5: IEncoderHelpers_1[Any]) -> Any:
            def mapping(tupled_arg: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg[0], tupled_arg[1].Encode(helpers_5))

            arg: IEnumerable_1[tuple[str, __A_]] = map(mapping, values)
            return helpers_5.encode_object(arg)

    return ObjectExpr1816()


context_jsonvalue: IEncodable = _arrow1817()

context_str: str = "\r\n{\r\n  \"@context\": {\r\n    \"sdo\": \"http://schema.org/\",\r\n    \"arc\": \"http://purl.org/nfdi4plants/ontology/\",\r\n\r\n    \"ProtocolParameter\": \"sdo:Thing\",\r\n    \"ArcProtocolParameter\": \"arc:ARC#ARC_00000063\",\r\n\r\n    \"parameterName\": \"arc:ARC#ARC_00000100\"\r\n  }\r\n}\r\n    "

__all__ = ["IContext_reflection", "context_jsonvalue", "context_str"]

