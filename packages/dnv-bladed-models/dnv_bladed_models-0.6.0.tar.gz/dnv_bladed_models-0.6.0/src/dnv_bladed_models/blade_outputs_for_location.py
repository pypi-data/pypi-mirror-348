# *********************************************************************#
# Bladed Python Models API                                             #
# Copyright (c) DNV Services UK Limited (c) 2025. All rights reserved. #
# MIT License (see license file)                                       #
# *********************************************************************#


# coding: utf-8

from __future__ import annotations

from abc import ABC

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

from dnv_bladed_models.bladed_model import BladedModel



class BladeOutputsForLocation_BladeOutputsForLocationTypeEnum(str, Enum):
    OUTPUTS_FOR_CROSS_SECTION = "OutputsForCrossSection"
    OUTPUTS_FOR_POSITION = "OutputsForPosition"
    __INSERT__ = "__insert__"

from .schema_helper import SchemaHelper 
from .models_impl import *


class BladeOutputsForLocation(BladedModel, ABC):
    r"""
    
    
    Not supported yet.
    
    Attributes
    ----------
    BladeOutputsForLocationType : BladeOutputsForLocation_BladeOutputsForLocationTypeEnum, Not supported yet
        Defines the specific type of model in use.
    
    Loads : bool, default=False, Not supported yet
        An array of blade station indices to output loads for (exclusive with BLOADS_POS).
    
    Motion : bool, default=False, Not supported yet
        An array of blade station indices to output deflections for (exclusive with BDEFLS_POS).
    
    Aerodynamics : bool, Not supported yet
        Whether to output loads on this node
    
    Hydrodynamics : bool, default=False, Not supported yet
        An array of blade radii to output water kinematics for (tidal only).
    
    Notes
    -----
    This model is not supported yet by the Bladed calculation engine.
    This class is an abstraction, with the following concrete implementations:
        - BladeOutputsForCrossSection
        - BladeOutputsForPosition
        - BladeOutputsForLocationInsert
    
    """
    _relative_schema_path: str = PrivateAttr('Components/Blade/BladeOutputGroupLibrary/BladeOutputGroup/BladeOutputsForLocation/common/BladeOutputsForLocation.json')

    BladeOutputsForLocationType: BladeOutputsForLocation_BladeOutputsForLocationTypeEnum = Field(alias="BladeOutputsForLocationType", default=None) # Not supported yet
    Loads: bool = Field(alias="Loads", default=None) # Not supported yet
    Motion: bool = Field(alias="Motion", default=None) # Not supported yet
    Aerodynamics: bool = Field(alias="Aerodynamics", default=None) # Not supported yet
    Hydrodynamics: bool = Field(alias="Hydrodynamics", default=None) # Not supported yet

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
        if self.insert is not None:
            kwargs['exclude'] = None
            kwargs['include'] = set(['insert'])
        else:
            exclude: Optional[Set[str]] = kwargs.get('exclude', set())
            if exclude is None:
                exclude = self._find_unused_containers()
            else:
                exclude.update(self._find_unused_containers())
            kwargs['exclude'] = exclude
        return super()._iter(**kwargs)



    def _find_unused_containers(self) -> Set[str]:
        unused_containers: Set[str] = super()._find_unused_containers()
        return unused_containers


    def _is_unused(self) -> bool:
        """
        Returns true if the model has no user-supplied values. This indicates the object should not be rendered in the final JSON output.
        """
        candidate_fields = self.__dict__.values()
        return (len(candidate_fields) == 0 or all(map(lambda f: f is None, candidate_fields))) and super()._is_unused()



BladeOutputsForLocation.update_forward_refs()
