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

from dnv_bladed_models.integrator import Integrator



from .schema_helper import SchemaHelper 
from .models_impl import *


class FixedStepIntegrator(Integrator, ABC):
    r"""
    Common settings for the fixed step integrators.
    
    Attributes
    ----------
    TimeStep : float
        The fixed time step used by the integrator.  It must be set as a divisor of the output time-step and external controller communication interval.
    
    Tolerance : float, default=0.005
        When the \"Maximum number of iterations\" > 1, the integrator relative tolerance is used to control how many iterations are carried out when integrating the first order and prescribed second order states.  Iterations are carried out until the maximum number of iterations is reached, or until the change in all first order and prescribed state derivatives between successive iterations is less than the relative tolerance multiplied by the state derivative absolute value.
    
    Notes
    -----
    
    """
    _relative_schema_path: str = PrivateAttr('Settings/SolverSettings/Integrator/common/FixedStepIntegrator.json')

    TimeStep: float = Field(alias="TimeStep", default=None)
    Tolerance: float = Field(alias="Tolerance", default=None)

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



FixedStepIntegrator.update_forward_refs()
