# *********************************************************************#
# Bladed Python Models API                                             #
# Copyright (c) DNV Services UK Limited (c) 2025. All rights reserved. #
# MIT License (see license file)                                       #
# *********************************************************************#


# coding: utf-8

from __future__ import annotations

from abc import ABC

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

from dnv_bladed_models.dynamic_upstream_wake import DynamicUpstreamWake

from dnv_bladed_models.exponential_shear_model import ExponentialShearModel

from dnv_bladed_models.gaussian import Gaussian

from dnv_bladed_models.logarithmic_shear_model import LogarithmicShearModel

from dnv_bladed_models.look_up_shear_model import LookUpShearModel

from dnv_bladed_models.preset_wind_direction_transient import PresetWindDirectionTransient

from dnv_bladed_models.steady_wake_deficit import SteadyWakeDeficit

from dnv_bladed_models.steady_wake_deficit_insert import SteadyWakeDeficitInsert

from dnv_bladed_models.user_defined_wake_deficit import UserDefinedWakeDeficit

from dnv_bladed_models.wind import Wind

from dnv_bladed_models.wind_direction_time_history import WindDirectionTimeHistory

from dnv_bladed_models.wind_direction_variation import WindDirectionVariation

from dnv_bladed_models.wind_direction_variation_insert import WindDirectionVariationInsert

from dnv_bladed_models.wind_shear import WindShear

from dnv_bladed_models.wind_shear_insert import WindShearInsert



from .schema_helper import SchemaHelper 
from .models_impl import *

TWindShearOptions = TypeVar('TWindShearOptions', ExponentialShearModel, LogarithmicShearModel, LookUpShearModel, WindShearInsert, WindShear, )
TWindDirectionVariationOptions = TypeVar('TWindDirectionVariationOptions', PresetWindDirectionTransient, WindDirectionTimeHistory, WindDirectionVariationInsert, WindDirectionVariation, )
TSteadyWakeDeficitOptions = TypeVar('TSteadyWakeDeficitOptions', Gaussian, UserDefinedWakeDeficit, SteadyWakeDeficitInsert, SteadyWakeDeficit, )

