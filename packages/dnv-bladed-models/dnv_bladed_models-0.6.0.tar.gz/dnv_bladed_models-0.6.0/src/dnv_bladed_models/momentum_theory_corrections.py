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

from dnv_bladed_models.dynamic_wake import DynamicWake

from dnv_bladed_models.dynamic_wake_insert import DynamicWakeInsert

from dnv_bladed_models.equilibrium_wake_model import EquilibriumWakeModel

from dnv_bladed_models.free_flow_model import FreeFlowModel

from dnv_bladed_models.frozen_wake_model import FrozenWakeModel

from dnv_bladed_models.glauert_skew_wake_model import GlauertSkewWakeModel

from dnv_bladed_models.oye_dynamic_wake import OyeDynamicWake

from dnv_bladed_models.pitt_and_peters_model import PittAndPetersModel



class MomentumTheoryCorrections_GlauertCorrectionMethodForHighInductionEnum(str, Enum):
    BLADED = "BLADED"
    NONE = "NONE"

from .schema_helper import SchemaHelper 
from .models_impl import *

TDynamicWakeOptions = TypeVar('TDynamicWakeOptions', EquilibriumWakeModel, FreeFlowModel, FrozenWakeModel, OyeDynamicWake, PittAndPetersModel, DynamicWakeInsert, DynamicWake, )

