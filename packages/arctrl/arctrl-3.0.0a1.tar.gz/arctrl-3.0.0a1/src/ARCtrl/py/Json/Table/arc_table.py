from __future__ import annotations
from collections.abc import Callable
from typing import (Any, TypeVar)
from ...fable_modules.fable_library.array_ import (map as map_2, iterate_indexed, fold, fill)
from ...fable_modules.fable_library.list import (FSharpList, empty as empty_1)
from ...fable_modules.fable_library.map import (of_seq, empty as empty_2)
from ...fable_modules.fable_library.map_util import (get_item_from_dict, add_to_dict)
from ...fable_modules.fable_library.mutable_map import Dictionary
from ...fable_modules.fable_library.option import default_arg
from ...fable_modules.fable_library.range import range_big_int
from ...fable_modules.fable_library.result import FSharpResult_2
from ...fable_modules.fable_library.seq import (to_list, delay, append, singleton, map, empty, collect, to_array)
from ...fable_modules.fable_library.types import Array
from ...fable_modules.fable_library.util import (IEnumerable_1, compare_arrays, equal_arrays, array_hash, equals, to_enumerable, int32_to_string, ignore)
from ...fable_modules.thoth_json_core.decode import (object, list_1 as list_1_1, IOptionalGetter, map_0027, tuple2 as tuple2_1, int_1, IRequiredGetter, string, IGetters, array as array_2, Helpers_prependPath)
from ...fable_modules.thoth_json_core.encode import (list_1, map as map_1, tuple2)
from ...fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1, Decoder_1, ErrorReason_1, IDecoderHelpers_1)
from ...Core.ontology_annotation import OntologyAnnotation
from ...Core.Table.arc_table import ArcTable
from ...Core.Table.composite_cell import CompositeCell
from ...Core.Table.composite_header import CompositeHeader
from ..string_table import (encode_string, decode_string)
from .cell_table import (encode_cell, decode_cell)
from .composite_cell import (encoder as encoder_2, decoder as decoder_2)
from .composite_header import (encoder as encoder_1, decoder as decoder_1)

__A_ = TypeVar("__A_")

_VALUE_ = TypeVar("_VALUE_")

_VALUE = TypeVar("_VALUE")

def encoder(table: ArcTable) -> IEncodable:
    def _arrow2778(__unit: None=None, table: Any=table) -> IEnumerable_1[tuple[str, IEncodable]]:
        def _arrow2767(__unit: None=None) -> IEncodable:
            value_4: str = table.Name
            class ObjectExpr2766(IEncodable):
                def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_2.encode_string(value_4)

            return ObjectExpr2766()

        def _arrow2777(__unit: None=None) -> IEnumerable_1[tuple[str, IEncodable]]:
            def _arrow2768(__unit: None=None) -> IEnumerable_1[IEncodable]:
                return map(encoder_1, table.Headers)

            def _arrow2776(__unit: None=None) -> IEnumerable_1[tuple[str, IEncodable]]:
                def key_encoder(tupled_arg: tuple[int, int]) -> IEncodable:
                    def _arrow2770(value: int, tupled_arg: Any=tupled_arg) -> IEncodable:
                        class ObjectExpr2769(IEncodable):
                            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                                return helpers.encode_signed_integral_number(value)

                        return ObjectExpr2769()

                    def _arrow2772(value_2: int, tupled_arg: Any=tupled_arg) -> IEncodable:
                        class ObjectExpr2771(IEncodable):
                            def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                                return helpers_1.encode_signed_integral_number(value_2)

                        return ObjectExpr2771()

                    return tuple2(_arrow2770, _arrow2772, tupled_arg[0], tupled_arg[1])

                def _arrow2774(__unit: None=None) -> IEnumerable_1[tuple[tuple[int, int], CompositeCell]]:
                    def _arrow2773(match_value: Any) -> IEnumerable_1[tuple[tuple[int, int], CompositeCell]]:
                        active_pattern_result: tuple[tuple[int, int], CompositeCell] = match_value
                        return singleton((active_pattern_result[0], active_pattern_result[1]))

                    return collect(_arrow2773, table.Values)

                class ObjectExpr2775:
                    @property
                    def Compare(self) -> Callable[[tuple[int, int], tuple[int, int]], int]:
                        return compare_arrays

                return singleton(("values", map_1(key_encoder, encoder_2, of_seq(to_list(delay(_arrow2774)), ObjectExpr2775())))) if (len(table.Values) != 0) else empty()

            return append(singleton(("header", list_1(to_list(delay(_arrow2768))))) if (len(table.Headers) != 0) else empty(), delay(_arrow2776))

        return append(singleton(("name", _arrow2767())), delay(_arrow2777))

    values: IEnumerable_1[tuple[str, IEncodable]] = to_list(delay(_arrow2778))
    class ObjectExpr2779(IEncodable):
        def Encode(self, helpers_3: IEncoderHelpers_1[Any], table: Any=table) -> Any:
            def mapping(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_3))

            arg: IEnumerable_1[tuple[str, __A_]] = map(mapping, values)
            return helpers_3.encode_object(arg)

    return ObjectExpr2779()