class TimeDomainWind(Wind, ABC):
    r"""
    The definition of a wind field that varies throughout a time domain simulation.
    
    Attributes
    ----------
    ReferenceHeight : float
        The reference height for the wind field, at which all flow conditions are at their nominal values.  If this is omitted, the hub height will be used, and if there is more than one the *highest* hub height.
    
    WindShear : Union[ExponentialShearModel, LogarithmicShearModel, LookUpShearModel, WindShearInsert]
    
    Inclination : float, default=0
        The inclination of the flow relative to the horizontal plane.  Typically this is in the order of 8 degrees for an onshore turbine, and 0 degrees for an offshore turbine.
    
    Direction : float, default=0
        The (constant) direction of the wind relative to the global x-axis.
    
    DirectionVariation : Union[PresetWindDirectionTransient, WindDirectionTimeHistory, WindDirectionVariationInsert]
    
    SteadyWakeDeficit : Union[Gaussian, UserDefinedWakeDeficit, SteadyWakeDeficitInsert]
    
    DynamicUpstreamWake : DynamicUpstreamWake
    
    Notes
    -----
    
    """
    _relative_schema_path: str = PrivateAttr('TimeDomainSimulation/Environment/Wind/common/TimeDomainWind.json')

    ReferenceHeight: float = Field(alias="ReferenceHeight", default=None)
    WindShear: Union[ExponentialShearModel, LogarithmicShearModel, LookUpShearModel, WindShearInsert] = Field(alias="WindShear", default=None, discriminator='WindShearType')
    Inclination: float = Field(alias="Inclination", default=None)
    Direction: float = Field(alias="Direction", default=None)
    DirectionVariation: Union[PresetWindDirectionTransient, WindDirectionTimeHistory, WindDirectionVariationInsert] = Field(alias="DirectionVariation", default=None, discriminator='DirectionVariationType')
    SteadyWakeDeficit: Union[Gaussian, UserDefinedWakeDeficit, SteadyWakeDeficitInsert] = Field(alias="SteadyWakeDeficit", default=None, discriminator='SteadyWakeDeficitType')
    DynamicUpstreamWake: DynamicUpstreamWake = Field(alias="DynamicUpstreamWake", default=None)

    @classmethod
    def parse_obj(cls: Type['Model'], obj: Any) -> 'Model':
        discriminated_props = [
            ('WindShear', 'WindShearType'),
            ('DirectionVariation', 'DirectionVariationType'),
            ('SteadyWakeDeficit', 'SteadyWakeDeficitType'),
        ]
        discriminated_arrays = [
        ]
        prepare_model_dict(cls, obj, discriminated_props, discriminated_arrays)
        return super().parse_obj(obj)


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
    def WindShear_as_ExponentialShearModel(self) -> ExponentialShearModel:
        """
        Retrieves the value of WindShear guaranteeing it is a ExponentialShearModel; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        ExponentialShearModel
            A model object, guaranteed to be a ExponentialShearModel.

        Raises
        ------
        TypeError
            If the value is not a ExponentialShearModel.
        """
        return self.WindShear_as(ExponentialShearModel)


    @property
    def WindShear_as_LogarithmicShearModel(self) -> LogarithmicShearModel:
        """
        Retrieves the value of WindShear guaranteeing it is a LogarithmicShearModel; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        LogarithmicShearModel
            A model object, guaranteed to be a LogarithmicShearModel.

        Raises
        ------
        TypeError
            If the value is not a LogarithmicShearModel.
        """
        return self.WindShear_as(LogarithmicShearModel)


    @property
    def WindShear_as_LookUpShearModel(self) -> LookUpShearModel:
        """
        Retrieves the value of WindShear guaranteeing it is a LookUpShearModel; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        LookUpShearModel
            A model object, guaranteed to be a LookUpShearModel.

        Raises
        ------
        TypeError
            If the value is not a LookUpShearModel.
        """
        return self.WindShear_as(LookUpShearModel)


    @property
    def WindShear_as_inline(self) -> Union[ExponentialShearModel, LogarithmicShearModel, LookUpShearModel]:
        """
        Retrieves the value of WindShear as a model object; if the value is specified with a '$insert', an error is raised.

        Returns
        -------
        Union[ExponentialShearModel, LogarithmicShearModel, LookUpShearModel]
            A model object at the specified index, guaranteed to not be a '$insert'.

        Raises
        ------
        TypeError
            If the value is not one of the concrete types of WindShear; i.e. it is specified with a '$insert'.
        """
        if isinstance(self.WindShear, WindShearInsert) or self.WindShear.is_insert:
            raise TypeError(f"Expected WindShear value to be an in-line object, but it is currently in the '$insert' state.")
        return self.WindShear


    def WindShear_as(self, cls: Type[TWindShearOptions])-> TWindShearOptions:
        """
        Retrieves the value of WindShear, ensuring it is of the specified type.
        The specified type must be one of the valid concrete types of WindShear, or the '$insert' type
        (in the case the model is defined to be inserted from an external resource).

        Useful when using type-checking development tools, as it provides a concise way to access a value with the correct type.

        Parameters
        ----------
        cls: Type[Union[ExponentialShearModel, LogarithmicShearModel, LookUpShearModel, WindShearInsert]]
            One of the valid concrete types of WindShear, or the '$insert' type
            (in the case the model is defined to be inserted from an external resource).

        Returns
        -------
        TWindShearOptions
            A model object of the specified type.

        Raises
        ------
        TypeError
            If the value is not of the specified type.

        Examples
        --------
        Get a reference to the value when it is one of the types of WindShear:
        >>> val_obj = model_obj.WindShear_as(models.ExponentialShearModel)
        >>> val_obj = model_obj.WindShear_as(models.LogarithmicShearModel)
        >>> val_obj = model_obj.WindShear_as(models.LookUpShearModel)

        Get a reference to the value, when it was specified with a '$insert' and read in from a file:
        >>> insert_obj = model_obj.WindShear_as(models.WindShearInsert)
        """
        if not isinstance(self.WindShear, cls):
            raise TypeError(f"Expected WindShear of type '{cls.__name__}' but was type '{type(self.WindShear).__name__}'")
        return self.WindShear


    @property
    def DirectionVariation_as_PresetWindDirectionTransient(self) -> PresetWindDirectionTransient:
        """
        Retrieves the value of DirectionVariation guaranteeing it is a PresetWindDirectionTransient; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        PresetWindDirectionTransient
            A model object, guaranteed to be a PresetWindDirectionTransient.

        Raises
        ------
        TypeError
            If the value is not a PresetWindDirectionTransient.
        """
        return self.DirectionVariation_as(PresetWindDirectionTransient)


    @property
    def DirectionVariation_as_WindDirectionTimeHistory(self) -> WindDirectionTimeHistory:
        """
        Retrieves the value of DirectionVariation guaranteeing it is a WindDirectionTimeHistory; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        WindDirectionTimeHistory
            A model object, guaranteed to be a WindDirectionTimeHistory.

        Raises
        ------
        TypeError
            If the value is not a WindDirectionTimeHistory.
        """
        return self.DirectionVariation_as(WindDirectionTimeHistory)


    @property
    def DirectionVariation_as_inline(self) -> Union[PresetWindDirectionTransient, WindDirectionTimeHistory]:
        """
        Retrieves the value of DirectionVariation as a model object; if the value is specified with a '$insert', an error is raised.

        Returns
        -------
        Union[PresetWindDirectionTransient, WindDirectionTimeHistory]
            A model object at the specified index, guaranteed to not be a '$insert'.

        Raises
        ------
        TypeError
            If the value is not one of the concrete types of WindDirectionVariation; i.e. it is specified with a '$insert'.
        """
        if isinstance(self.DirectionVariation, WindDirectionVariationInsert) or self.DirectionVariation.is_insert:
            raise TypeError(f"Expected DirectionVariation value to be an in-line object, but it is currently in the '$insert' state.")
        return self.DirectionVariation


    def DirectionVariation_as(self, cls: Type[TWindDirectionVariationOptions])-> TWindDirectionVariationOptions:
        """
        Retrieves the value of DirectionVariation, ensuring it is of the specified type.
        The specified type must be one of the valid concrete types of WindDirectionVariation, or the '$insert' type
        (in the case the model is defined to be inserted from an external resource).

        Useful when using type-checking development tools, as it provides a concise way to access a value with the correct type.

        Parameters
        ----------
        cls: Type[Union[PresetWindDirectionTransient, WindDirectionTimeHistory, WindDirectionVariationInsert]]
            One of the valid concrete types of WindDirectionVariation, or the '$insert' type
            (in the case the model is defined to be inserted from an external resource).

        Returns
        -------
        TWindDirectionVariationOptions
            A model object of the specified type.

        Raises
        ------
        TypeError
            If the value is not of the specified type.

        Examples
        --------
        Get a reference to the value when it is one of the types of WindDirectionVariation:
        >>> val_obj = model_obj.DirectionVariation_as(models.PresetWindDirectionTransient)
        >>> val_obj = model_obj.DirectionVariation_as(models.WindDirectionTimeHistory)

        Get a reference to the value, when it was specified with a '$insert' and read in from a file:
        >>> insert_obj = model_obj.DirectionVariation_as(models.WindDirectionVariationInsert)
        """
        if not isinstance(self.DirectionVariation, cls):
            raise TypeError(f"Expected DirectionVariation of type '{cls.__name__}' but was type '{type(self.DirectionVariation).__name__}'")
        return self.DirectionVariation


    @property
    def SteadyWakeDeficit_as_Gaussian(self) -> Gaussian:
        """
        Retrieves the value of SteadyWakeDeficit guaranteeing it is a Gaussian; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        Gaussian
            A model object, guaranteed to be a Gaussian.

        Raises
        ------
        TypeError
            If the value is not a Gaussian.
        """
        return self.SteadyWakeDeficit_as(Gaussian)


    @property
    def SteadyWakeDeficit_as_UserDefinedWakeDeficit(self) -> UserDefinedWakeDeficit:
        """
        Retrieves the value of SteadyWakeDeficit guaranteeing it is a UserDefinedWakeDeficit; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        UserDefinedWakeDeficit
            A model object, guaranteed to be a UserDefinedWakeDeficit.

        Raises
        ------
        TypeError
            If the value is not a UserDefinedWakeDeficit.
        """
        return self.SteadyWakeDeficit_as(UserDefinedWakeDeficit)


    @property
    def SteadyWakeDeficit_as_inline(self) -> Union[Gaussian, UserDefinedWakeDeficit]:
        """
        Retrieves the value of SteadyWakeDeficit as a model object; if the value is specified with a '$insert', an error is raised.

        Returns
        -------
        Union[Gaussian, UserDefinedWakeDeficit]
            A model object at the specified index, guaranteed to not be a '$insert'.

        Raises
        ------
        TypeError
            If the value is not one of the concrete types of SteadyWakeDeficit; i.e. it is specified with a '$insert'.
        """
        if isinstance(self.SteadyWakeDeficit, SteadyWakeDeficitInsert) or self.SteadyWakeDeficit.is_insert:
            raise TypeError(f"Expected SteadyWakeDeficit value to be an in-line object, but it is currently in the '$insert' state.")
        return self.SteadyWakeDeficit


    def SteadyWakeDeficit_as(self, cls: Type[TSteadyWakeDeficitOptions])-> TSteadyWakeDeficitOptions:
        """
        Retrieves the value of SteadyWakeDeficit, ensuring it is of the specified type.
        The specified type must be one of the valid concrete types of SteadyWakeDeficit, or the '$insert' type
        (in the case the model is defined to be inserted from an external resource).

        Useful when using type-checking development tools, as it provides a concise way to access a value with the correct type.

        Parameters
        ----------
        cls: Type[Union[Gaussian, UserDefinedWakeDeficit, SteadyWakeDeficitInsert]]
            One of the valid concrete types of SteadyWakeDeficit, or the '$insert' type
            (in the case the model is defined to be inserted from an external resource).

        Returns
        -------
        TSteadyWakeDeficitOptions
            A model object of the specified type.

        Raises
        ------
        TypeError
            If the value is not of the specified type.

        Examples
        --------
        Get a reference to the value when it is one of the types of SteadyWakeDeficit:
        >>> val_obj = model_obj.SteadyWakeDeficit_as(models.Gaussian)
        >>> val_obj = model_obj.SteadyWakeDeficit_as(models.UserDefinedWakeDeficit)

        Get a reference to the value, when it was specified with a '$insert' and read in from a file:
        >>> insert_obj = model_obj.SteadyWakeDeficit_as(models.SteadyWakeDeficitInsert)
        """
        if not isinstance(self.SteadyWakeDeficit, cls):
            raise TypeError(f"Expected SteadyWakeDeficit of type '{cls.__name__}' but was type '{type(self.SteadyWakeDeficit).__name__}'")
        return self.SteadyWakeDeficit



    def _find_unused_containers(self) -> Set[str]:
        unused_containers: Set[str] = super()._find_unused_containers()
        return unused_containers


    def _is_unused(self) -> bool:
        """
        Returns true if the model has no user-supplied values. This indicates the object should not be rendered in the final JSON output.
        """
        candidate_fields = self.__dict__.values()
        return (len(candidate_fields) == 0 or all(map(lambda f: f is None, candidate_fields))) and super()._is_unused()



TimeDomainWind.update_forward_refs()
