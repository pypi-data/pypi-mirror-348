from __future__ import annotations
from collections.abc import Callable
from typing import (Any, TypeVar)
from ..fable_modules.fable_library.array_ import map as map_2
from ..fable_modules.fable_library.list import (choose, of_array, FSharpList)
from ..fable_modules.fable_library.option import (map, default_arg)
from ..fable_modules.fable_library.seq import (map as map_1, try_pick)
from ..fable_modules.fable_library.string_ import (replace, split, join)
from ..fable_modules.fable_library.types import Array
from ..fable_modules.fable_library.util import IEnumerable_1
from ..fable_modules.thoth_json_core.decode import (object, IOptionalGetter, string, resize_array, IGetters, IRequiredGetter, map as map_3, array as array_3)
from ..fable_modules.thoth_json_core.types import (IEncodable, IEncoderHelpers_1, Decoder_1)
from ..Core.comment import Comment
from ..Core.conversion import (Person_setCommentFromORCID, Person_setOrcidFromComments)
from ..Core.ontology_annotation import OntologyAnnotation
from ..Core.person import Person
from .comment import (encoder as encoder_1, decoder as decoder_1, ROCrate_encoderDisambiguatingDescription, ROCrate_decoderDisambiguatingDescription)
from .context.rocrate.isa_organization_context import context_jsonvalue
from .context.rocrate.isa_person_context import (context_jsonvalue as context_jsonvalue_1, context_minimal_json_value)
from .decode import Decode_objectNoAdditionalProperties
from .encode import (try_include, try_include_seq)
from .idtable import encode
from .ontology_annotation import (OntologyAnnotation_encoder, OntologyAnnotation_decoder, OntologyAnnotation_ROCrate_encoderDefinedTerm, OntologyAnnotation_ROCrate_decoderDefinedTerm)

__A_ = TypeVar("__A_")

