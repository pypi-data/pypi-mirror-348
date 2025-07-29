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

from dnv_bladed_models.bladed_model import BladedModel

from dnv_bladed_models.first_order_response import FirstOrderResponse

from dnv_bladed_models.immediate_response import ImmediateResponse

from dnv_bladed_models.proportional_integral_deriviative import ProportionalIntegralDeriviative

from dnv_bladed_models.response_to_demand import ResponseToDemand

from dnv_bladed_models.response_to_demand_insert import ResponseToDemandInsert

from dnv_bladed_models.second_order_response import SecondOrderResponse



class PitchSystemDemand_PitchSystemDemandTypeEnum(str, Enum):
    POSITION = "Position"
    RATE = "Rate"
    __INSERT__ = "__insert__"

from .schema_helper import SchemaHelper 
from .models_impl import *

TResponseToDemandOptions = TypeVar('TResponseToDemandOptions', FirstOrderResponse, ImmediateResponse, ProportionalIntegralDeriviative, SecondOrderResponse, ResponseToDemandInsert, ResponseToDemand, )

class PitchSystemDemand(BladedModel, ABC):
    r"""
    The common properties of the pitch and rate demand responses.
    
    Attributes
    ----------
    PitchSystemDemandType : PitchSystemDemand_PitchSystemDemandTypeEnum
        Defines the specific type of model in use.
    
    ResponseToDemand : Union[FirstOrderResponse, ImmediateResponse, ProportionalIntegralDeriviative, SecondOrderResponse, ResponseToDemandInsert]
    
    Notes
    -----
    
    This class is an abstraction, with the following concrete implementations:
        - PitchPositionDemand
        - PitchRateDemand
        - PitchSystemDemandInsert
    
    """
    _relative_schema_path: str = PrivateAttr('Components/PitchSystem/PitchController/PitchSystemDemand/common/PitchSystemDemand.json')

    PitchSystemDemandType: PitchSystemDemand_PitchSystemDemandTypeEnum = Field(alias="PitchSystemDemandType", default=None)
    ResponseToDemand: Union[FirstOrderResponse, ImmediateResponse, ProportionalIntegralDeriviative, SecondOrderResponse, ResponseToDemandInsert] = Field(alias="ResponseToDemand", default=None, discriminator='ResponseToDemandType')

    @classmethod
    def parse_obj(cls: Type['Model'], obj: Any) -> 'Model':
        discriminated_props = [
            ('ResponseToDemand', 'ResponseToDemandType'),
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
    def ResponseToDemand_as_FirstOrderResponse(self) -> FirstOrderResponse:
        """
        Retrieves the value of ResponseToDemand guaranteeing it is a FirstOrderResponse; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        FirstOrderResponse
            A model object, guaranteed to be a FirstOrderResponse.

        Raises
        ------
        TypeError
            If the value is not a FirstOrderResponse.
        """
        return self.ResponseToDemand_as(FirstOrderResponse)


    @property
    def ResponseToDemand_as_ImmediateResponse(self) -> ImmediateResponse:
        """
        Retrieves the value of ResponseToDemand guaranteeing it is a ImmediateResponse; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        ImmediateResponse
            A model object, guaranteed to be a ImmediateResponse.

        Raises
        ------
        TypeError
            If the value is not a ImmediateResponse.
        """
        return self.ResponseToDemand_as(ImmediateResponse)


    @property
    def ResponseToDemand_as_ProportionalIntegralDeriviative(self) -> ProportionalIntegralDeriviative:
        """
        Retrieves the value of ResponseToDemand guaranteeing it is a ProportionalIntegralDeriviative; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        ProportionalIntegralDeriviative
            A model object, guaranteed to be a ProportionalIntegralDeriviative.

        Raises
        ------
        TypeError
            If the value is not a ProportionalIntegralDeriviative.
        """
        return self.ResponseToDemand_as(ProportionalIntegralDeriviative)


    @property
    def ResponseToDemand_as_SecondOrderResponse(self) -> SecondOrderResponse:
        """
        Retrieves the value of ResponseToDemand guaranteeing it is a SecondOrderResponse; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        SecondOrderResponse
            A model object, guaranteed to be a SecondOrderResponse.

        Raises
        ------
        TypeError
            If the value is not a SecondOrderResponse.
        """
        return self.ResponseToDemand_as(SecondOrderResponse)


    @property
    def ResponseToDemand_as_inline(self) -> Union[FirstOrderResponse, ImmediateResponse, ProportionalIntegralDeriviative, SecondOrderResponse]:
        """
        Retrieves the value of ResponseToDemand as a model object; if the value is specified with a '$insert', an error is raised.

        Returns
        -------
        Union[FirstOrderResponse, ImmediateResponse, ProportionalIntegralDeriviative, SecondOrderResponse]
            A model object at the specified index, guaranteed to not be a '$insert'.

        Raises
        ------
        TypeError
            If the value is not one of the concrete types of ResponseToDemand; i.e. it is specified with a '$insert'.
        """
        if isinstance(self.ResponseToDemand, ResponseToDemandInsert) or self.ResponseToDemand.is_insert:
            raise TypeError(f"Expected ResponseToDemand value to be an in-line object, but it is currently in the '$insert' state.")
        return self.ResponseToDemand


    def ResponseToDemand_as(self, cls: Type[TResponseToDemandOptions])-> TResponseToDemandOptions:
        """
        Retrieves the value of ResponseToDemand, ensuring it is of the specified type.
        The specified type must be one of the valid concrete types of ResponseToDemand, or the '$insert' type
        (in the case the model is defined to be inserted from an external resource).

        Useful when using type-checking development tools, as it provides a concise way to access a value with the correct type.

        Parameters
        ----------
        cls: Type[Union[FirstOrderResponse, ImmediateResponse, ProportionalIntegralDeriviative, SecondOrderResponse, ResponseToDemandInsert]]
            One of the valid concrete types of ResponseToDemand, or the '$insert' type
            (in the case the model is defined to be inserted from an external resource).

        Returns
        -------
        TResponseToDemandOptions
            A model object of the specified type.

        Raises
        ------
        TypeError
            If the value is not of the specified type.

        Examples
        --------
        Get a reference to the value when it is one of the types of ResponseToDemand:
        >>> val_obj = model_obj.ResponseToDemand_as(models.FirstOrderResponse)
        >>> val_obj = model_obj.ResponseToDemand_as(models.ImmediateResponse)
        >>> val_obj = model_obj.ResponseToDemand_as(models.ProportionalIntegralDeriviative)
        >>> val_obj = model_obj.ResponseToDemand_as(models.SecondOrderResponse)

        Get a reference to the value, when it was specified with a '$insert' and read in from a file:
        >>> insert_obj = model_obj.ResponseToDemand_as(models.ResponseToDemandInsert)
        """
        if not isinstance(self.ResponseToDemand, cls):
            raise TypeError(f"Expected ResponseToDemand of type '{cls.__name__}' but was type '{type(self.ResponseToDemand).__name__}'")
        return self.ResponseToDemand



    def _find_unused_containers(self) -> Set[str]:
        unused_containers: Set[str] = super()._find_unused_containers()
        return unused_containers


    def _is_unused(self) -> bool:
        """
        Returns true if the model has no user-supplied values. This indicates the object should not be rendered in the final JSON output.
        """
        candidate_fields = self.__dict__.values()
        return (len(candidate_fields) == 0 or all(map(lambda f: f is None, candidate_fields))) and super()._is_unused()



PitchSystemDemand.update_forward_refs()
