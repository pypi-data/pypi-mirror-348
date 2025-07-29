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

from dnv_bladed_models.blade_stability_perturbations import BladeStabilityPerturbations

from dnv_bladed_models.custom_linear_model_dll import CustomLinearModelDll

from dnv_bladed_models.linearisation_calculation import LinearisationCalculation



from .schema_helper import SchemaHelper 
from .models_impl import *


class BladeStabilityAnalysisCalculation(LinearisationCalculation, ABC):
    r"""
    
    
    Not supported yet.
    
    Attributes
    ----------
    AzimuthAngle : float, default=0, Not supported yet
        The fixed azimuth angle of the rotor (zero azimuth indicates blade 1 pointing upwards).
    
    MaximumPlotFrequency : float, default=125.663706144, Not supported yet
        The maximum frequency for modes to be shown in the Campbell diagram plot. The default value is 20 * 2 * 3.14159265358979323
    
    CustomLinearModelDll : CustomLinearModelDll, Not supported yet
    
    Perturbations : BladeStabilityPerturbations, Not supported yet
    
    Notes
    -----
    This model is not supported yet by the Bladed calculation engine.
    """
    _relative_schema_path: str = PrivateAttr('SteadyCalculation/common/BladeStabilityAnalysisCalculation.json')

    AzimuthAngle: float = Field(alias="AzimuthAngle", default=None) # Not supported yet
    MaximumPlotFrequency: float = Field(alias="MaximumPlotFrequency", default=None) # Not supported yet
    CustomLinearModelDll: CustomLinearModelDll = Field(alias="CustomLinearModelDll", default=None) # Not supported yet
    Perturbations: BladeStabilityPerturbations = Field(alias="Perturbations", default=None) # Not supported yet

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



BladeStabilityAnalysisCalculation.update_forward_refs()
