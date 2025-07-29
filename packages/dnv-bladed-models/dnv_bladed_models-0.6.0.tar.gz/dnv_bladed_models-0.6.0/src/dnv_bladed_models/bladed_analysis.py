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

from dnv_bladed_models.aerodynamic_information_calculation import AerodynamicInformationCalculation

from dnv_bladed_models.blade_stability_analysis import BladeStabilityAnalysis

from dnv_bladed_models.bladed_model import BladedModel

from dnv_bladed_models.campbell_diagram import CampbellDiagram

from dnv_bladed_models.constants import Constants

from dnv_bladed_models.model_linearisation import ModelLinearisation

from dnv_bladed_models.performance_coefficients_calculation import PerformanceCoefficientsCalculation

from dnv_bladed_models.settings import Settings

from dnv_bladed_models.steady_calculation import SteadyCalculation

from dnv_bladed_models.steady_calculation_insert import SteadyCalculationInsert

from dnv_bladed_models.steady_operational_loads_calculation import SteadyOperationalLoadsCalculation

from dnv_bladed_models.steady_parked_loads_calculation import SteadyParkedLoadsCalculation

from dnv_bladed_models.steady_power_curve_calculation import SteadyPowerCurveCalculation

from dnv_bladed_models.time_domain_simulation import TimeDomainSimulation

from dnv_bladed_models.turbine import Turbine



from .schema_helper import SchemaHelper 
from .models_impl import *

TSteadyCalculationOptions = TypeVar('TSteadyCalculationOptions', AerodynamicInformationCalculation, BladeStabilityAnalysis, CampbellDiagram, ModelLinearisation, PerformanceCoefficientsCalculation, SteadyOperationalLoadsCalculation, SteadyParkedLoadsCalculation, SteadyPowerCurveCalculation, SteadyCalculationInsert, SteadyCalculation, )