def _arrow2785(get: IGetters) -> ArcTable:
    def _arrow2780(__unit: None=None) -> FSharpList[CompositeHeader] | None:
        arg_1: Decoder_1[FSharpList[CompositeHeader]] = list_1_1(decoder_1)
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("header", arg_1)

    decoded_header: Array[CompositeHeader] = list(default_arg(_arrow2780(), empty_1()))
    def _arrow2781(__unit: None=None) -> Any | None:
        arg_3: Decoder_1[Any] = map_0027(tuple2_1(int_1, int_1), decoder_2)
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("values", arg_3)

    class ObjectExpr2782:
        @property
        def Compare(self) -> Callable[[tuple[int, int], tuple[int, int]], int]:
            return compare_arrays

    class ObjectExpr2783:
        @property
        def Equals(self) -> Callable[[tuple[int, int], tuple[int, int]], bool]:
            return equal_arrays

        @property
        def GetHashCode(self) -> Callable[[tuple[int, int]], int]:
            return array_hash

    decoded_values: Any = Dictionary(default_arg(_arrow2781(), empty_2(ObjectExpr2782())), ObjectExpr2783())
    def _arrow2784(__unit: None=None) -> str:
        object_arg_2: IRequiredGetter = get.Required
        return object_arg_2.Field("name", string)

    return ArcTable.create(_arrow2784(), decoded_header, decoded_values)


decoder: Decoder_1[ArcTable] = object(_arrow2785)

