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

from dnv_bladed_models.dynamic_stall import DynamicStall



from .schema_helper import SchemaHelper 
from .models_impl import *


class IAGModel(DynamicStall):
    r"""
    The IAG dynamic stall model.
    
    Attributes
    ----------
    DynamicStallType : Literal['IAGModel'], default='IAGModel'
        Defines the specific type of DynamicStall model in use.  For a `IAGModel` object, this must always be set to a value of `IAGModel`.
    
    UseImpulsiveContributions : bool, default=True
        Enabling the impulsive contributions in lift and moment coefficient.
    
    PressureLagTimeConstant : float, default=1.7
        The lag between the pressure and the lift.
    
    VortexLiftTimeConstant : float, default=6
        The rate of decay of the vortex induced lift that is generated when aerofoils undergo a rapid change in angle of attack towards positive or negative stall.
    
    VortexTravelTimeConstant : float, default=6
        The time constant that controls the duration of the vortex induced lift that is generated when aerofoils undergo a rapid change in angle of attack towards positive or negative stall.
    
    AttachedFlowConstantA1 : float, default=0.3
        The constant A1 for the IAG dynamic stall model to control the attached flow states.
    
    AttachedFlowConstantA2 : float, default=0.7
        The constant A2 for the IAG dynamic stall model to control the attached flow states.
    
    AttachedFlowConstantB1 : float, default=0.7
        The constant B1 for the IAG dynamic stall model to control the attached flow states.
    
    AttachedFlowConstantB2 : float, default=0.53
        The constant B2 for the IAG dynamic stall model to control the attached flow states.
    
    Notes
    -----
    
    """
    _relative_schema_path: str = PrivateAttr('Settings/AerodynamicSettings/DynamicStall/IAGModel.json')

    DynamicStallType: Literal['IAGModel'] = Field(alias="DynamicStallType", default='IAGModel', allow_mutation=False, const=True)
    UseImpulsiveContributions: bool = Field(alias="UseImpulsiveContributions", default=None)
    PressureLagTimeConstant: float = Field(alias="PressureLagTimeConstant", default=None)
    VortexLiftTimeConstant: float = Field(alias="VortexLiftTimeConstant", default=None)
    VortexTravelTimeConstant: float = Field(alias="VortexTravelTimeConstant", default=None)
    AttachedFlowConstantA1: float = Field(alias="AttachedFlowConstantA1", default=None)
    AttachedFlowConstantA2: float = Field(alias="AttachedFlowConstantA2", default=None)
    AttachedFlowConstantB1: float = Field(alias="AttachedFlowConstantB1", default=None)
    AttachedFlowConstantB2: float = Field(alias="AttachedFlowConstantB2", default=None)

    class Config:
        extra = Extra.forbid
        validate_assignment = True
        allow_population_by_field_name = True
        pass


    @classmethod
    def parse_obj(cls: Type['Model'], obj: Any) -> 'Model':
        discriminated_props = [
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
        if isinstance(data, IAGModel):
            return data
        if not isinstance(data, dict):
            raise TypeError('An object is required to define IAGModel models')
        return IAGModel.parse_obj(data)


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
        candidate_fields = [x[1] for x in self.__dict__.items() if x[0] != 'DynamicStallType']
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
        IAGModel
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = IAGModel.from_file('/path/to/file')
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
        IAGModel
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = IAGModel.from_json('{ ... }')
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
        IAGModel
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


IAGModel.update_forward_refs()