class MomentumTheoryCorrections(BladedModel):
    r"""
    The Blade Element Momentum (BEM) theory model.
    
    Attributes
    ----------
    GlauertCorrectionMethodForHighInduction : MomentumTheoryCorrections_GlauertCorrectionMethodForHighInductionEnum, default='BLADED'
        The Glauert correction method for when the rotor has high induction.
    
    GlauertSkewedWakeCorrectionModel : GlauertSkewWakeModel
    
    InductionFactorsTolerance : float, default=0.00010
        In the steady state (e.g. finding initial conditions) and/or when using equilibrium wake in the dynamic state, the axial and tangential factors are found by iteration. The precision to which these induction factors are found is determined by this tolerance.
    
    NoInflowBelowTipSpeedRatio : float, default=1
        The tip speed ratio below which the inflow calculations will be switched off. Default = 1
    
    FullInflowAboveTipSpeedRatio : float, default=2
        The tip speed ratio above which the inflow calculations will be switched on. Default = 2
    
    DynamicWake : Union[EquilibriumWakeModel, FreeFlowModel, FrozenWakeModel, OyeDynamicWake, PittAndPetersModel, DynamicWakeInsert]
    
    IncludeStructuralVelocityInInductionCalculation : bool, default=True
        If true, the axial structural velocity will be included in the induction calculations. Enabled by default.
    
    Notes
    -----
    
    """
    _relative_schema_path: str = PrivateAttr('Settings/AerodynamicSettings/AerodynamicModel/MomentumTheoryCorrections/MomentumTheoryCorrections.json')

    GlauertCorrectionMethodForHighInduction: MomentumTheoryCorrections_GlauertCorrectionMethodForHighInductionEnum = Field(alias="GlauertCorrectionMethodForHighInduction", default=None)
    GlauertSkewedWakeCorrectionModel: GlauertSkewWakeModel = Field(alias="GlauertSkewedWakeCorrectionModel", default=None)
    InductionFactorsTolerance: float = Field(alias="InductionFactorsTolerance", default=None)
    NoInflowBelowTipSpeedRatio: float = Field(alias="NoInflowBelowTipSpeedRatio", default=None)
    FullInflowAboveTipSpeedRatio: float = Field(alias="FullInflowAboveTipSpeedRatio", default=None)
    DynamicWake: Union[EquilibriumWakeModel, FreeFlowModel, FrozenWakeModel, OyeDynamicWake, PittAndPetersModel, DynamicWakeInsert] = Field(alias="DynamicWake", default=None, discriminator='DynamicWakeType')
    IncludeStructuralVelocityInInductionCalculation: bool = Field(alias="IncludeStructuralVelocityInInductionCalculation", default=None)

    class Config:
        extra = Extra.forbid
        validate_assignment = True
        allow_population_by_field_name = True
        pass


    @classmethod
    def parse_obj(cls: Type['Model'], obj: Any) -> 'Model':
        discriminated_props = [
            ('DynamicWake', 'DynamicWakeType'),
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
        if isinstance(data, MomentumTheoryCorrections):
            return data
        if not isinstance(data, dict):
            raise TypeError('An object is required to define MomentumTheoryCorrections models')
        return MomentumTheoryCorrections.parse_obj(data)


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
    def DynamicWake_as_EquilibriumWakeModel(self) -> EquilibriumWakeModel:
        """
        Retrieves the value of DynamicWake guaranteeing it is a EquilibriumWakeModel; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        EquilibriumWakeModel
            A model object, guaranteed to be a EquilibriumWakeModel.

        Raises
        ------
        TypeError
            If the value is not a EquilibriumWakeModel.
        """
        return self.DynamicWake_as(EquilibriumWakeModel)


    @property
    def DynamicWake_as_FreeFlowModel(self) -> FreeFlowModel:
        """
        Retrieves the value of DynamicWake guaranteeing it is a FreeFlowModel; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        FreeFlowModel
            A model object, guaranteed to be a FreeFlowModel.

        Raises
        ------
        TypeError
            If the value is not a FreeFlowModel.
        """
        return self.DynamicWake_as(FreeFlowModel)


    @property
    def DynamicWake_as_FrozenWakeModel(self) -> FrozenWakeModel:
        """
        Retrieves the value of DynamicWake guaranteeing it is a FrozenWakeModel; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        FrozenWakeModel
            A model object, guaranteed to be a FrozenWakeModel.

        Raises
        ------
        TypeError
            If the value is not a FrozenWakeModel.
        """
        return self.DynamicWake_as(FrozenWakeModel)


    @property
    def DynamicWake_as_OyeDynamicWake(self) -> OyeDynamicWake:
        """
        Retrieves the value of DynamicWake guaranteeing it is a OyeDynamicWake; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        OyeDynamicWake
            A model object, guaranteed to be a OyeDynamicWake.

        Raises
        ------
        TypeError
            If the value is not a OyeDynamicWake.
        """
        return self.DynamicWake_as(OyeDynamicWake)


    @property
    def DynamicWake_as_PittAndPetersModel(self) -> PittAndPetersModel:
        """
        Retrieves the value of DynamicWake guaranteeing it is a PittAndPetersModel; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        PittAndPetersModel
            A model object, guaranteed to be a PittAndPetersModel.

        Raises
        ------
        TypeError
            If the value is not a PittAndPetersModel.
        """
        return self.DynamicWake_as(PittAndPetersModel)


    @property
    def DynamicWake_as_inline(self) -> Union[EquilibriumWakeModel, FreeFlowModel, FrozenWakeModel, OyeDynamicWake, PittAndPetersModel]:
        """
        Retrieves the value of DynamicWake as a model object; if the value is specified with a '$insert', an error is raised.

        Returns
        -------
        Union[EquilibriumWakeModel, FreeFlowModel, FrozenWakeModel, OyeDynamicWake, PittAndPetersModel]
            A model object at the specified index, guaranteed to not be a '$insert'.

        Raises
        ------
        TypeError
            If the value is not one of the concrete types of DynamicWake; i.e. it is specified with a '$insert'.
        """
        if isinstance(self.DynamicWake, DynamicWakeInsert) or self.DynamicWake.is_insert:
            raise TypeError(f"Expected DynamicWake value to be an in-line object, but it is currently in the '$insert' state.")
        return self.DynamicWake


    def DynamicWake_as(self, cls: Type[TDynamicWakeOptions])-> TDynamicWakeOptions:
        """
        Retrieves the value of DynamicWake, ensuring it is of the specified type.
        The specified type must be one of the valid concrete types of DynamicWake, or the '$insert' type
        (in the case the model is defined to be inserted from an external resource).

        Useful when using type-checking development tools, as it provides a concise way to access a value with the correct type.

        Parameters
        ----------
        cls: Type[Union[EquilibriumWakeModel, FreeFlowModel, FrozenWakeModel, OyeDynamicWake, PittAndPetersModel, DynamicWakeInsert]]
            One of the valid concrete types of DynamicWake, or the '$insert' type
            (in the case the model is defined to be inserted from an external resource).

        Returns
        -------
        TDynamicWakeOptions
            A model object of the specified type.

        Raises
        ------
        TypeError
            If the value is not of the specified type.

        Examples
        --------
        Get a reference to the value when it is one of the types of DynamicWake:
        >>> val_obj = model_obj.DynamicWake_as(models.EquilibriumWakeModel)
        >>> val_obj = model_obj.DynamicWake_as(models.FreeFlowModel)
        >>> val_obj = model_obj.DynamicWake_as(models.FrozenWakeModel)
        >>> val_obj = model_obj.DynamicWake_as(models.OyeDynamicWake)
        >>> val_obj = model_obj.DynamicWake_as(models.PittAndPetersModel)

        Get a reference to the value, when it was specified with a '$insert' and read in from a file:
        >>> insert_obj = model_obj.DynamicWake_as(models.DynamicWakeInsert)
        """
        if not isinstance(self.DynamicWake, cls):
            raise TypeError(f"Expected DynamicWake of type '{cls.__name__}' but was type '{type(self.DynamicWake).__name__}'")
        return self.DynamicWake



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
        MomentumTheoryCorrections
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = MomentumTheoryCorrections.from_file('/path/to/file')
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
        MomentumTheoryCorrections
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = MomentumTheoryCorrections.from_json('{ ... }')
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
        MomentumTheoryCorrections
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


MomentumTheoryCorrections.update_forward_refs()
