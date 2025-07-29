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

from dnv_bladed_models.additional_constrained_wave import AdditionalConstrainedWave

from dnv_bladed_models.automatic_mac_camy_fuchs import AutomaticMacCamyFuchs

from dnv_bladed_models.automatic_simple_cutoff_frequency import AutomaticSimpleCutoffFrequency

from dnv_bladed_models.mac_camy_fuchs import MacCamyFuchs

from dnv_bladed_models.simple_cutoff_frequency import SimpleCutoffFrequency

from dnv_bladed_models.wave_diffraction_approximation import WaveDiffractionApproximation

from dnv_bladed_models.wave_diffraction_approximation_insert import WaveDiffractionApproximationInsert

from dnv_bladed_models.waves import Waves



from .schema_helper import SchemaHelper 
from .models_impl import *

TWaveDiffractionApproximationOptions = TypeVar('TWaveDiffractionApproximationOptions', AutomaticMacCamyFuchs, AutomaticSimpleCutoffFrequency, MacCamyFuchs, SimpleCutoffFrequency, WaveDiffractionApproximationInsert, WaveDiffractionApproximation, )

class IrregularWaves(Waves, ABC):
    r"""
    The definition of irregular waves.
    
    Not supported yet.
    
    Attributes
    ----------
    DirectionOfApproachClockwiseFromNorth : float, Not supported yet
        The bearing from which waves arrive at the turbine.
    
    RandomNumberSeed : int, Not supported yet
        A arbitrary integer used to generate a realisation of the irregular waves.  This ensures that the 'randomness' is consistent from simulation to simulation.
    
    WaveDiffractionApproximation : Union[AutomaticMacCamyFuchs, AutomaticSimpleCutoffFrequency, MacCamyFuchs, SimpleCutoffFrequency, WaveDiffractionApproximationInsert], Not supported yet
    
    AdditionalConstrainedWave : AdditionalConstrainedWave, Not supported yet
    
    Notes
    -----
    This model is not supported yet by the Bladed calculation engine.
    """
    _relative_schema_path: str = PrivateAttr('TimeDomainSimulation/Environment/SeaState/Waves/common/IrregularWaves.json')

    DirectionOfApproachClockwiseFromNorth: float = Field(alias="DirectionOfApproachClockwiseFromNorth", default=None) # Not supported yet
    RandomNumberSeed: int = Field(alias="RandomNumberSeed", default=None) # Not supported yet
    WaveDiffractionApproximation: Union[AutomaticMacCamyFuchs, AutomaticSimpleCutoffFrequency, MacCamyFuchs, SimpleCutoffFrequency, WaveDiffractionApproximationInsert] = Field(alias="WaveDiffractionApproximation", default=None, discriminator='WaveDiffractionApproximationType') # Not supported yet
    AdditionalConstrainedWave: AdditionalConstrainedWave = Field(alias="AdditionalConstrainedWave", default=None) # Not supported yet

    @classmethod
    def parse_obj(cls: Type['Model'], obj: Any) -> 'Model':
        discriminated_props = [
            ('WaveDiffractionApproximation', 'WaveDiffractionApproximationType'),
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
    def WaveDiffractionApproximation_as_AutomaticMacCamyFuchs(self) -> AutomaticMacCamyFuchs:
        """
        Retrieves the value of WaveDiffractionApproximation guaranteeing it is a AutomaticMacCamyFuchs; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        AutomaticMacCamyFuchs
            A model object, guaranteed to be a AutomaticMacCamyFuchs.

        Raises
        ------
        TypeError
            If the value is not a AutomaticMacCamyFuchs.
        """
        return self.WaveDiffractionApproximation_as(AutomaticMacCamyFuchs)


    @property
    def WaveDiffractionApproximation_as_AutomaticSimpleCutoffFrequency(self) -> AutomaticSimpleCutoffFrequency:
        """
        Retrieves the value of WaveDiffractionApproximation guaranteeing it is a AutomaticSimpleCutoffFrequency; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        AutomaticSimpleCutoffFrequency
            A model object, guaranteed to be a AutomaticSimpleCutoffFrequency.

        Raises
        ------
        TypeError
            If the value is not a AutomaticSimpleCutoffFrequency.
        """
        return self.WaveDiffractionApproximation_as(AutomaticSimpleCutoffFrequency)


    @property
    def WaveDiffractionApproximation_as_MacCamyFuchs(self) -> MacCamyFuchs:
        """
        Retrieves the value of WaveDiffractionApproximation guaranteeing it is a MacCamyFuchs; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        MacCamyFuchs
            A model object, guaranteed to be a MacCamyFuchs.

        Raises
        ------
        TypeError
            If the value is not a MacCamyFuchs.
        """
        return self.WaveDiffractionApproximation_as(MacCamyFuchs)


    @property
    def WaveDiffractionApproximation_as_SimpleCutoffFrequency(self) -> SimpleCutoffFrequency:
        """
        Retrieves the value of WaveDiffractionApproximation guaranteeing it is a SimpleCutoffFrequency; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        SimpleCutoffFrequency
            A model object, guaranteed to be a SimpleCutoffFrequency.

        Raises
        ------
        TypeError
            If the value is not a SimpleCutoffFrequency.
        """
        return self.WaveDiffractionApproximation_as(SimpleCutoffFrequency)


    @property
    def WaveDiffractionApproximation_as_inline(self) -> Union[AutomaticMacCamyFuchs, AutomaticSimpleCutoffFrequency, MacCamyFuchs, SimpleCutoffFrequency]:
        """
        Retrieves the value of WaveDiffractionApproximation as a model object; if the value is specified with a '$insert', an error is raised.

        Returns
        -------
        Union[AutomaticMacCamyFuchs, AutomaticSimpleCutoffFrequency, MacCamyFuchs, SimpleCutoffFrequency]
            A model object at the specified index, guaranteed to not be a '$insert'.

        Raises
        ------
        TypeError
            If the value is not one of the concrete types of WaveDiffractionApproximation; i.e. it is specified with a '$insert'.
        """
        if isinstance(self.WaveDiffractionApproximation, WaveDiffractionApproximationInsert) or self.WaveDiffractionApproximation.is_insert:
            raise TypeError(f"Expected WaveDiffractionApproximation value to be an in-line object, but it is currently in the '$insert' state.")
        return self.WaveDiffractionApproximation


    def WaveDiffractionApproximation_as(self, cls: Type[TWaveDiffractionApproximationOptions])-> TWaveDiffractionApproximationOptions:
        """
        Retrieves the value of WaveDiffractionApproximation, ensuring it is of the specified type.
        The specified type must be one of the valid concrete types of WaveDiffractionApproximation, or the '$insert' type
        (in the case the model is defined to be inserted from an external resource).

        Useful when using type-checking development tools, as it provides a concise way to access a value with the correct type.

        Parameters
        ----------
        cls: Type[Union[AutomaticMacCamyFuchs, AutomaticSimpleCutoffFrequency, MacCamyFuchs, SimpleCutoffFrequency, WaveDiffractionApproximationInsert]]
            One of the valid concrete types of WaveDiffractionApproximation, or the '$insert' type
            (in the case the model is defined to be inserted from an external resource).

        Returns
        -------
        TWaveDiffractionApproximationOptions
            A model object of the specified type.

        Raises
        ------
        TypeError
            If the value is not of the specified type.

        Examples
        --------
        Get a reference to the value when it is one of the types of WaveDiffractionApproximation:
        >>> val_obj = model_obj.WaveDiffractionApproximation_as(models.AutomaticMacCamyFuchs)
        >>> val_obj = model_obj.WaveDiffractionApproximation_as(models.AutomaticSimpleCutoffFrequency)
        >>> val_obj = model_obj.WaveDiffractionApproximation_as(models.MacCamyFuchs)
        >>> val_obj = model_obj.WaveDiffractionApproximation_as(models.SimpleCutoffFrequency)

        Get a reference to the value, when it was specified with a '$insert' and read in from a file:
        >>> insert_obj = model_obj.WaveDiffractionApproximation_as(models.WaveDiffractionApproximationInsert)
        """
        if not isinstance(self.WaveDiffractionApproximation, cls):
            raise TypeError(f"Expected WaveDiffractionApproximation of type '{cls.__name__}' but was type '{type(self.WaveDiffractionApproximation).__name__}'")
        return self.WaveDiffractionApproximation



    def _find_unused_containers(self) -> Set[str]:
        unused_containers: Set[str] = super()._find_unused_containers()
        return unused_containers


    def _is_unused(self) -> bool:
        """
        Returns true if the model has no user-supplied values. This indicates the object should not be rendered in the final JSON output.
        """
        candidate_fields = self.__dict__.values()
        return (len(candidate_fields) == 0 or all(map(lambda f: f is None, candidate_fields))) and super()._is_unused()



IrregularWaves.update_forward_refs()
