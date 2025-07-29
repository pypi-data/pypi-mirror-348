# *********************************************************************#
# Bladed Python Models API                                             #
# Copyright (c) DNV Services UK Limited (c) 2025. All rights reserved. #
# MIT License (see license file)                                       #
# *********************************************************************#


# coding: utf-8

from __future__ import annotations

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

from dnv_bladed_models.actuator_response import ActuatorResponse

from dnv_bladed_models.actuator_response_insert import ActuatorResponseInsert

from dnv_bladed_models.first_order_actuator_response import FirstOrderActuatorResponse

from dnv_bladed_models.instantaneous_actuator_response import InstantaneousActuatorResponse

from dnv_bladed_models.linear_spring_damper import LinearSpringDamper

from dnv_bladed_models.pitch_actuator import PitchActuator

from dnv_bladed_models.pitch_torque_limits import PitchTorqueLimits

from dnv_bladed_models.second_order_actuator_response import SecondOrderActuatorResponse



from .schema_helper import SchemaHelper 
from .models_impl import *

TActuatorResponseOptions = TypeVar('TActuatorResponseOptions', FirstOrderActuatorResponse, InstantaneousActuatorResponse, SecondOrderActuatorResponse, ActuatorResponseInsert, ActuatorResponse, )

class PitchSystemRotaryDrive(PitchActuator):
    r"""
    A rotary pitch actuation system.
    
    Attributes
    ----------
    ActuatorDriveType : Literal['RotaryDrive'], default='RotaryDrive'
        Defines the specific type of ActuatorDrive model in use.  For a `RotaryDrive` object, this must always be set to a value of `RotaryDrive`.
    
    TorqueResponse : Union[FirstOrderActuatorResponse, InstantaneousActuatorResponse, SecondOrderActuatorResponse, ActuatorResponseInsert]
    
    GearRatio : float, default=1
        The combined gearbox and pinion to ring gear ratio (gearbox ratio multiplied by pnion to ring gear ratio).
    
    GearEfficiency : float, default=1
        The efficiency between actuator motor and bearing.
    
    MotorInertia : float, default=0
        The rotational inertia of the motor, referred to the high speed side of the pitch gearbox.
    
    BrakeTorque : float, default=0
        The maximum restraining brake torque applied when the safety limit switches are tripped or permanently on in idling and parked simulations.
    
    TorqueLimits : PitchTorqueLimits
    
    BackupPowerTorqueLimits : PitchTorqueLimits
    
    TorqueLimitsOnceSafetySystemTripped : PitchTorqueLimits
    
    LinearSpringDamper : LinearSpringDamper
    
    Notes
    -----
    
    """
    _relative_schema_path: str = PrivateAttr('Components/PitchSystem/PitchActuator/PitchSystemRotaryDrive.json')

    ActuatorDriveType: Literal['RotaryDrive'] = Field(alias="ActuatorDriveType", default='RotaryDrive', allow_mutation=False, const=True)
    TorqueResponse: Union[FirstOrderActuatorResponse, InstantaneousActuatorResponse, SecondOrderActuatorResponse, ActuatorResponseInsert] = Field(alias="TorqueResponse", default=None, discriminator='ActuatorResponseType')
    GearRatio: float = Field(alias="GearRatio", default=None)
    GearEfficiency: float = Field(alias="GearEfficiency", default=None)
    MotorInertia: float = Field(alias="MotorInertia", default=None)
    BrakeTorque: float = Field(alias="BrakeTorque", default=None)
    TorqueLimits: PitchTorqueLimits = Field(alias="TorqueLimits", default=None)
    BackupPowerTorqueLimits: PitchTorqueLimits = Field(alias="BackupPowerTorqueLimits", default=None)
    TorqueLimitsOnceSafetySystemTripped: PitchTorqueLimits = Field(alias="TorqueLimitsOnceSafetySystemTripped", default=None)
    LinearSpringDamper: LinearSpringDamper = Field(alias="LinearSpringDamper", default=None)

    class Config:
        extra = Extra.forbid
        validate_assignment = True
        allow_population_by_field_name = True
        pass


    @classmethod
    def parse_obj(cls: Type['Model'], obj: Any) -> 'Model':
        discriminated_props = [
            ('TorqueResponse', 'ActuatorResponseType'),
        ]
        discriminated_arrays = [
        ]
        prepare_model_dict(cls, obj, discriminated_props, discriminated_arrays)
        return super().parse_obj(obj)


    @classmethod
    def __get_validators__(cls):
        yield cls._factory


    @classmethod
    def _factory(cls, data):
        if isinstance(data, PitchSystemRotaryDrive):
            return data
        if not isinstance(data, dict):
            raise TypeError('An object is required to define PitchSystemRotaryDrive models')
        return PitchSystemRotaryDrive.parse_obj(data)


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


    @property
    def TorqueResponse_as_FirstOrderActuatorResponse(self) -> FirstOrderActuatorResponse:
        """
        Retrieves the value of TorqueResponse guaranteeing it is a FirstOrderActuatorResponse; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        FirstOrderActuatorResponse
            A model object, guaranteed to be a FirstOrderActuatorResponse.

        Raises
        ------
        TypeError
            If the value is not a FirstOrderActuatorResponse.
        """
        return self.TorqueResponse_as(FirstOrderActuatorResponse)


    @property
    def TorqueResponse_as_InstantaneousActuatorResponse(self) -> InstantaneousActuatorResponse:
        """
        Retrieves the value of TorqueResponse guaranteeing it is a InstantaneousActuatorResponse; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        InstantaneousActuatorResponse
            A model object, guaranteed to be a InstantaneousActuatorResponse.

        Raises
        ------
        TypeError
            If the value is not a InstantaneousActuatorResponse.
        """
        return self.TorqueResponse_as(InstantaneousActuatorResponse)


    @property
    def TorqueResponse_as_SecondOrderActuatorResponse(self) -> SecondOrderActuatorResponse:
        """
        Retrieves the value of TorqueResponse guaranteeing it is a SecondOrderActuatorResponse; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        SecondOrderActuatorResponse
            A model object, guaranteed to be a SecondOrderActuatorResponse.

        Raises
        ------
        TypeError
            If the value is not a SecondOrderActuatorResponse.
        """
        return self.TorqueResponse_as(SecondOrderActuatorResponse)


    @property
    def TorqueResponse_as_inline(self) -> Union[FirstOrderActuatorResponse, InstantaneousActuatorResponse, SecondOrderActuatorResponse]:
        """
        Retrieves the value of TorqueResponse as a model object; if the value is specified with a '$insert', an error is raised.

        Returns
        -------
        Union[FirstOrderActuatorResponse, InstantaneousActuatorResponse, SecondOrderActuatorResponse]
            A model object at the specified index, guaranteed to not be a '$insert'.

        Raises
        ------
        TypeError
            If the value is not one of the concrete types of ActuatorResponse; i.e. it is specified with a '$insert'.
        """
        if isinstance(self.TorqueResponse, ActuatorResponseInsert) or self.TorqueResponse.is_insert:
            raise TypeError(f"Expected TorqueResponse value to be an in-line object, but it is currently in the '$insert' state.")
        return self.TorqueResponse


    def TorqueResponse_as(self, cls: Type[TActuatorResponseOptions])-> TActuatorResponseOptions:
        """
        Retrieves the value of TorqueResponse, ensuring it is of the specified type.
        The specified type must be one of the valid concrete types of ActuatorResponse, or the '$insert' type
        (in the case the model is defined to be inserted from an external resource).

        Useful when using type-checking development tools, as it provides a concise way to access a value with the correct type.

        Parameters
        ----------
        cls: Type[Union[FirstOrderActuatorResponse, InstantaneousActuatorResponse, SecondOrderActuatorResponse, ActuatorResponseInsert]]
            One of the valid concrete types of ActuatorResponse, or the '$insert' type
            (in the case the model is defined to be inserted from an external resource).

        Returns
        -------
        TActuatorResponseOptions
            A model object of the specified type.

        Raises
        ------
        TypeError
            If the value is not of the specified type.

        Examples
        --------
        Get a reference to the value when it is one of the types of ActuatorResponse:
        >>> val_obj = model_obj.TorqueResponse_as(models.FirstOrderActuatorResponse)
        >>> val_obj = model_obj.TorqueResponse_as(models.InstantaneousActuatorResponse)
        >>> val_obj = model_obj.TorqueResponse_as(models.SecondOrderActuatorResponse)

        Get a reference to the value, when it was specified with a '$insert' and read in from a file:
        >>> insert_obj = model_obj.TorqueResponse_as(models.ActuatorResponseInsert)
        """
        if not isinstance(self.TorqueResponse, cls):
            raise TypeError(f"Expected TorqueResponse of type '{cls.__name__}' but was type '{type(self.TorqueResponse).__name__}'")
        return self.TorqueResponse



    def _find_unused_containers(self) -> Set[str]:
        unused_containers: Set[str] = super()._find_unused_containers()
        return unused_containers


    def _is_unused(self) -> bool:
        """
        Returns true if the model has no user-supplied values. This indicates the object should not be rendered in the final JSON output.
        """
        candidate_fields = [x[1] for x in self.__dict__.items() if x[0] != 'ActuatorDriveType']
        return (len(candidate_fields) == 0 or all(map(lambda f: f is None, candidate_fields))) and super()._is_unused()


    def to_json(self, indent: Optional[int] = 2, **json_kwargs: Any) -> str:
        r"""
        Generates a JSON string representation of the model.

        Parameters
        ----------
        indent : int
            The whitespace indentation to use for formatting, as per json.dumps().

        Examples
        --------
        >>> model.to_json()
        Renders the full JSON representation of the model object.
        """

        json_kwargs['by_alias'] = True
        json_kwargs['exclude_unset'] = False
        json_kwargs['exclude_none'] = True
        if self.Schema is None:
            self.Schema = SchemaHelper.construct_schema_url(self._relative_schema_path)
        
        return super().json(indent=indent, **json_kwargs)


    @classmethod
    def from_file(cls: Type['Model'], path: Union[str, Path]) -> 'Model':
        r"""
        Loads a model from a given file path.

        Parameters
        ----------
        path : string
            The file path to the model.

        Returns
        -------
        PitchSystemRotaryDrive
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = PitchSystemRotaryDrive.from_file('/path/to/file')
        """
        
        return super().parse_file(path=path)


    @classmethod
    def from_json(cls: Type['Model'], b: StrBytes) -> 'Model':
        r"""
        Creates a model object from a JSON string.

        Parameters
        ----------
        b: StrBytes
            The JSON string describing the model.

        Returns
        -------
        PitchSystemRotaryDrive
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = PitchSystemRotaryDrive.from_json('{ ... }')
        """

        return super().parse_raw(
            b=b,
            content_type='application/json')
        

    @classmethod
    def from_dict(cls: Type['Model'], obj: Any) -> 'Model':
        r"""
        Creates a model object from a dict.
        
        Parameters
        ----------
        obj : Any
            The dictionary object describing the model.

        Returns
        -------
        PitchSystemRotaryDrive
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.
        """
        
        return cls.parse_obj(obj=obj)


    def to_file(self, path: Union[str, Path]) -> None:
        r"""
        Writes the model as a JSON document to a file with UTF8 encoding.

        Parameters
        ----------                
        path : string
            The file path to which the model will be written.

        Examples
        --------
        >>> model.to_file('/path/to/file')
        """

        with open(file=path, mode='w', encoding="utf8") as output_file:
            output_file.write(self.to_json())


PitchSystemRotaryDrive.update_forward_refs()
