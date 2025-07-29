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

from dnv_bladed_models.brake import Brake

from dnv_bladed_models.brake_insert import BrakeInsert

from dnv_bladed_models.component import Component

from dnv_bladed_models.drivetrain_and_nacelle_mass_properties import DrivetrainAndNacelleMassProperties

from dnv_bladed_models.drivetrain_connectable_nodes import DrivetrainConnectableNodes

from dnv_bladed_models.drivetrain_output_group_library import DrivetrainOutputGroupLibrary

from dnv_bladed_models.high_speed_shaft_flexibility import HighSpeedShaftFlexibility

from dnv_bladed_models.low_speed_shaft import LowSpeedShaft

from dnv_bladed_models.mechanical_losses import MechanicalLosses

from dnv_bladed_models.nacelle_accelerometer import NacelleAccelerometer

from dnv_bladed_models.nacelle_cover import NacelleCover

from dnv_bladed_models.nacelle_inclinometer import NacelleInclinometer

from dnv_bladed_models.nacelle_sensor import NacelleSensor

from dnv_bladed_models.nacelle_sensor_insert import NacelleSensorInsert

from dnv_bladed_models.non_linear_shaft_brake import NonLinearShaftBrake

from dnv_bladed_models.pallet_mounting_flexibility import PalletMountingFlexibility

from dnv_bladed_models.position_of_hub_centre import PositionOfHubCentre

from dnv_bladed_models.simple_shaft_brake import SimpleShaftBrake

from dnv_bladed_models.slipping_clutch import SlippingClutch



from .schema_helper import SchemaHelper 
from .models_impl import *

TNacelleSensorOptions = TypeVar('TNacelleSensorOptions', NacelleAccelerometer, NacelleInclinometer, NacelleSensorInsert, NacelleSensor, )
TBrakeOptions = TypeVar('TBrakeOptions', NonLinearShaftBrake, SimpleShaftBrake, BrakeInsert, Brake, )