class BladedAnalysis(BladedModel):
    r"""
    The definition of a single Bladed analysis.
    
    Attributes
    ----------
    TimeDomainSimulation : TimeDomainSimulation
    
    SteadyCalculation : Union[AerodynamicInformationCalculation, BladeStabilityAnalysis, CampbellDiagram, ModelLinearisation, PerformanceCoefficientsCalculation, SteadyOperationalLoadsCalculation, SteadyParkedLoadsCalculation, SteadyPowerCurveCalculation, SteadyCalculationInsert]
    
    Settings : Settings
    
    Constants : Constants
    
    Turbine : Turbine
    
    Notes
    -----
    
    """
    _relative_schema_path: str = PrivateAttr('BladedAnalysis.json')

    TimeDomainSimulation: TimeDomainSimulation = Field(alias="TimeDomainSimulation", default=None)
    SteadyCalculation: Union[AerodynamicInformationCalculation, BladeStabilityAnalysis, CampbellDiagram, ModelLinearisation, PerformanceCoefficientsCalculation, SteadyOperationalLoadsCalculation, SteadyParkedLoadsCalculation, SteadyPowerCurveCalculation, SteadyCalculationInsert] = Field(alias="SteadyCalculation", default=None, discriminator='SteadyCalculationType')
    Settings: Settings = Field(alias="Settings", default=None)
    Constants: Constants = Field(alias="Constants", default=None)
    Turbine: Turbine = Field(alias="Turbine", default=None)

    class Config:
        extra = Extra.forbid
        validate_assignment = True
        allow_population_by_field_name = True
        pass


    @classmethod
    def parse_obj(cls: Type['Model'], obj: Any) -> 'Model':
        discriminated_props = [
            ('SteadyCalculation', 'SteadyCalculationType'),
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
        if isinstance(data, BladedAnalysis):
            return data
        if not isinstance(data, dict):
            raise TypeError('An object is required to define BladedAnalysis models')
        return BladedAnalysis.parse_obj(data)


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
    def SteadyCalculation_as_AerodynamicInformationCalculation(self) -> AerodynamicInformationCalculation:
        """
        Retrieves the value of SteadyCalculation guaranteeing it is a AerodynamicInformationCalculation; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        AerodynamicInformationCalculation
            A model object, guaranteed to be a AerodynamicInformationCalculation.

        Raises
        ------
        TypeError
            If the value is not a AerodynamicInformationCalculation.
        """
        return self.SteadyCalculation_as(AerodynamicInformationCalculation)


    @property
    def SteadyCalculation_as_BladeStabilityAnalysis(self) -> BladeStabilityAnalysis:
        """
        Retrieves the value of SteadyCalculation guaranteeing it is a BladeStabilityAnalysis; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        BladeStabilityAnalysis
            A model object, guaranteed to be a BladeStabilityAnalysis.

        Raises
        ------
        TypeError
            If the value is not a BladeStabilityAnalysis.
        """
        return self.SteadyCalculation_as(BladeStabilityAnalysis)


    @property
    def SteadyCalculation_as_CampbellDiagram(self) -> CampbellDiagram:
        """
        Retrieves the value of SteadyCalculation guaranteeing it is a CampbellDiagram; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        CampbellDiagram
            A model object, guaranteed to be a CampbellDiagram.

        Raises
        ------
        TypeError
            If the value is not a CampbellDiagram.
        """
        return self.SteadyCalculation_as(CampbellDiagram)


    @property
    def SteadyCalculation_as_ModelLinearisation(self) -> ModelLinearisation:
        """
        Retrieves the value of SteadyCalculation guaranteeing it is a ModelLinearisation; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        ModelLinearisation
            A model object, guaranteed to be a ModelLinearisation.

        Raises
        ------
        TypeError
            If the value is not a ModelLinearisation.
        """
        return self.SteadyCalculation_as(ModelLinearisation)


    @property
    def SteadyCalculation_as_PerformanceCoefficientsCalculation(self) -> PerformanceCoefficientsCalculation:
        """
        Retrieves the value of SteadyCalculation guaranteeing it is a PerformanceCoefficientsCalculation; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        PerformanceCoefficientsCalculation
            A model object, guaranteed to be a PerformanceCoefficientsCalculation.

        Raises
        ------
        TypeError
            If the value is not a PerformanceCoefficientsCalculation.
        """
        return self.SteadyCalculation_as(PerformanceCoefficientsCalculation)


    @property
    def SteadyCalculation_as_SteadyOperationalLoadsCalculation(self) -> SteadyOperationalLoadsCalculation:
        """
        Retrieves the value of SteadyCalculation guaranteeing it is a SteadyOperationalLoadsCalculation; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        SteadyOperationalLoadsCalculation
            A model object, guaranteed to be a SteadyOperationalLoadsCalculation.

        Raises
        ------
        TypeError
            If the value is not a SteadyOperationalLoadsCalculation.
        """
        return self.SteadyCalculation_as(SteadyOperationalLoadsCalculation)


    @property
    def SteadyCalculation_as_SteadyParkedLoadsCalculation(self) -> SteadyParkedLoadsCalculation:
        """
        Retrieves the value of SteadyCalculation guaranteeing it is a SteadyParkedLoadsCalculation; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        SteadyParkedLoadsCalculation
            A model object, guaranteed to be a SteadyParkedLoadsCalculation.

        Raises
        ------
        TypeError
            If the value is not a SteadyParkedLoadsCalculation.
        """
        return self.SteadyCalculation_as(SteadyParkedLoadsCalculation)


    @property
    def SteadyCalculation_as_SteadyPowerCurveCalculation(self) -> SteadyPowerCurveCalculation:
        """
        Retrieves the value of SteadyCalculation guaranteeing it is a SteadyPowerCurveCalculation; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        SteadyPowerCurveCalculation
            A model object, guaranteed to be a SteadyPowerCurveCalculation.

        Raises
        ------
        TypeError
            If the value is not a SteadyPowerCurveCalculation.
        """
        return self.SteadyCalculation_as(SteadyPowerCurveCalculation)


    @property
    def SteadyCalculation_as_inline(self) -> Union[AerodynamicInformationCalculation, BladeStabilityAnalysis, CampbellDiagram, ModelLinearisation, PerformanceCoefficientsCalculation, SteadyOperationalLoadsCalculation, SteadyParkedLoadsCalculation, SteadyPowerCurveCalculation]:
        """
        Retrieves the value of SteadyCalculation as a model object; if the value is specified with a '$insert', an error is raised.

        Returns
        -------
        Union[AerodynamicInformationCalculation, BladeStabilityAnalysis, CampbellDiagram, ModelLinearisation, PerformanceCoefficientsCalculation, SteadyOperationalLoadsCalculation, SteadyParkedLoadsCalculation, SteadyPowerCurveCalculation]
            A model object at the specified index, guaranteed to not be a '$insert'.

        Raises
        ------
        TypeError
            If the value is not one of the concrete types of SteadyCalculation; i.e. it is specified with a '$insert'.
        """
        if isinstance(self.SteadyCalculation, SteadyCalculationInsert) or self.SteadyCalculation.is_insert:
            raise TypeError(f"Expected SteadyCalculation value to be an in-line object, but it is currently in the '$insert' state.")
        return self.SteadyCalculation


    def SteadyCalculation_as(self, cls: Type[TSteadyCalculationOptions])-> TSteadyCalculationOptions:
        """
        Retrieves the value of SteadyCalculation, ensuring it is of the specified type.
        The specified type must be one of the valid concrete types of SteadyCalculation, or the '$insert' type
        (in the case the model is defined to be inserted from an external resource).

        Useful when using type-checking development tools, as it provides a concise way to access a value with the correct type.

        Parameters
        ----------
        cls: Type[Union[AerodynamicInformationCalculation, BladeStabilityAnalysis, CampbellDiagram, ModelLinearisation, PerformanceCoefficientsCalculation, SteadyOperationalLoadsCalculation, SteadyParkedLoadsCalculation, SteadyPowerCurveCalculation, SteadyCalculationInsert]]
            One of the valid concrete types of SteadyCalculation, or the '$insert' type
            (in the case the model is defined to be inserted from an external resource).

        Returns
        -------
        TSteadyCalculationOptions
            A model object of the specified type.

        Raises
        ------
        TypeError
            If the value is not of the specified type.

        Examples
        --------
        Get a reference to the value when it is one of the types of SteadyCalculation:
        >>> val_obj = model_obj.SteadyCalculation_as(models.AerodynamicInformationCalculation)
        >>> val_obj = model_obj.SteadyCalculation_as(models.BladeStabilityAnalysis)
        >>> val_obj = model_obj.SteadyCalculation_as(models.CampbellDiagram)
        >>> val_obj = model_obj.SteadyCalculation_as(models.ModelLinearisation)
        >>> val_obj = model_obj.SteadyCalculation_as(models.PerformanceCoefficientsCalculation)
        >>> val_obj = model_obj.SteadyCalculation_as(models.SteadyOperationalLoadsCalculation)
        >>> val_obj = model_obj.SteadyCalculation_as(models.SteadyParkedLoadsCalculation)
        >>> val_obj = model_obj.SteadyCalculation_as(models.SteadyPowerCurveCalculation)

        Get a reference to the value, when it was specified with a '$insert' and read in from a file:
        >>> insert_obj = model_obj.SteadyCalculation_as(models.SteadyCalculationInsert)
        """
        if not isinstance(self.SteadyCalculation, cls):
            raise TypeError(f"Expected SteadyCalculation of type '{cls.__name__}' but was type '{type(self.SteadyCalculation).__name__}'")
        return self.SteadyCalculation



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
        BladedAnalysis
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = BladedAnalysis.from_file('/path/to/file')
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
        BladedAnalysis
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = BladedAnalysis.from_json('{ ... }')
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
        BladedAnalysis
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


BladedAnalysis.update_forward_refs()
