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

from dnv_bladed_models.added_inertia import AddedInertia

from dnv_bladed_models.added_inertia_insert import AddedInertiaInsert

from dnv_bladed_models.explicit_tower_can import ExplicitTowerCan

from dnv_bladed_models.foundation import Foundation

from dnv_bladed_models.foundation_insert import FoundationInsert

from dnv_bladed_models.linear_foundation import LinearFoundation

from dnv_bladed_models.point_inertia import PointInertia

from dnv_bladed_models.simple_tower_can import SimpleTowerCan

from dnv_bladed_models.simplified_linear_foundation import SimplifiedLinearFoundation

from dnv_bladed_models.six_by_six_inertia import SixBySixInertia

from dnv_bladed_models.structure import Structure

from dnv_bladed_models.tower_aerodynamic_properties import TowerAerodynamicProperties

from dnv_bladed_models.tower_can import TowerCan

from dnv_bladed_models.tower_can_insert import TowerCanInsert

from dnv_bladed_models.tower_connectable_nodes import TowerConnectableNodes

from dnv_bladed_models.tower_hydrodynamic_properties import TowerHydrodynamicProperties

from dnv_bladed_models.tower_materials_library import TowerMaterialsLibrary

from dnv_bladed_models.tower_output_group_library import TowerOutputGroupLibrary



from .schema_helper import SchemaHelper 
from .models_impl import *

TFoundationOptions = TypeVar('TFoundationOptions', LinearFoundation, SimplifiedLinearFoundation, FoundationInsert, Foundation, )
TTowerCanOptions = TypeVar('TTowerCanOptions', ExplicitTowerCan, SimpleTowerCan, TowerCanInsert, TowerCan, )
TAddedInertiaOptions = TypeVar('TAddedInertiaOptions', PointInertia, SixBySixInertia, AddedInertiaInsert, AddedInertia, )