def encoder_compressed_column(column_index: int, row_count: int, cell_table: Any, table: ArcTable) -> IEncodable:
    if True if table.Headers[column_index].IsIOType else (row_count < 100):
        def _arrow2787(__unit: None=None, column_index: Any=column_index, row_count: Any=row_count, cell_table: Any=cell_table, table: Any=table) -> IEnumerable_1[IEncodable]:
            def _arrow2786(r: int) -> IEncodable:
                return encode_cell(cell_table, get_item_from_dict(table.Values, (column_index, r)))

            return map(_arrow2786, range_big_int(0, 1, row_count - 1))

        values: Array[IEncodable] = to_array(delay(_arrow2787))
        class ObjectExpr2788(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any], column_index: Any=column_index, row_count: Any=row_count, cell_table: Any=cell_table, table: Any=table) -> Any:
                def mapping(v: IEncodable) -> __A_:
                    return v.Encode(helpers)

                arg: Array[__A_] = map_2(mapping, values, None)
                return helpers.encode_array(arg)

        return ObjectExpr2788()

    else: 
        current: CompositeCell = get_item_from_dict(table.Values, (column_index, 0))
        from_: int = 0
        def _arrow2807(__unit: None=None, column_index: Any=column_index, row_count: Any=row_count, cell_table: Any=cell_table, table: Any=table) -> IEnumerable_1[IEncodable]:
            def _arrow2796(i: int) -> IEnumerable_1[IEncodable]:
                next_1: CompositeCell = get_item_from_dict(table.Values, (column_index, i))
                def _arrow2794(__unit: None=None) -> IEncodable:
                    def _arrow2790(__unit: None=None) -> IEncodable:
                        value: int = from_ or 0
                        class ObjectExpr2789(IEncodable):
                            def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                                return helpers_1.encode_signed_integral_number(value)

                        return ObjectExpr2789()

                    def _arrow2792(__unit: None=None) -> IEncodable:
                        value_1: int = (i - 1) or 0
                        class ObjectExpr2791(IEncodable):
                            def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                                return helpers_2.encode_signed_integral_number(value_1)

                        return ObjectExpr2791()

                    values_1: IEnumerable_1[tuple[str, IEncodable]] = to_enumerable([("f", _arrow2790()), ("t", _arrow2792()), ("v", encode_cell(cell_table, current))])
                    class ObjectExpr2793(IEncodable):
                        def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                            def mapping_1(tupled_arg: tuple[str, IEncodable]) -> tuple[str, __A_]:
                                return (tupled_arg[0], tupled_arg[1].Encode(helpers_3))

                            arg_1: IEnumerable_1[tuple[str, __A_]] = map(mapping_1, values_1)
                            return helpers_3.encode_object(arg_1)

                    return ObjectExpr2793()

                def _arrow2795(__unit: None=None) -> IEnumerable_1[IEncodable]:
                    nonlocal current, from_
                    current = next_1
                    from_ = i or 0
                    return empty()

                return append(singleton(_arrow2794()), delay(_arrow2795)) if (not equals(next_1, current)) else empty()

            def _arrow2806(__unit: None=None) -> IEnumerable_1[IEncodable]:
                def _arrow2805(__unit: None=None) -> IEncodable:
                    def _arrow2798(__unit: None=None) -> IEncodable:
                        value_2: int = from_ or 0
                        class ObjectExpr2797(IEncodable):
                            def Encode(self, helpers_4: IEncoderHelpers_1[Any]) -> Any:
                                return helpers_4.encode_signed_integral_number(value_2)

                        return ObjectExpr2797()

                    def _arrow2801(__unit: None=None) -> IEncodable:
                        value_3: int = (row_count - 1) or 0
                        class ObjectExpr2799(IEncodable):
                            def Encode(self, helpers_5: IEncoderHelpers_1[Any]) -> Any:
                                return helpers_5.encode_signed_integral_number(value_3)

                        return ObjectExpr2799()

                    values_2: IEnumerable_1[tuple[str, IEncodable]] = to_enumerable([("f", _arrow2798()), ("t", _arrow2801()), ("v", encode_cell(cell_table, current))])
                    class ObjectExpr2804(IEncodable):
                        def Encode(self, helpers_6: IEncoderHelpers_1[Any]) -> Any:
                            def mapping_2(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_6))

                            arg_2: IEnumerable_1[tuple[str, __A_]] = map(mapping_2, values_2)
                            return helpers_6.encode_object(arg_2)

                    return ObjectExpr2804()

                return singleton(_arrow2805())

            return append(collect(_arrow2796, range_big_int(1, 1, row_count - 1)), delay(_arrow2806))

        values_3: Array[IEncodable] = to_array(delay(_arrow2807))
        class ObjectExpr2810(IEncodable):
            def Encode(self, helpers_7: IEncoderHelpers_1[Any], column_index: Any=column_index, row_count: Any=row_count, cell_table: Any=cell_table, table: Any=table) -> Any:
                def mapping_3(v_3: IEncodable) -> __A_:
                    return v_3.Encode(helpers_7)

                arg_3: Array[__A_] = map_2(mapping_3, values_3, None)
                return helpers_7.encode_array(arg_3)

        return ObjectExpr2810()



