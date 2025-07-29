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

from dnv_bladed_models.aerodynamic_model import AerodynamicModel



class VortexLine_WakeTypeEnum(str, Enum):
    FREE_WAKE = "FreeWake"
    FIXED_WAKE = "FixedWake"

class VortexLine_CoreGrowthModelEnum(str, Enum):
    RL_MODEL = "RL_Model"
    LO_MODEL = "LO_Model"
    FIXED = "Fixed"

class VortexLine_InitialVortexCoreSizeModelEnum(str, Enum):
    RL_MODEL = "RL_Model"
    LO_MODEL = "LO_Model"
    FIXED = "Fixed"

from .schema_helper import SchemaHelper 
from .models_impl import *


class VortexLine(AerodynamicModel):
    r"""
    The Vortex Line aerodynamic model.
    
    Not supported yet.
    
    Attributes
    ----------
    AerodynamicModelType : Literal['VortexLine'], default='VortexLine', Not supported yet
        Defines the specific type of AerodynamicModel model in use.  For a `VortexLine` object, this must always be set to a value of `VortexLine`.
    
    MaximumNumberofFreeWakeSteps : int, default=200, Not supported yet
        Each free wake node that is emitted from the trailing edge will be allowed a maximum number of free wake steps after it will be no longer considered in the free wake solution and convected with local wind speed and last computed induction.
    
    MaximumNumberofWakeSteps : int, default=10000, Not supported yet
        Each wake node will be allowed a maximum number of steps before it is removed. This option puts an upper bound on the number of wake nodes.
    
    NumberOfThreads : int, default=1, Not supported yet
        The number of parallel CPU threads used in evaluation of the Biot-Savart law.  This option is only relevant when the wake type is set to \"Free Wake\".
    
    VortexWakeTimeStep : float, default=0.05, Not supported yet
        The time step used to update the vortex wake.  It is recommended to select a time step such that at least 60 vortex wake steps are taken each rotor revolution.
    
    WakeType : VortexLine_WakeTypeEnum, default='FreeWake', Not supported yet
        The \"Free Wake\" option will calculate the mutual influence of all wake elements on all wake nodes during each time step.  The \"Fixed Wake\" option will assume that the induced velocity in all wake nodes is equal to the average wake induced velocity at 70% blade radius.  The \"Free Wake\" option requires substantially more calculations to be performed, and is likely to significantly slow the analysis.
    
    CoreGrowthModel : VortexLine_CoreGrowthModelEnum, default='RL_Model', Not supported yet
        The Core Growth Model.
    
    InitialVortexCoreSizeModel : VortexLine_InitialVortexCoreSizeModelEnum, default='RL_Model', Not supported yet
        The intial vortex core size Model.
    
    FilamentStrain : bool, default=True, Not supported yet
        The filament strain.
    
    LambOseenCoreGrowthConstant : float, default=1.234, Not supported yet
        The Lamb-Oseen core growth constant,
    
    CoreGrowthConstant : float, default=50, Not supported yet
        The core growth constant.
    
    RamasamyLeishmanConstant : float, default=0.000065, Not supported yet
        The Ramasamy-Leishman constant.
    
    Notes
    -----
    This model is not supported yet by the Bladed calculation engine.
    """
    _relative_schema_path: str = PrivateAttr('Settings/AerodynamicSettings/AerodynamicModel/VortexLine.json')

    AerodynamicModelType: Literal['VortexLine'] = Field(alias="AerodynamicModelType", default='VortexLine', allow_mutation=False, const=True) # Not supported yet
    MaximumNumberofFreeWakeSteps: int = Field(alias="MaximumNumberofFreeWakeSteps", default=None) # Not supported yet
    MaximumNumberofWakeSteps: int = Field(alias="MaximumNumberofWakeSteps", default=None) # Not supported yet
    NumberOfThreads: int = Field(alias="NumberOfThreads", default=None) # Not supported yet
    VortexWakeTimeStep: float = Field(alias="VortexWakeTimeStep", default=None) # Not supported yet
    WakeType: VortexLine_WakeTypeEnum = Field(alias="WakeType", default=None) # Not supported yet
    CoreGrowthModel: VortexLine_CoreGrowthModelEnum = Field(alias="CoreGrowthModel", default=None) # Not supported yet
    InitialVortexCoreSizeModel: VortexLine_InitialVortexCoreSizeModelEnum = Field(alias="InitialVortexCoreSizeModel", default=None) # Not supported yet
    FilamentStrain: bool = Field(alias="FilamentStrain", default=None) # Not supported yet
    LambOseenCoreGrowthConstant: float = Field(alias="LambOseenCoreGrowthConstant", default=None) # Not supported yet
    CoreGrowthConstant: float = Field(alias="CoreGrowthConstant", default=None) # Not supported yet
    RamasamyLeishmanConstant: float = Field(alias="RamasamyLeishmanConstant", default=None) # Not supported yet

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
        if isinstance(data, VortexLine):
            return data
        if not isinstance(data, dict):
            raise TypeError('An object is required to define VortexLine models')
        return VortexLine.parse_obj(data)


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
        candidate_fields = [x[1] for x in self.__dict__.items() if x[0] != 'AerodynamicModelType']
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
        VortexLine
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = VortexLine.from_file('/path/to/file')
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
        VortexLine
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = VortexLine.from_json('{ ... }')
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
        VortexLine
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


VortexLine.update_forward_refs()
