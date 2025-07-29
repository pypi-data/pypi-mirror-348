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



class Event_EventTypeEnum(str, Enum):
    CONTROLLER_FAULT = "ControllerFault"
    EMERGENCY_STOP_OPERATION = "EmergencyStopOperation"
    GRID_LOSS = "GridLoss"
    NETWORK_FREQUENCY_DISTURBANCE = "NetworkFrequencyDisturbance"
    NETWORK_VOLTAGE_DISTURBANCE = "NetworkVoltageDisturbance"
    NORMAL_STOP_OPERATION = "NormalStopOperation"
    PERMANENTLY_STUCK_PITCH_SYSTEM = "PermanentlyStuckPitchSystem"
    PITCH_FAULT_CONSTANT_RATE = "PitchFaultConstantRate"
    PITCH_FAULT_CONSTANT_TORQUE = "PitchFaultConstantTorque"
    PITCH_FAULT_LIMP = "PitchFaultLimp"
    PITCH_FAULT_SEIZURE = "PitchFaultSeizure"
    PITCH_FAULT_SEIZURE_AT_ANGLE = "PitchFaultSeizureAtAngle"
    SHORT_CIRCUIT = "ShortCircuit"
    START_UP_OPERATION = "StartUpOperation"
    YAW_FAULT_CONSTANT_RATE = "YawFaultConstantRate"
    YAW_FAULT_CONSTANT_TORQUE = "YawFaultConstantTorque"
    YAW_FAULT_LIMP = "YawFaultLimp"
    YAW_MANOEVER = "YawManoever"
    __INSERT__ = "__insert__"

from .schema_helper import SchemaHelper 
from .models_impl import *


class Event(BladedModel, ABC):
    r"""
    An event which may occur during the simulation.  These can either be timed events, or based on a set of conditions which may or may not occur.
    
    Not supported yet.
    
    Attributes
    ----------
    EventType : Event_EventTypeEnum, Not supported yet
        Defines the specific type of model in use.
    
    Notes
    -----
    This model is not supported yet by the Bladed calculation engine.
    This class is an abstraction, with the following concrete implementations:
        - ControllerFault
        - EmergencyStopOperation
        - GridLoss
        - NetworkFrequencyDisturbance
        - NetworkVoltageDisturbance
        - NormalStopOperation
        - PermanentlyStuckPitchSystem
        - PitchFaultConstantRate
        - PitchFaultConstantTorque
        - PitchFaultLimp
        - PitchFaultSeizure
        - PitchFaultSeizureAtAngle
        - ShortCircuit
        - StartUpOperation
        - YawFaultConstantRate
        - YawFaultConstantTorque
        - YawFaultLimp
        - YawManoever
        - EventInsert
    
    """
    _relative_schema_path: str = PrivateAttr('TimeDomainSimulation/Event/common/Event.json')

    EventType: Event_EventTypeEnum = Field(alias="EventType", default=None) # Not supported yet

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



Event.update_forward_refs()
