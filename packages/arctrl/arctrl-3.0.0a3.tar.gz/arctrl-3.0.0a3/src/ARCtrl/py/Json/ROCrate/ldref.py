from __future__ import annotations
from typing import (Any, TypeVar)
from ...fable_modules.fable_library.list import (singleton, FSharpList)
from ...fable_modules.fable_library.seq import map
from ...fable_modules.fable_library.util import IEnumerable_1
from ...fable_modules.thoth_json_core.decode import (object, IRequiredGetter, string, IGetters)
from ...fable_modules.thoth_json_core.types import (Decoder_1, IEncodable, IEncoderHelpers_1)
from ...ROCrate.ldobject import LDRef

__A_ = TypeVar("__A_")

def _arrow1888(decoders: IGetters) -> LDRef:
    def _arrow1887(__unit: None=None) -> str:
        object_arg: IRequiredGetter = decoders.Required
        return object_arg.Field("@id", string)

    return LDRef(_arrow1887())


decoder: Decoder_1[LDRef] = object(_arrow1888)

def encoder(r: LDRef) -> IEncodable:
    def _arrow1890(__unit: None=None, r: Any=r) -> IEncodable:
        value: str = r.Id
        class ObjectExpr1889(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr1889()

    values: FSharpList[tuple[str, IEncodable]] = singleton(("@id", _arrow1890()))
    class ObjectExpr1891(IEncodable):
        def Encode(self, helpers_1: IEncoderHelpers_1[Any], r: Any=r) -> Any:
            def mapping(tupled_arg: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg[0], tupled_arg[1].Encode(helpers_1))

            arg: IEnumerable_1[tuple[str, __A_]] = map(mapping, values)
            return helpers_1.encode_object(arg)

    return ObjectExpr1891()


__all__ = ["decoder", "encoder"]

