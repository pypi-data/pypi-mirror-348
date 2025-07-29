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



class TransducerFaults_FaultTypeEnum(str, Enum):
    NONE = "None"
    NOISE = "Noise"
    TO_CONSTANT = "ToConstant"
    CONSTANT_OFFSET = "ConstantOffset"
    GROWING_OFFSET = "GrowingOffset"
    HARMONIC_OFFSET = "HarmonicOffset"

from .schema_helper import SchemaHelper 
from .models_impl import *


class TransducerFaults(BladedModel, ABC):
    r"""
    
    
    Not supported yet.
    
    Attributes
    ----------
    ApplyOnlyToFirst : bool, default=True, Not supported yet
        If true, the fault will be aplied only to the first instance of this transducer.  If false, all sensors of this type will fail identically.
    
    MiscalibrationOffset : float, default=0, Not supported yet
        A constant value added to the sensor's output - for example, if the sensor had been incorrectly installed or poorly calibrated.
    
    InverseInstallation : bool, default=False, Not supported yet
        Whether the sensor was installed in reverse, resulting in its outputs being multiplied by -1.0.
    
    FailTime : float, default=0, Not supported yet
        The time at which any time-dependent failure occurs.  This will be from the beginning of the simulation, and not from the start of logging.  Please ensure that this time will equate to a period which is being clearly logged.
    
    FaultType : TransducerFaults_FaultTypeEnum, default='None', Not supported yet
        What fault occurs at a specified time in the simulation.
    
    NoiseMultiplier : float, default=1, Not supported yet
        The factor by which the noise on the signal increases (or decreases) by.
    
    FailureValue : float, default=0, Not supported yet
        The value which the sensor reverts to in the case of failure.
    
    FailureValueRampRate : float, default=0, Not supported yet
        The rate at which the signal reverts to its fail value.  A rate of 0.0 represents an instantaneous step change to the fail value.
    
    ConstantOffset : float, default=0, Not supported yet
        The value by which the signal is offset by.
    
    GrowingOffset : float, default=0, Not supported yet
        The rate at which the signal is deviating from its calibrated value.
    
    Magnitude : float, default=0, Not supported yet
        The greatest magnitude of the harmonic interference from the 'true' value.
    
    Period : float, default=1, Not supported yet
        The time period of the full sinusoidal interference pattern.
    
    Notes
    -----
    This model is not supported yet by the Bladed calculation engine.
    """
    _relative_schema_path: str = PrivateAttr('Turbine/BladedControl/MeasuredSignalProperties/common/TransducerFaults.json')

    ApplyOnlyToFirst: bool = Field(alias="ApplyOnlyToFirst", default=None) # Not supported yet
    MiscalibrationOffset: float = Field(alias="MiscalibrationOffset", default=None) # Not supported yet
    InverseInstallation: bool = Field(alias="InverseInstallation", default=None) # Not supported yet
    FailTime: float = Field(alias="FailTime", default=None) # Not supported yet
    FaultType: TransducerFaults_FaultTypeEnum = Field(alias="FaultType", default=None) # Not supported yet
    NoiseMultiplier: float = Field(alias="NoiseMultiplier", default=None) # Not supported yet
    FailureValue: float = Field(alias="FailureValue", default=None) # Not supported yet
    FailureValueRampRate: float = Field(alias="FailureValueRampRate", default=None) # Not supported yet
    ConstantOffset: float = Field(alias="ConstantOffset", default=None) # Not supported yet
    GrowingOffset: float = Field(alias="GrowingOffset", default=None) # Not supported yet
    Magnitude: float = Field(alias="Magnitude", default=None) # Not supported yet
    Period: float = Field(alias="Period", default=None) # Not supported yet

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



TransducerFaults.update_forward_refs()
