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

from dnv_bladed_models.aerofoil_library import AerofoilLibrary

from dnv_bladed_models.aileron_aerofoil_library import AileronAerofoilLibrary

from dnv_bladed_models.blade_additional_inertia import BladeAdditionalInertia

from dnv_bladed_models.blade_modelling import BladeModelling

from dnv_bladed_models.blade_modelling_insert import BladeModellingInsert

from dnv_bladed_models.blade_output_group_library import BladeOutputGroupLibrary

from dnv_bladed_models.component import Component

from dnv_bladed_models.cross_section import CrossSection

from dnv_bladed_models.finite_element_blade_modelling import FiniteElementBladeModelling

from dnv_bladed_models.interpolated_aerofoil_library import InterpolatedAerofoilLibrary

from dnv_bladed_models.modal_blade_modelling import ModalBladeModelling

from dnv_bladed_models.mounting import Mounting

from dnv_bladed_models.rigid_blade_modelling import RigidBladeModelling



from .schema_helper import SchemaHelper 
from .models_impl import *

TBladeModellingOptions = TypeVar('TBladeModellingOptions', FiniteElementBladeModelling, ModalBladeModelling, RigidBladeModelling, BladeModellingInsert, BladeModelling, )

class Blade(Component):
    r"""
    A blade component.
    
    Attributes
    ----------
    ComponentType : Literal['Blade'], default='Blade'
        Defines the specific type of Component model in use.  For a `Blade` object, this must always be set to a value of `Blade`.
    
    Modelling : Union[FiniteElementBladeModelling, ModalBladeModelling, RigidBladeModelling, BladeModellingInsert]
    
    AerofoilLibrary : AerofoilLibrary
    
    InterpolatedAerofoilLibrary : InterpolatedAerofoilLibrary
    
    AileronAerofoilLibrary : AileronAerofoilLibrary, Not supported yet
    
    Mounting : Mounting
    
    ToleranceForRepeatedCrossSections : float, default=0.001
        The tolerance used to determine whether two blade cross-sections are merely adjacent, or represent a step-change in properties at a discrete point.  If the plane point of the reference axes lie within this distance of each other, then it will be taken that the two blade cross-section definitions represent the properties inboard and outboard of a single structural point.
    
    CrossSections : List[CrossSection]
        A list of blade cross-sections which describes the geometric, structural, and aerodynamic properties of the blade.
    
    AdditionalInertia : BladeAdditionalInertia
    
    OutputGroups : BladeOutputGroupLibrary, Not supported yet
    
    Notes
    -----
    
    """
    _relative_schema_path: str = PrivateAttr('Components/Blade/Blade.json')

    ComponentType: Literal['Blade'] = Field(alias="ComponentType", default='Blade', allow_mutation=False, const=True)
    Modelling: Union[FiniteElementBladeModelling, ModalBladeModelling, RigidBladeModelling, BladeModellingInsert] = Field(alias="Modelling", default=None, discriminator='BladeModellingType')
    AerofoilLibrary: AerofoilLibrary = Field(alias="AerofoilLibrary", default=AerofoilLibrary())
    InterpolatedAerofoilLibrary: InterpolatedAerofoilLibrary = Field(alias="InterpolatedAerofoilLibrary", default=InterpolatedAerofoilLibrary())
    AileronAerofoilLibrary: AileronAerofoilLibrary = Field(alias="AileronAerofoilLibrary", default=AileronAerofoilLibrary()) # Not supported yet
    Mounting: Mounting = Field(alias="Mounting", default=None)
    ToleranceForRepeatedCrossSections: float = Field(alias="ToleranceForRepeatedCrossSections", default=None)
    CrossSections: List[CrossSection] = Field(alias="CrossSections", default=list())
    AdditionalInertia: BladeAdditionalInertia = Field(alias="AdditionalInertia", default=None)
    OutputGroups: BladeOutputGroupLibrary = Field(alias="OutputGroups", default=BladeOutputGroupLibrary()) # Not supported yet

    class Config:
        extra = Extra.forbid
        validate_assignment = True
        allow_population_by_field_name = True
        pass


    @classmethod
    def parse_obj(cls: Type['Model'], obj: Any) -> 'Model':
        discriminated_props = [
            ('Modelling', 'BladeModellingType'),
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
        if isinstance(data, Blade):
            return data
        if not isinstance(data, dict):
            raise TypeError('An object is required to define Blade models')
        return Blade.parse_obj(data)


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
    def Modelling_as_FiniteElementBladeModelling(self) -> FiniteElementBladeModelling:
        """
        Retrieves the value of Modelling guaranteeing it is a FiniteElementBladeModelling; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        FiniteElementBladeModelling
            A model object, guaranteed to be a FiniteElementBladeModelling.

        Raises
        ------
        TypeError
            If the value is not a FiniteElementBladeModelling.
        """
        return self.Modelling_as(FiniteElementBladeModelling)


    @property
    def Modelling_as_ModalBladeModelling(self) -> ModalBladeModelling:
        """
        Retrieves the value of Modelling guaranteeing it is a ModalBladeModelling; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        ModalBladeModelling
            A model object, guaranteed to be a ModalBladeModelling.

        Raises
        ------
        TypeError
            If the value is not a ModalBladeModelling.
        """
        return self.Modelling_as(ModalBladeModelling)


    @property
    def Modelling_as_RigidBladeModelling(self) -> RigidBladeModelling:
        """
        Retrieves the value of Modelling guaranteeing it is a RigidBladeModelling; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        RigidBladeModelling
            A model object, guaranteed to be a RigidBladeModelling.

        Raises
        ------
        TypeError
            If the value is not a RigidBladeModelling.
        """
        return self.Modelling_as(RigidBladeModelling)


    @property
    def Modelling_as_inline(self) -> Union[FiniteElementBladeModelling, ModalBladeModelling, RigidBladeModelling]:
        """
        Retrieves the value of Modelling as a model object; if the value is specified with a '$insert', an error is raised.

        Returns
        -------
        Union[FiniteElementBladeModelling, ModalBladeModelling, RigidBladeModelling]
            A model object at the specified index, guaranteed to not be a '$insert'.

        Raises
        ------
        TypeError
            If the value is not one of the concrete types of BladeModelling; i.e. it is specified with a '$insert'.
        """
        if isinstance(self.Modelling, BladeModellingInsert) or self.Modelling.is_insert:
            raise TypeError(f"Expected Modelling value to be an in-line object, but it is currently in the '$insert' state.")
        return self.Modelling


    def Modelling_as(self, cls: Type[TBladeModellingOptions])-> TBladeModellingOptions:
        """
        Retrieves the value of Modelling, ensuring it is of the specified type.
        The specified type must be one of the valid concrete types of BladeModelling, or the '$insert' type
        (in the case the model is defined to be inserted from an external resource).

        Useful when using type-checking development tools, as it provides a concise way to access a value with the correct type.

        Parameters
        ----------
        cls: Type[Union[FiniteElementBladeModelling, ModalBladeModelling, RigidBladeModelling, BladeModellingInsert]]
            One of the valid concrete types of BladeModelling, or the '$insert' type
            (in the case the model is defined to be inserted from an external resource).

        Returns
        -------
        TBladeModellingOptions
            A model object of the specified type.

        Raises
        ------
        TypeError
            If the value is not of the specified type.

        Examples
        --------
        Get a reference to the value when it is one of the types of BladeModelling:
        >>> val_obj = model_obj.Modelling_as(models.FiniteElementBladeModelling)
        >>> val_obj = model_obj.Modelling_as(models.ModalBladeModelling)
        >>> val_obj = model_obj.Modelling_as(models.RigidBladeModelling)

        Get a reference to the value, when it was specified with a '$insert' and read in from a file:
        >>> insert_obj = model_obj.Modelling_as(models.BladeModellingInsert)
        """
        if not isinstance(self.Modelling, cls):
            raise TypeError(f"Expected Modelling of type '{cls.__name__}' but was type '{type(self.Modelling).__name__}'")
        return self.Modelling



    def _find_unused_containers(self) -> Set[str]:
        unused_containers: Set[str] = super()._find_unused_containers()
        if self.AerofoilLibrary._is_unused():
            unused_containers.add('AerofoilLibrary')
        if self.InterpolatedAerofoilLibrary._is_unused():
            unused_containers.add('InterpolatedAerofoilLibrary')
        if self.AileronAerofoilLibrary._is_unused():
            unused_containers.add('AileronAerofoilLibrary')
        if self.CrossSections is not None and len(self.CrossSections) == 0: #type: ignore
            unused_containers.add('CrossSections')
        if self.OutputGroups._is_unused():
            unused_containers.add('OutputGroups')
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
        Blade
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = Blade.from_file('/path/to/file')
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
        Blade
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = Blade.from_json('{ ... }')
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
        Blade
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


Blade.update_forward_refs()