def encoder(person: Person) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], person: Any=person) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow2318(value: str, person: Any=person) -> IEncodable:
        class ObjectExpr2317(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr2317()

    def _arrow2321(value_2: str, person: Any=person) -> IEncodable:
        class ObjectExpr2320(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                return helpers_1.encode_string(value_2)

        return ObjectExpr2320()

    def _arrow2323(value_4: str, person: Any=person) -> IEncodable:
        class ObjectExpr2322(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                return helpers_2.encode_string(value_4)

        return ObjectExpr2322()

    def _arrow2325(value_6: str, person: Any=person) -> IEncodable:
        class ObjectExpr2324(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                return helpers_3.encode_string(value_6)

        return ObjectExpr2324()

    def _arrow2328(value_8: str, person: Any=person) -> IEncodable:
        class ObjectExpr2327(IEncodable):
            def Encode(self, helpers_4: IEncoderHelpers_1[Any]) -> Any:
                return helpers_4.encode_string(value_8)

        return ObjectExpr2327()

    def _arrow2331(value_10: str, person: Any=person) -> IEncodable:
        class ObjectExpr2330(IEncodable):
            def Encode(self, helpers_5: IEncoderHelpers_1[Any]) -> Any:
                return helpers_5.encode_string(value_10)

        return ObjectExpr2330()

    def _arrow2333(value_12: str, person: Any=person) -> IEncodable:
        class ObjectExpr2332(IEncodable):
            def Encode(self, helpers_6: IEncoderHelpers_1[Any]) -> Any:
                return helpers_6.encode_string(value_12)

        return ObjectExpr2332()

    def _arrow2337(value_14: str, person: Any=person) -> IEncodable:
        class ObjectExpr2335(IEncodable):
            def Encode(self, helpers_7: IEncoderHelpers_1[Any]) -> Any:
                return helpers_7.encode_string(value_14)

        return ObjectExpr2335()

    def _arrow2340(value_16: str, person: Any=person) -> IEncodable:
        class ObjectExpr2339(IEncodable):
            def Encode(self, helpers_8: IEncoderHelpers_1[Any]) -> Any:
                return helpers_8.encode_string(value_16)

        return ObjectExpr2339()

    def _arrow2341(oa: OntologyAnnotation, person: Any=person) -> IEncodable:
        return OntologyAnnotation_encoder(oa)

    def _arrow2344(comment: Comment, person: Any=person) -> IEncodable:
        return encoder_1(comment)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([try_include("firstName", _arrow2318, person.FirstName), try_include("lastName", _arrow2321, person.LastName), try_include("midInitials", _arrow2323, person.MidInitials), try_include("orcid", _arrow2325, person.ORCID), try_include("email", _arrow2328, person.EMail), try_include("phone", _arrow2331, person.Phone), try_include("fax", _arrow2333, person.Fax), try_include("address", _arrow2337, person.Address), try_include("affiliation", _arrow2340, person.Affiliation), try_include_seq("roles", _arrow2341, person.Roles), try_include_seq("comments", _arrow2344, person.Comments)]))
    class ObjectExpr2345(IEncodable):
        def Encode(self, helpers_9: IEncoderHelpers_1[Any], person: Any=person) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_9))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_9.encode_object(arg)

    return ObjectExpr2345()


def _arrow2357(get: IGetters) -> Person:
    def _arrow2346(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("orcid", string)

    def _arrow2347(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("lastName", string)

    def _arrow2348(__unit: None=None) -> str | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("firstName", string)

    def _arrow2349(__unit: None=None) -> str | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("midInitials", string)

    def _arrow2350(__unit: None=None) -> str | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("email", string)

    def _arrow2351(__unit: None=None) -> str | None:
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("phone", string)

    def _arrow2352(__unit: None=None) -> str | None:
        object_arg_6: IOptionalGetter = get.Optional
        return object_arg_6.Field("fax", string)

    def _arrow2353(__unit: None=None) -> str | None:
        object_arg_7: IOptionalGetter = get.Optional
        return object_arg_7.Field("address", string)

    def _arrow2354(__unit: None=None) -> str | None:
        object_arg_8: IOptionalGetter = get.Optional
        return object_arg_8.Field("affiliation", string)

    def _arrow2355(__unit: None=None) -> Array[OntologyAnnotation] | None:
        arg_19: Decoder_1[Array[OntologyAnnotation]] = resize_array(OntologyAnnotation_decoder)
        object_arg_9: IOptionalGetter = get.Optional
        return object_arg_9.Field("roles", arg_19)

    def _arrow2356(__unit: None=None) -> Array[Comment] | None:
        arg_21: Decoder_1[Array[Comment]] = resize_array(decoder_1)
        object_arg_10: IOptionalGetter = get.Optional
        return object_arg_10.Field("comments", arg_21)

    return Person(_arrow2346(), _arrow2347(), _arrow2348(), _arrow2349(), _arrow2350(), _arrow2351(), _arrow2352(), _arrow2353(), _arrow2354(), _arrow2355(), _arrow2356())


decoder: Decoder_1[Person] = object(_arrow2357)

def ROCrate_genID(p: Person) -> str:
    def chooser(c: Comment, p: Any=p) -> str | None:
        match_value: str | None = c.Name
        match_value_1: str | None = c.Value
        (pattern_matching_result, n, v) = (None, None, None)
        if match_value is not None:
            if match_value_1 is not None:
                pattern_matching_result = 0
                n = match_value
                v = match_value_1

            else: 
                pattern_matching_result = 1


        else: 
            pattern_matching_result = 1

        if pattern_matching_result == 0:
            if True if (True if (n == "orcid") else (n == "Orcid")) else (n == "ORCID"):
                return v

            else: 
                return None


        elif pattern_matching_result == 1:
            return None


    orcid: str | None = try_pick(chooser, p.Comments)
    if orcid is None:
        match_value_1: str | None = p.EMail
        if match_value_1 is None:
            match_value_2: str | None = p.FirstName
            match_value_3: str | None = p.MidInitials
            match_value_4: str | None = p.LastName
            (pattern_matching_result_1, fn, ln, mn, fn_1, ln_1, ln_2, fn_2) = (None, None, None, None, None, None, None, None)
            if match_value_2 is None:
                if match_value_3 is None:
                    if match_value_4 is not None:
                        pattern_matching_result_1 = 2
                        ln_2 = match_value_4

                    else: 
                        pattern_matching_result_1 = 4


                else: 
                    pattern_matching_result_1 = 4


            elif match_value_3 is None:
                if match_value_4 is None:
                    pattern_matching_result_1 = 3
                    fn_2 = match_value_2

                else: 
                    pattern_matching_result_1 = 1
                    fn_1 = match_value_2
                    ln_1 = match_value_4


            elif match_value_4 is not None:
                pattern_matching_result_1 = 0
                fn = match_value_2
                ln = match_value_4
                mn = match_value_3

            else: 
                pattern_matching_result_1 = 4

            if pattern_matching_result_1 == 0:
                return (((("#" + replace(fn, " ", "_")) + "_") + replace(mn, " ", "_")) + "_") + replace(ln, " ", "_")

            elif pattern_matching_result_1 == 1:
                return (("#" + replace(fn_1, " ", "_")) + "_") + replace(ln_1, " ", "_")

            elif pattern_matching_result_1 == 2:
                return "#" + replace(ln_2, " ", "_")

            elif pattern_matching_result_1 == 3:
                return "#" + replace(fn_2, " ", "_")

            elif pattern_matching_result_1 == 4:
                return "#EmptyPerson"


        else: 
            return match_value_1


    else: 
        return orcid



def ROCrate_Affiliation_encoder(affiliation: str) -> IEncodable:
    class ObjectExpr2359(IEncodable):
        def Encode(self, helpers: IEncoderHelpers_1[Any], affiliation: Any=affiliation) -> Any:
            return helpers.encode_string("Organization")

    def _arrow2361(__unit: None=None, affiliation: Any=affiliation) -> IEncodable:
        value_1: str = replace(("#Organization_" + affiliation) + "", " ", "_")
        class ObjectExpr2360(IEncodable):
            def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                return helpers_1.encode_string(value_1)

        return ObjectExpr2360()

    class ObjectExpr2362(IEncodable):
        def Encode(self, helpers_2: IEncoderHelpers_1[Any], affiliation: Any=affiliation) -> Any:
            return helpers_2.encode_string(affiliation)

    values: FSharpList[tuple[str, IEncodable]] = of_array([("@type", ObjectExpr2359()), ("@id", _arrow2361()), ("name", ObjectExpr2362()), ("@context", context_jsonvalue)])
    class ObjectExpr2363(IEncodable):
        def Encode(self, helpers_3: IEncoderHelpers_1[Any], affiliation: Any=affiliation) -> Any:
            def mapping(tupled_arg: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg[0], tupled_arg[1].Encode(helpers_3))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping, values)
            return helpers_3.encode_object(arg)

    return ObjectExpr2363()


def _arrow2364(get: IGetters) -> str:
    object_arg: IRequiredGetter = get.Required
    return object_arg.Field("name", string)


ROCrate_Affiliation_decoder: Decoder_1[str] = object(_arrow2364)

def ROCrate_encoder(oa: Person) -> IEncodable:
    def chooser(tupled_arg: tuple[str, IEncodable | None], oa: Any=oa) -> tuple[str, IEncodable] | None:
        def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
            return (tupled_arg[0], v_1)

        return map(mapping, tupled_arg[1])

    def _arrow2368(__unit: None=None, oa: Any=oa) -> IEncodable:
        value: str = ROCrate_genID(oa)
        class ObjectExpr2367(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                return helpers.encode_string(value)

        return ObjectExpr2367()

    class ObjectExpr2369(IEncodable):
        def Encode(self, helpers_1: IEncoderHelpers_1[Any], oa: Any=oa) -> Any:
            return helpers_1.encode_string("Person")

    def _arrow2371(value_2: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr2370(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                return helpers_2.encode_string(value_2)

        return ObjectExpr2370()

    def _arrow2373(value_4: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr2372(IEncodable):
            def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                return helpers_3.encode_string(value_4)

        return ObjectExpr2372()

    def _arrow2375(value_6: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr2374(IEncodable):
            def Encode(self, helpers_4: IEncoderHelpers_1[Any]) -> Any:
                return helpers_4.encode_string(value_6)

        return ObjectExpr2374()

    def _arrow2377(value_8: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr2376(IEncodable):
            def Encode(self, helpers_5: IEncoderHelpers_1[Any]) -> Any:
                return helpers_5.encode_string(value_8)

        return ObjectExpr2376()

    def _arrow2379(value_10: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr2378(IEncodable):
            def Encode(self, helpers_6: IEncoderHelpers_1[Any]) -> Any:
                return helpers_6.encode_string(value_10)

        return ObjectExpr2378()

    def _arrow2381(value_12: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr2380(IEncodable):
            def Encode(self, helpers_7: IEncoderHelpers_1[Any]) -> Any:
                return helpers_7.encode_string(value_12)

        return ObjectExpr2380()

    def _arrow2383(value_14: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr2382(IEncodable):
            def Encode(self, helpers_8: IEncoderHelpers_1[Any]) -> Any:
                return helpers_8.encode_string(value_14)

        return ObjectExpr2382()

    def _arrow2385(value_16: str, oa: Any=oa) -> IEncodable:
        class ObjectExpr2384(IEncodable):
            def Encode(self, helpers_9: IEncoderHelpers_1[Any]) -> Any:
                return helpers_9.encode_string(value_16)

        return ObjectExpr2384()

    def _arrow2386(affiliation: str, oa: Any=oa) -> IEncodable:
        return ROCrate_Affiliation_encoder(affiliation)

    def _arrow2387(oa_1: OntologyAnnotation, oa: Any=oa) -> IEncodable:
        return OntologyAnnotation_ROCrate_encoderDefinedTerm(oa_1)

    def _arrow2388(comment: Comment, oa: Any=oa) -> IEncodable:
        return ROCrate_encoderDisambiguatingDescription(comment)

    values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([("@id", _arrow2368()), ("@type", ObjectExpr2369()), try_include("orcid", _arrow2371, oa.ORCID), try_include("firstName", _arrow2373, oa.FirstName), try_include("lastName", _arrow2375, oa.LastName), try_include("midInitials", _arrow2377, oa.MidInitials), try_include("email", _arrow2379, oa.EMail), try_include("phone", _arrow2381, oa.Phone), try_include("fax", _arrow2383, oa.Fax), try_include("address", _arrow2385, oa.Address), try_include("affiliation", _arrow2386, oa.Affiliation), try_include_seq("roles", _arrow2387, oa.Roles), try_include_seq("comments", _arrow2388, oa.Comments), ("@context", context_jsonvalue_1)]))
    class ObjectExpr2389(IEncodable):
        def Encode(self, helpers_10: IEncoderHelpers_1[Any], oa: Any=oa) -> Any:
            def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_10))

            arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
            return helpers_10.encode_object(arg)

    return ObjectExpr2389()


def _arrow2401(get: IGetters) -> Person:
    def _arrow2390(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("orcid", string)

    def _arrow2391(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("lastName", string)

    def _arrow2392(__unit: None=None) -> str | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("firstName", string)

    def _arrow2393(__unit: None=None) -> str | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("midInitials", string)

    def _arrow2394(__unit: None=None) -> str | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("email", string)

    def _arrow2395(__unit: None=None) -> str | None:
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("phone", string)

    def _arrow2396(__unit: None=None) -> str | None:
        object_arg_6: IOptionalGetter = get.Optional
        return object_arg_6.Field("fax", string)

    def _arrow2397(__unit: None=None) -> str | None:
        object_arg_7: IOptionalGetter = get.Optional
        return object_arg_7.Field("address", string)

    def _arrow2398(__unit: None=None) -> str | None:
        object_arg_8: IOptionalGetter = get.Optional
        return object_arg_8.Field("affiliation", ROCrate_Affiliation_decoder)

    def _arrow2399(__unit: None=None) -> Array[OntologyAnnotation] | None:
        arg_19: Decoder_1[Array[OntologyAnnotation]] = resize_array(OntologyAnnotation_ROCrate_decoderDefinedTerm)
        object_arg_9: IOptionalGetter = get.Optional
        return object_arg_9.Field("roles", arg_19)

    def _arrow2400(__unit: None=None) -> Array[Comment] | None:
        arg_21: Decoder_1[Array[Comment]] = resize_array(ROCrate_decoderDisambiguatingDescription)
        object_arg_10: IOptionalGetter = get.Optional
        return object_arg_10.Field("comments", arg_21)

    return Person(_arrow2390(), _arrow2391(), _arrow2392(), _arrow2393(), _arrow2394(), _arrow2395(), _arrow2396(), _arrow2397(), _arrow2398(), _arrow2399(), _arrow2400())


ROCrate_decoder: Decoder_1[Person] = object(_arrow2401)

def ROCrate_encodeAuthorListString(author_list: str) -> IEncodable:
    def encode_single(name: str, author_list: Any=author_list) -> IEncodable:
        def chooser(tupled_arg: tuple[str, IEncodable | None], name: Any=name) -> tuple[str, IEncodable] | None:
            def mapping_1(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
                return (tupled_arg[0], v_1)

            return map(mapping_1, tupled_arg[1])

        class ObjectExpr2404(IEncodable):
            def Encode(self, helpers: IEncoderHelpers_1[Any], name: Any=name) -> Any:
                return helpers.encode_string("Person")

        def _arrow2409(value_1: str, name: Any=name) -> IEncodable:
            class ObjectExpr2408(IEncodable):
                def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_1.encode_string(value_1)

            return ObjectExpr2408()

        values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([("@type", ObjectExpr2404()), try_include("name", _arrow2409, name), ("@context", context_minimal_json_value)]))
        class ObjectExpr2411(IEncodable):
            def Encode(self, helpers_2: IEncoderHelpers_1[Any], name: Any=name) -> Any:
                def mapping_2(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                    return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_2))

                arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_2, values)
                return helpers_2.encode_object(arg)

        return ObjectExpr2411()

    def mapping(s: str, author_list: Any=author_list) -> str:
        return s.strip()

    values_2: Array[IEncodable] = map_2(encode_single, map_2(mapping, split(author_list, ["\t" if (author_list.find("\t") >= 0) else (";" if (author_list.find(";") >= 0) else ",")], None, 0), None), None)
    class ObjectExpr2413(IEncodable):
        def Encode(self, helpers_3: IEncoderHelpers_1[Any], author_list: Any=author_list) -> Any:
            def mapping_3(v_3: IEncodable) -> __A_:
                return v_3.Encode(helpers_3)

            arg_1: Array[__A_] = map_2(mapping_3, values_2, None)
            return helpers_3.encode_array(arg_1)

    return ObjectExpr2413()


def ctor(v: Array[str]) -> str:
    return join(", ", v)


def _arrow2417(get: IGetters) -> str:
    def _arrow2416(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("name", string)

    return default_arg(_arrow2416(), "")


ROCrate_decodeAuthorListString: Decoder_1[str] = map_3(ctor, array_3(object(_arrow2417)))

ISAJson_allowedFields: FSharpList[str] = of_array(["@id", "firstName", "lastName", "midInitials", "email", "phone", "fax", "address", "affiliation", "roles", "comments", "@type", "@context"])

def ISAJson_encoder(id_map: Any | None, person: Person) -> IEncodable:
    def f(person_1: Person, id_map: Any=id_map, person: Any=person) -> IEncodable:
        person_2: Person = Person_setCommentFromORCID(person_1)
        def chooser(tupled_arg: tuple[str, IEncodable | None], person_1: Any=person_1) -> tuple[str, IEncodable] | None:
            def mapping(v_1: IEncodable, tupled_arg: Any=tupled_arg) -> tuple[str, IEncodable]:
                return (tupled_arg[0], v_1)

            return map(mapping, tupled_arg[1])

        def _arrow2421(value: str, person_1: Any=person_1) -> IEncodable:
            class ObjectExpr2420(IEncodable):
                def Encode(self, helpers: IEncoderHelpers_1[Any]) -> Any:
                    return helpers.encode_string(value)

            return ObjectExpr2420()

        def _arrow2423(value_2: str, person_1: Any=person_1) -> IEncodable:
            class ObjectExpr2422(IEncodable):
                def Encode(self, helpers_1: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_1.encode_string(value_2)

            return ObjectExpr2422()

        def _arrow2425(value_4: str, person_1: Any=person_1) -> IEncodable:
            class ObjectExpr2424(IEncodable):
                def Encode(self, helpers_2: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_2.encode_string(value_4)

            return ObjectExpr2424()

        def _arrow2427(value_6: str, person_1: Any=person_1) -> IEncodable:
            class ObjectExpr2426(IEncodable):
                def Encode(self, helpers_3: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_3.encode_string(value_6)

            return ObjectExpr2426()

        def _arrow2429(value_8: str, person_1: Any=person_1) -> IEncodable:
            class ObjectExpr2428(IEncodable):
                def Encode(self, helpers_4: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_4.encode_string(value_8)

            return ObjectExpr2428()

        def _arrow2431(value_10: str, person_1: Any=person_1) -> IEncodable:
            class ObjectExpr2430(IEncodable):
                def Encode(self, helpers_5: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_5.encode_string(value_10)

            return ObjectExpr2430()

        def _arrow2433(value_12: str, person_1: Any=person_1) -> IEncodable:
            class ObjectExpr2432(IEncodable):
                def Encode(self, helpers_6: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_6.encode_string(value_12)

            return ObjectExpr2432()

        def _arrow2435(value_14: str, person_1: Any=person_1) -> IEncodable:
            class ObjectExpr2434(IEncodable):
                def Encode(self, helpers_7: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_7.encode_string(value_14)

            return ObjectExpr2434()

        def _arrow2437(value_16: str, person_1: Any=person_1) -> IEncodable:
            class ObjectExpr2436(IEncodable):
                def Encode(self, helpers_8: IEncoderHelpers_1[Any]) -> Any:
                    return helpers_8.encode_string(value_16)

            return ObjectExpr2436()

        def _arrow2438(oa: OntologyAnnotation, person_1: Any=person_1) -> IEncodable:
            return OntologyAnnotation_encoder(oa)

        def _arrow2439(comment: Comment, person_1: Any=person_1) -> IEncodable:
            return encoder_1(comment)

        values: FSharpList[tuple[str, IEncodable]] = choose(chooser, of_array([try_include("@id", _arrow2421, ROCrate_genID(person_2)), try_include("firstName", _arrow2423, person_2.FirstName), try_include("lastName", _arrow2425, person_2.LastName), try_include("midInitials", _arrow2427, person_2.MidInitials), try_include("email", _arrow2429, person_2.EMail), try_include("phone", _arrow2431, person_2.Phone), try_include("fax", _arrow2433, person_2.Fax), try_include("address", _arrow2435, person_2.Address), try_include("affiliation", _arrow2437, person_2.Affiliation), try_include_seq("roles", _arrow2438, person_2.Roles), try_include_seq("comments", _arrow2439, person_2.Comments)]))
        class ObjectExpr2440(IEncodable):
            def Encode(self, helpers_9: IEncoderHelpers_1[Any], person_1: Any=person_1) -> Any:
                def mapping_1(tupled_arg_1: tuple[str, IEncodable]) -> tuple[str, __A_]:
                    return (tupled_arg_1[0], tupled_arg_1[1].Encode(helpers_9))

                arg: IEnumerable_1[tuple[str, __A_]] = map_1(mapping_1, values)
                return helpers_9.encode_object(arg)

        return ObjectExpr2440()

    if id_map is not None:
        def _arrow2441(p_1: Person, id_map: Any=id_map, person: Any=person) -> str:
            return ROCrate_genID(p_1)

        return encode(_arrow2441, f, person, id_map)

    else: 
        return f(person)



def _arrow2452(get: IGetters) -> Person:
    def _arrow2442(__unit: None=None) -> str | None:
        object_arg: IOptionalGetter = get.Optional
        return object_arg.Field("lastName", string)

    def _arrow2443(__unit: None=None) -> str | None:
        object_arg_1: IOptionalGetter = get.Optional
        return object_arg_1.Field("firstName", string)

    def _arrow2444(__unit: None=None) -> str | None:
        object_arg_2: IOptionalGetter = get.Optional
        return object_arg_2.Field("midInitials", string)

    def _arrow2445(__unit: None=None) -> str | None:
        object_arg_3: IOptionalGetter = get.Optional
        return object_arg_3.Field("email", string)

    def _arrow2446(__unit: None=None) -> str | None:
        object_arg_4: IOptionalGetter = get.Optional
        return object_arg_4.Field("phone", string)

    def _arrow2447(__unit: None=None) -> str | None:
        object_arg_5: IOptionalGetter = get.Optional
        return object_arg_5.Field("fax", string)

    def _arrow2448(__unit: None=None) -> str | None:
        object_arg_6: IOptionalGetter = get.Optional
        return object_arg_6.Field("address", string)

    def _arrow2449(__unit: None=None) -> str | None:
        object_arg_7: IOptionalGetter = get.Optional
        return object_arg_7.Field("affiliation", string)

    def _arrow2450(__unit: None=None) -> Array[OntologyAnnotation] | None:
        arg_17: Decoder_1[Array[OntologyAnnotation]] = resize_array(OntologyAnnotation_decoder)
        object_arg_8: IOptionalGetter = get.Optional
        return object_arg_8.Field("roles", arg_17)

    def _arrow2451(__unit: None=None) -> Array[Comment] | None:
        arg_19: Decoder_1[Array[Comment]] = resize_array(decoder_1)
        object_arg_9: IOptionalGetter = get.Optional
        return object_arg_9.Field("comments", arg_19)

    return Person_setOrcidFromComments(Person(None, _arrow2442(), _arrow2443(), _arrow2444(), _arrow2445(), _arrow2446(), _arrow2447(), _arrow2448(), _arrow2449(), _arrow2450(), _arrow2451()))


ISAJson_decoder: Decoder_1[Person] = Decode_objectNoAdditionalProperties(ISAJson_allowedFields, _arrow2452)

__all__ = ["encoder", "decoder", "ROCrate_genID", "ROCrate_Affiliation_encoder", "ROCrate_Affiliation_decoder", "ROCrate_encoder", "ROCrate_decoder", "ROCrate_encodeAuthorListString", "ROCrate_decodeAuthorListString", "ISAJson_allowedFields", "ISAJson_encoder", "ISAJson_decoder"]

