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

from dnv_bladed_models.vector3_d import Vector3D



class AppliedLoad_AppliedLoadTypeEnum(str, Enum):
    BLADE_POINT_LOADING = "BladePointLoading"
    TOWER_POINT_LOADING = "TowerPointLoading"
    __INSERT__ = "__insert__"

from .schema_helper import SchemaHelper 
from .models_impl import *


class AppliedLoad(BladedModel, ABC):
    r"""
    The common properties of a point loading time history.
    
    Attributes
    ----------
    AppliedLoadType : AppliedLoad_AppliedLoadTypeEnum
        Defines the specific type of model in use.
    
    StartTime : float
        The time into the simulation at which to start applying the loading (excluding the lead-in time).
    
    LoadingFilepath : str
        A filepath or URI containing one or six degree of loading data.  In the case of the six degrees of freedom, these will be applied in the component's coordinate system.  Where a single degree of freedom is provided, SingleDirectionLoading must also be specified.
    
    DirectionOfLoading : Vector3D
    
    OnComponentInAssembly : str, regex=^Assembly.(.+)$
        A qualified, dot-separated path to a component in the assembly tree to which to apply the force.  i.e. `Assembly.<name1>.<name2>`
    
    Notes
    -----
    
    This class is an abstraction, with the following concrete implementations:
        - BladePointLoading
        - TowerPointLoading
        - AppliedLoadInsert
    
    """
    _relative_schema_path: str = PrivateAttr('TimeDomainSimulation/AppliedLoad/common/AppliedLoad.json')

    AppliedLoadType: AppliedLoad_AppliedLoadTypeEnum = Field(alias="AppliedLoadType", default=None)
    StartTime: float = Field(alias="StartTime", default=None)
    LoadingFilepath: str = Field(alias="LoadingFilepath", default=None)
    DirectionOfLoading: Vector3D = Field(alias="DirectionOfLoading", default=None)
    OnComponentInAssembly: str = Field(alias="@OnComponentInAssembly", default=None, regex='^Assembly.(.+)$')

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



AppliedLoad.update_forward_refs()
