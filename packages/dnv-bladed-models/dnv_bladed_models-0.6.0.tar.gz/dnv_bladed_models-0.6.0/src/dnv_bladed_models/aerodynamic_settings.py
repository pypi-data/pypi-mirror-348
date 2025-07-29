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

from dnv_bladed_models.aerodynamic_model_insert import AerodynamicModelInsert

from dnv_bladed_models.blade_element_momentum import BladeElementMomentum

from dnv_bladed_models.bladed_model import BladedModel

from dnv_bladed_models.compressible_beddoes_leishman_model import CompressibleBeddoesLeishmanModel

from dnv_bladed_models.dynamic_stall import DynamicStall

from dnv_bladed_models.dynamic_stall_insert import DynamicStallInsert

from dnv_bladed_models.iag_model import IAGModel

from dnv_bladed_models.incompressible_beddoes_leishman_model import IncompressibleBeddoesLeishmanModel

from dnv_bladed_models.oye_model import OyeModel

from dnv_bladed_models.vortex_line import VortexLine



from .schema_helper import SchemaHelper 
from .models_impl import *

TAerodynamicModelOptions = TypeVar('TAerodynamicModelOptions', BladeElementMomentum, VortexLine, AerodynamicModelInsert, AerodynamicModel, )
TDynamicStallOptions = TypeVar('TDynamicStallOptions', CompressibleBeddoesLeishmanModel, IAGModel, IncompressibleBeddoesLeishmanModel, OyeModel, DynamicStallInsert, DynamicStall, )

