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

from dnv_bladed_models.component import Component

from dnv_bladed_models.electrical_losses import ElectricalLosses

from dnv_bladed_models.electrical_losses_insert import ElectricalLossesInsert

from dnv_bladed_models.generator_output_group_library import GeneratorOutputGroupLibrary

from dnv_bladed_models.linear_electrical_losses import LinearElectricalLosses

from dnv_bladed_models.non_linear_electrical_losses import NonLinearElectricalLosses



from .schema_helper import SchemaHelper 
from .models_impl import *

TElectricalLossesOptions = TypeVar('TElectricalLossesOptions', LinearElectricalLosses, NonLinearElectricalLosses, ElectricalLossesInsert, ElectricalLosses, )

class Generator(Component, ABC):
    r"""
    The common properties for all types of generator.
    
    Attributes
    ----------
    GeneratorInertia : float
        The total rotational inertia of the generator, including that of the high-speed shaft after the clutch.
    
    Losses : Union[LinearElectricalLosses, NonLinearElectricalLosses, ElectricalLossesInsert]
    
    OutputGroups : GeneratorOutputGroupLibrary, Not supported yet
    
    Notes
    -----
    
    """
    _relative_schema_path: str = PrivateAttr('Components/Generator/common/Generator.json')

    GeneratorInertia: float = Field(alias="GeneratorInertia", default=None)
    Losses: Union[LinearElectricalLosses, NonLinearElectricalLosses, ElectricalLossesInsert] = Field(alias="Losses", default=None, discriminator='ElectricalLossesType')
    OutputGroups: GeneratorOutputGroupLibrary = Field(alias="OutputGroups", default=GeneratorOutputGroupLibrary()) # Not supported yet

    @classmethod
    def parse_obj(cls: Type['Model'], obj: Any) -> 'Model':
        discriminated_props = [
            ('Losses', 'ElectricalLossesType'),
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
    def Losses_as_LinearElectricalLosses(self) -> LinearElectricalLosses:
        """
        Retrieves the value of Losses guaranteeing it is a LinearElectricalLosses; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        LinearElectricalLosses
            A model object, guaranteed to be a LinearElectricalLosses.

        Raises
        ------
        TypeError
            If the value is not a LinearElectricalLosses.
        """
        return self.Losses_as(LinearElectricalLosses)


    @property
    def Losses_as_NonLinearElectricalLosses(self) -> NonLinearElectricalLosses:
        """
        Retrieves the value of Losses guaranteeing it is a NonLinearElectricalLosses; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        NonLinearElectricalLosses
            A model object, guaranteed to be a NonLinearElectricalLosses.

        Raises
        ------
        TypeError
            If the value is not a NonLinearElectricalLosses.
        """
        return self.Losses_as(NonLinearElectricalLosses)


    @property
    def Losses_as_inline(self) -> Union[LinearElectricalLosses, NonLinearElectricalLosses]:
        """
        Retrieves the value of Losses as a model object; if the value is specified with a '$insert', an error is raised.

        Returns
        -------
        Union[LinearElectricalLosses, NonLinearElectricalLosses]
            A model object at the specified index, guaranteed to not be a '$insert'.

        Raises
        ------
        TypeError
            If the value is not one of the concrete types of ElectricalLosses; i.e. it is specified with a '$insert'.
        """
        if isinstance(self.Losses, ElectricalLossesInsert) or self.Losses.is_insert:
            raise TypeError(f"Expected Losses value to be an in-line object, but it is currently in the '$insert' state.")
        return self.Losses


    def Losses_as(self, cls: Type[TElectricalLossesOptions])-> TElectricalLossesOptions:
        """
        Retrieves the value of Losses, ensuring it is of the specified type.
        The specified type must be one of the valid concrete types of ElectricalLosses, or the '$insert' type
        (in the case the model is defined to be inserted from an external resource).

        Useful when using type-checking development tools, as it provides a concise way to access a value with the correct type.

        Parameters
        ----------
        cls: Type[Union[LinearElectricalLosses, NonLinearElectricalLosses, ElectricalLossesInsert]]
            One of the valid concrete types of ElectricalLosses, or the '$insert' type
            (in the case the model is defined to be inserted from an external resource).

        Returns
        -------
        TElectricalLossesOptions
            A model object of the specified type.

        Raises
        ------
        TypeError
            If the value is not of the specified type.

        Examples
        --------
        Get a reference to the value when it is one of the types of ElectricalLosses:
        >>> val_obj = model_obj.Losses_as(models.LinearElectricalLosses)
        >>> val_obj = model_obj.Losses_as(models.NonLinearElectricalLosses)

        Get a reference to the value, when it was specified with a '$insert' and read in from a file:
        >>> insert_obj = model_obj.Losses_as(models.ElectricalLossesInsert)
        """
        if not isinstance(self.Losses, cls):
            raise TypeError(f"Expected Losses of type '{cls.__name__}' but was type '{type(self.Losses).__name__}'")
        return self.Losses



    def _find_unused_containers(self) -> Set[str]:
        unused_containers: Set[str] = super()._find_unused_containers()
        if self.OutputGroups._is_unused():
            unused_containers.add('OutputGroups')
        return unused_containers


    def _is_unused(self) -> bool:
        """
        Returns true if the model has no user-supplied values. This indicates the object should not be rendered in the final JSON output.
        """
        candidate_fields = self.__dict__.values()
        return (len(candidate_fields) == 0 or all(map(lambda f: f is None, candidate_fields))) and super()._is_unused()



Generator.update_forward_refs()