class DrivetrainAndNacelle(Component):
    r"""
    A drivetrain component.  This includes the gearbox; all shafts and brakes right up to the hub centre; the mainframe of the nacelle; all fairings and ancilliary items on the nacelle.  It excludes the generator.
    
    Attributes
    ----------
    ComponentType : Literal['DrivetrainAndNacelle'], default='DrivetrainAndNacelle'
        Defines the specific type of Component model in use.  For a `DrivetrainAndNacelle` object, this must always be set to a value of `DrivetrainAndNacelle`.
    
    PositionOfHubCentre : PositionOfHubCentre
    
    NacelleCover : NacelleCover
    
    MassProperties : DrivetrainAndNacelleMassProperties
    
    Sensors : List[Union[NacelleAccelerometer, NacelleInclinometer, NacelleSensorInsert]]
        A list of sensors that the controller has access to.
    
    ShaftBrakes : List[Union[NonLinearShaftBrake, SimpleShaftBrake, BrakeInsert]]
        Definitions for the brakes on the various shafts of the drivetrain.
    
    GearboxRatio : float
        The ratio of the high speed shaft (connected to the generator) to the low speed shaft (connected to the hub). Negative values cause the low-speed shaft and high-speed shaft to rotate in opposite directions.
    
    GearboxInertia : float
        The total rotational inertia of the gearbox, referred to the high speed side.
    
    SlippingClutch : SlippingClutch
    
    HighSpeedShaftTorsion : HighSpeedShaftFlexibility
    
    MountingFlexibility : PalletMountingFlexibility
    
    LowSpeedShaft : LowSpeedShaft
    
    Losses : MechanicalLosses
    
    OutputGroups : DrivetrainOutputGroupLibrary, Not supported yet
    
    ConnectableNodes : DrivetrainConnectableNodes, Not supported yet
    
    Notes
    -----
    
    """
    _relative_schema_path: str = PrivateAttr('Components/DrivetrainAndNacelle/DrivetrainAndNacelle.json')

    ComponentType: Literal['DrivetrainAndNacelle'] = Field(alias="ComponentType", default='DrivetrainAndNacelle', allow_mutation=False, const=True)
    PositionOfHubCentre: PositionOfHubCentre = Field(alias="PositionOfHubCentre", default=None)
    NacelleCover: NacelleCover = Field(alias="NacelleCover", default=None)
    MassProperties: DrivetrainAndNacelleMassProperties = Field(alias="MassProperties", default=None)
    Sensors: List[Annotated[Union[NacelleAccelerometer, NacelleInclinometer, NacelleSensorInsert], Field(discriminator='NacelleSensorType')]] = Field(alias="Sensors", default=list())
    ShaftBrakes: List[Annotated[Union[NonLinearShaftBrake, SimpleShaftBrake, BrakeInsert], Field(discriminator='BrakeType')]] = Field(alias="ShaftBrakes", default=list())
    GearboxRatio: float = Field(alias="GearboxRatio", default=None)
    GearboxInertia: float = Field(alias="GearboxInertia", default=None)
    SlippingClutch: SlippingClutch = Field(alias="SlippingClutch", default=None)
    HighSpeedShaftTorsion: HighSpeedShaftFlexibility = Field(alias="HighSpeedShaftTorsion", default=None)
    MountingFlexibility: PalletMountingFlexibility = Field(alias="MountingFlexibility", default=None)
    LowSpeedShaft: LowSpeedShaft = Field(alias="LowSpeedShaft", default=None)
    Losses: MechanicalLosses = Field(alias="Losses", default=None)
    OutputGroups: DrivetrainOutputGroupLibrary = Field(alias="OutputGroups", default=DrivetrainOutputGroupLibrary()) # Not supported yet
    ConnectableNodes: DrivetrainConnectableNodes = Field(alias="ConnectableNodes", default=DrivetrainConnectableNodes()) # Not supported yet

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
            ('Sensors', 'NacelleSensorType'),
            ('ShaftBrakes', 'BrakeType'),
        ]
        prepare_model_dict(cls, obj, discriminated_props, discriminated_arrays)
        return super().parse_obj(obj)


    @classmethod
    def __get_validators__(cls):
        yield cls._factory


    @classmethod
    def _factory(cls, data):
        if isinstance(data, DrivetrainAndNacelle):
            return data
        if not isinstance(data, dict):
            raise TypeError('An object is required to define DrivetrainAndNacelle models')
        return DrivetrainAndNacelle.parse_obj(data)


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
    def Sensors_as_inline(self) -> Iterable[Union[NacelleAccelerometer, NacelleInclinometer]]:
        """
        Retrieves the value of Sensors as an iterable of model objects; if any of the values are specified with a '$insert', an error is raised.

        Returns
        -------
        Iterable[Union[NacelleAccelerometer, NacelleInclinometer]]
            A list of model objects, guaranteed to not be a '$insert'.

        Raises
        ------
        TypeError
            If any of the values are not one of the concrete types of NacelleSensor; i.e. they are specified with an 'insert'.

        Examples
        --------
        >>> for i, NacelleSensor_obj in enumerate(obj.Sensors_as_any):
                print(f"Element {i} is of type NacelleSensor_obj.NacelleSensorType}")

        or

        >>> for NacelleSensor_obj in obj.Sensors_as_any:
                # process object
        """
        for val in self.Sensors:
            if isinstance(val, NacelleSensorInsert) or val.is_insert == True:
                raise TypeError(f"Expected element value to be an in-line object, but it is currently in the '$insert' state.")
            yield val


    def Sensors_element_as_NacelleAccelerometer(self, index: int) -> NacelleAccelerometer:
        """
        Retrieves an object from the Sensors array field, ensuring it is a NacelleAccelerometer.        

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        Returns
        -------
        NacelleAccelerometer
            A model object at the specified index, guaranteed to be a NacelleAccelerometer.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the value at the specified index is not a NacelleAccelerometer.

        Examples
        --------
        Gets a reference to the 2nd element, typed to a NacelleAccelerometer, that is specified in-line:
        >>> entry_obj = obj.Sensors_element_as_NacelleAccelerometer(2)
        """
        return self.Sensors_element_as(index, NacelleAccelerometer)


    def Sensors_element_as_NacelleInclinometer(self, index: int) -> NacelleInclinometer:
        """
        Retrieves an object from the Sensors array field, ensuring it is a NacelleInclinometer.        

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        Returns
        -------
        NacelleInclinometer
            A model object at the specified index, guaranteed to be a NacelleInclinometer.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the value at the specified index is not a NacelleInclinometer.

        Examples
        --------
        Gets a reference to the 2nd element, typed to a NacelleInclinometer, that is specified in-line:
        >>> entry_obj = obj.Sensors_element_as_NacelleInclinometer(2)
        """
        return self.Sensors_element_as(index, NacelleInclinometer)


    def Sensors_element_as_inline(self, index: int) -> Union[NacelleAccelerometer, NacelleInclinometer]:
        """
        Retrieves an object from the Sensors array field; if the value is specified with a '$insert', an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        Returns
        -------
        Union[NacelleAccelerometer, NacelleInclinometer]
            A model object at the specified index, guaranteed to not be an '$insert'.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the value at the specified index is not one of the concrete types of NacelleSensor; i.e. it is specified with an '$insert'.

        Examples
        --------
        Get a reference to the 2nd element, as any of the concrete types:
        >>> Sensors_obj = obj.Sensors_element_as_inline(2)
        """
        val = self.Sensors[index]
        if isinstance(val, NacelleSensorInsert) or val.is_insert == True:
            raise TypeError(f"Expected element value at '{index}' to be an in-line object, but it is currently in the '$insert' state.")
        return val


    def Sensors_element_as(self, index: int, element_cls: Type[TNacelleSensorOptions]) -> TNacelleSensorOptions:
        """
        Retrieves an object from the Sensors array field, ensuring it is of the specified type.
        The specified type must be one of the valid concrete types of NacelleSensor, or the '$insert' type
        (in the case the model is defined to be inserted from an external resource).

        Useful when using type-checking development tools, as it provides a concise way to access a value with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        element_cls: Type[Union[NacelleAccelerometer, NacelleInclinometer, NacelleSensorInsert]]
            One of the valid concrete types of NacelleSensor, or the '$insert' type
            (in the case the model is defined to be inserted from an external resource).

        Returns
        -------
        TNacelleSensorOptions
            A model object of the specified type.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the model object for the specified index is not of the specified type.

        Examples
        --------
        Get a reference to the 2nd element when it was one of the types of NacelleSensor:
        >>> entry_obj = obj.Sensors_element_as(2, models.NacelleAccelerometer)
        >>> entry_obj = obj.Sensors_element_as(2, models.NacelleInclinometer)

        Get a reference to the value, when it was specified with a '$insert' and read in from a file:
        >>> insert_obj = obj.Sensors_element_as(2, models.NacelleSensorInsert)
        """
        val = self.Sensors[index]
        if not isinstance(val, element_cls):
            raise TypeError(f"Expected value of type '{element_cls.__name__}' at index {index} but found type '{type(val).__name__}'")
        return val


    @property
    def ShaftBrakes_as_inline(self) -> Iterable[Union[NonLinearShaftBrake, SimpleShaftBrake]]:
        """
        Retrieves the value of ShaftBrakes as an iterable of model objects; if any of the values are specified with a '$insert', an error is raised.

        Returns
        -------
        Iterable[Union[NonLinearShaftBrake, SimpleShaftBrake]]
            A list of model objects, guaranteed to not be a '$insert'.

        Raises
        ------
        TypeError
            If any of the values are not one of the concrete types of Brake; i.e. they are specified with an 'insert'.

        Examples
        --------
        >>> for i, Brake_obj in enumerate(obj.ShaftBrakes_as_any):
                print(f"Element {i} is of type Brake_obj.BrakeType}")

        or

        >>> for Brake_obj in obj.ShaftBrakes_as_any:
                # process object
        """
        for val in self.ShaftBrakes:
            if isinstance(val, BrakeInsert) or val.is_insert == True:
                raise TypeError(f"Expected element value to be an in-line object, but it is currently in the '$insert' state.")
            yield val


    def ShaftBrakes_element_as_NonLinearShaftBrake(self, index: int) -> NonLinearShaftBrake:
        """
        Retrieves an object from the ShaftBrakes array field, ensuring it is a NonLinearShaftBrake.        

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        Returns
        -------
        NonLinearShaftBrake
            A model object at the specified index, guaranteed to be a NonLinearShaftBrake.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the value at the specified index is not a NonLinearShaftBrake.

        Examples
        --------
        Gets a reference to the 2nd element, typed to a NonLinearShaftBrake, that is specified in-line:
        >>> entry_obj = obj.ShaftBrakes_element_as_NonLinearShaftBrake(2)
        """
        return self.ShaftBrakes_element_as(index, NonLinearShaftBrake)


    def ShaftBrakes_element_as_SimpleShaftBrake(self, index: int) -> SimpleShaftBrake:
        """
        Retrieves an object from the ShaftBrakes array field, ensuring it is a SimpleShaftBrake.        

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        Returns
        -------
        SimpleShaftBrake
            A model object at the specified index, guaranteed to be a SimpleShaftBrake.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the value at the specified index is not a SimpleShaftBrake.

        Examples
        --------
        Gets a reference to the 2nd element, typed to a SimpleShaftBrake, that is specified in-line:
        >>> entry_obj = obj.ShaftBrakes_element_as_SimpleShaftBrake(2)
        """
        return self.ShaftBrakes_element_as(index, SimpleShaftBrake)


    def ShaftBrakes_element_as_inline(self, index: int) -> Union[NonLinearShaftBrake, SimpleShaftBrake]:
        """
        Retrieves an object from the ShaftBrakes array field; if the value is specified with a '$insert', an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        Returns
        -------
        Union[NonLinearShaftBrake, SimpleShaftBrake]
            A model object at the specified index, guaranteed to not be an '$insert'.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the value at the specified index is not one of the concrete types of Brake; i.e. it is specified with an '$insert'.

        Examples
        --------
        Get a reference to the 2nd element, as any of the concrete types:
        >>> ShaftBrakes_obj = obj.ShaftBrakes_element_as_inline(2)
        """
        val = self.ShaftBrakes[index]
        if isinstance(val, BrakeInsert) or val.is_insert == True:
            raise TypeError(f"Expected element value at '{index}' to be an in-line object, but it is currently in the '$insert' state.")
        return val


    def ShaftBrakes_element_as(self, index: int, element_cls: Type[TBrakeOptions]) -> TBrakeOptions:
        """
        Retrieves an object from the ShaftBrakes array field, ensuring it is of the specified type.
        The specified type must be one of the valid concrete types of Brake, or the '$insert' type
        (in the case the model is defined to be inserted from an external resource).

        Useful when using type-checking development tools, as it provides a concise way to access a value with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        element_cls: Type[Union[NonLinearShaftBrake, SimpleShaftBrake, BrakeInsert]]
            One of the valid concrete types of Brake, or the '$insert' type
            (in the case the model is defined to be inserted from an external resource).

        Returns
        -------
        TBrakeOptions
            A model object of the specified type.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the model object for the specified index is not of the specified type.

        Examples
        --------
        Get a reference to the 2nd element when it was one of the types of Brake:
        >>> entry_obj = obj.ShaftBrakes_element_as(2, models.NonLinearShaftBrake)
        >>> entry_obj = obj.ShaftBrakes_element_as(2, models.SimpleShaftBrake)

        Get a reference to the value, when it was specified with a '$insert' and read in from a file:
        >>> insert_obj = obj.ShaftBrakes_element_as(2, models.BrakeInsert)
        """
        val = self.ShaftBrakes[index]
        if not isinstance(val, element_cls):
            raise TypeError(f"Expected value of type '{element_cls.__name__}' at index {index} but found type '{type(val).__name__}'")
        return val



    def _find_unused_containers(self) -> Set[str]:
        unused_containers: Set[str] = super()._find_unused_containers()
        if self.Sensors is not None and len(self.Sensors) == 0: #type: ignore
            unused_containers.add('Sensors')
        if self.ShaftBrakes is not None and len(self.ShaftBrakes) == 0: #type: ignore
            unused_containers.add('ShaftBrakes')
        if self.OutputGroups._is_unused():
            unused_containers.add('OutputGroups')
        if self.ConnectableNodes._is_unused():
            unused_containers.add('ConnectableNodes')
        return unused_containers


    def _is_unused(self) -> bool:
        """
        Returns true if the model has no user-supplied values. This indicates the object should not be rendered in the final JSON output.
        """
        candidate_fields = [x[1] for x in self.__dict__.items() if x[0] != 'ComponentType']
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
        DrivetrainAndNacelle
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = DrivetrainAndNacelle.from_file('/path/to/file')
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
        DrivetrainAndNacelle
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = DrivetrainAndNacelle.from_json('{ ... }')
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
        DrivetrainAndNacelle
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


DrivetrainAndNacelle.update_forward_refs()
