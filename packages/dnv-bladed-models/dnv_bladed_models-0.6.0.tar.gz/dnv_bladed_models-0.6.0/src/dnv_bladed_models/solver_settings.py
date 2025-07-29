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

from dnv_bladed_models.equilibrium_state_solver_settings import EquilibriumStateSolverSettings

from dnv_bladed_models.explicit_newmark_beta_fixed_step import ExplicitNewmarkBetaFixedStep

from dnv_bladed_models.generalised_alpha_fixed_step import GeneralisedAlphaFixedStep

from dnv_bladed_models.implicit_newmark_beta_fixed_step import ImplicitNewmarkBetaFixedStep

from dnv_bladed_models.integrator import Integrator

from dnv_bladed_models.integrator_insert import IntegratorInsert

from dnv_bladed_models.runge_kutta_variable_step import RungeKuttaVariableStep



from .schema_helper import SchemaHelper 
from .models_impl import *

TIntegratorOptions = TypeVar('TIntegratorOptions', ExplicitNewmarkBetaFixedStep, GeneralisedAlphaFixedStep, ImplicitNewmarkBetaFixedStep, RungeKuttaVariableStep, IntegratorInsert, Integrator, )

class SolverSettings(BladedModel):
    r"""
    Settings for the numerical solving of the analysis, including integrator settings.
    
    Attributes
    ----------
    EquilibriumStateIteration : EquilibriumStateSolverSettings
    
    TimeDomainIntegration : Union[ExplicitNewmarkBetaFixedStep, GeneralisedAlphaFixedStep, ImplicitNewmarkBetaFixedStep, RungeKuttaVariableStep, IntegratorInsert]
    
    Notes
    -----
    
    """
    _relative_schema_path: str = PrivateAttr('Settings/SolverSettings/SolverSettings.json')

    EquilibriumStateIteration: EquilibriumStateSolverSettings = Field(alias="EquilibriumStateIteration", default=None)
    TimeDomainIntegration: Union[ExplicitNewmarkBetaFixedStep, GeneralisedAlphaFixedStep, ImplicitNewmarkBetaFixedStep, RungeKuttaVariableStep, IntegratorInsert] = Field(alias="TimeDomainIntegration", default=None, discriminator='IntegratorType')

    class Config:
        extra = Extra.forbid
        validate_assignment = True
        allow_population_by_field_name = True
        pass


    @classmethod
    def parse_obj(cls: Type['Model'], obj: Any) -> 'Model':
        discriminated_props = [
            ('TimeDomainIntegration', 'IntegratorType'),
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
        if isinstance(data, SolverSettings):
            return data
        if not isinstance(data, dict):
            raise TypeError('An object is required to define SolverSettings models')
        return SolverSettings.parse_obj(data)


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
    def TimeDomainIntegration_as_ExplicitNewmarkBetaFixedStep(self) -> ExplicitNewmarkBetaFixedStep:
        """
        Retrieves the value of TimeDomainIntegration guaranteeing it is a ExplicitNewmarkBetaFixedStep; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        ExplicitNewmarkBetaFixedStep
            A model object, guaranteed to be a ExplicitNewmarkBetaFixedStep.

        Raises
        ------
        TypeError
            If the value is not a ExplicitNewmarkBetaFixedStep.
        """
        return self.TimeDomainIntegration_as(ExplicitNewmarkBetaFixedStep)


    @property
    def TimeDomainIntegration_as_GeneralisedAlphaFixedStep(self) -> GeneralisedAlphaFixedStep:
        """
        Retrieves the value of TimeDomainIntegration guaranteeing it is a GeneralisedAlphaFixedStep; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        GeneralisedAlphaFixedStep
            A model object, guaranteed to be a GeneralisedAlphaFixedStep.

        Raises
        ------
        TypeError
            If the value is not a GeneralisedAlphaFixedStep.
        """
        return self.TimeDomainIntegration_as(GeneralisedAlphaFixedStep)


    @property
    def TimeDomainIntegration_as_ImplicitNewmarkBetaFixedStep(self) -> ImplicitNewmarkBetaFixedStep:
        """
        Retrieves the value of TimeDomainIntegration guaranteeing it is a ImplicitNewmarkBetaFixedStep; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        ImplicitNewmarkBetaFixedStep
            A model object, guaranteed to be a ImplicitNewmarkBetaFixedStep.

        Raises
        ------
        TypeError
            If the value is not a ImplicitNewmarkBetaFixedStep.
        """
        return self.TimeDomainIntegration_as(ImplicitNewmarkBetaFixedStep)


    @property
    def TimeDomainIntegration_as_RungeKuttaVariableStep(self) -> RungeKuttaVariableStep:
        """
        Retrieves the value of TimeDomainIntegration guaranteeing it is a RungeKuttaVariableStep; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        RungeKuttaVariableStep
            A model object, guaranteed to be a RungeKuttaVariableStep.

        Raises
        ------
        TypeError
            If the value is not a RungeKuttaVariableStep.
        """
        return self.TimeDomainIntegration_as(RungeKuttaVariableStep)


    @property
    def TimeDomainIntegration_as_inline(self) -> Union[ExplicitNewmarkBetaFixedStep, GeneralisedAlphaFixedStep, ImplicitNewmarkBetaFixedStep, RungeKuttaVariableStep]:
        """
        Retrieves the value of TimeDomainIntegration as a model object; if the value is specified with a '$insert', an error is raised.

        Returns
        -------
        Union[ExplicitNewmarkBetaFixedStep, GeneralisedAlphaFixedStep, ImplicitNewmarkBetaFixedStep, RungeKuttaVariableStep]
            A model object at the specified index, guaranteed to not be a '$insert'.

        Raises
        ------
        TypeError
            If the value is not one of the concrete types of Integrator; i.e. it is specified with a '$insert'.
        """
        if isinstance(self.TimeDomainIntegration, IntegratorInsert) or self.TimeDomainIntegration.is_insert:
            raise TypeError(f"Expected TimeDomainIntegration value to be an in-line object, but it is currently in the '$insert' state.")
        return self.TimeDomainIntegration


    def TimeDomainIntegration_as(self, cls: Type[TIntegratorOptions])-> TIntegratorOptions:
        """
        Retrieves the value of TimeDomainIntegration, ensuring it is of the specified type.
        The specified type must be one of the valid concrete types of Integrator, or the '$insert' type
        (in the case the model is defined to be inserted from an external resource).

        Useful when using type-checking development tools, as it provides a concise way to access a value with the correct type.

        Parameters
        ----------
        cls: Type[Union[ExplicitNewmarkBetaFixedStep, GeneralisedAlphaFixedStep, ImplicitNewmarkBetaFixedStep, RungeKuttaVariableStep, IntegratorInsert]]
            One of the valid concrete types of Integrator, or the '$insert' type
            (in the case the model is defined to be inserted from an external resource).

        Returns
        -------
        TIntegratorOptions
            A model object of the specified type.

        Raises
        ------
        TypeError
            If the value is not of the specified type.

        Examples
        --------
        Get a reference to the value when it is one of the types of Integrator:
        >>> val_obj = model_obj.TimeDomainIntegration_as(models.ExplicitNewmarkBetaFixedStep)
        >>> val_obj = model_obj.TimeDomainIntegration_as(models.GeneralisedAlphaFixedStep)
        >>> val_obj = model_obj.TimeDomainIntegration_as(models.ImplicitNewmarkBetaFixedStep)
        >>> val_obj = model_obj.TimeDomainIntegration_as(models.RungeKuttaVariableStep)

        Get a reference to the value, when it was specified with a '$insert' and read in from a file:
        >>> insert_obj = model_obj.TimeDomainIntegration_as(models.IntegratorInsert)
        """
        if not isinstance(self.TimeDomainIntegration, cls):
            raise TypeError(f"Expected TimeDomainIntegration of type '{cls.__name__}' but was type '{type(self.TimeDomainIntegration).__name__}'")
        return self.TimeDomainIntegration



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
        SolverSettings
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = SolverSettings.from_file('/path/to/file')
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
        SolverSettings
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = SolverSettings.from_json('{ ... }')
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
        SolverSettings
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


SolverSettings.update_forward_refs()
