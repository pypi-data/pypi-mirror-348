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

from dnv_bladed_models.exponential_shear_model import ExponentialShearModel

from dnv_bladed_models.logarithmic_shear_model import LogarithmicShearModel

from dnv_bladed_models.look_up_shear_model import LookUpShearModel

from dnv_bladed_models.steady_calculation import SteadyCalculation

from dnv_bladed_models.steady_calculation_with_component_outputs import SteadyCalculationWithComponentOutputs

from dnv_bladed_models.wind_shear import WindShear

from dnv_bladed_models.wind_shear_insert import WindShearInsert



class SteadyParkedLoadsCalculation_SweepParameterEnum(str, Enum):
    AZIMUTH_ANGLE = "AZIMUTH_ANGLE"
    YAW_ANGLE = "YAW_ANGLE"
    FLOW_INCLINATION = "FLOW_INCLINATION"
    PITCH_ANGLE = "PITCH_ANGLE"

from .schema_helper import SchemaHelper 
from .models_impl import *

TWindShearOptions = TypeVar('TWindShearOptions', ExponentialShearModel, LogarithmicShearModel, LookUpShearModel, WindShearInsert, WindShear, )

class SteadyParkedLoadsCalculation(SteadyCalculation):
    r"""
    Defines a calculation which produces loads on the parked turbine in a steady wind.  Most realities such as tower shadow and wind shear are included, making the calculation almost equivalent to a time domain simulation in a steady wind.
    
    Not supported yet.
    
    Attributes
    ----------
    SteadyCalculationType : Literal['SteadyParkedLoads'], default='SteadyParkedLoads', Not supported yet
        Defines the specific type of SteadyCalculation model in use.  For a `SteadyParkedLoads` object, this must always be set to a value of `SteadyParkedLoads`.
    
    WindSpeed : float, Not supported yet
        The wind speed at the hub height to be used for the calculation.
    
    AzimuthAngle : float, default=0, Not supported yet
        The fixed azimuth angle of the rotor (zero azimuth indicates blade 1 pointing upwards).
    
    YawAngle : float, default=0, Not supported yet
        The yaw angle to be used for the calculation.
    
    FlowInclination : float, default=0, Not supported yet
        The flow inclination to be used for the calculation.
    
    ReferenceHeight : float, Not supported yet
        The reference height used for wind shear.  If this is omitted, the hub height will be used, and if there is more than one the *highest* hub height.
    
    WindShear : Union[ExponentialShearModel, LogarithmicShearModel, LookUpShearModel, WindShearInsert]
    
    PitchAngle : float, Not supported yet
        The pitch angle of all of the blades to be used for the calculation.  If not provided, the PitchAngleWhilstParked from TurbineOperationalParameters be used.
    
    SweepParameter : SteadyParkedLoadsCalculation_SweepParameterEnum, Not supported yet
        The parameter to perform the sweep over.
    
    SweepEnd : float, Not supported yet
        The value for the end of the sweep.  The start value will be whatever it is in the parameters for the calculation.
    
    SweepInterval : float, Not supported yet
        The step size to take from the lowest to the highest value.
    
    Outputs : SteadyCalculationWithComponentOutputs
    
    Notes
    -----
    This model is not supported yet by the Bladed calculation engine.
    """
    _relative_schema_path: str = PrivateAttr('SteadyCalculation/SteadyParkedLoadsCalculation.json')

    SteadyCalculationType: Literal['SteadyParkedLoads'] = Field(alias="SteadyCalculationType", default='SteadyParkedLoads', allow_mutation=False, const=True) # Not supported yet
    WindSpeed: float = Field(alias="WindSpeed", default=None) # Not supported yet
    AzimuthAngle: float = Field(alias="AzimuthAngle", default=None) # Not supported yet
    YawAngle: float = Field(alias="YawAngle", default=None) # Not supported yet
    FlowInclination: float = Field(alias="FlowInclination", default=None) # Not supported yet
    ReferenceHeight: float = Field(alias="ReferenceHeight", default=None) # Not supported yet
    WindShear: Union[ExponentialShearModel, LogarithmicShearModel, LookUpShearModel, WindShearInsert] = Field(alias="WindShear", default=None, discriminator='WindShearType')
    PitchAngle: float = Field(alias="PitchAngle", default=None) # Not supported yet
    SweepParameter: SteadyParkedLoadsCalculation_SweepParameterEnum = Field(alias="SweepParameter", default=None) # Not supported yet
    SweepEnd: float = Field(alias="SweepEnd", default=None) # Not supported yet
    SweepInterval: float = Field(alias="SweepInterval", default=None) # Not supported yet
    Outputs: SteadyCalculationWithComponentOutputs = Field(alias="Outputs", default=None)

    class Config:
        extra = Extra.forbid
        validate_assignment = True
        allow_population_by_field_name = True
        pass


    @classmethod
    def parse_obj(cls: Type['Model'], obj: Any) -> 'Model':
        discriminated_props = [
            ('WindShear', 'WindShearType'),
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
        if isinstance(data, SteadyParkedLoadsCalculation):
            return data
        if not isinstance(data, dict):
            raise TypeError('An object is required to define SteadyParkedLoadsCalculation models')
        return SteadyParkedLoadsCalculation.parse_obj(data)


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
    def WindShear_as_ExponentialShearModel(self) -> ExponentialShearModel:
        """
        Retrieves the value of WindShear guaranteeing it is a ExponentialShearModel; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        ExponentialShearModel
            A model object, guaranteed to be a ExponentialShearModel.

        Raises
        ------
        TypeError
            If the value is not a ExponentialShearModel.
        """
        return self.WindShear_as(ExponentialShearModel)


    @property
    def WindShear_as_LogarithmicShearModel(self) -> LogarithmicShearModel:
        """
        Retrieves the value of WindShear guaranteeing it is a LogarithmicShearModel; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        LogarithmicShearModel
            A model object, guaranteed to be a LogarithmicShearModel.

        Raises
        ------
        TypeError
            If the value is not a LogarithmicShearModel.
        """
        return self.WindShear_as(LogarithmicShearModel)


    @property
    def WindShear_as_LookUpShearModel(self) -> LookUpShearModel:
        """
        Retrieves the value of WindShear guaranteeing it is a LookUpShearModel; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        LookUpShearModel
            A model object, guaranteed to be a LookUpShearModel.

        Raises
        ------
        TypeError
            If the value is not a LookUpShearModel.
        """
        return self.WindShear_as(LookUpShearModel)


    @property
    def WindShear_as_inline(self) -> Union[ExponentialShearModel, LogarithmicShearModel, LookUpShearModel]:
        """
        Retrieves the value of WindShear as a model object; if the value is specified with a '$insert', an error is raised.

        Returns
        -------
        Union[ExponentialShearModel, LogarithmicShearModel, LookUpShearModel]
            A model object at the specified index, guaranteed to not be a '$insert'.

        Raises
        ------
        TypeError
            If the value is not one of the concrete types of WindShear; i.e. it is specified with a '$insert'.
        """
        if isinstance(self.WindShear, WindShearInsert) or self.WindShear.is_insert:
            raise TypeError(f"Expected WindShear value to be an in-line object, but it is currently in the '$insert' state.")
        return self.WindShear


    def WindShear_as(self, cls: Type[TWindShearOptions])-> TWindShearOptions:
        """
        Retrieves the value of WindShear, ensuring it is of the specified type.
        The specified type must be one of the valid concrete types of WindShear, or the '$insert' type
        (in the case the model is defined to be inserted from an external resource).

        Useful when using type-checking development tools, as it provides a concise way to access a value with the correct type.

        Parameters
        ----------
        cls: Type[Union[ExponentialShearModel, LogarithmicShearModel, LookUpShearModel, WindShearInsert]]
            One of the valid concrete types of WindShear, or the '$insert' type
            (in the case the model is defined to be inserted from an external resource).

        Returns
        -------
        TWindShearOptions
            A model object of the specified type.

        Raises
        ------
        TypeError
            If the value is not of the specified type.

        Examples
        --------
        Get a reference to the value when it is one of the types of WindShear:
        >>> val_obj = model_obj.WindShear_as(models.ExponentialShearModel)
        >>> val_obj = model_obj.WindShear_as(models.LogarithmicShearModel)
        >>> val_obj = model_obj.WindShear_as(models.LookUpShearModel)

        Get a reference to the value, when it was specified with a '$insert' and read in from a file:
        >>> insert_obj = model_obj.WindShear_as(models.WindShearInsert)
        """
        if not isinstance(self.WindShear, cls):
            raise TypeError(f"Expected WindShear of type '{cls.__name__}' but was type '{type(self.WindShear).__name__}'")
        return self.WindShear



    def _find_unused_containers(self) -> Set[str]:
        unused_containers: Set[str] = super()._find_unused_containers()
        return unused_containers


    def _is_unused(self) -> bool:
        """
        Returns true if the model has no user-supplied values. This indicates the object should not be rendered in the final JSON output.
        """
        candidate_fields = [x[1] for x in self.__dict__.items() if x[0] != 'SteadyCalculationType']
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
        SteadyParkedLoadsCalculation
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = SteadyParkedLoadsCalculation.from_file('/path/to/file')
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
        SteadyParkedLoadsCalculation
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = SteadyParkedLoadsCalculation.from_json('{ ... }')
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
        SteadyParkedLoadsCalculation
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


SteadyParkedLoadsCalculation.update_forward_refs()
