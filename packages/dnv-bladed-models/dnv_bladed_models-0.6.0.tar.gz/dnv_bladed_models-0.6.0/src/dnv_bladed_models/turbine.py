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

from dnv_bladed_models.assembly import Assembly

from dnv_bladed_models.bladed_control import BladedControl

from dnv_bladed_models.bladed_model import BladedModel

from dnv_bladed_models.component_library import ComponentLibrary

from dnv_bladed_models.electrical_grid import ElectricalGrid

from dnv_bladed_models.external_module import ExternalModule

from dnv_bladed_models.turbine_operational_parameters import TurbineOperationalParameters



from .schema_helper import SchemaHelper 
from .models_impl import *


class Turbine(BladedModel):
    r"""
    The definition of the turbine and its installation that is to be modelled.
    
    Attributes
    ----------
    ElectricalGrid : ElectricalGrid, Not supported yet
    
    TurbineOperationalParameters : TurbineOperationalParameters
    
    Control : BladedControl
    
    GlobalExternalModules : List[ExternalModule], Not supported yet
        A list of any external modules that will be run with the time domain simulations.  It is expected that external modules defined here will interact with more than one area of the turbine, such as to apply additional aerodynamics loads to the entire structure.  Any external modules that represent a single component should be added to the Assembly tree.
    
    MeanSeaLevel : float, default=0
        The mean sea depth at the turbine location.  If omited, the Turbine will be considered an on-shore turbine and any sea states will be ignored.
    
    Assembly : Assembly
    
    ComponentLibrary : ComponentLibrary
    
    Notes
    -----
    
    """
    _relative_schema_path: str = PrivateAttr('Turbine/Turbine.json')

    ElectricalGrid: ElectricalGrid = Field(alias="ElectricalGrid", default=None) # Not supported yet
    TurbineOperationalParameters: TurbineOperationalParameters = Field(alias="TurbineOperationalParameters", default=None)
    Control: BladedControl = Field(alias="Control", default=None)
    GlobalExternalModules: List[ExternalModule] = Field(alias="GlobalExternalModules", default=list()) # Not supported yet
    MeanSeaLevel: float = Field(alias="MeanSeaLevel", default=None)
    Assembly: Assembly = Field(alias="Assembly", default=Assembly())
    ComponentLibrary: ComponentLibrary = Field(alias="ComponentLibrary", default=ComponentLibrary())

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
        if isinstance(data, Turbine):
            return data
        if not isinstance(data, dict):
            raise TypeError('An object is required to define Turbine models')
        return Turbine.parse_obj(data)


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
        if self.GlobalExternalModules is not None and len(self.GlobalExternalModules) == 0: #type: ignore
            unused_containers.add('GlobalExternalModules')
        if self.Assembly._is_unused():
            unused_containers.add('Assembly')
        if self.ComponentLibrary._is_unused():
            unused_containers.add('ComponentLibrary')
        return unused_containers


    def _is_unused(self) -> bool:
        """
        Returns true if the model has no user-supplied values. This indicates the object should not be rendered in the final JSON output.
        """
        candidate_fields = self.__dict__.values()
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
        Turbine
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = Turbine.from_file('/path/to/file')
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
        Turbine
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = Turbine.from_json('{ ... }')
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
        Turbine
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


Turbine.update_forward_refs()
