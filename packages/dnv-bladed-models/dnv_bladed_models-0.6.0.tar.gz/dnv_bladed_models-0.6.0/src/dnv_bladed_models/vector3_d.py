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



from .schema_helper import SchemaHelper 
from .models_impl import *


class Vector3D(CommonRoot):
    r"""
    A 3x1 vector representing a location or direction.
    
    Attributes
    ----------
    X : float
        A number representing a length.  The SI units for length are metres.
    
    Y : float
        A number representing a length.  The SI units for length are metres.
    
    Z : float
        A number representing a length.  The SI units for length are metres.
    
    Notes
    -----
    
    """
    _relative_schema_path: str = PrivateAttr('')

    X: float = Field(alias="X", default=None)
    Y: float = Field(alias="Y", default=None)
    Z: float = Field(alias="Z", default=None)

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





    def _find_unused_containers(self) -> Set[str]:
        unused_containers: Set[str] = set()
        return unused_containers


    def _is_unused(self) -> bool:
        """
        Returns true if the model has no user-supplied values. This indicates the object should not be rendered in the final JSON output.
        """
        candidate_fields = self.__dict__.values()
        return (len(candidate_fields) == 0 or all(map(lambda f: f is None, candidate_fields)))



Vector3D.update_forward_refs()
