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

from dnv_bladed_models.bladed_model import BladedModel

from dnv_bladed_models.earthquake import Earthquake

from dnv_bladed_models.external_flow_source_for_wind import ExternalFlowSourceForWind

from dnv_bladed_models.laminar_flow_wind import LaminarFlowWind

from dnv_bladed_models.sea_state import SeaState

from dnv_bladed_models.turbulent_wind import TurbulentWind

from dnv_bladed_models.wind import Wind

from dnv_bladed_models.wind_insert import WindInsert



from .schema_helper import SchemaHelper 
from .models_impl import *

TWindOptions = TypeVar('TWindOptions', ExternalFlowSourceForWind, LaminarFlowWind, TurbulentWind, WindInsert, Wind, )

class Environment(BladedModel):
    r"""
    The definition of the environment conditions affecting the turbine location during this simulation.
    
    Attributes
    ----------
    Wind : Union[ExternalFlowSourceForWind, LaminarFlowWind, TurbulentWind, WindInsert]
    
    SeaState : SeaState, Not supported yet
    
    Earthquake : Earthquake, Not supported yet
    
    Notes
    -----
    
    """
    _relative_schema_path: str = PrivateAttr('TimeDomainSimulation/Environment/Environment.json')

    Wind: Union[ExternalFlowSourceForWind, LaminarFlowWind, TurbulentWind, WindInsert] = Field(alias="Wind", default=None, discriminator='WindType')
    SeaState: SeaState = Field(alias="SeaState", default=None) # Not supported yet
    Earthquake: Earthquake = Field(alias="Earthquake", default=None) # Not supported yet

    class Config:
        extra = Extra.forbid
        validate_assignment = True
        allow_population_by_field_name = True
        pass


    @classmethod
    def parse_obj(cls: Type['Model'], obj: Any) -> 'Model':
        discriminated_props = [
            ('Wind', 'WindType'),
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
        if isinstance(data, Environment):
            return data
        if not isinstance(data, dict):
            raise TypeError('An object is required to define Environment models')
        return Environment.parse_obj(data)


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
    def Wind_as_ExternalFlowSourceForWind(self) -> ExternalFlowSourceForWind:
        """
        Retrieves the value of Wind guaranteeing it is a ExternalFlowSourceForWind; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        ExternalFlowSourceForWind
            A model object, guaranteed to be a ExternalFlowSourceForWind.

        Raises
        ------
        TypeError
            If the value is not a ExternalFlowSourceForWind.
        """
        return self.Wind_as(ExternalFlowSourceForWind)


    @property
    def Wind_as_LaminarFlowWind(self) -> LaminarFlowWind:
        """
        Retrieves the value of Wind guaranteeing it is a LaminarFlowWind; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        LaminarFlowWind
            A model object, guaranteed to be a LaminarFlowWind.

        Raises
        ------
        TypeError
            If the value is not a LaminarFlowWind.
        """
        return self.Wind_as(LaminarFlowWind)


    @property
    def Wind_as_TurbulentWind(self) -> TurbulentWind:
        """
        Retrieves the value of Wind guaranteeing it is a TurbulentWind; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        TurbulentWind
            A model object, guaranteed to be a TurbulentWind.

        Raises
        ------
        TypeError
            If the value is not a TurbulentWind.
        """
        return self.Wind_as(TurbulentWind)


    @property
    def Wind_as_inline(self) -> Union[ExternalFlowSourceForWind, LaminarFlowWind, TurbulentWind]:
        """
        Retrieves the value of Wind as a model object; if the value is specified with a '$insert', an error is raised.

        Returns
        -------
        Union[ExternalFlowSourceForWind, LaminarFlowWind, TurbulentWind]
            A model object at the specified index, guaranteed to not be a '$insert'.

        Raises
        ------
        TypeError
            If the value is not one of the concrete types of Wind; i.e. it is specified with a '$insert'.
        """
        if isinstance(self.Wind, WindInsert) or self.Wind.is_insert:
            raise TypeError(f"Expected Wind value to be an in-line object, but it is currently in the '$insert' state.")
        return self.Wind


    def Wind_as(self, cls: Type[TWindOptions])-> TWindOptions:
        """
        Retrieves the value of Wind, ensuring it is of the specified type.
        The specified type must be one of the valid concrete types of Wind, or the '$insert' type
        (in the case the model is defined to be inserted from an external resource).

        Useful when using type-checking development tools, as it provides a concise way to access a value with the correct type.

        Parameters
        ----------
        cls: Type[Union[ExternalFlowSourceForWind, LaminarFlowWind, TurbulentWind, WindInsert]]
            One of the valid concrete types of Wind, or the '$insert' type
            (in the case the model is defined to be inserted from an external resource).

        Returns
        -------
        TWindOptions
            A model object of the specified type.

        Raises
        ------
        TypeError
            If the value is not of the specified type.

        Examples
        --------
        Get a reference to the value when it is one of the types of Wind:
        >>> val_obj = model_obj.Wind_as(models.ExternalFlowSourceForWind)
        >>> val_obj = model_obj.Wind_as(models.LaminarFlowWind)
        >>> val_obj = model_obj.Wind_as(models.TurbulentWind)

        Get a reference to the value, when it was specified with a '$insert' and read in from a file:
        >>> insert_obj = model_obj.Wind_as(models.WindInsert)
        """
        if not isinstance(self.Wind, cls):
            raise TypeError(f"Expected Wind of type '{cls.__name__}' but was type '{type(self.Wind).__name__}'")
        return self.Wind



    def _find_unused_containers(self) -> Set[str]:
        unused_containers: Set[str] = super()._find_unused_containers()
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
        Environment
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = Environment.from_file('/path/to/file')
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
        Environment
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = Environment.from_json('{ ... }')
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
        Environment
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


Environment.update_forward_refs()
