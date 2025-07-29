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



class EvolvingTurbulence_EvolvingTurbulenceTypeEnum(str, Enum):
    EVOLVING_TURBULENCE_EXPONENTIAL = "EvolvingTurbulenceExponential"
    EVOLVING_TURBULENCE_KRISTENSEN = "EvolvingTurbulenceKristensen"
    __INSERT__ = "__insert__"

from .schema_helper import SchemaHelper 
from .models_impl import *


class EvolvingTurbulence(BladedModel, ABC):
    r"""
    The settings for evolving turbulence.  In the case of a normal turbulent wind field, the turbulence is \"frozen\" and approaches the turbine at a constant block.  Although this doesn't match physical reality, it is a particular problem for Lidar - as it gives them a \"perfect\" insight into the oncoming wind field.  In order to represent the nature of real turbulence, a second turbulence file is superimposed on the windfield so that it \"evolves\" as it moves forward.  This is computationally expensive, and is usually applied only to the Lidar readings - although it can be applied to all the wind values in a simulation.
    
    Attributes
    ----------
    EvolvingTurbulenceType : EvolvingTurbulence_EvolvingTurbulenceTypeEnum
        Defines the specific type of model in use.
    
    SecondTurbulenceFilepath : str
        The filepath or URI of the second turbulence file.  The turbulence in this file will be used to simulate an evolving turbulence field.
    
    Notes
    -----
    
    This class is an abstraction, with the following concrete implementations:
        - EvolvingTurbulenceExponential
        - EvolvingTurbulenceKristensen
        - EvolvingTurbulenceInsert
    
    """
    _relative_schema_path: str = PrivateAttr('TimeDomainSimulation/Environment/Wind/EvolvingTurbulence/common/EvolvingTurbulence.json')

    EvolvingTurbulenceType: EvolvingTurbulence_EvolvingTurbulenceTypeEnum = Field(alias="EvolvingTurbulenceType", default=None)
    SecondTurbulenceFilepath: str = Field(alias="SecondTurbulenceFilepath", default=None)

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



EvolvingTurbulence.update_forward_refs()