def decoder_compressed_column(cell_table: Array[CompositeCell], table: ArcTable, column_index: int) -> Decoder_1[None]:
    class ObjectExpr2817(Decoder_1[None]):
        def Decode(self, helper: IDecoderHelpers_1[Any], column: Any, cell_table: Any=cell_table, table: Any=table, column_index: Any=column_index) -> FSharpResult_2[None, tuple[str, ErrorReason_1[__A_]]]:
            match_value: FSharpResult_2[Array[CompositeCell], tuple[str, ErrorReason_1[__A_]]] = array_2(decode_cell(cell_table)).Decode(helper, column)
            if match_value.tag == 1:
                def _arrow2816(get: IGetters) -> None:
                    from_: int
                    object_arg: IRequiredGetter = get.Required
                    from_ = object_arg.Field("f", int_1)
                    to_: int
                    object_arg_1: IRequiredGetter = get.Required
                    to_ = object_arg_1.Field("t", int_1)
                    value: CompositeCell
                    arg_5: Decoder_1[CompositeCell] = decode_cell(cell_table)
                    object_arg_2: IRequiredGetter = get.Required
                    value = object_arg_2.Field("v", arg_5)
                    for i in range(from_, to_ + 1, 1):
                        add_to_dict(table.Values, (column_index, i), value)

                range_decoder: Decoder_1[None] = object(_arrow2816)
                match_value_1: FSharpResult_2[Array[None], tuple[str, ErrorReason_1[__A_]]] = array_2(range_decoder).Decode(helper, column)
                return FSharpResult_2(1, match_value_1.fields[0]) if (match_value_1.tag == 1) else FSharpResult_2(0, None)

            else: 
                def action(r: int, cell: CompositeCell) -> None:
                    add_to_dict(table.Values, (column_index, r), cell)

                iterate_indexed(action, match_value.fields[0])
                return FSharpResult_2(0, None)


    return ObjectExpr2817()


def arrayi(decoderi: Callable[[int], Decoder_1[_VALUE]]) -> Decoder_1[Array[Any]]:
    class ObjectExpr2826(Decoder_1[Array[_VALUE_]]):
        def Decode(self, helpers: IDecoderHelpers_1[Any], value: Any, decoderi: Any=decoderi) -> FSharpResult_2[Array[_VALUE_], tuple[str, ErrorReason_1[__A_]]]:
            if helpers.is_array(value):
                i: int = -1
                tokens: Array[__A_] = helpers.as_array(value)
                def folder(acc: FSharpResult_2[Array[_VALUE_], tuple[str, ErrorReason_1[__A_]]], value_1: __A_) -> FSharpResult_2[Array[_VALUE_], tuple[str, ErrorReason_1[__A_]]]:
                    nonlocal i
                    i = (i + 1) or 0
                    if acc.tag == 0:
                        acc_1: Array[_VALUE_] = acc.fields[0]
                        match_value: FSharpResult_2[_VALUE_, tuple[str, ErrorReason_1[__A_]]] = decoderi(i).Decode(helpers, value_1)
                        if match_value.tag == 0:
                            acc_1[i] = match_value.fields[0]
                            return FSharpResult_2(0, acc_1)

                        else: 
                            def _arrow2824(__unit: None=None, acc: Any=acc, value_1: Any=value_1) -> tuple[str, ErrorReason_1[__A_]]:
                                tupled_arg: tuple[str, ErrorReason_1[__A_]] = match_value.fields[0]
                                return Helpers_prependPath((".[" + int32_to_string(i)) + "]", tupled_arg[0], tupled_arg[1])

                            return FSharpResult_2(1, _arrow2824())


                    else: 
                        return acc


                return fold(folder, FSharpResult_2(0, fill([0] * len(tokens), 0, len(tokens), None)), tokens)

            else: 
                return FSharpResult_2(1, ("", ErrorReason_1(0, "an array", value)))


    return ObjectExpr2826()