class AerodynamicSettings(BladedModel):
    r"""
    Settings controlling the aerodynamic modelling in Bladed.
    
    Attributes
    ----------
    AerodynamicModel : Union[BladeElementMomentum, VortexLine, AerodynamicModelInsert]
    
    DynamicStall : Union[CompressibleBeddoesLeishmanModel, IAGModel, IncompressibleBeddoesLeishmanModel, OyeModel, DynamicStallInsert]
    
    Notes
    -----
    
    """
    _relative_schema_path: str = PrivateAttr('Settings/AerodynamicSettings/AerodynamicSettings.json')

    AerodynamicModel: Union[BladeElementMomentum, VortexLine, AerodynamicModelInsert] = Field(alias="AerodynamicModel", default=None, discriminator='AerodynamicModelType')
    DynamicStall: Union[CompressibleBeddoesLeishmanModel, IAGModel, IncompressibleBeddoesLeishmanModel, OyeModel, DynamicStallInsert] = Field(alias="DynamicStall", default=None, discriminator='DynamicStallType')

    class Config:
        extra = Extra.forbid
        validate_assignment = True
        allow_population_by_field_name = True
        pass


    @classmethod
    def parse_obj(cls: Type['Model'], obj: Any) -> 'Model':
        discriminated_props = [
            ('AerodynamicModel', 'AerodynamicModelType'),
            ('DynamicStall', 'DynamicStallType'),
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
        if isinstance(data, AerodynamicSettings):
            return data
        if not isinstance(data, dict):
            raise TypeError('An object is required to define AerodynamicSettings models')
        return AerodynamicSettings.parse_obj(data)


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
    def AerodynamicModel_as_BladeElementMomentum(self) -> BladeElementMomentum:
        """
        Retrieves the value of AerodynamicModel guaranteeing it is a BladeElementMomentum; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        BladeElementMomentum
            A model object, guaranteed to be a BladeElementMomentum.

        Raises
        ------
        TypeError
            If the value is not a BladeElementMomentum.
        """
        return self.AerodynamicModel_as(BladeElementMomentum)


    @property
    def AerodynamicModel_as_VortexLine(self) -> VortexLine:
        """
        Retrieves the value of AerodynamicModel guaranteeing it is a VortexLine; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        VortexLine
            A model object, guaranteed to be a VortexLine.

        Raises
        ------
        TypeError
            If the value is not a VortexLine.
        """
        return self.AerodynamicModel_as(VortexLine)


    @property
    def AerodynamicModel_as_inline(self) -> Union[BladeElementMomentum, VortexLine]:
        """
        Retrieves the value of AerodynamicModel as a model object; if the value is specified with a '$insert', an error is raised.

        Returns
        -------
        Union[BladeElementMomentum, VortexLine]
            A model object at the specified index, guaranteed to not be a '$insert'.

        Raises
        ------
        TypeError
            If the value is not one of the concrete types of AerodynamicModel; i.e. it is specified with a '$insert'.
        """
        if isinstance(self.AerodynamicModel, AerodynamicModelInsert) or self.AerodynamicModel.is_insert:
            raise TypeError(f"Expected AerodynamicModel value to be an in-line object, but it is currently in the '$insert' state.")
        return self.AerodynamicModel


    def AerodynamicModel_as(self, cls: Type[TAerodynamicModelOptions])-> TAerodynamicModelOptions:
        """
        Retrieves the value of AerodynamicModel, ensuring it is of the specified type.
        The specified type must be one of the valid concrete types of AerodynamicModel, or the '$insert' type
        (in the case the model is defined to be inserted from an external resource).

        Useful when using type-checking development tools, as it provides a concise way to access a value with the correct type.

        Parameters
        ----------
        cls: Type[Union[BladeElementMomentum, VortexLine, AerodynamicModelInsert]]
            One of the valid concrete types of AerodynamicModel, or the '$insert' type
            (in the case the model is defined to be inserted from an external resource).

        Returns
        -------
        TAerodynamicModelOptions
            A model object of the specified type.

        Raises
        ------
        TypeError
            If the value is not of the specified type.

        Examples
        --------
        Get a reference to the value when it is one of the types of AerodynamicModel:
        >>> val_obj = model_obj.AerodynamicModel_as(models.BladeElementMomentum)
        >>> val_obj = model_obj.AerodynamicModel_as(models.VortexLine)

        Get a reference to the value, when it was specified with a '$insert' and read in from a file:
        >>> insert_obj = model_obj.AerodynamicModel_as(models.AerodynamicModelInsert)
        """
        if not isinstance(self.AerodynamicModel, cls):
            raise TypeError(f"Expected AerodynamicModel of type '{cls.__name__}' but was type '{type(self.AerodynamicModel).__name__}'")
        return self.AerodynamicModel


    @property
    def DynamicStall_as_CompressibleBeddoesLeishmanModel(self) -> CompressibleBeddoesLeishmanModel:
        """
        Retrieves the value of DynamicStall guaranteeing it is a CompressibleBeddoesLeishmanModel; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        CompressibleBeddoesLeishmanModel
            A model object, guaranteed to be a CompressibleBeddoesLeishmanModel.

        Raises
        ------
        TypeError
            If the value is not a CompressibleBeddoesLeishmanModel.
        """
        return self.DynamicStall_as(CompressibleBeddoesLeishmanModel)


    @property
    def DynamicStall_as_IAGModel(self) -> IAGModel:
        """
        Retrieves the value of DynamicStall guaranteeing it is a IAGModel; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        IAGModel
            A model object, guaranteed to be a IAGModel.

        Raises
        ------
        TypeError
            If the value is not a IAGModel.
        """
        return self.DynamicStall_as(IAGModel)


    @property
    def DynamicStall_as_IncompressibleBeddoesLeishmanModel(self) -> IncompressibleBeddoesLeishmanModel:
        """
        Retrieves the value of DynamicStall guaranteeing it is a IncompressibleBeddoesLeishmanModel; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        IncompressibleBeddoesLeishmanModel
            A model object, guaranteed to be a IncompressibleBeddoesLeishmanModel.

        Raises
        ------
        TypeError
            If the value is not a IncompressibleBeddoesLeishmanModel.
        """
        return self.DynamicStall_as(IncompressibleBeddoesLeishmanModel)


    @property
    def DynamicStall_as_OyeModel(self) -> OyeModel:
        """
        Retrieves the value of DynamicStall guaranteeing it is a OyeModel; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        OyeModel
            A model object, guaranteed to be a OyeModel.

        Raises
        ------
        TypeError
            If the value is not a OyeModel.
        """
        return self.DynamicStall_as(OyeModel)


    @property
    def DynamicStall_as_inline(self) -> Union[CompressibleBeddoesLeishmanModel, IAGModel, IncompressibleBeddoesLeishmanModel, OyeModel]:
        """
        Retrieves the value of DynamicStall as a model object; if the value is specified with a '$insert', an error is raised.

        Returns
        -------
        Union[CompressibleBeddoesLeishmanModel, IAGModel, IncompressibleBeddoesLeishmanModel, OyeModel]
            A model object at the specified index, guaranteed to not be a '$insert'.

        Raises
        ------
        TypeError
            If the value is not one of the concrete types of DynamicStall; i.e. it is specified with a '$insert'.
        """
        if isinstance(self.DynamicStall, DynamicStallInsert) or self.DynamicStall.is_insert:
            raise TypeError(f"Expected DynamicStall value to be an in-line object, but it is currently in the '$insert' state.")
        return self.DynamicStall


    def DynamicStall_as(self, cls: Type[TDynamicStallOptions])-> TDynamicStallOptions:
        """
        Retrieves the value of DynamicStall, ensuring it is of the specified type.
        The specified type must be one of the valid concrete types of DynamicStall, or the '$insert' type
        (in the case the model is defined to be inserted from an external resource).

        Useful when using type-checking development tools, as it provides a concise way to access a value with the correct type.

        Parameters
        ----------
        cls: Type[Union[CompressibleBeddoesLeishmanModel, IAGModel, IncompressibleBeddoesLeishmanModel, OyeModel, DynamicStallInsert]]
            One of the valid concrete types of DynamicStall, or the '$insert' type
            (in the case the model is defined to be inserted from an external resource).

        Returns
        -------
        TDynamicStallOptions
            A model object of the specified type.

        Raises
        ------
        TypeError
            If the value is not of the specified type.

        Examples
        --------
        Get a reference to the value when it is one of the types of DynamicStall:
        >>> val_obj = model_obj.DynamicStall_as(models.CompressibleBeddoesLeishmanModel)
        >>> val_obj = model_obj.DynamicStall_as(models.IAGModel)
        >>> val_obj = model_obj.DynamicStall_as(models.IncompressibleBeddoesLeishmanModel)
        >>> val_obj = model_obj.DynamicStall_as(models.OyeModel)

        Get a reference to the value, when it was specified with a '$insert' and read in from a file:
        >>> insert_obj = model_obj.DynamicStall_as(models.DynamicStallInsert)
        """
        if not isinstance(self.DynamicStall, cls):
            raise TypeError(f"Expected DynamicStall of type '{cls.__name__}' but was type '{type(self.DynamicStall).__name__}'")
        return self.DynamicStall



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
        AerodynamicSettings
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = AerodynamicSettings.from_file('/path/to/file')
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
        AerodynamicSettings
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = AerodynamicSettings.from_json('{ ... }')
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
        AerodynamicSettings
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


AerodynamicSettings.update_forward_refs()
