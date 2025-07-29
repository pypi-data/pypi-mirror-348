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

from dnv_bladed_models.current import Current

from dnv_bladed_models.current_insert import CurrentInsert

from dnv_bladed_models.currents import Currents

from dnv_bladed_models.jonswap_pierson_moskowitz import JonswapPiersonMoskowitz

from dnv_bladed_models.laminar_flow_current import LaminarFlowCurrent

from dnv_bladed_models.linear_airy import LinearAiry

from dnv_bladed_models.stream_function import StreamFunction

from dnv_bladed_models.tide import Tide

from dnv_bladed_models.turbulent_current import TurbulentCurrent

from dnv_bladed_models.user_defined_waves import UserDefinedWaves

from dnv_bladed_models.wave_spectrum import WaveSpectrum

from dnv_bladed_models.waves import Waves

from dnv_bladed_models.waves_insert import WavesInsert



from .schema_helper import SchemaHelper 
from .models_impl import *

TCurrentOptions = TypeVar('TCurrentOptions', Currents, LaminarFlowCurrent, TurbulentCurrent, CurrentInsert, Current, )
TWavesOptions = TypeVar('TWavesOptions', JonswapPiersonMoskowitz, LinearAiry, StreamFunction, UserDefinedWaves, WaveSpectrum, WavesInsert, Waves, )

