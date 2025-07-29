from __future__ import annotations
from collections.abc import Callable
from typing import Any
from ..fable_modules.fable_library.array_ import add_range_in_place
from ..fable_modules.fable_library.option import default_arg
from ..fable_modules.fable_library.reflection import (TypeInfo, class_type)
from ..fable_modules.fable_library.seq import contains as contains_1
from ..fable_modules.fable_library.seq2 import Array_distinct
from ..fable_modules.fable_library.types import Array
from ..fable_modules.fable_library.util import (get_enumerator, dispose, equals, safe_hash, uncurry2)
from .Helper.collections_ import (ResizeArray_filter, ResizeArray_distinct, ResizeArray_collect, ResizeArray_append)
from .ontology_annotation import OntologyAnnotation
from .template import Template

def TemplatesAux_getComparer(match_all: bool | None=None) -> Callable[[bool, bool], bool]:
    if default_arg(match_all, False):
        def _arrow783(e: bool, match_all: Any=match_all) -> Callable[[bool], bool]:
            def _arrow782(e_1: bool) -> bool:
                return e and e_1

            return _arrow782

        return _arrow783

    else: 
        def _arrow785(e_2: bool, match_all: Any=match_all) -> Callable[[bool], bool]:
            def _arrow784(e_3: bool) -> bool:
                return e_2 or e_3

            return _arrow784

        return _arrow785



def TemplatesAux_filterOnTags(tag_getter: Callable[[Template], Array[OntologyAnnotation]], query_tags: Array[OntologyAnnotation], comparer: Callable[[bool, bool], bool], templates: Array[Template]) -> Array[Template]:
    def f(t: Template, tag_getter: Any=tag_getter, query_tags: Any=query_tags, comparer: Any=comparer, templates: Any=templates) -> bool:
        template_tags: Array[OntologyAnnotation] = tag_getter(t)
        is_valid: bool | None = None
        enumerator: Any = get_enumerator(query_tags)
        try: 
            while enumerator.System_Collections_IEnumerator_MoveNext():
                class ObjectExpr786:
                    @property
                    def Equals(self) -> Callable[[OntologyAnnotation, OntologyAnnotation], bool]:
                        return equals

                    @property
                    def GetHashCode(self) -> Callable[[OntologyAnnotation], int]:
                        return safe_hash

                contains: bool = contains_1(enumerator.System_Collections_Generic_IEnumerator_1_get_Current(), template_tags, ObjectExpr786())
                is_valid_1: bool | None = is_valid
                if is_valid_1 is not None:
                    maybe: bool = is_valid_1
                    is_valid = comparer(maybe, contains)

                else: 
                    is_valid = contains


        finally: 
            dispose(enumerator)

        return default_arg(is_valid, False)

    return ResizeArray_filter(f, templates)


def _expr796() -> TypeInfo:
    return class_type("ARCtrl.Templates", None, Templates)


class Templates:
    @staticmethod
    def get_distinct_tags(templates: Array[Template]) -> Array[OntologyAnnotation]:
        def f(t: Template) -> Array[OntologyAnnotation]:
            return t.Tags

        return ResizeArray_distinct(ResizeArray_collect(f, templates))

    @staticmethod
    def get_distinct_endpoint_repositories(templates: Array[Template]) -> Array[OntologyAnnotation]:
        def f(t: Template) -> Array[OntologyAnnotation]:
            return t.EndpointRepositories

        return ResizeArray_distinct(ResizeArray_collect(f, templates))

    @staticmethod
    def get_distinct_ontology_annotations(templates: Array[Template]) -> Array[OntologyAnnotation]:
        oas: Array[OntologyAnnotation] = []
        for idx in range(0, (len(templates) - 1) + 1, 1):
            t: Template = templates[idx]
            add_range_in_place(t.Tags, oas)
            add_range_in_place(t.EndpointRepositories, oas)
        class ObjectExpr788:
            @property
            def Equals(self) -> Callable[[OntologyAnnotation, OntologyAnnotation], bool]:
                return equals

            @property
            def GetHashCode(self) -> Callable[[OntologyAnnotation], int]:
                return safe_hash

        return Array_distinct(list(oas), ObjectExpr788())

    @staticmethod
    def filter_by_tags(query_tags: Array[OntologyAnnotation], match_all: bool | None=None) -> Callable[[Array[Template]], Array[Template]]:
        def _arrow790(templates: Array[Template]) -> Array[Template]:
            def _arrow789(t: Template) -> Array[OntologyAnnotation]:
                return t.Tags

            return TemplatesAux_filterOnTags(_arrow789, query_tags, uncurry2(TemplatesAux_getComparer(match_all)), templates)

        return _arrow790

    @staticmethod
    def filter_by_endpoint_repositories(query_tags: Array[OntologyAnnotation], match_all: bool | None=None) -> Callable[[Array[Template]], Array[Template]]:
        def _arrow792(templates: Array[Template]) -> Array[Template]:
            def _arrow791(t: Template) -> Array[OntologyAnnotation]:
                return t.EndpointRepositories

            return TemplatesAux_filterOnTags(_arrow791, query_tags, uncurry2(TemplatesAux_getComparer(match_all)), templates)

        return _arrow792

    @staticmethod
    def filter_by_ontology_annotation(query_tags: Array[OntologyAnnotation], match_all: bool | None=None) -> Callable[[Array[Template]], Array[Template]]:
        def _arrow794(templates: Array[Template]) -> Array[Template]:
            def _arrow793(t: Template) -> Array[OntologyAnnotation]:
                return ResizeArray_append(t.Tags, t.EndpointRepositories)

            return TemplatesAux_filterOnTags(_arrow793, query_tags, uncurry2(TemplatesAux_getComparer(match_all)), templates)

        return _arrow794

    @staticmethod
    def filter_by_data_plant(templates: Array[Template]) -> Array[Template]:
        def f(t: Template) -> bool:
            return t.Organisation.IsOfficial()

        return ResizeArray_filter(f, templates)


Templates_reflection = _expr796

__all__ = ["TemplatesAux_getComparer", "TemplatesAux_filterOnTags", "Templates_reflection"]

