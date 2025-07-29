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

from dnv_bladed_models.fixed_step_integrator import FixedStepIntegrator



from .schema_helper import SchemaHelper 
from .models_impl import *


class ImplicitNewmarkBetaFixedStep(FixedStepIntegrator):
    r"""
    Settings for the Implicit Newmark Beta Fixed Step integrator.
    
    Attributes
    ----------
    IntegratorType : Literal['ImplicitNewmarkBetaFixedStep'], default='ImplicitNewmarkBetaFixedStep'
        Defines the specific type of Integrator model in use.  For a `ImplicitNewmarkBetaFixedStep` object, this must always be set to a value of `ImplicitNewmarkBetaFixedStep`.
    
    MaximumNumberOfIterations : int, default=1
        The maximum number of iterations for prescribed freedoms and first order states (e.g. dynamic stall & wake).  A value of 1 may sometimes inprecisely integrate first order states
    
    Beta : float, default=0.25
        The β parameter for the Newmark-β integration method.  The recommended value of 0.25 (with a γ value of 0.50) results in the constant average acceleration method that is unconditionally stable for linear systems.  A value of 0.26 (with a γ value of 0.52) results in a method that is close to the constant average acceleration method but includes a small amount of numerical damping to reduce unwanted vibrations of high-frequency modes. Note that the numerical damping increases with the step size.
    
    Gamma : float, default=0.5
        The γ parameter for the Newmark-β integration method.  The recommended value depends on the β parameter and given by the formula γ = 2.sqrt(β) - 0.5.  Values higher than 0.5 introduce positive numerical damping, whereas lower values introduce negative numerical damping.
    
    ToleranceMultiplier : float, default=1
        The tolerance used for defining the convergence criteria of the Newton-Raphson equilibrium iterations for 1st and 2nd order states.  Reduced values of this parameter result in more iterations and more accurate solutions, whereas increased values result in less iterations and less accurate solutions, which eventually may cause stability problems.  The allowable range of values for this parameter is 0.001 to 1000.
    
    Notes
    -----
    
    """
    _relative_schema_path: str = PrivateAttr('Settings/SolverSettings/Integrator/ImplicitNewmarkBetaFixedStep.json')

    IntegratorType: Literal['ImplicitNewmarkBetaFixedStep'] = Field(alias="IntegratorType", default='ImplicitNewmarkBetaFixedStep', allow_mutation=False, const=True)
    MaximumNumberOfIterations: int = Field(alias="MaximumNumberOfIterations", default=None)
    Beta: float = Field(alias="Beta", default=None)
    Gamma: float = Field(alias="Gamma", default=None)
    ToleranceMultiplier: float = Field(alias="ToleranceMultiplier", default=None)

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
        if isinstance(data, ImplicitNewmarkBetaFixedStep):
            return data
        if not isinstance(data, dict):
            raise TypeError('An object is required to define ImplicitNewmarkBetaFixedStep models')
        return ImplicitNewmarkBetaFixedStep.parse_obj(data)


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
        candidate_fields = [x[1] for x in self.__dict__.items() if x[0] != 'IntegratorType']
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
        ImplicitNewmarkBetaFixedStep
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = ImplicitNewmarkBetaFixedStep.from_file('/path/to/file')
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
        ImplicitNewmarkBetaFixedStep
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = ImplicitNewmarkBetaFixedStep.from_json('{ ... }')
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
        ImplicitNewmarkBetaFixedStep
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


ImplicitNewmarkBetaFixedStep.update_forward_refs()
