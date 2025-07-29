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



class BladeModelling_BladeModellingTypeEnum(str, Enum):
    FINITE_ELEMENT_BLADE_MODELLING = "FiniteElementBladeModelling"
    MODAL_BLADE_MODELLING = "ModalBladeModelling"
    RIGID_BLADE_MODELLING = "RigidBladeModelling"
    __INSERT__ = "__insert__"

class BladeModelling_GeometricStiffnessModelEnum(str, Enum):
    AXIAL_LOADS_ONLY = "AxialLoadsOnly"
    FULL_MODEL_WITH_ORIENTATION_CORRECTION = "FullModelWithOrientationCorrection"
    INTERNAL_LOADS_ONLY = "InternalLoadsOnly"
    DISABLED = "Disabled"

from .schema_helper import SchemaHelper 
from .models_impl import *


class BladeModelling(BladedModel, ABC):
    r"""
    Common properties for all blade modelling methods.
    
    Attributes
    ----------
    BladeModellingType : BladeModelling_BladeModellingTypeEnum
        Defines the specific type of model in use.
    
    GeometricStiffnessModel : BladeModelling_GeometricStiffnessModelEnum, default='AxialLoadsOnly'
        The geometric stiffness model to use for the blades. For blades with 1 part, the \"axial loads only\" model is recommended. This configuration is only appropriate for relatively stiff blades, undergoing small deflection.  For more flexible blade models, a multi-part blade model is more appropriate. In this case, the \"full with orientation correction\" is the recommended option, as long as deflection remains small within each blade part.
    
    IgnoreAxesOrientationDifferencesForShear : bool, default=False
        With this option selected, the effect of orientation difference between the elastic axis and shear axis on the blade elements are not taken into account. Please refer to the theory manual for details (blade bend-twist coupling).
    
    Notes
    -----
    
    This class is an abstraction, with the following concrete implementations:
        - FiniteElementBladeModelling
        - ModalBladeModelling
        - RigidBladeModelling
        - BladeModellingInsert
    
    """
    _relative_schema_path: str = PrivateAttr('Components/Blade/BladeModelling/common/BladeModelling.json')

    BladeModellingType: BladeModelling_BladeModellingTypeEnum = Field(alias="BladeModellingType", default=None)
    GeometricStiffnessModel: BladeModelling_GeometricStiffnessModelEnum = Field(alias="GeometricStiffnessModel", default=None)
    IgnoreAxesOrientationDifferencesForShear: bool = Field(alias="IgnoreAxesOrientationDifferencesForShear", default=None)

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



BladeModelling.update_forward_refs()
