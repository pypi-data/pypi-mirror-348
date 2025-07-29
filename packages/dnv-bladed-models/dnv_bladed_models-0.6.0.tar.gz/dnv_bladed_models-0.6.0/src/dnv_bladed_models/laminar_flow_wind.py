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

from dnv_bladed_models.preset_wind_direction_shear_transient import PresetWindDirectionShearTransient

from dnv_bladed_models.preset_wind_horizontal_shear_transient import PresetWindHorizontalShearTransient

from dnv_bladed_models.preset_wind_mean_speed_transient import PresetWindMeanSpeedTransient

from dnv_bladed_models.preset_wind_vertical_shear_transient import PresetWindVerticalShearTransient

from dnv_bladed_models.time_domain_wind import TimeDomainWind

from dnv_bladed_models.wind_direction_shear_time_history import WindDirectionShearTimeHistory

from dnv_bladed_models.wind_direction_shear_variation import WindDirectionShearVariation

from dnv_bladed_models.wind_direction_shear_variation_insert import WindDirectionShearVariationInsert

from dnv_bladed_models.wind_horizontal_shear_time_history import WindHorizontalShearTimeHistory

from dnv_bladed_models.wind_horizontal_shear_variation import WindHorizontalShearVariation

from dnv_bladed_models.wind_horizontal_shear_variation_insert import WindHorizontalShearVariationInsert

from dnv_bladed_models.wind_mean_speed_time_history import WindMeanSpeedTimeHistory

from dnv_bladed_models.wind_mean_speed_variation import WindMeanSpeedVariation

from dnv_bladed_models.wind_mean_speed_variation_insert import WindMeanSpeedVariationInsert

from dnv_bladed_models.wind_vertical_shear_time_history import WindVerticalShearTimeHistory

from dnv_bladed_models.wind_vertical_shear_variation import WindVerticalShearVariation

from dnv_bladed_models.wind_vertical_shear_variation_insert import WindVerticalShearVariationInsert



from .schema_helper import SchemaHelper 
from .models_impl import *

TWindMeanSpeedVariationOptions = TypeVar('TWindMeanSpeedVariationOptions', PresetWindMeanSpeedTransient, WindMeanSpeedTimeHistory, WindMeanSpeedVariationInsert, WindMeanSpeedVariation, )
TWindVerticalShearVariationOptions = TypeVar('TWindVerticalShearVariationOptions', PresetWindVerticalShearTransient, WindVerticalShearTimeHistory, WindVerticalShearVariationInsert, WindVerticalShearVariation, )
TWindHorizontalShearVariationOptions = TypeVar('TWindHorizontalShearVariationOptions', PresetWindHorizontalShearTransient, WindHorizontalShearTimeHistory, WindHorizontalShearVariationInsert, WindHorizontalShearVariation, )
TWindDirectionShearVariationOptions = TypeVar('TWindDirectionShearVariationOptions', PresetWindDirectionShearTransient, WindDirectionShearTimeHistory, WindDirectionShearVariationInsert, WindDirectionShearVariation, )

