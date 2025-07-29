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

from dnv_bladed_models.current import Current

from dnv_bladed_models.current_direction_time_history import CurrentDirectionTimeHistory

from dnv_bladed_models.current_direction_variation import CurrentDirectionVariation

from dnv_bladed_models.current_direction_variation_insert import CurrentDirectionVariationInsert

from dnv_bladed_models.preset_current_direction_transient import PresetCurrentDirectionTransient



from .schema_helper import SchemaHelper 
from .models_impl import *

TCurrentDirectionVariationOptions = TypeVar('TCurrentDirectionVariationOptions', PresetCurrentDirectionTransient, CurrentDirectionTimeHistory, CurrentDirectionVariationInsert, CurrentDirectionVariation, )

class TimeDomainCurrent(Current, ABC):
    r"""
    The definition of a current field that varies throughout a time domain simulation.
    
    Not supported yet.
    
    Attributes
    ----------
    ReferenceHeight : float, Not supported yet
        The reference height for the current field, above which the free-field current conditions take over.  If this is omitted, the hub height will be used, and if there is more than one the *highest* hub height.
    
    Inclination : float, default=0, Not supported yet
        The inclination of the flow relative to the horizontal plane.
    
    Direction : float, Not supported yet
        The (constant) direction of the current relative to the global x-axis.
    
    DirectionVariation : Union[PresetCurrentDirectionTransient, CurrentDirectionTimeHistory, CurrentDirectionVariationInsert], Not supported yet
    
    Notes
    -----
    This model is not supported yet by the Bladed calculation engine.
    """
    _relative_schema_path: str = PrivateAttr('TimeDomainSimulation/Environment/SeaState/Current/common/TimeDomainCurrent.json')

    ReferenceHeight: float = Field(alias="ReferenceHeight", default=None) # Not supported yet
    Inclination: float = Field(alias="Inclination", default=None) # Not supported yet
    Direction: float = Field(alias="Direction", default=None) # Not supported yet
    DirectionVariation: Union[PresetCurrentDirectionTransient, CurrentDirectionTimeHistory, CurrentDirectionVariationInsert] = Field(alias="DirectionVariation", default=None, discriminator='DirectionVariationType') # Not supported yet

    @classmethod
    def parse_obj(cls: Type['Model'], obj: Any) -> 'Model':
        discriminated_props = [
            ('DirectionVariation', 'DirectionVariationType'),
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
    def DirectionVariation_as_PresetCurrentDirectionTransient(self) -> PresetCurrentDirectionTransient:
        """
        Retrieves the value of DirectionVariation guaranteeing it is a PresetCurrentDirectionTransient; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        PresetCurrentDirectionTransient
            A model object, guaranteed to be a PresetCurrentDirectionTransient.

        Raises
        ------
        TypeError
            If the value is not a PresetCurrentDirectionTransient.
        """
        return self.DirectionVariation_as(PresetCurrentDirectionTransient)


    @property
    def DirectionVariation_as_CurrentDirectionTimeHistory(self) -> CurrentDirectionTimeHistory:
        """
        Retrieves the value of DirectionVariation guaranteeing it is a CurrentDirectionTimeHistory; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        CurrentDirectionTimeHistory
            A model object, guaranteed to be a CurrentDirectionTimeHistory.

        Raises
        ------
        TypeError
            If the value is not a CurrentDirectionTimeHistory.
        """
        return self.DirectionVariation_as(CurrentDirectionTimeHistory)


    @property
    def DirectionVariation_as_inline(self) -> Union[PresetCurrentDirectionTransient, CurrentDirectionTimeHistory]:
        """
        Retrieves the value of DirectionVariation as a model object; if the value is specified with a '$insert', an error is raised.

        Returns
        -------
        Union[PresetCurrentDirectionTransient, CurrentDirectionTimeHistory]
            A model object at the specified index, guaranteed to not be a '$insert'.

        Raises
        ------
        TypeError
            If the value is not one of the concrete types of CurrentDirectionVariation; i.e. it is specified with a '$insert'.
        """
        if isinstance(self.DirectionVariation, CurrentDirectionVariationInsert) or self.DirectionVariation.is_insert:
            raise TypeError(f"Expected DirectionVariation value to be an in-line object, but it is currently in the '$insert' state.")
        return self.DirectionVariation


    def DirectionVariation_as(self, cls: Type[TCurrentDirectionVariationOptions])-> TCurrentDirectionVariationOptions:
        """
        Retrieves the value of DirectionVariation, ensuring it is of the specified type.
        The specified type must be one of the valid concrete types of CurrentDirectionVariation, or the '$insert' type
        (in the case the model is defined to be inserted from an external resource).

        Useful when using type-checking development tools, as it provides a concise way to access a value with the correct type.

        Parameters
        ----------
        cls: Type[Union[PresetCurrentDirectionTransient, CurrentDirectionTimeHistory, CurrentDirectionVariationInsert]]
            One of the valid concrete types of CurrentDirectionVariation, or the '$insert' type
            (in the case the model is defined to be inserted from an external resource).

        Returns
        -------
        TCurrentDirectionVariationOptions
            A model object of the specified type.

        Raises
        ------
        TypeError
            If the value is not of the specified type.

        Examples
        --------
        Get a reference to the value when it is one of the types of CurrentDirectionVariation:
        >>> val_obj = model_obj.DirectionVariation_as(models.PresetCurrentDirectionTransient)
        >>> val_obj = model_obj.DirectionVariation_as(models.CurrentDirectionTimeHistory)

        Get a reference to the value, when it was specified with a '$insert' and read in from a file:
        >>> insert_obj = model_obj.DirectionVariation_as(models.CurrentDirectionVariationInsert)
        """
        if not isinstance(self.DirectionVariation, cls):
            raise TypeError(f"Expected DirectionVariation of type '{cls.__name__}' but was type '{type(self.DirectionVariation).__name__}'")
        return self.DirectionVariation



    def _find_unused_containers(self) -> Set[str]:
        unused_containers: Set[str] = super()._find_unused_containers()
        return unused_containers


    def _is_unused(self) -> bool:
        """
        Returns true if the model has no user-supplied values. This indicates the object should not be rendered in the final JSON output.
        """
        candidate_fields = self.__dict__.values()
        return (len(candidate_fields) == 0 or all(map(lambda f: f is None, candidate_fields))) and super()._is_unused()



TimeDomainCurrent.update_forward_refs()
