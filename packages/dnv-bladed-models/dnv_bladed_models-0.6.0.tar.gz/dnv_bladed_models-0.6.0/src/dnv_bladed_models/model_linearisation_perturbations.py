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

from dnv_bladed_models.perturbation_settings import PerturbationSettings



from .schema_helper import SchemaHelper 
from .models_impl import *


class ModelLinearisationPerturbations(PerturbationSettings):
    r"""
    
    
    Not supported yet.
    
    Attributes
    ----------
    WindSpeedPerturbation : float, Not supported yet
        The magnitude of perturbation of the wind speed around the equilibrium value.  It should be small so that the analysis stays in the linear region  Omit keyword in order to let Bladed calculate a default perturbation.
    
    PitchPerturbation : float, Not supported yet
        The magnitude of perturbation of the pitch angle around the equilibrium value.  It should be small so that the analysis stays in the linear region.  Omit keyword in order to let Bladed calculate a default perturbation.
    
    GeneratorTorquePerturbation : float, Not supported yet
        The magnitude of perturbation of the generator torque around the equilibrium value.  It should be small so that the analysis stays in the linear region.  Omit keyword in order to let Bladed calculate a default perturbation.
    
    WindShearPerturbation : float, default=0, Not supported yet
        The magnitude of both horizontal and vertical shear perturbations   The default is to have no perturbation on the wind shear.
    
    ApplyPitchPerturbationToEachBlade : bool, default=False, Not supported yet
        If true, the pitch angle will be perturbed in turn for each blade as well as collectively for all blades
    
    YawActuatorTorquePerturbation : float, Not supported yet
        Yaw actuator torque perturbation. The torque perturbation is evenly distributed across the actuator banks.
    
    Notes
    -----
    This model is not supported yet by the Bladed calculation engine.
    """
    _relative_schema_path: str = PrivateAttr('SteadyCalculation/ModelLinearisationPerturbations/ModelLinearisationPerturbations.json')

    WindSpeedPerturbation: float = Field(alias="WindSpeedPerturbation", default=None) # Not supported yet
    PitchPerturbation: float = Field(alias="PitchPerturbation", default=None) # Not supported yet
    GeneratorTorquePerturbation: float = Field(alias="GeneratorTorquePerturbation", default=None) # Not supported yet
    WindShearPerturbation: float = Field(alias="WindShearPerturbation", default=None) # Not supported yet
    ApplyPitchPerturbationToEachBlade: bool = Field(alias="ApplyPitchPerturbationToEachBlade", default=None) # Not supported yet
    YawActuatorTorquePerturbation: float = Field(alias="YawActuatorTorquePerturbation", default=None) # Not supported yet

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
        if isinstance(data, ModelLinearisationPerturbations):
            return data
        if not isinstance(data, dict):
            raise TypeError('An object is required to define ModelLinearisationPerturbations models')
        return ModelLinearisationPerturbations.parse_obj(data)


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
        ModelLinearisationPerturbations
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = ModelLinearisationPerturbations.from_file('/path/to/file')
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
        ModelLinearisationPerturbations
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = ModelLinearisationPerturbations.from_json('{ ... }')
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
        ModelLinearisationPerturbations
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


ModelLinearisationPerturbations.update_forward_refs()