class Tower(Structure):
    r"""
    An axisymmetric tower, made from a series of tower \"cans\".
    
    Attributes
    ----------
    ComponentType : Literal['Tower'], default='Tower'
        Defines the specific type of Component model in use.  For a `Tower` object, this must always be set to a value of `Tower`.
    
    MaterialsLibrary : TowerMaterialsLibrary
    
    Foundation : Union[LinearFoundation, SimplifiedLinearFoundation, FoundationInsert]
    
    Cans : List[Union[ExplicitTowerCan, SimpleTowerCan, TowerCanInsert]]
        A list of cans, each one placed on top of the previous one.  These cans can be either prismatic or tapered.
    
    AerodynamicProperties : TowerAerodynamicProperties
    
    HydrodynamicProperties : TowerHydrodynamicProperties, Not supported yet
    
    PointInertias : List[Union[PointInertia, SixBySixInertia, AddedInertiaInsert]]
        A list of additional inertias to add to the tower.
    
    OutputGroups : TowerOutputGroupLibrary, Not supported yet
    
    ConnectableNodes : TowerConnectableNodes, Not supported yet
    
    Notes
    -----
    
    """
    _relative_schema_path: str = PrivateAttr('Components/Tower/Tower.json')

    ComponentType: Literal['Tower'] = Field(alias="ComponentType", default='Tower', allow_mutation=False, const=True)
    MaterialsLibrary: TowerMaterialsLibrary = Field(alias="MaterialsLibrary", default=TowerMaterialsLibrary())
    Foundation: Union[LinearFoundation, SimplifiedLinearFoundation, FoundationInsert] = Field(alias="Foundation", default=None, discriminator='FoundationType')
    Cans: List[Annotated[Union[ExplicitTowerCan, SimpleTowerCan, TowerCanInsert], Field(discriminator='TowerCanType')]] = Field(alias="Cans", default=list())
    AerodynamicProperties: TowerAerodynamicProperties = Field(alias="AerodynamicProperties", default=None)
    HydrodynamicProperties: TowerHydrodynamicProperties = Field(alias="HydrodynamicProperties", default=None) # Not supported yet
    PointInertias: List[Annotated[Union[PointInertia, SixBySixInertia, AddedInertiaInsert], Field(discriminator='AddedInertiaType')]] = Field(alias="PointInertias", default=list())
    OutputGroups: TowerOutputGroupLibrary = Field(alias="OutputGroups", default=TowerOutputGroupLibrary()) # Not supported yet
    ConnectableNodes: TowerConnectableNodes = Field(alias="ConnectableNodes", default=TowerConnectableNodes()) # Not supported yet

    class Config:
        extra = Extra.forbid
        validate_assignment = True
        allow_population_by_field_name = True
        pass


    @classmethod
    def parse_obj(cls: Type['Model'], obj: Any) -> 'Model':
        discriminated_props = [
            ('Foundation', 'FoundationType'),
        ]
        discriminated_arrays = [
            ('Cans', 'TowerCanType'),
            ('PointInertias', 'AddedInertiaType'),
        ]
        prepare_model_dict(cls, obj, discriminated_props, discriminated_arrays)
        return super().parse_obj(obj)


    @classmethod
    def __get_validators__(cls):
        yield cls._factory


    @classmethod
    def _factory(cls, data):
        if isinstance(data, Tower):
            return data
        if not isinstance(data, dict):
            raise TypeError('An object is required to define Tower models')
        return Tower.parse_obj(data)


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
    def Foundation_as_LinearFoundation(self) -> LinearFoundation:
        """
        Retrieves the value of Foundation guaranteeing it is a LinearFoundation; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        LinearFoundation
            A model object, guaranteed to be a LinearFoundation.

        Raises
        ------
        TypeError
            If the value is not a LinearFoundation.
        """
        return self.Foundation_as(LinearFoundation)


    @property
    def Foundation_as_SimplifiedLinearFoundation(self) -> SimplifiedLinearFoundation:
        """
        Retrieves the value of Foundation guaranteeing it is a SimplifiedLinearFoundation; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        SimplifiedLinearFoundation
            A model object, guaranteed to be a SimplifiedLinearFoundation.

        Raises
        ------
        TypeError
            If the value is not a SimplifiedLinearFoundation.
        """
        return self.Foundation_as(SimplifiedLinearFoundation)


    @property
    def Foundation_as_inline(self) -> Union[LinearFoundation, SimplifiedLinearFoundation]:
        """
        Retrieves the value of Foundation as a model object; if the value is specified with a '$insert', an error is raised.

        Returns
        -------
        Union[LinearFoundation, SimplifiedLinearFoundation]
            A model object at the specified index, guaranteed to not be a '$insert'.

        Raises
        ------
        TypeError
            If the value is not one of the concrete types of Foundation; i.e. it is specified with a '$insert'.
        """
        if isinstance(self.Foundation, FoundationInsert) or self.Foundation.is_insert:
            raise TypeError(f"Expected Foundation value to be an in-line object, but it is currently in the '$insert' state.")
        return self.Foundation


    def Foundation_as(self, cls: Type[TFoundationOptions])-> TFoundationOptions:
        """
        Retrieves the value of Foundation, ensuring it is of the specified type.
        The specified type must be one of the valid concrete types of Foundation, or the '$insert' type
        (in the case the model is defined to be inserted from an external resource).

        Useful when using type-checking development tools, as it provides a concise way to access a value with the correct type.

        Parameters
        ----------
        cls: Type[Union[LinearFoundation, SimplifiedLinearFoundation, FoundationInsert]]
            One of the valid concrete types of Foundation, or the '$insert' type
            (in the case the model is defined to be inserted from an external resource).

        Returns
        -------
        TFoundationOptions
            A model object of the specified type.

        Raises
        ------
        TypeError
            If the value is not of the specified type.

        Examples
        --------
        Get a reference to the value when it is one of the types of Foundation:
        >>> val_obj = model_obj.Foundation_as(models.LinearFoundation)
        >>> val_obj = model_obj.Foundation_as(models.SimplifiedLinearFoundation)

        Get a reference to the value, when it was specified with a '$insert' and read in from a file:
        >>> insert_obj = model_obj.Foundation_as(models.FoundationInsert)
        """
        if not isinstance(self.Foundation, cls):
            raise TypeError(f"Expected Foundation of type '{cls.__name__}' but was type '{type(self.Foundation).__name__}'")
        return self.Foundation


    @property
    def Cans_as_inline(self) -> Iterable[Union[ExplicitTowerCan, SimpleTowerCan]]:
        """
        Retrieves the value of Cans as an iterable of model objects; if any of the values are specified with a '$insert', an error is raised.

        Returns
        -------
        Iterable[Union[ExplicitTowerCan, SimpleTowerCan]]
            A list of model objects, guaranteed to not be a '$insert'.

        Raises
        ------
        TypeError
            If any of the values are not one of the concrete types of TowerCan; i.e. they are specified with an 'insert'.

        Examples
        --------
        >>> for i, TowerCan_obj in enumerate(obj.Cans_as_any):
                print(f"Element {i} is of type TowerCan_obj.TowerCanType}")

        or

        >>> for TowerCan_obj in obj.Cans_as_any:
                # process object
        """
        for val in self.Cans:
            if isinstance(val, TowerCanInsert) or val.is_insert == True:
                raise TypeError(f"Expected element value to be an in-line object, but it is currently in the '$insert' state.")
            yield val


    def Cans_element_as_ExplicitTowerCan(self, index: int) -> ExplicitTowerCan:
        """
        Retrieves an object from the Cans array field, ensuring it is a ExplicitTowerCan.        

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        Returns
        -------
        ExplicitTowerCan
            A model object at the specified index, guaranteed to be a ExplicitTowerCan.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the value at the specified index is not a ExplicitTowerCan.

        Examples
        --------
        Gets a reference to the 2nd element, typed to a ExplicitTowerCan, that is specified in-line:
        >>> entry_obj = obj.Cans_element_as_ExplicitTowerCan(2)
        """
        return self.Cans_element_as(index, ExplicitTowerCan)


    def Cans_element_as_SimpleTowerCan(self, index: int) -> SimpleTowerCan:
        """
        Retrieves an object from the Cans array field, ensuring it is a SimpleTowerCan.        

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        Returns
        -------
        SimpleTowerCan
            A model object at the specified index, guaranteed to be a SimpleTowerCan.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the value at the specified index is not a SimpleTowerCan.

        Examples
        --------
        Gets a reference to the 2nd element, typed to a SimpleTowerCan, that is specified in-line:
        >>> entry_obj = obj.Cans_element_as_SimpleTowerCan(2)
        """
        return self.Cans_element_as(index, SimpleTowerCan)


    def Cans_element_as_inline(self, index: int) -> Union[ExplicitTowerCan, SimpleTowerCan]:
        """
        Retrieves an object from the Cans array field; if the value is specified with a '$insert', an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        Returns
        -------
        Union[ExplicitTowerCan, SimpleTowerCan]
            A model object at the specified index, guaranteed to not be an '$insert'.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the value at the specified index is not one of the concrete types of TowerCan; i.e. it is specified with an '$insert'.

        Examples
        --------
        Get a reference to the 2nd element, as any of the concrete types:
        >>> Cans_obj = obj.Cans_element_as_inline(2)
        """
        val = self.Cans[index]
        if isinstance(val, TowerCanInsert) or val.is_insert == True:
            raise TypeError(f"Expected element value at '{index}' to be an in-line object, but it is currently in the '$insert' state.")
        return val


    def Cans_element_as(self, index: int, element_cls: Type[TTowerCanOptions]) -> TTowerCanOptions:
        """
        Retrieves an object from the Cans array field, ensuring it is of the specified type.
        The specified type must be one of the valid concrete types of TowerCan, or the '$insert' type
        (in the case the model is defined to be inserted from an external resource).

        Useful when using type-checking development tools, as it provides a concise way to access a value with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        element_cls: Type[Union[ExplicitTowerCan, SimpleTowerCan, TowerCanInsert]]
            One of the valid concrete types of TowerCan, or the '$insert' type
            (in the case the model is defined to be inserted from an external resource).

        Returns
        -------
        TTowerCanOptions
            A model object of the specified type.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the model object for the specified index is not of the specified type.

        Examples
        --------
        Get a reference to the 2nd element when it was one of the types of TowerCan:
        >>> entry_obj = obj.Cans_element_as(2, models.ExplicitTowerCan)
        >>> entry_obj = obj.Cans_element_as(2, models.SimpleTowerCan)

        Get a reference to the value, when it was specified with a '$insert' and read in from a file:
        >>> insert_obj = obj.Cans_element_as(2, models.TowerCanInsert)
        """
        val = self.Cans[index]
        if not isinstance(val, element_cls):
            raise TypeError(f"Expected value of type '{element_cls.__name__}' at index {index} but found type '{type(val).__name__}'")
        return val


    @property
    def PointInertias_as_inline(self) -> Iterable[Union[PointInertia, SixBySixInertia]]:
        """
        Retrieves the value of PointInertias as an iterable of model objects; if any of the values are specified with a '$insert', an error is raised.

        Returns
        -------
        Iterable[Union[PointInertia, SixBySixInertia]]
            A list of model objects, guaranteed to not be a '$insert'.

        Raises
        ------
        TypeError
            If any of the values are not one of the concrete types of AddedInertia; i.e. they are specified with an 'insert'.

        Examples
        --------
        >>> for i, AddedInertia_obj in enumerate(obj.PointInertias_as_any):
                print(f"Element {i} is of type AddedInertia_obj.AddedInertiaType}")

        or

        >>> for AddedInertia_obj in obj.PointInertias_as_any:
                # process object
        """
        for val in self.PointInertias:
            if isinstance(val, AddedInertiaInsert) or val.is_insert == True:
                raise TypeError(f"Expected element value to be an in-line object, but it is currently in the '$insert' state.")
            yield val


    def PointInertias_element_as_PointInertia(self, index: int) -> PointInertia:
        """
        Retrieves an object from the PointInertias array field, ensuring it is a PointInertia.        

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        Returns
        -------
        PointInertia
            A model object at the specified index, guaranteed to be a PointInertia.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the value at the specified index is not a PointInertia.

        Examples
        --------
        Gets a reference to the 2nd element, typed to a PointInertia, that is specified in-line:
        >>> entry_obj = obj.PointInertias_element_as_PointInertia(2)
        """
        return self.PointInertias_element_as(index, PointInertia)


    def PointInertias_element_as_SixBySixInertia(self, index: int) -> SixBySixInertia:
        """
        Retrieves an object from the PointInertias array field, ensuring it is a SixBySixInertia.        

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        Returns
        -------
        SixBySixInertia
            A model object at the specified index, guaranteed to be a SixBySixInertia.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the value at the specified index is not a SixBySixInertia.

        Examples
        --------
        Gets a reference to the 2nd element, typed to a SixBySixInertia, that is specified in-line:
        >>> entry_obj = obj.PointInertias_element_as_SixBySixInertia(2)
        """
        return self.PointInertias_element_as(index, SixBySixInertia)


    def PointInertias_element_as_inline(self, index: int) -> Union[PointInertia, SixBySixInertia]:
        """
        Retrieves an object from the PointInertias array field; if the value is specified with a '$insert', an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        Returns
        -------
        Union[PointInertia, SixBySixInertia]
            A model object at the specified index, guaranteed to not be an '$insert'.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the value at the specified index is not one of the concrete types of AddedInertia; i.e. it is specified with an '$insert'.

        Examples
        --------
        Get a reference to the 2nd element, as any of the concrete types:
        >>> PointInertias_obj = obj.PointInertias_element_as_inline(2)
        """
        val = self.PointInertias[index]
        if isinstance(val, AddedInertiaInsert) or val.is_insert == True:
            raise TypeError(f"Expected element value at '{index}' to be an in-line object, but it is currently in the '$insert' state.")
        return val


    def PointInertias_element_as(self, index: int, element_cls: Type[TAddedInertiaOptions]) -> TAddedInertiaOptions:
        """
        Retrieves an object from the PointInertias array field, ensuring it is of the specified type.
        The specified type must be one of the valid concrete types of AddedInertia, or the '$insert' type
        (in the case the model is defined to be inserted from an external resource).

        Useful when using type-checking development tools, as it provides a concise way to access a value with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        element_cls: Type[Union[PointInertia, SixBySixInertia, AddedInertiaInsert]]
            One of the valid concrete types of AddedInertia, or the '$insert' type
            (in the case the model is defined to be inserted from an external resource).

        Returns
        -------
        TAddedInertiaOptions
            A model object of the specified type.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the model object for the specified index is not of the specified type.

        Examples
        --------
        Get a reference to the 2nd element when it was one of the types of AddedInertia:
        >>> entry_obj = obj.PointInertias_element_as(2, models.PointInertia)
        >>> entry_obj = obj.PointInertias_element_as(2, models.SixBySixInertia)

        Get a reference to the value, when it was specified with a '$insert' and read in from a file:
        >>> insert_obj = obj.PointInertias_element_as(2, models.AddedInertiaInsert)
        """
        val = self.PointInertias[index]
        if not isinstance(val, element_cls):
            raise TypeError(f"Expected value of type '{element_cls.__name__}' at index {index} but found type '{type(val).__name__}'")
        return val



    def _find_unused_containers(self) -> Set[str]:
        unused_containers: Set[str] = super()._find_unused_containers()
        if self.MaterialsLibrary._is_unused():
            unused_containers.add('MaterialsLibrary')
        if self.Cans is not None and len(self.Cans) == 0: #type: ignore
            unused_containers.add('Cans')
        if self.PointInertias is not None and len(self.PointInertias) == 0: #type: ignore
            unused_containers.add('PointInertias')
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
        Tower
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = Tower.from_file('/path/to/file')
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
        Tower
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = Tower.from_json('{ ... }')
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
        Tower
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


Tower.update_forward_refs()
