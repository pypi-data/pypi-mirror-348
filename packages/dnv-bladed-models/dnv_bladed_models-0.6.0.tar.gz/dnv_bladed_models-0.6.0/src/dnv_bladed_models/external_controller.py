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



class ExternalController_CallingConventionEnum(str, Enum):
    CDECL = "__cdecl"
    STDCALL = "__stdcall"

class ExternalController_TimeStepMultiplierEnum(str, Enum):
    EVERY = "Every"
    SECOND = "Second"
    THIRD = "Third"
    FOURTH = "Fourth"
    FIFTH = "Fifth"
    SIXTH = "Sixth"
    SEVENTH = "Seventh"
    EIGTH = "Eigth"
    NINTH = "Ninth"
    TENTH = "Tenth"

from .schema_helper import SchemaHelper 
from .models_impl import *


class ExternalController(BladedModel):
    r"""
    A definition of a single controller for the turbine.
    
    Attributes
    ----------
    Filepath : str
        The location of the external controller dll.
    
    CallingConvention : ExternalController_CallingConventionEnum, default='__cdecl'
        The calling convention to be used when calling the external controller.  The default for all C-family languages is '__cdecl'.  The default for FORTRAN is '__stdcall' unless the [C] qualifier is specfied immediately after the function name.  Specifying the wrong calling convention can lead to unexplained system exceptions when attempting to call the external controller.
    
    FunctionName : str, default='ExternalController'
        The name of the function in the dll to run.  This must satisfy the standard external controller typedef, found in the ExternalControllerApi.h.
    
    PassParametersByFile : bool, default=False
        If true, a file will be written containing the parameters in the above box.  The location of this file can be obtained in the external controller using the function GetInfileFilepath.  The name of this file will be \"DISCON.IN\" if there is only one controller, or of the pattern \"DISCONn.IN\", where 'n' is the number of the controller.  If not checked (the default), this string will be directly available using the function GetUserParameters.
    
    ForceLegacy : bool, default=False
        If true, only the old-style 'DISCON' function will be looked for in the controller, and raise an error if it cannot be found.  This is only used for testing legacy controllers where both CONTROLLER and DISCON functions are both defined, but the DISCON function is required.
    
    TimeStepMultiplier : ExternalController_TimeStepMultiplierEnum, default='Every'
        Whether the controller should be called on every discrete timestep, set above.
    
    ParametersAsString : str
        A string that will be passed to the external controller.
    
    ParametersAsJson : Dict[str, Any]
        A JSON object that will be serialised as a string and passed to the external controller.
    
    UseFloatingPointProtection : bool, default=True
        If true, this will apply floating point protection when calling the external controllers.  When the protection is on, any floating point errors are trapped and reported.  When this is switched off, the behaviour will default to that of the computer's floating point machine, but this can often be to not report the error, and to use a semi-random (but often very large) number instead of the correct result.  This can lead to unrepeatable results and numeric errors.
    
    Notes
    -----
    
    """
    _relative_schema_path: str = PrivateAttr('Turbine/BladedControl/ExternalController/ExternalController.json')

    Filepath: str = Field(alias="Filepath", default=None)
    CallingConvention: ExternalController_CallingConventionEnum = Field(alias="CallingConvention", default=None)
    FunctionName: str = Field(alias="FunctionName", default=None)
    PassParametersByFile: bool = Field(alias="PassParametersByFile", default=None)
    ForceLegacy: bool = Field(alias="ForceLegacy", default=None)
    TimeStepMultiplier: ExternalController_TimeStepMultiplierEnum = Field(alias="TimeStepMultiplier", default=None)
    ParametersAsString: str = Field(alias="ParametersAsString", default=None)
    ParametersAsJson: Dict[str, Any] = Field(alias="ParametersAsJson", default=None)
    UseFloatingPointProtection: bool = Field(alias="UseFloatingPointProtection", default=None)

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
        if isinstance(data, ExternalController):
            return data
        if not isinstance(data, dict):
            raise TypeError('An object is required to define ExternalController models')
        return ExternalController.parse_obj(data)


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
        ExternalController
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = ExternalController.from_file('/path/to/file')
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
        ExternalController
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = ExternalController.from_json('{ ... }')
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
        ExternalController
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


ExternalController.update_forward_refs()
