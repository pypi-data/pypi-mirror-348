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

from dnv_bladed_models.blade_stability_analysis_calculation import BladeStabilityAnalysisCalculation

from dnv_bladed_models.campbell_diagram_mode_of_operation import CampbellDiagramModeOfOperation

from dnv_bladed_models.campbell_diagram_mode_of_operation_insert import CampbellDiagramModeOfOperationInsert

from dnv_bladed_models.campbell_idling import CampbellIdling

from dnv_bladed_models.campbell_parked import CampbellParked

from dnv_bladed_models.campbell_power_production import CampbellPowerProduction



from .schema_helper import SchemaHelper 
from .models_impl import *

TCampbellDiagramModeOfOperationOptions = TypeVar('TCampbellDiagramModeOfOperationOptions', CampbellIdling, CampbellParked, CampbellPowerProduction, CampbellDiagramModeOfOperationInsert, CampbellDiagramModeOfOperation, )

class CampbellDiagram(BladeStabilityAnalysisCalculation):
    r"""
    Defines a calculation which produces a Campbell diagram, showing how the system response frequencies change with the rotor's rotational speed.
    
    Not supported yet.
    
    Attributes
    ----------
    SteadyCalculationType : Literal['CampbellDiagram'], default='CampbellDiagram', Not supported yet
        Defines the specific type of SteadyCalculation model in use.  For a `CampbellDiagram` object, this must always be set to a value of `CampbellDiagram`.
    
    ModeOfOperation : Union[CampbellIdling, CampbellParked, CampbellPowerProduction, CampbellDiagramModeOfOperationInsert], Not supported yet
    
    Notes
    -----
    This model is not supported yet by the Bladed calculation engine.
    """
    _relative_schema_path: str = PrivateAttr('SteadyCalculation/CampbellDiagram.json')

    SteadyCalculationType: Literal['CampbellDiagram'] = Field(alias="SteadyCalculationType", default='CampbellDiagram', allow_mutation=False, const=True) # Not supported yet
    ModeOfOperation: Union[CampbellIdling, CampbellParked, CampbellPowerProduction, CampbellDiagramModeOfOperationInsert] = Field(alias="ModeOfOperation", default=None, discriminator='CampbellDiagramModeOfOperationType') # Not supported yet

    class Config:
        extra = Extra.forbid
        validate_assignment = True
        allow_population_by_field_name = True
        pass


    @classmethod
    def parse_obj(cls: Type['Model'], obj: Any) -> 'Model':
        discriminated_props = [
            ('ModeOfOperation', 'CampbellDiagramModeOfOperationType'),
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
        if isinstance(data, CampbellDiagram):
            return data
        if not isinstance(data, dict):
            raise TypeError('An object is required to define CampbellDiagram models')
        return CampbellDiagram.parse_obj(data)


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
    def ModeOfOperation_as_CampbellIdling(self) -> CampbellIdling:
        """
        Retrieves the value of ModeOfOperation guaranteeing it is a CampbellIdling; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        CampbellIdling
            A model object, guaranteed to be a CampbellIdling.

        Raises
        ------
        TypeError
            If the value is not a CampbellIdling.
        """
        return self.ModeOfOperation_as(CampbellIdling)


    @property
    def ModeOfOperation_as_CampbellParked(self) -> CampbellParked:
        """
        Retrieves the value of ModeOfOperation guaranteeing it is a CampbellParked; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        CampbellParked
            A model object, guaranteed to be a CampbellParked.

        Raises
        ------
        TypeError
            If the value is not a CampbellParked.
        """
        return self.ModeOfOperation_as(CampbellParked)


    @property
    def ModeOfOperation_as_CampbellPowerProduction(self) -> CampbellPowerProduction:
        """
        Retrieves the value of ModeOfOperation guaranteeing it is a CampbellPowerProduction; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        CampbellPowerProduction
            A model object, guaranteed to be a CampbellPowerProduction.

        Raises
        ------
        TypeError
            If the value is not a CampbellPowerProduction.
        """
        return self.ModeOfOperation_as(CampbellPowerProduction)


    @property
    def ModeOfOperation_as_inline(self) -> Union[CampbellIdling, CampbellParked, CampbellPowerProduction]:
        """
        Retrieves the value of ModeOfOperation as a model object; if the value is specified with a '$insert', an error is raised.

        Returns
        -------
        Union[CampbellIdling, CampbellParked, CampbellPowerProduction]
            A model object at the specified index, guaranteed to not be a '$insert'.

        Raises
        ------
        TypeError
            If the value is not one of the concrete types of CampbellDiagramModeOfOperation; i.e. it is specified with a '$insert'.
        """
        if isinstance(self.ModeOfOperation, CampbellDiagramModeOfOperationInsert) or self.ModeOfOperation.is_insert:
            raise TypeError(f"Expected ModeOfOperation value to be an in-line object, but it is currently in the '$insert' state.")
        return self.ModeOfOperation


    def ModeOfOperation_as(self, cls: Type[TCampbellDiagramModeOfOperationOptions])-> TCampbellDiagramModeOfOperationOptions:
        """
        Retrieves the value of ModeOfOperation, ensuring it is of the specified type.
        The specified type must be one of the valid concrete types of CampbellDiagramModeOfOperation, or the '$insert' type
        (in the case the model is defined to be inserted from an external resource).

        Useful when using type-checking development tools, as it provides a concise way to access a value with the correct type.

        Parameters
        ----------
        cls: Type[Union[CampbellIdling, CampbellParked, CampbellPowerProduction, CampbellDiagramModeOfOperationInsert]]
            One of the valid concrete types of CampbellDiagramModeOfOperation, or the '$insert' type
            (in the case the model is defined to be inserted from an external resource).

        Returns
        -------
        TCampbellDiagramModeOfOperationOptions
            A model object of the specified type.

        Raises
        ------
        TypeError
            If the value is not of the specified type.

        Examples
        --------
        Get a reference to the value when it is one of the types of CampbellDiagramModeOfOperation:
        >>> val_obj = model_obj.ModeOfOperation_as(models.CampbellIdling)
        >>> val_obj = model_obj.ModeOfOperation_as(models.CampbellParked)
        >>> val_obj = model_obj.ModeOfOperation_as(models.CampbellPowerProduction)

        Get a reference to the value, when it was specified with a '$insert' and read in from a file:
        >>> insert_obj = model_obj.ModeOfOperation_as(models.CampbellDiagramModeOfOperationInsert)
        """
        if not isinstance(self.ModeOfOperation, cls):
            raise TypeError(f"Expected ModeOfOperation of type '{cls.__name__}' but was type '{type(self.ModeOfOperation).__name__}'")
        return self.ModeOfOperation



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
        CampbellDiagram
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = CampbellDiagram.from_file('/path/to/file')
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
        CampbellDiagram
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = CampbellDiagram.from_json('{ ... }')
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
        CampbellDiagram
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


CampbellDiagram.update_forward_refs()
