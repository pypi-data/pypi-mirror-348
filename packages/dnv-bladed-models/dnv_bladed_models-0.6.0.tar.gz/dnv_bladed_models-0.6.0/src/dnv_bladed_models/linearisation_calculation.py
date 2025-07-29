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

from dnv_bladed_models.steady_calculation import SteadyCalculation

from dnv_bladed_models.steady_calculation_outputs import SteadyCalculationOutputs



from .schema_helper import SchemaHelper 
from .models_impl import *


class LinearisationCalculation(SteadyCalculation, ABC):
    r"""
    The common properties of calculations which use small perturbations to generate system responses, from which the dynamics of the fully coupled system can be analysed.
    
    Not supported yet.
    
    Attributes
    ----------
    MinimumCorrelationCoefficient : float, default=0.8, Not supported yet
        The minimum acceptable correlation coefficient for the relationship between a state value and a state derivative.  If it is below the minimum, the relationship is disregarded and a zero value is taken.
    
    Outputs : SteadyCalculationOutputs
    
    TransformRotorModesToNonRotating : bool, default=False, Not supported yet
        If true, a multi-blade coordinate (MBC) transform will be performed to transform the rotating modes into the stationary frame of reference.  This will generate forward and backward whirling modes in a Campbell diagram.
    
    AlignWindFieldWithDeflectedHubAxis : bool, default=True, Not supported yet
        If true, the deflected steady-state operating conditions of the turbine are calculated, and then the wind field is rotated to align with the rotating axis of the (first) hub for linearisation.
    
    Notes
    -----
    This model is not supported yet by the Bladed calculation engine.
    """
    _relative_schema_path: str = PrivateAttr('SteadyCalculation/common/LinearisationCalculation.json')

    MinimumCorrelationCoefficient: float = Field(alias="MinimumCorrelationCoefficient", default=None) # Not supported yet
    Outputs: SteadyCalculationOutputs = Field(alias="Outputs", default=None)
    TransformRotorModesToNonRotating: bool = Field(alias="TransformRotorModesToNonRotating", default=None) # Not supported yet
    AlignWindFieldWithDeflectedHubAxis: bool = Field(alias="AlignWindFieldWithDeflectedHubAxis", default=None) # Not supported yet

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



LinearisationCalculation.update_forward_refs()