def encoder_compressed(string_table: Any, oa_table: Any, cell_table: Any, table: ArcTable) -> IEncodable:
    def _arrow2835(__unit: None=None, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, table: Any=table) -> IEnumerable_1[tuple[str, IEncodable]]:
        def _arrow2834(__unit: None=None) -> IEnumerable_1[tuple[str, IEncodable]]:
            def _arrow2827(__unit: None=None) -> IEnumerable_1[IEncodable]:
                return map(encoder_1, table.Headers)

            def _arrow2833(__unit: None=None) -> IEnumerable_1[tuple[str, IEncodable]]:
                if len(table.Values) != 0:
                    row_count: int = table.RowCount or 0
                    def _arrow2829(__unit: None=None) -> IEnumerable_1[IEncodable]:
                        def _arrow2828(c: int) -> IEncodable:
                            return encoder_compressed_column(c, row_count, cell_table, table)

                        return map(_arrow2828, range_big_int(0, 1, table.ColumnCount - 1))

                    columns: Array[IEncodable] = to_array(delay(_arrow2829))
                    class ObjectExpr2831(IEncodable):
                        def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                            def mapping(v: IEncodable) -> __A_:
                                return v.Encode(helpers)

                            arg: Array[__A_] = map_2(mapping, columns, None)
                            return helpers.encode_array(arg)

                    return singleton(("c", ObjectExpr2831()))

                else: 
                    return empty()


            return append(singleton(("h", list_1(to_list(delay(_arrow2827))))) if (len(table.Headers) != 0) else empty(), delay(_arrow2833))

        return append(singleton(("n", encode_string(string_table, table.Name))), delay(_arrow2834))

    values_1: IEnumerable_1[tuple[str, IEncodable]] = to_list(delay(_arrow2835))
    class ObjectExpr2836(IEncodable):
        def Encode(self, helpers_1: IEncoderHelpers_1[Any], string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table, table: Any=table) -> Any:
            def mapping_1(tupled_arg: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg[0], tupled_arg[1].Encode(helpers_1))

            arg_1: IEnumerable_1[tuple[str, __A_]] = map(mapping_1, values_1)
            return helpers_1.encode_object(arg_1)

    return ObjectExpr2836()


def decoder_compressed(string_table: Array[str], oa_table: Array[OntologyAnnotation], cell_table: Array[CompositeCell]) -> Decoder_1[ArcTable]:
    def _arrow2850(get: IGetters, string_table: Any=string_table, oa_table: Any=oa_table, cell_table: Any=cell_table) -> ArcTable:
        def _arrow2841(__unit: None=None) -> FSharpList[CompositeHeader] | None:
            arg_1: Decoder_1[FSharpList[CompositeHeader]] = list_1_1(decoder_1)
            object_arg: IOptionalGetter = get.Optional
            return object_arg.Field("h", arg_1)

        decoded_header: Array[CompositeHeader] = list(default_arg(_arrow2841(), empty_1()))
        def _arrow2846(__unit: None=None) -> str:
            arg_3: Decoder_1[str] = decode_string(string_table)
            object_arg_1: IRequiredGetter = get.Required
            return object_arg_1.Field("n", arg_3)

        class ObjectExpr2847:
            @property
            def Equals(self) -> Callable[[tuple[int, int], tuple[int, int]], bool]:
                return equal_arrays

            @property
            def GetHashCode(self) -> Callable[[tuple[int, int]], int]:
                return array_hash

        table: ArcTable = ArcTable.create(_arrow2846(), decoded_header, Dictionary([], ObjectExpr2847()))
        def _arrow2849(__unit: None=None) -> Array[None] | None:
            def _arrow2848(column_index: int) -> Decoder_1[None]:
                return decoder_compressed_column(cell_table, table, column_index)

            arg_5: Decoder_1[Array[None]] = arrayi(_arrow2848)
            object_arg_2: IOptionalGetter = get.Optional
            return object_arg_2.Field("c", arg_5)

        ignore(_arrow2849())
        return table

    return object(_arrow2850)


__all__ = ["encoder", "decoder", "encoder_compressed_column", "decoder_compressed_column", "arrayi", "encoder_compressed", "decoder_compressed"]

