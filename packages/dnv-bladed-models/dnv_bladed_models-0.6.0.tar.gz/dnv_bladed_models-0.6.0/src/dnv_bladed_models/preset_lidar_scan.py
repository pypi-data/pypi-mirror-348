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

from dnv_bladed_models.lidar_scanning_pattern import LidarScanningPattern



class PresetLidarScan_BeamSamplingEnum(str, Enum):
    SIMULTANEOUS = "Simultaneous"
    SEQUENTIAL = "Sequential"

from .schema_helper import SchemaHelper 
from .models_impl import *


class PresetLidarScan(LidarScanningPattern, ABC):
    r"""
    the common properties of scan patterns which are set by the Lidar, rather than controlled in realtime by the turbine's controller.
    
    Not supported yet.
    
    Attributes
    ----------
    SamplesPerScan : int, default=1, Not supported yet
        The number of samples taken during a complete scan.
    
    LidarInterval : float, Not supported yet
        The time interval between scans.  Note that all fossing distances will be sampled at the same time.
    
    BeamSampling : PresetLidarScan_BeamSamplingEnum, Not supported yet
        The method of how each beam is sampled - whether is is simultaneously, or in sequence.
    
    Notes
    -----
    This model is not supported yet by the Bladed calculation engine.
    """
    _relative_schema_path: str = PrivateAttr('Components/Lidar/LidarScanningPattern/common/PresetLidarScan.json')

    SamplesPerScan: int = Field(alias="SamplesPerScan", default=None) # Not supported yet
    LidarInterval: float = Field(alias="LidarInterval", default=None) # Not supported yet
    BeamSampling: PresetLidarScan_BeamSamplingEnum = Field(alias="BeamSampling", default=None) # Not supported yet

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



PresetLidarScan.update_forward_refs()
