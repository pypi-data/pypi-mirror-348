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



class Component_ComponentTypeEnum(str, Enum):
    BLADE = "Blade"
    DRIVETRAIN_AND_NACELLE = "DrivetrainAndNacelle"
    EXTERNAL_MODULE_COMPONENT = "ExternalModuleComponent"
    FIXED_SPEED_ACTIVE_DAMPER = "FixedSpeedActiveDamper"
    FLEXIBILITY = "Flexibility"
    INDEPENDENT_PITCH_HUB = "IndependentPitchHub"
    LIDAR = "Lidar"
    LINEAR_PASSIVE_DAMPER = "LinearPassiveDamper"
    PENDULUM_DAMPER = "PendulumDamper"
    PITCH_SYSTEM = "PitchSystem"
    ROTATION = "Rotation"
    SUPERELEMENT = "Superelement"
    TOWER = "Tower"
    TRANSLATION = "Translation"
    VARIABLE_SPEED_ACTIVE_DAMPER = "VariableSpeedActiveDamper"
    VARIABLE_SPEED_GENERATOR = "VariableSpeedGenerator"
    YAW_SYSTEM = "YawSystem"
    __INSERT__ = "__insert__"

from .schema_helper import SchemaHelper 
from .models_impl import *


class Component(BladedModel, ABC):
    r"""
    The common properties of all components.
    
    Attributes
    ----------
    ComponentType : Component_ComponentTypeEnum
        Defines the specific type of model in use.
    
    Notes
    -----
    
    This class is an abstraction, with the following concrete implementations:
        - Blade
        - DrivetrainAndNacelle
        - ExternalModuleComponent
        - FixedSpeedActiveDamper
        - Flexibility
        - IndependentPitchHub
        - Lidar
        - LinearPassiveDamper
        - PendulumDamper
        - PitchSystem
        - Rotation
        - Superelement
        - Tower
        - Translation
        - VariableSpeedActiveDamper
        - VariableSpeedGenerator
        - YawSystem
        - ComponentInsert
    
    """
    _relative_schema_path: str = PrivateAttr('Components/common/Component.json')

    ComponentType: Component_ComponentTypeEnum = Field(alias="ComponentType", default=None)

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



Component.update_forward_refs()
