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

from dnv_bladed_models.blade_aerodynamic_outputs import BladeAerodynamicOutputs

from dnv_bladed_models.blade_hydrodynamic_outputs import BladeHydrodynamicOutputs

from dnv_bladed_models.blade_load_outputs import BladeLoadOutputs

from dnv_bladed_models.blade_motion_outputs import BladeMotionOutputs

from dnv_bladed_models.blade_outputs_for_cross_section import BladeOutputsForCrossSection

from dnv_bladed_models.blade_outputs_for_location import BladeOutputsForLocation

from dnv_bladed_models.blade_outputs_for_location_insert import BladeOutputsForLocationInsert

from dnv_bladed_models.blade_outputs_for_position import BladeOutputsForPosition

from dnv_bladed_models.bladed_model import BladedModel

from dnv_bladed_models.xml_blade_outputs import XMLBladeOutputs



from .schema_helper import SchemaHelper 
from .models_impl import *

TBladeOutputsForLocationOptions = TypeVar('TBladeOutputsForLocationOptions', BladeOutputsForCrossSection, BladeOutputsForPosition, BladeOutputsForLocationInsert, BladeOutputsForLocation, )

class BladeOutputGroup(BladedModel):
    r"""
    An output group definition for the blade.
    
    Not supported yet.
    
    Attributes
    ----------
    XML : XMLBladeOutputs, Not supported yet
    
    LoadOutputs : BladeLoadOutputs, Not supported yet
    
    MotionOutputs : BladeMotionOutputs, Not supported yet
    
    AerodynamicOutputs : BladeAerodynamicOutputs, Not supported yet
    
    HydrodynamicOutputs : BladeHydrodynamicOutputs, Not supported yet
    
    OutputLocations : List[Union[BladeOutputsForCrossSection, BladeOutputsForPosition, BladeOutputsForLocationInsert]], Not supported yet
        List of BladeOutputsForLocation, originally enumerated by Fortran.OUTPUT.AEROD_NSTS
    
    Notes
    -----
    This model is not supported yet by the Bladed calculation engine.
    """
    _relative_schema_path: str = PrivateAttr('Components/Blade/BladeOutputGroupLibrary/BladeOutputGroup/BladeOutputGroup.json')

    XML: XMLBladeOutputs = Field(alias="XML", default=None) # Not supported yet
    LoadOutputs: BladeLoadOutputs = Field(alias="LoadOutputs", default=None) # Not supported yet
    MotionOutputs: BladeMotionOutputs = Field(alias="MotionOutputs", default=None) # Not supported yet
    AerodynamicOutputs: BladeAerodynamicOutputs = Field(alias="AerodynamicOutputs", default=None) # Not supported yet
    HydrodynamicOutputs: BladeHydrodynamicOutputs = Field(alias="HydrodynamicOutputs", default=None) # Not supported yet
    OutputLocations: List[Annotated[Union[BladeOutputsForCrossSection, BladeOutputsForPosition, BladeOutputsForLocationInsert], Field(discriminator='BladeOutputsForLocationType')]] = Field(alias="OutputLocations", default=list()) # Not supported yet

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
            ('OutputLocations', 'BladeOutputsForLocationType'),
        ]
        prepare_model_dict(cls, obj, discriminated_props, discriminated_arrays)
        return super().parse_obj(obj)


    @classmethod
    def __get_validators__(cls):
        yield cls._factory


    @classmethod
    def _factory(cls, data):
        if isinstance(data, BladeOutputGroup):
            return data
        if not isinstance(data, dict):
            raise TypeError('An object is required to define BladeOutputGroup models')
        return BladeOutputGroup.parse_obj(data)


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
    def OutputLocations_as_inline(self) -> Iterable[Union[BladeOutputsForCrossSection, BladeOutputsForPosition]]:
        """
        Retrieves the value of OutputLocations as an iterable of model objects; if any of the values are specified with a '$insert', an error is raised.

        Returns
        -------
        Iterable[Union[BladeOutputsForCrossSection, BladeOutputsForPosition]]
            A list of model objects, guaranteed to not be a '$insert'.

        Raises
        ------
        TypeError
            If any of the values are not one of the concrete types of BladeOutputsForLocation; i.e. they are specified with an 'insert'.

        Examples
        --------
        >>> for i, BladeOutputsForLocation_obj in enumerate(obj.OutputLocations_as_any):
                print(f"Element {i} is of type BladeOutputsForLocation_obj.BladeOutputsForLocationType}")

        or

        >>> for BladeOutputsForLocation_obj in obj.OutputLocations_as_any:
                # process object
        """
        for val in self.OutputLocations:
            if isinstance(val, BladeOutputsForLocationInsert) or val.is_insert == True:
                raise TypeError(f"Expected element value to be an in-line object, but it is currently in the '$insert' state.")
            yield val


    def OutputLocations_element_as_BladeOutputsForCrossSection(self, index: int) -> BladeOutputsForCrossSection:
        """
        Retrieves an object from the OutputLocations array field, ensuring it is a BladeOutputsForCrossSection.        

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        Returns
        -------
        BladeOutputsForCrossSection
            A model object at the specified index, guaranteed to be a BladeOutputsForCrossSection.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the value at the specified index is not a BladeOutputsForCrossSection.

        Examples
        --------
        Gets a reference to the 2nd element, typed to a BladeOutputsForCrossSection, that is specified in-line:
        >>> entry_obj = obj.OutputLocations_element_as_BladeOutputsForCrossSection(2)
        """
        return self.OutputLocations_element_as(index, BladeOutputsForCrossSection)


    def OutputLocations_element_as_BladeOutputsForPosition(self, index: int) -> BladeOutputsForPosition:
        """
        Retrieves an object from the OutputLocations array field, ensuring it is a BladeOutputsForPosition.        

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        Returns
        -------
        BladeOutputsForPosition
            A model object at the specified index, guaranteed to be a BladeOutputsForPosition.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the value at the specified index is not a BladeOutputsForPosition.

        Examples
        --------
        Gets a reference to the 2nd element, typed to a BladeOutputsForPosition, that is specified in-line:
        >>> entry_obj = obj.OutputLocations_element_as_BladeOutputsForPosition(2)
        """
        return self.OutputLocations_element_as(index, BladeOutputsForPosition)


    def OutputLocations_element_as_inline(self, index: int) -> Union[BladeOutputsForCrossSection, BladeOutputsForPosition]:
        """
        Retrieves an object from the OutputLocations array field; if the value is specified with a '$insert', an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        Returns
        -------
        Union[BladeOutputsForCrossSection, BladeOutputsForPosition]
            A model object at the specified index, guaranteed to not be an '$insert'.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the value at the specified index is not one of the concrete types of BladeOutputsForLocation; i.e. it is specified with an '$insert'.

        Examples
        --------
        Get a reference to the 2nd element, as any of the concrete types:
        >>> OutputLocations_obj = obj.OutputLocations_element_as_inline(2)
        """
        val = self.OutputLocations[index]
        if isinstance(val, BladeOutputsForLocationInsert) or val.is_insert == True:
            raise TypeError(f"Expected element value at '{index}' to be an in-line object, but it is currently in the '$insert' state.")
        return val


    def OutputLocations_element_as(self, index: int, element_cls: Type[TBladeOutputsForLocationOptions]) -> TBladeOutputsForLocationOptions:
        """
        Retrieves an object from the OutputLocations array field, ensuring it is of the specified type.
        The specified type must be one of the valid concrete types of BladeOutputsForLocation, or the '$insert' type
        (in the case the model is defined to be inserted from an external resource).

        Useful when using type-checking development tools, as it provides a concise way to access a value with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        element_cls: Type[Union[BladeOutputsForCrossSection, BladeOutputsForPosition, BladeOutputsForLocationInsert]]
            One of the valid concrete types of BladeOutputsForLocation, or the '$insert' type
            (in the case the model is defined to be inserted from an external resource).

        Returns
        -------
        TBladeOutputsForLocationOptions
            A model object of the specified type.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the model object for the specified index is not of the specified type.

        Examples
        --------
        Get a reference to the 2nd element when it was one of the types of BladeOutputsForLocation:
        >>> entry_obj = obj.OutputLocations_element_as(2, models.BladeOutputsForCrossSection)
        >>> entry_obj = obj.OutputLocations_element_as(2, models.BladeOutputsForPosition)

        Get a reference to the value, when it was specified with a '$insert' and read in from a file:
        >>> insert_obj = obj.OutputLocations_element_as(2, models.BladeOutputsForLocationInsert)
        """
        val = self.OutputLocations[index]
        if not isinstance(val, element_cls):
            raise TypeError(f"Expected value of type '{element_cls.__name__}' at index {index} but found type '{type(val).__name__}'")
        return val



    def _find_unused_containers(self) -> Set[str]:
        unused_containers: Set[str] = super()._find_unused_containers()
        if self.OutputLocations is not None and len(self.OutputLocations) == 0: #type: ignore
            unused_containers.add('OutputLocations')
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
        BladeOutputGroup
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = BladeOutputGroup.from_file('/path/to/file')
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
        BladeOutputGroup
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = BladeOutputGroup.from_json('{ ... }')
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
        BladeOutputGroup
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


BladeOutputGroup.update_forward_refs()
