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

from dnv_bladed_models.accelerometer import Accelerometer

from dnv_bladed_models.aerodynamic_properties import AerodynamicProperties

from dnv_bladed_models.bladed_model import BladedModel

from dnv_bladed_models.coordinate_systems import CoordinateSystems

from dnv_bladed_models.inclinometer import Inclinometer

from dnv_bladed_models.load_sensor import LoadSensor

from dnv_bladed_models.mass_properties import MassProperties

from dnv_bladed_models.sensor import Sensor

from dnv_bladed_models.sensor_insert import SensorInsert

from dnv_bladed_models.stiffness_properties import StiffnessProperties



from .schema_helper import SchemaHelper 
from .models_impl import *

TSensorOptions = TypeVar('TSensorOptions', Accelerometer, Inclinometer, LoadSensor, SensorInsert, Sensor, )

class CrossSection(BladedModel):
    r"""
    A blade cross-section which defines the geometric, structural, and aerodynamic properties of the blade.
    
    Attributes
    ----------
    IsCrossSectionAMultipartBoundary : bool, default=False
        If true, this cross-section will serve as a boundary between parts of a multipart blade, allowing the blade to be split accordingly. Note that it is not possible to split the blade at the first or last cross-section of the blade.
    
    CoordinateSystems : CoordinateSystems
    
    StiffnessProperties : StiffnessProperties
    
    AerodynamicProperties : AerodynamicProperties
    
    MassProperties : MassProperties
    
    Sensors : List[Union[Accelerometer, Inclinometer, LoadSensor, SensorInsert]]
        A list of sensors that the external controller has access to.  The indices of the sensors will depend on their type (LoadSensor, Accelerometer, or Inclinometer) and the order in which they are defined on the Blade, from inboard to outpurd.  The details of exactly where the sensors are will be unavailable if the component is encrypted.
    
    Notes
    -----
    
    """
    _relative_schema_path: str = PrivateAttr('Components/Blade/CrossSection/CrossSection.json')

    IsCrossSectionAMultipartBoundary: bool = Field(alias="IsCrossSectionAMultipartBoundary", default=None)
    CoordinateSystems: CoordinateSystems = Field(alias="CoordinateSystems", default=None)
    StiffnessProperties: StiffnessProperties = Field(alias="StiffnessProperties", default=None)
    AerodynamicProperties: AerodynamicProperties = Field(alias="AerodynamicProperties", default=None)
    MassProperties: MassProperties = Field(alias="MassProperties", default=None)
    Sensors: List[Annotated[Union[Accelerometer, Inclinometer, LoadSensor, SensorInsert], Field(discriminator='SensorType')]] = Field(alias="Sensors", default=list())

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
            ('Sensors', 'SensorType'),
        ]
        prepare_model_dict(cls, obj, discriminated_props, discriminated_arrays)
        return super().parse_obj(obj)


    @classmethod
    def __get_validators__(cls):
        yield cls._factory


    @classmethod
    def _factory(cls, data):
        if isinstance(data, CrossSection):
            return data
        if not isinstance(data, dict):
            raise TypeError('An object is required to define CrossSection models')
        return CrossSection.parse_obj(data)


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
    def Sensors_as_inline(self) -> Iterable[Union[Accelerometer, Inclinometer, LoadSensor]]:
        """
        Retrieves the value of Sensors as an iterable of model objects; if any of the values are specified with a '$insert', an error is raised.

        Returns
        -------
        Iterable[Union[Accelerometer, Inclinometer, LoadSensor]]
            A list of model objects, guaranteed to not be a '$insert'.

        Raises
        ------
        TypeError
            If any of the values are not one of the concrete types of Sensor; i.e. they are specified with an 'insert'.

        Examples
        --------
        >>> for i, Sensor_obj in enumerate(obj.Sensors_as_any):
                print(f"Element {i} is of type Sensor_obj.SensorType}")

        or

        >>> for Sensor_obj in obj.Sensors_as_any:
                # process object
        """
        for val in self.Sensors:
            if isinstance(val, SensorInsert) or val.is_insert == True:
                raise TypeError(f"Expected element value to be an in-line object, but it is currently in the '$insert' state.")
            yield val


    def Sensors_element_as_Accelerometer(self, index: int) -> Accelerometer:
        """
        Retrieves an object from the Sensors array field, ensuring it is a Accelerometer.        

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        Returns
        -------
        Accelerometer
            A model object at the specified index, guaranteed to be a Accelerometer.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the value at the specified index is not a Accelerometer.

        Examples
        --------
        Gets a reference to the 2nd element, typed to a Accelerometer, that is specified in-line:
        >>> entry_obj = obj.Sensors_element_as_Accelerometer(2)
        """
        return self.Sensors_element_as(index, Accelerometer)


    def Sensors_element_as_Inclinometer(self, index: int) -> Inclinometer:
        """
        Retrieves an object from the Sensors array field, ensuring it is a Inclinometer.        

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        Returns
        -------
        Inclinometer
            A model object at the specified index, guaranteed to be a Inclinometer.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the value at the specified index is not a Inclinometer.

        Examples
        --------
        Gets a reference to the 2nd element, typed to a Inclinometer, that is specified in-line:
        >>> entry_obj = obj.Sensors_element_as_Inclinometer(2)
        """
        return self.Sensors_element_as(index, Inclinometer)


    def Sensors_element_as_LoadSensor(self, index: int) -> LoadSensor:
        """
        Retrieves an object from the Sensors array field, ensuring it is a LoadSensor.        

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        Returns
        -------
        LoadSensor
            A model object at the specified index, guaranteed to be a LoadSensor.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the value at the specified index is not a LoadSensor.

        Examples
        --------
        Gets a reference to the 2nd element, typed to a LoadSensor, that is specified in-line:
        >>> entry_obj = obj.Sensors_element_as_LoadSensor(2)
        """
        return self.Sensors_element_as(index, LoadSensor)


    def Sensors_element_as_inline(self, index: int) -> Union[Accelerometer, Inclinometer, LoadSensor]:
        """
        Retrieves an object from the Sensors array field; if the value is specified with a '$insert', an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        Returns
        -------
        Union[Accelerometer, Inclinometer, LoadSensor]
            A model object at the specified index, guaranteed to not be an '$insert'.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the value at the specified index is not one of the concrete types of Sensor; i.e. it is specified with an '$insert'.

        Examples
        --------
        Get a reference to the 2nd element, as any of the concrete types:
        >>> Sensors_obj = obj.Sensors_element_as_inline(2)
        """
        val = self.Sensors[index]
        if isinstance(val, SensorInsert) or val.is_insert == True:
            raise TypeError(f"Expected element value at '{index}' to be an in-line object, but it is currently in the '$insert' state.")
        return val


    def Sensors_element_as(self, index: int, element_cls: Type[TSensorOptions]) -> TSensorOptions:
        """
        Retrieves an object from the Sensors array field, ensuring it is of the specified type.
        The specified type must be one of the valid concrete types of Sensor, or the '$insert' type
        (in the case the model is defined to be inserted from an external resource).

        Useful when using type-checking development tools, as it provides a concise way to access a value with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        element_cls: Type[Union[Accelerometer, Inclinometer, LoadSensor, SensorInsert]]
            One of the valid concrete types of Sensor, or the '$insert' type
            (in the case the model is defined to be inserted from an external resource).

        Returns
        -------
        TSensorOptions
            A model object of the specified type.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the model object for the specified index is not of the specified type.

        Examples
        --------
        Get a reference to the 2nd element when it was one of the types of Sensor:
        >>> entry_obj = obj.Sensors_element_as(2, models.Accelerometer)
        >>> entry_obj = obj.Sensors_element_as(2, models.Inclinometer)
        >>> entry_obj = obj.Sensors_element_as(2, models.LoadSensor)

        Get a reference to the value, when it was specified with a '$insert' and read in from a file:
        >>> insert_obj = obj.Sensors_element_as(2, models.SensorInsert)
        """
        val = self.Sensors[index]
        if not isinstance(val, element_cls):
            raise TypeError(f"Expected value of type '{element_cls.__name__}' at index {index} but found type '{type(val).__name__}'")
        return val



    def _find_unused_containers(self) -> Set[str]:
        unused_containers: Set[str] = super()._find_unused_containers()
        if self.Sensors is not None and len(self.Sensors) == 0: #type: ignore
            unused_containers.add('Sensors')
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
        CrossSection
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = CrossSection.from_file('/path/to/file')
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
        CrossSection
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = CrossSection.from_json('{ ... }')
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
        CrossSection
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


CrossSection.update_forward_refs()
