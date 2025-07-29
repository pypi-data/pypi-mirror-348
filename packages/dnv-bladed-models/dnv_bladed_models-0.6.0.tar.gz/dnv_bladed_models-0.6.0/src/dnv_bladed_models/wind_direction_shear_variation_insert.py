# *********************************************************************#
# Bladed Python Models API                                             #
# Copyright (c) DNV Services UK Limited (c) 2025. All rights reserved. #
# MIT License (see license file)                                       #
# *********************************************************************#


# coding: utf-8

from __future__ import annotations

from datetime import date, datetime  # noqa: F401
from enum import Enum, IntEnum

import os
import re  # noqa: F401
from typing import Annotated, Any, Dict, List, Literal, Optional, Set, Type, Union, Callable, Iterable  # noqa: F401
from pathlib import Path
from typing import TypeVar
Model = TypeVar('Model', bound='BaseModel')
StrBytes = Union[str, bytes]

from pydantic import AnyUrl, BaseModel, EmailStr, Field, validator, root_validator, Extra,PrivateAttr  # noqa: F401
from pydantic import ValidationError
from pydantic.error_wrappers import ErrorWrapper
from pydantic.utils import ROOT_KEY
from json import encoder

from dnv_bladed_models.wind_direction_shear_variation import WindDirectionShearVariation



from .schema_helper import SchemaHelper 
from .models_impl import *


class WindDirectionShearVariationInsert(CommonRoot):
    r"""
    A WindDirectionShearVariation is to be inserted from an external resource. The exact type of WindDirectionShearVariation is not currently known.
    
    Attributes
    ----------
    DirectionShearVariationType : Literal['__insert__'], default='__insert__'
        For internal use when reading & writing JSON.
    
    insert : str
        A path to a resource from which a valid JSON model object can be resolved. All properties will be taken from the resolved object; no properties can be specified in-line.

    Notes
    -----
    
    """
    _relative_schema_path: str = PrivateAttr('')

    DirectionShearVariationType: Literal['__insert__'] = Field(alias="DirectionShearVariationType", default='__insert__', allow_mutation=False, const=True)
    insert: str = Field(alias="$insert", default=None)

    class Config:
        extra = Extra.forbid
        validate_assignment = True
        allow_population_by_field_name = True
        pass


    @classmethod
    def parse_obj(cls: Type['Model'], obj: Any) -> 'Model':
        discriminated_props = [
        ]
        discriminated_arrays = [
        ]
        prepare_model_dict(cls, obj, discriminated_props, discriminated_arrays)
        return super().parse_obj(obj)


    def _iter( # type: ignore
        self,
        **kwargs: Any
    ):
        kwargs['exclude'] = None
        kwargs['include'] = set(['insert'])
        return super()._iter(**kwargs)


    @property
    def is_insert(self) -> bool:
        """
        Returns true if the model is to be loaded from an external resource by the Bladed application; i.e. the 'insert' field is set with a resource location.
        """
        return True
    



    def _find_unused_containers(self) -> Set[str]:
        unused_containers: Set[str] = super()._find_unused_containers()
        return unused_containers


    def _is_unused(self) -> bool:
        """
        Returns true if the model has no user-supplied values. This indicates the object should not be rendered in the final JSON output.
        """
        candidate_fields = [x[1] for x in self.__dict__.items() if x[0] != 'DirectionShearVariationType']
        return (len(candidate_fields) == 0 or all(map(lambda f: f is None, candidate_fields))) and super()._is_unused()



WindDirectionShearVariationInsert.update_forward_refs()
