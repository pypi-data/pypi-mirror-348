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

from dnv_bladed_models.outputs import Outputs

from dnv_bladed_models.selected_component_output_group import SelectedComponentOutputGroup



from .schema_helper import SchemaHelper 
from .models_impl import *


class TimeDomainOutputs(Outputs):
    r"""
    The definition outputs to write for this simulation.
    
    Attributes
    ----------
    TimeStepForOutputs : float
        The output time step for the simulation.
    
    LengthOfOutputBuffer : float
        The length of time to buffer the output logs.
    
    OutputSummaryInformation : bool, default=True
        If true, the summary information output group will be created.
    
    OutputExternalControllers : bool, default=True
        If true, the controller output group will be created.
    
    OutputBuoyancyInformation : bool, default=False
        If true, the buoyancy output group will be created.
    
    OutputFiniteElementMatrices : bool, default=False
        If true, the finite element output group will be created, providing far more detail about the finite element matrices.
    
    OutputSignalProperties : bool, default=False
        If true, the signal properties output group will be created.  This records the properties provided to the controller, with and without noise and other distortions.
    
    OutputWakePropagation : bool, default=False
        If true, the eddy viscosity propagation of the wake is output as a 2D table of relative velocity against radial position and distance traveled to a \".wake\" file in the output folder.
    
    OutputSoftwarePerformance : bool, default=False
        If true, the software performance output group will be created.
    
    OutputStateInformation : bool, default=False
        If true, the integrator state output group will be created.  This can be used to help understand how efficiently the integrator is coping with the simulation.
    
    OutputExternalControllerExchangeObject : bool, default=False
        If true, this will output all of the values contained in the external controller interface before and after each external controller call.  This is intended to assist debugging external controllers.
    
    OutputExternalControllerLegacySwapArray : bool, default=False
        If true, the contents of the swap array passed to a legacy controller will be logged.  This is used only when trying to debug legacy controllers, and will not produce useful results if there is more than one legacy controller being run.
    
    SelectedComponentOutputGroups : List[SelectedComponentOutputGroup], Not supported yet
        A list of references to the OutputGroup of specific components to output.  This allows the outputs of individual components to be switched off, or chosen from an available list of output regimes.  If a component is not mentioned, it will produce outputs according to its default output group, if there is one available.
    
    Notes
    -----
    
    """
    _relative_schema_path: str = PrivateAttr('TimeDomainSimulation/TimeDomainOutputs/TimeDomainOutputs.json')

    TimeStepForOutputs: float = Field(alias="TimeStepForOutputs", default=None)
    LengthOfOutputBuffer: float = Field(alias="LengthOfOutputBuffer", default=None)
    OutputSummaryInformation: bool = Field(alias="OutputSummaryInformation", default=None)
    OutputExternalControllers: bool = Field(alias="OutputExternalControllers", default=None)
    OutputBuoyancyInformation: bool = Field(alias="OutputBuoyancyInformation", default=None)
    OutputFiniteElementMatrices: bool = Field(alias="OutputFiniteElementMatrices", default=None)
    OutputSignalProperties: bool = Field(alias="OutputSignalProperties", default=None)
    OutputWakePropagation: bool = Field(alias="OutputWakePropagation", default=None)
    OutputSoftwarePerformance: bool = Field(alias="OutputSoftwarePerformance", default=None)
    OutputStateInformation: bool = Field(alias="OutputStateInformation", default=None)
    OutputExternalControllerExchangeObject: bool = Field(alias="OutputExternalControllerExchangeObject", default=None)
    OutputExternalControllerLegacySwapArray: bool = Field(alias="OutputExternalControllerLegacySwapArray", default=None)
    SelectedComponentOutputGroups: List[SelectedComponentOutputGroup] = Field(alias="SelectedComponentOutputGroups", default=list()) # Not supported yet

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
        if isinstance(data, TimeDomainOutputs):
            return data
        if not isinstance(data, dict):
            raise TypeError('An object is required to define TimeDomainOutputs models')
        return TimeDomainOutputs.parse_obj(data)


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
        if self.SelectedComponentOutputGroups is not None and len(self.SelectedComponentOutputGroups) == 0: #type: ignore
            unused_containers.add('SelectedComponentOutputGroups')
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
        TimeDomainOutputs
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = TimeDomainOutputs.from_file('/path/to/file')
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
        TimeDomainOutputs
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = TimeDomainOutputs.from_json('{ ... }')
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
        TimeDomainOutputs
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


TimeDomainOutputs.update_forward_refs()