class SeaState(BladedModel):
    r"""
    The sea state at the turbine location.  The mean sea level is defined in the Turbine section of the data model.
    
    Not supported yet.
    
    Attributes
    ----------
    Current : Union[Currents, LaminarFlowCurrent, TurbulentCurrent, CurrentInsert], Not supported yet
    
    Waves : Union[JonswapPiersonMoskowitz, LinearAiry, StreamFunction, UserDefinedWaves, WaveSpectrum, WavesInsert], Not supported yet
    
    Tide : Tide, Not supported yet
    
    Notes
    -----
    This model is not supported yet by the Bladed calculation engine.
    """
    _relative_schema_path: str = PrivateAttr('TimeDomainSimulation/Environment/SeaState/SeaState.json')

    Current: Union[Currents, LaminarFlowCurrent, TurbulentCurrent, CurrentInsert] = Field(alias="Current", default=None, discriminator='CurrentType') # Not supported yet
    Waves: Union[JonswapPiersonMoskowitz, LinearAiry, StreamFunction, UserDefinedWaves, WaveSpectrum, WavesInsert] = Field(alias="Waves", default=None, discriminator='WavesType') # Not supported yet
    Tide: Tide = Field(alias="Tide", default=None) # Not supported yet

    class Config:
        extra = Extra.forbid
        validate_assignment = True
        allow_population_by_field_name = True
        pass


    @classmethod
    def parse_obj(cls: Type['Model'], obj: Any) -> 'Model':
        discriminated_props = [
            ('Current', 'CurrentType'),
            ('Waves', 'WavesType'),
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
        if isinstance(data, SeaState):
            return data
        if not isinstance(data, dict):
            raise TypeError('An object is required to define SeaState models')
        return SeaState.parse_obj(data)


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
    def Current_as_Currents(self) -> Currents:
        """
        Retrieves the value of Current guaranteeing it is a Currents; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        Currents
            A model object, guaranteed to be a Currents.

        Raises
        ------
        TypeError
            If the value is not a Currents.
        """
        return self.Current_as(Currents)


    @property
    def Current_as_LaminarFlowCurrent(self) -> LaminarFlowCurrent:
        """
        Retrieves the value of Current guaranteeing it is a LaminarFlowCurrent; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        LaminarFlowCurrent
            A model object, guaranteed to be a LaminarFlowCurrent.

        Raises
        ------
        TypeError
            If the value is not a LaminarFlowCurrent.
        """
        return self.Current_as(LaminarFlowCurrent)


    @property
    def Current_as_TurbulentCurrent(self) -> TurbulentCurrent:
        """
        Retrieves the value of Current guaranteeing it is a TurbulentCurrent; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        TurbulentCurrent
            A model object, guaranteed to be a TurbulentCurrent.

        Raises
        ------
        TypeError
            If the value is not a TurbulentCurrent.
        """
        return self.Current_as(TurbulentCurrent)


    @property
    def Current_as_inline(self) -> Union[Currents, LaminarFlowCurrent, TurbulentCurrent]:
        """
        Retrieves the value of Current as a model object; if the value is specified with a '$insert', an error is raised.

        Returns
        -------
        Union[Currents, LaminarFlowCurrent, TurbulentCurrent]
            A model object at the specified index, guaranteed to not be a '$insert'.

        Raises
        ------
        TypeError
            If the value is not one of the concrete types of Current; i.e. it is specified with a '$insert'.
        """
        if isinstance(self.Current, CurrentInsert) or self.Current.is_insert:
            raise TypeError(f"Expected Current value to be an in-line object, but it is currently in the '$insert' state.")
        return self.Current


    def Current_as(self, cls: Type[TCurrentOptions])-> TCurrentOptions:
        """
        Retrieves the value of Current, ensuring it is of the specified type.
        The specified type must be one of the valid concrete types of Current, or the '$insert' type
        (in the case the model is defined to be inserted from an external resource).

        Useful when using type-checking development tools, as it provides a concise way to access a value with the correct type.

        Parameters
        ----------
        cls: Type[Union[Currents, LaminarFlowCurrent, TurbulentCurrent, CurrentInsert]]
            One of the valid concrete types of Current, or the '$insert' type
            (in the case the model is defined to be inserted from an external resource).

        Returns
        -------
        TCurrentOptions
            A model object of the specified type.

        Raises
        ------
        TypeError
            If the value is not of the specified type.

        Examples
        --------
        Get a reference to the value when it is one of the types of Current:
        >>> val_obj = model_obj.Current_as(models.Currents)
        >>> val_obj = model_obj.Current_as(models.LaminarFlowCurrent)
        >>> val_obj = model_obj.Current_as(models.TurbulentCurrent)

        Get a reference to the value, when it was specified with a '$insert' and read in from a file:
        >>> insert_obj = model_obj.Current_as(models.CurrentInsert)
        """
        if not isinstance(self.Current, cls):
            raise TypeError(f"Expected Current of type '{cls.__name__}' but was type '{type(self.Current).__name__}'")
        return self.Current


    @property
    def Waves_as_JonswapPiersonMoskowitz(self) -> JonswapPiersonMoskowitz:
        """
        Retrieves the value of Waves guaranteeing it is a JonswapPiersonMoskowitz; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        JonswapPiersonMoskowitz
            A model object, guaranteed to be a JonswapPiersonMoskowitz.

        Raises
        ------
        TypeError
            If the value is not a JonswapPiersonMoskowitz.
        """
        return self.Waves_as(JonswapPiersonMoskowitz)


    @property
    def Waves_as_LinearAiry(self) -> LinearAiry:
        """
        Retrieves the value of Waves guaranteeing it is a LinearAiry; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        LinearAiry
            A model object, guaranteed to be a LinearAiry.

        Raises
        ------
        TypeError
            If the value is not a LinearAiry.
        """
        return self.Waves_as(LinearAiry)


    @property
    def Waves_as_StreamFunction(self) -> StreamFunction:
        """
        Retrieves the value of Waves guaranteeing it is a StreamFunction; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        StreamFunction
            A model object, guaranteed to be a StreamFunction.

        Raises
        ------
        TypeError
            If the value is not a StreamFunction.
        """
        return self.Waves_as(StreamFunction)


    @property
    def Waves_as_UserDefinedWaves(self) -> UserDefinedWaves:
        """
        Retrieves the value of Waves guaranteeing it is a UserDefinedWaves; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        UserDefinedWaves
            A model object, guaranteed to be a UserDefinedWaves.

        Raises
        ------
        TypeError
            If the value is not a UserDefinedWaves.
        """
        return self.Waves_as(UserDefinedWaves)


    @property
    def Waves_as_WaveSpectrum(self) -> WaveSpectrum:
        """
        Retrieves the value of Waves guaranteeing it is a WaveSpectrum; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        WaveSpectrum
            A model object, guaranteed to be a WaveSpectrum.

        Raises
        ------
        TypeError
            If the value is not a WaveSpectrum.
        """
        return self.Waves_as(WaveSpectrum)


    @property
    def Waves_as_inline(self) -> Union[JonswapPiersonMoskowitz, LinearAiry, StreamFunction, UserDefinedWaves, WaveSpectrum]:
        """
        Retrieves the value of Waves as a model object; if the value is specified with a '$insert', an error is raised.

        Returns
        -------
        Union[JonswapPiersonMoskowitz, LinearAiry, StreamFunction, UserDefinedWaves, WaveSpectrum]
            A model object at the specified index, guaranteed to not be a '$insert'.

        Raises
        ------
        TypeError
            If the value is not one of the concrete types of Waves; i.e. it is specified with a '$insert'.
        """
        if isinstance(self.Waves, WavesInsert) or self.Waves.is_insert:
            raise TypeError(f"Expected Waves value to be an in-line object, but it is currently in the '$insert' state.")
        return self.Waves


    def Waves_as(self, cls: Type[TWavesOptions])-> TWavesOptions:
        """
        Retrieves the value of Waves, ensuring it is of the specified type.
        The specified type must be one of the valid concrete types of Waves, or the '$insert' type
        (in the case the model is defined to be inserted from an external resource).

        Useful when using type-checking development tools, as it provides a concise way to access a value with the correct type.

        Parameters
        ----------
        cls: Type[Union[JonswapPiersonMoskowitz, LinearAiry, StreamFunction, UserDefinedWaves, WaveSpectrum, WavesInsert]]
            One of the valid concrete types of Waves, or the '$insert' type
            (in the case the model is defined to be inserted from an external resource).

        Returns
        -------
        TWavesOptions
            A model object of the specified type.

        Raises
        ------
        TypeError
            If the value is not of the specified type.

        Examples
        --------
        Get a reference to the value when it is one of the types of Waves:
        >>> val_obj = model_obj.Waves_as(models.JonswapPiersonMoskowitz)
        >>> val_obj = model_obj.Waves_as(models.LinearAiry)
        >>> val_obj = model_obj.Waves_as(models.StreamFunction)
        >>> val_obj = model_obj.Waves_as(models.UserDefinedWaves)
        >>> val_obj = model_obj.Waves_as(models.WaveSpectrum)

        Get a reference to the value, when it was specified with a '$insert' and read in from a file:
        >>> insert_obj = model_obj.Waves_as(models.WavesInsert)
        """
        if not isinstance(self.Waves, cls):
            raise TypeError(f"Expected Waves of type '{cls.__name__}' but was type '{type(self.Waves).__name__}'")
        return self.Waves



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
        SeaState
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = SeaState.from_file('/path/to/file')
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
        SeaState
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = SeaState.from_json('{ ... }')
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
        SeaState
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


SeaState.update_forward_refs()
