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

from dnv_bladed_models.component import Component

from dnv_bladed_models.friction import Friction

from dnv_bladed_models.idealised_pitch_actuator import IdealisedPitchActuator

from dnv_bladed_models.linear_pitch_actuator import LinearPitchActuator

from dnv_bladed_models.pitch_actuator import PitchActuator

from dnv_bladed_models.pitch_actuator_insert import PitchActuatorInsert

from dnv_bladed_models.pitch_controller import PitchController

from dnv_bladed_models.pitch_end_stops import PitchEndStops

from dnv_bladed_models.pitch_limit_switches import PitchLimitSwitches

from dnv_bladed_models.pitch_system_connectable_nodes import PitchSystemConnectableNodes

from dnv_bladed_models.pitch_system_output_group_library import PitchSystemOutputGroupLibrary

from dnv_bladed_models.pitch_system_rotary_drive import PitchSystemRotaryDrive



from .schema_helper import SchemaHelper 
from .models_impl import *

TPitchActuatorOptions = TypeVar('TPitchActuatorOptions', IdealisedPitchActuator, LinearPitchActuator, PitchSystemRotaryDrive, PitchActuatorInsert, PitchActuator, )

class PitchSystem(Component):
    r"""
    A pitch system, including bearing, actuation, and independent control system.
    
    Attributes
    ----------
    ComponentType : Literal['PitchSystem'], default='PitchSystem'
        Defines the specific type of Component model in use.  For a `PitchSystem` object, this must always be set to a value of `PitchSystem`.
    
    PitchController : PitchController
    
    LimitSwitches : PitchLimitSwitches
    
    EndStops : PitchEndStops
    
    Bearing : Friction
    
    Actuator : Union[IdealisedPitchActuator, LinearPitchActuator, PitchSystemRotaryDrive, PitchActuatorInsert]
    
    OutputGroups : PitchSystemOutputGroupLibrary, Not supported yet
    
    ConnectableNodes : PitchSystemConnectableNodes, Not supported yet
    
    Notes
    -----
    
    """
    _relative_schema_path: str = PrivateAttr('Components/PitchSystem/PitchSystem.json')

    ComponentType: Literal['PitchSystem'] = Field(alias="ComponentType", default='PitchSystem', allow_mutation=False, const=True)
    PitchController: PitchController = Field(alias="PitchController", default=None)
    LimitSwitches: PitchLimitSwitches = Field(alias="LimitSwitches", default=None)
    EndStops: PitchEndStops = Field(alias="EndStops", default=None)
    Bearing: Friction = Field(alias="Bearing", default=None)
    Actuator: Union[IdealisedPitchActuator, LinearPitchActuator, PitchSystemRotaryDrive, PitchActuatorInsert] = Field(alias="Actuator", default=None, discriminator='ActuatorDriveType')
    OutputGroups: PitchSystemOutputGroupLibrary = Field(alias="OutputGroups", default=PitchSystemOutputGroupLibrary()) # Not supported yet
    ConnectableNodes: PitchSystemConnectableNodes = Field(alias="ConnectableNodes", default=PitchSystemConnectableNodes()) # Not supported yet

    class Config:
        extra = Extra.forbid
        validate_assignment = True
        allow_population_by_field_name = True
        pass


    @classmethod
    def parse_obj(cls: Type['Model'], obj: Any) -> 'Model':
        discriminated_props = [
            ('Actuator', 'ActuatorDriveType'),
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
        if isinstance(data, PitchSystem):
            return data
        if not isinstance(data, dict):
            raise TypeError('An object is required to define PitchSystem models')
        return PitchSystem.parse_obj(data)


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
    def Actuator_as_IdealisedPitchActuator(self) -> IdealisedPitchActuator:
        """
        Retrieves the value of Actuator guaranteeing it is a IdealisedPitchActuator; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        IdealisedPitchActuator
            A model object, guaranteed to be a IdealisedPitchActuator.

        Raises
        ------
        TypeError
            If the value is not a IdealisedPitchActuator.
        """
        return self.Actuator_as(IdealisedPitchActuator)


    @property
    def Actuator_as_LinearPitchActuator(self) -> LinearPitchActuator:
        """
        Retrieves the value of Actuator guaranteeing it is a LinearPitchActuator; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        LinearPitchActuator
            A model object, guaranteed to be a LinearPitchActuator.

        Raises
        ------
        TypeError
            If the value is not a LinearPitchActuator.
        """
        return self.Actuator_as(LinearPitchActuator)


    @property
    def Actuator_as_PitchSystemRotaryDrive(self) -> PitchSystemRotaryDrive:
        """
        Retrieves the value of Actuator guaranteeing it is a PitchSystemRotaryDrive; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        PitchSystemRotaryDrive
            A model object, guaranteed to be a PitchSystemRotaryDrive.

        Raises
        ------
        TypeError
            If the value is not a PitchSystemRotaryDrive.
        """
        return self.Actuator_as(PitchSystemRotaryDrive)


    @property
    def Actuator_as_inline(self) -> Union[IdealisedPitchActuator, LinearPitchActuator, PitchSystemRotaryDrive]:
        """
        Retrieves the value of Actuator as a model object; if the value is specified with a '$insert', an error is raised.

        Returns
        -------
        Union[IdealisedPitchActuator, LinearPitchActuator, PitchSystemRotaryDrive]
            A model object at the specified index, guaranteed to not be a '$insert'.

        Raises
        ------
        TypeError
            If the value is not one of the concrete types of PitchActuator; i.e. it is specified with a '$insert'.
        """
        if isinstance(self.Actuator, PitchActuatorInsert) or self.Actuator.is_insert:
            raise TypeError(f"Expected Actuator value to be an in-line object, but it is currently in the '$insert' state.")
        return self.Actuator


    def Actuator_as(self, cls: Type[TPitchActuatorOptions])-> TPitchActuatorOptions:
        """
        Retrieves the value of Actuator, ensuring it is of the specified type.
        The specified type must be one of the valid concrete types of PitchActuator, or the '$insert' type
        (in the case the model is defined to be inserted from an external resource).

        Useful when using type-checking development tools, as it provides a concise way to access a value with the correct type.

        Parameters
        ----------
        cls: Type[Union[IdealisedPitchActuator, LinearPitchActuator, PitchSystemRotaryDrive, PitchActuatorInsert]]
            One of the valid concrete types of PitchActuator, or the '$insert' type
            (in the case the model is defined to be inserted from an external resource).

        Returns
        -------
        TPitchActuatorOptions
            A model object of the specified type.

        Raises
        ------
        TypeError
            If the value is not of the specified type.

        Examples
        --------
        Get a reference to the value when it is one of the types of PitchActuator:
        >>> val_obj = model_obj.Actuator_as(models.IdealisedPitchActuator)
        >>> val_obj = model_obj.Actuator_as(models.LinearPitchActuator)
        >>> val_obj = model_obj.Actuator_as(models.PitchSystemRotaryDrive)

        Get a reference to the value, when it was specified with a '$insert' and read in from a file:
        >>> insert_obj = model_obj.Actuator_as(models.PitchActuatorInsert)
        """
        if not isinstance(self.Actuator, cls):
            raise TypeError(f"Expected Actuator of type '{cls.__name__}' but was type '{type(self.Actuator).__name__}'")
        return self.Actuator



    def _find_unused_containers(self) -> Set[str]:
        unused_containers: Set[str] = super()._find_unused_containers()
        if self.OutputGroups._is_unused():
            unused_containers.add('OutputGroups')
        if self.ConnectableNodes._is_unused():
            unused_containers.add('ConnectableNodes')
        return unused_containers


    def _is_unused(self) -> bool:
        """
        Returns true if the model has no user-supplied values. This indicates the object should not be rendered in the final JSON output.
        """
        candidate_fields = [x[1] for x in self.__dict__.items() if x[0] != 'ComponentType']
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
        PitchSystem
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = PitchSystem.from_file('/path/to/file')
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
        PitchSystem
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = PitchSystem.from_json('{ ... }')
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
        PitchSystem
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


PitchSystem.update_forward_refs()