class LaminarFlowWind(TimeDomainWind):
    r"""
    The definition of a wind field that varies throughout a time domain simulation, but does not have turbulence.
    
    Attributes
    ----------
    WindType : Literal['LaminarFlow'], default='LaminarFlow'
        Defines the specific type of Wind model in use.  For a `LaminarFlow` object, this must always be set to a value of `LaminarFlow`.
    
    MeanSpeed : float
        The (constant) mean wind speed for the duration of the simulation.
    
    MeanSpeedVariation : Union[PresetWindMeanSpeedTransient, WindMeanSpeedTimeHistory, WindMeanSpeedVariationInsert]
    
    VerticalShear : float, default=0
        The exponential factor governing the shape of the wind shear variation.  This is typically in the order of 0.2.
    
    VerticalShearVariation : Union[PresetWindVerticalShearTransient, WindVerticalShearTimeHistory, WindVerticalShearVariationInsert]
    
    HorizontalShear : float, default=0
        The change in wind velocity for every unit of distance to either side of the hub.  This represents a linear horizontal wind shear, where the wind speed at the hub centre is at the free-field speed.
    
    HorizontalShearVariation : Union[PresetWindHorizontalShearTransient, WindHorizontalShearTimeHistory, WindHorizontalShearVariationInsert]
    
    DirectionShear : float, default=0
        The direction shear, otherwise known as \"wind veer\".  This models the case where the direction of the wind field varies as the height increases.
    
    DirectionShearVariation : Union[PresetWindDirectionShearTransient, WindDirectionShearTimeHistory, WindDirectionShearVariationInsert]
    
    UseGustPropagation : bool
        If true, gust propagation will be applied (where the transient properties only \"arrive\" at the turbine as the flow does).  This is only relevant to transient flows.
    
    Notes
    -----
    
    """
    _relative_schema_path: str = PrivateAttr('TimeDomainSimulation/Environment/Wind/LaminarFlowWind.json')

    WindType: Literal['LaminarFlow'] = Field(alias="WindType", default='LaminarFlow', allow_mutation=False, const=True)
    MeanSpeed: float = Field(alias="MeanSpeed", default=None)
    MeanSpeedVariation: Union[PresetWindMeanSpeedTransient, WindMeanSpeedTimeHistory, WindMeanSpeedVariationInsert] = Field(alias="MeanSpeedVariation", default=None, discriminator='MeanSpeedVariationType')
    VerticalShear: float = Field(alias="VerticalShear", default=None)
    VerticalShearVariation: Union[PresetWindVerticalShearTransient, WindVerticalShearTimeHistory, WindVerticalShearVariationInsert] = Field(alias="VerticalShearVariation", default=None, discriminator='VerticalShearVariationType')
    HorizontalShear: float = Field(alias="HorizontalShear", default=None)
    HorizontalShearVariation: Union[PresetWindHorizontalShearTransient, WindHorizontalShearTimeHistory, WindHorizontalShearVariationInsert] = Field(alias="HorizontalShearVariation", default=None, discriminator='HorizontalShearVariationType')
    DirectionShear: float = Field(alias="DirectionShear", default=None)
    DirectionShearVariation: Union[PresetWindDirectionShearTransient, WindDirectionShearTimeHistory, WindDirectionShearVariationInsert] = Field(alias="DirectionShearVariation", default=None, discriminator='DirectionShearVariationType')
    UseGustPropagation: bool = Field(alias="UseGustPropagation", default=None)

    class Config:
        extra = Extra.forbid
        validate_assignment = True
        allow_population_by_field_name = True
        pass


    @classmethod
    def parse_obj(cls: Type['Model'], obj: Any) -> 'Model':
        discriminated_props = [
            ('MeanSpeedVariation', 'MeanSpeedVariationType'),
            ('VerticalShearVariation', 'VerticalShearVariationType'),
            ('HorizontalShearVariation', 'HorizontalShearVariationType'),
            ('DirectionShearVariation', 'DirectionShearVariationType'),
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
        if isinstance(data, LaminarFlowWind):
            return data
        if not isinstance(data, dict):
            raise TypeError('An object is required to define LaminarFlowWind models')
        return LaminarFlowWind.parse_obj(data)


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
    def MeanSpeedVariation_as_PresetWindMeanSpeedTransient(self) -> PresetWindMeanSpeedTransient:
        """
        Retrieves the value of MeanSpeedVariation guaranteeing it is a PresetWindMeanSpeedTransient; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        PresetWindMeanSpeedTransient
            A model object, guaranteed to be a PresetWindMeanSpeedTransient.

        Raises
        ------
        TypeError
            If the value is not a PresetWindMeanSpeedTransient.
        """
        return self.MeanSpeedVariation_as(PresetWindMeanSpeedTransient)


    @property
    def MeanSpeedVariation_as_WindMeanSpeedTimeHistory(self) -> WindMeanSpeedTimeHistory:
        """
        Retrieves the value of MeanSpeedVariation guaranteeing it is a WindMeanSpeedTimeHistory; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        WindMeanSpeedTimeHistory
            A model object, guaranteed to be a WindMeanSpeedTimeHistory.

        Raises
        ------
        TypeError
            If the value is not a WindMeanSpeedTimeHistory.
        """
        return self.MeanSpeedVariation_as(WindMeanSpeedTimeHistory)


    @property
    def MeanSpeedVariation_as_inline(self) -> Union[PresetWindMeanSpeedTransient, WindMeanSpeedTimeHistory]:
        """
        Retrieves the value of MeanSpeedVariation as a model object; if the value is specified with a '$insert', an error is raised.

        Returns
        -------
        Union[PresetWindMeanSpeedTransient, WindMeanSpeedTimeHistory]
            A model object at the specified index, guaranteed to not be a '$insert'.

        Raises
        ------
        TypeError
            If the value is not one of the concrete types of WindMeanSpeedVariation; i.e. it is specified with a '$insert'.
        """
        if isinstance(self.MeanSpeedVariation, WindMeanSpeedVariationInsert) or self.MeanSpeedVariation.is_insert:
            raise TypeError(f"Expected MeanSpeedVariation value to be an in-line object, but it is currently in the '$insert' state.")
        return self.MeanSpeedVariation


    def MeanSpeedVariation_as(self, cls: Type[TWindMeanSpeedVariationOptions])-> TWindMeanSpeedVariationOptions:
        """
        Retrieves the value of MeanSpeedVariation, ensuring it is of the specified type.
        The specified type must be one of the valid concrete types of WindMeanSpeedVariation, or the '$insert' type
        (in the case the model is defined to be inserted from an external resource).

        Useful when using type-checking development tools, as it provides a concise way to access a value with the correct type.

        Parameters
        ----------
        cls: Type[Union[PresetWindMeanSpeedTransient, WindMeanSpeedTimeHistory, WindMeanSpeedVariationInsert]]
            One of the valid concrete types of WindMeanSpeedVariation, or the '$insert' type
            (in the case the model is defined to be inserted from an external resource).

        Returns
        -------
        TWindMeanSpeedVariationOptions
            A model object of the specified type.

        Raises
        ------
        TypeError
            If the value is not of the specified type.

        Examples
        --------
        Get a reference to the value when it is one of the types of WindMeanSpeedVariation:
        >>> val_obj = model_obj.MeanSpeedVariation_as(models.PresetWindMeanSpeedTransient)
        >>> val_obj = model_obj.MeanSpeedVariation_as(models.WindMeanSpeedTimeHistory)

        Get a reference to the value, when it was specified with a '$insert' and read in from a file:
        >>> insert_obj = model_obj.MeanSpeedVariation_as(models.WindMeanSpeedVariationInsert)
        """
        if not isinstance(self.MeanSpeedVariation, cls):
            raise TypeError(f"Expected MeanSpeedVariation of type '{cls.__name__}' but was type '{type(self.MeanSpeedVariation).__name__}'")
        return self.MeanSpeedVariation


    @property
    def VerticalShearVariation_as_PresetWindVerticalShearTransient(self) -> PresetWindVerticalShearTransient:
        """
        Retrieves the value of VerticalShearVariation guaranteeing it is a PresetWindVerticalShearTransient; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        PresetWindVerticalShearTransient
            A model object, guaranteed to be a PresetWindVerticalShearTransient.

        Raises
        ------
        TypeError
            If the value is not a PresetWindVerticalShearTransient.
        """
        return self.VerticalShearVariation_as(PresetWindVerticalShearTransient)


    @property
    def VerticalShearVariation_as_WindVerticalShearTimeHistory(self) -> WindVerticalShearTimeHistory:
        """
        Retrieves the value of VerticalShearVariation guaranteeing it is a WindVerticalShearTimeHistory; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        WindVerticalShearTimeHistory
            A model object, guaranteed to be a WindVerticalShearTimeHistory.

        Raises
        ------
        TypeError
            If the value is not a WindVerticalShearTimeHistory.
        """
        return self.VerticalShearVariation_as(WindVerticalShearTimeHistory)


    @property
    def VerticalShearVariation_as_inline(self) -> Union[PresetWindVerticalShearTransient, WindVerticalShearTimeHistory]:
        """
        Retrieves the value of VerticalShearVariation as a model object; if the value is specified with a '$insert', an error is raised.

        Returns
        -------
        Union[PresetWindVerticalShearTransient, WindVerticalShearTimeHistory]
            A model object at the specified index, guaranteed to not be a '$insert'.

        Raises
        ------
        TypeError
            If the value is not one of the concrete types of WindVerticalShearVariation; i.e. it is specified with a '$insert'.
        """
        if isinstance(self.VerticalShearVariation, WindVerticalShearVariationInsert) or self.VerticalShearVariation.is_insert:
            raise TypeError(f"Expected VerticalShearVariation value to be an in-line object, but it is currently in the '$insert' state.")
        return self.VerticalShearVariation


    def VerticalShearVariation_as(self, cls: Type[TWindVerticalShearVariationOptions])-> TWindVerticalShearVariationOptions:
        """
        Retrieves the value of VerticalShearVariation, ensuring it is of the specified type.
        The specified type must be one of the valid concrete types of WindVerticalShearVariation, or the '$insert' type
        (in the case the model is defined to be inserted from an external resource).

        Useful when using type-checking development tools, as it provides a concise way to access a value with the correct type.

        Parameters
        ----------
        cls: Type[Union[PresetWindVerticalShearTransient, WindVerticalShearTimeHistory, WindVerticalShearVariationInsert]]
            One of the valid concrete types of WindVerticalShearVariation, or the '$insert' type
            (in the case the model is defined to be inserted from an external resource).

        Returns
        -------
        TWindVerticalShearVariationOptions
            A model object of the specified type.

        Raises
        ------
        TypeError
            If the value is not of the specified type.

        Examples
        --------
        Get a reference to the value when it is one of the types of WindVerticalShearVariation:
        >>> val_obj = model_obj.VerticalShearVariation_as(models.PresetWindVerticalShearTransient)
        >>> val_obj = model_obj.VerticalShearVariation_as(models.WindVerticalShearTimeHistory)

        Get a reference to the value, when it was specified with a '$insert' and read in from a file:
        >>> insert_obj = model_obj.VerticalShearVariation_as(models.WindVerticalShearVariationInsert)
        """
        if not isinstance(self.VerticalShearVariation, cls):
            raise TypeError(f"Expected VerticalShearVariation of type '{cls.__name__}' but was type '{type(self.VerticalShearVariation).__name__}'")
        return self.VerticalShearVariation


    @property
    def HorizontalShearVariation_as_PresetWindHorizontalShearTransient(self) -> PresetWindHorizontalShearTransient:
        """
        Retrieves the value of HorizontalShearVariation guaranteeing it is a PresetWindHorizontalShearTransient; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        PresetWindHorizontalShearTransient
            A model object, guaranteed to be a PresetWindHorizontalShearTransient.

        Raises
        ------
        TypeError
            If the value is not a PresetWindHorizontalShearTransient.
        """
        return self.HorizontalShearVariation_as(PresetWindHorizontalShearTransient)


    @property
    def HorizontalShearVariation_as_WindHorizontalShearTimeHistory(self) -> WindHorizontalShearTimeHistory:
        """
        Retrieves the value of HorizontalShearVariation guaranteeing it is a WindHorizontalShearTimeHistory; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        WindHorizontalShearTimeHistory
            A model object, guaranteed to be a WindHorizontalShearTimeHistory.

        Raises
        ------
        TypeError
            If the value is not a WindHorizontalShearTimeHistory.
        """
        return self.HorizontalShearVariation_as(WindHorizontalShearTimeHistory)


    @property
    def HorizontalShearVariation_as_inline(self) -> Union[PresetWindHorizontalShearTransient, WindHorizontalShearTimeHistory]:
        """
        Retrieves the value of HorizontalShearVariation as a model object; if the value is specified with a '$insert', an error is raised.

        Returns
        -------
        Union[PresetWindHorizontalShearTransient, WindHorizontalShearTimeHistory]
            A model object at the specified index, guaranteed to not be a '$insert'.

        Raises
        ------
        TypeError
            If the value is not one of the concrete types of WindHorizontalShearVariation; i.e. it is specified with a '$insert'.
        """
        if isinstance(self.HorizontalShearVariation, WindHorizontalShearVariationInsert) or self.HorizontalShearVariation.is_insert:
            raise TypeError(f"Expected HorizontalShearVariation value to be an in-line object, but it is currently in the '$insert' state.")
        return self.HorizontalShearVariation


    def HorizontalShearVariation_as(self, cls: Type[TWindHorizontalShearVariationOptions])-> TWindHorizontalShearVariationOptions:
        """
        Retrieves the value of HorizontalShearVariation, ensuring it is of the specified type.
        The specified type must be one of the valid concrete types of WindHorizontalShearVariation, or the '$insert' type
        (in the case the model is defined to be inserted from an external resource).

        Useful when using type-checking development tools, as it provides a concise way to access a value with the correct type.

        Parameters
        ----------
        cls: Type[Union[PresetWindHorizontalShearTransient, WindHorizontalShearTimeHistory, WindHorizontalShearVariationInsert]]
            One of the valid concrete types of WindHorizontalShearVariation, or the '$insert' type
            (in the case the model is defined to be inserted from an external resource).

        Returns
        -------
        TWindHorizontalShearVariationOptions
            A model object of the specified type.

        Raises
        ------
        TypeError
            If the value is not of the specified type.

        Examples
        --------
        Get a reference to the value when it is one of the types of WindHorizontalShearVariation:
        >>> val_obj = model_obj.HorizontalShearVariation_as(models.PresetWindHorizontalShearTransient)
        >>> val_obj = model_obj.HorizontalShearVariation_as(models.WindHorizontalShearTimeHistory)

        Get a reference to the value, when it was specified with a '$insert' and read in from a file:
        >>> insert_obj = model_obj.HorizontalShearVariation_as(models.WindHorizontalShearVariationInsert)
        """
        if not isinstance(self.HorizontalShearVariation, cls):
            raise TypeError(f"Expected HorizontalShearVariation of type '{cls.__name__}' but was type '{type(self.HorizontalShearVariation).__name__}'")
        return self.HorizontalShearVariation


    @property
    def DirectionShearVariation_as_PresetWindDirectionShearTransient(self) -> PresetWindDirectionShearTransient:
        """
        Retrieves the value of DirectionShearVariation guaranteeing it is a PresetWindDirectionShearTransient; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        PresetWindDirectionShearTransient
            A model object, guaranteed to be a PresetWindDirectionShearTransient.

        Raises
        ------
        TypeError
            If the value is not a PresetWindDirectionShearTransient.
        """
        return self.DirectionShearVariation_as(PresetWindDirectionShearTransient)


    @property
    def DirectionShearVariation_as_WindDirectionShearTimeHistory(self) -> WindDirectionShearTimeHistory:
        """
        Retrieves the value of DirectionShearVariation guaranteeing it is a WindDirectionShearTimeHistory; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        WindDirectionShearTimeHistory
            A model object, guaranteed to be a WindDirectionShearTimeHistory.

        Raises
        ------
        TypeError
            If the value is not a WindDirectionShearTimeHistory.
        """
        return self.DirectionShearVariation_as(WindDirectionShearTimeHistory)


    @property
    def DirectionShearVariation_as_inline(self) -> Union[PresetWindDirectionShearTransient, WindDirectionShearTimeHistory]:
        """
        Retrieves the value of DirectionShearVariation as a model object; if the value is specified with a '$insert', an error is raised.

        Returns
        -------
        Union[PresetWindDirectionShearTransient, WindDirectionShearTimeHistory]
            A model object at the specified index, guaranteed to not be a '$insert'.

        Raises
        ------
        TypeError
            If the value is not one of the concrete types of WindDirectionShearVariation; i.e. it is specified with a '$insert'.
        """
        if isinstance(self.DirectionShearVariation, WindDirectionShearVariationInsert) or self.DirectionShearVariation.is_insert:
            raise TypeError(f"Expected DirectionShearVariation value to be an in-line object, but it is currently in the '$insert' state.")
        return self.DirectionShearVariation


    def DirectionShearVariation_as(self, cls: Type[TWindDirectionShearVariationOptions])-> TWindDirectionShearVariationOptions:
        """
        Retrieves the value of DirectionShearVariation, ensuring it is of the specified type.
        The specified type must be one of the valid concrete types of WindDirectionShearVariation, or the '$insert' type
        (in the case the model is defined to be inserted from an external resource).

        Useful when using type-checking development tools, as it provides a concise way to access a value with the correct type.

        Parameters
        ----------
        cls: Type[Union[PresetWindDirectionShearTransient, WindDirectionShearTimeHistory, WindDirectionShearVariationInsert]]
            One of the valid concrete types of WindDirectionShearVariation, or the '$insert' type
            (in the case the model is defined to be inserted from an external resource).

        Returns
        -------
        TWindDirectionShearVariationOptions
            A model object of the specified type.

        Raises
        ------
        TypeError
            If the value is not of the specified type.

        Examples
        --------
        Get a reference to the value when it is one of the types of WindDirectionShearVariation:
        >>> val_obj = model_obj.DirectionShearVariation_as(models.PresetWindDirectionShearTransient)
        >>> val_obj = model_obj.DirectionShearVariation_as(models.WindDirectionShearTimeHistory)

        Get a reference to the value, when it was specified with a '$insert' and read in from a file:
        >>> insert_obj = model_obj.DirectionShearVariation_as(models.WindDirectionShearVariationInsert)
        """
        if not isinstance(self.DirectionShearVariation, cls):
            raise TypeError(f"Expected DirectionShearVariation of type '{cls.__name__}' but was type '{type(self.DirectionShearVariation).__name__}'")
        return self.DirectionShearVariation



    def _find_unused_containers(self) -> Set[str]:
        unused_containers: Set[str] = super()._find_unused_containers()
        return unused_containers


    def _is_unused(self) -> bool:
        """
        Returns true if the model has no user-supplied values. This indicates the object should not be rendered in the final JSON output.
        """
        candidate_fields = [x[1] for x in self.__dict__.items() if x[0] != 'WindType']
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
        LaminarFlowWind
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = LaminarFlowWind.from_file('/path/to/file')
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
        LaminarFlowWind
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = LaminarFlowWind.from_json('{ ... }')
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
        LaminarFlowWind
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


LaminarFlowWind.update_forward_refs()
