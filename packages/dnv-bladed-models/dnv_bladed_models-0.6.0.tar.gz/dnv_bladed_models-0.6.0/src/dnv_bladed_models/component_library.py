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

from dnv_bladed_models.blade import Blade

from dnv_bladed_models.bladed_model import BladedModel

from dnv_bladed_models.component import Component

from dnv_bladed_models.component_insert import ComponentInsert

from dnv_bladed_models.drivetrain_and_nacelle import DrivetrainAndNacelle

from dnv_bladed_models.external_module_component import ExternalModuleComponent

from dnv_bladed_models.fixed_speed_active_damper import FixedSpeedActiveDamper

from dnv_bladed_models.flexibility import Flexibility

from dnv_bladed_models.independent_pitch_hub import IndependentPitchHub

from dnv_bladed_models.lidar import Lidar

from dnv_bladed_models.linear_passive_damper import LinearPassiveDamper

from dnv_bladed_models.pendulum_damper import PendulumDamper

from dnv_bladed_models.pitch_system import PitchSystem

from dnv_bladed_models.rotation import Rotation

from dnv_bladed_models.superelement import Superelement

from dnv_bladed_models.tower import Tower

from dnv_bladed_models.translation import Translation

from dnv_bladed_models.variable_speed_active_damper import VariableSpeedActiveDamper

from dnv_bladed_models.variable_speed_generator import VariableSpeedGenerator

from dnv_bladed_models.yaw_system import YawSystem



from .schema_helper import SchemaHelper 
from .models_impl import *

TComponentOptions = TypeVar('TComponentOptions', Blade, DrivetrainAndNacelle, ExternalModuleComponent, FixedSpeedActiveDamper, Flexibility, IndependentPitchHub, Lidar, LinearPassiveDamper, PendulumDamper, PitchSystem, Rotation, Superelement, Tower, Translation, VariableSpeedActiveDamper, VariableSpeedGenerator, YawSystem, ComponentInsert, )

class ComponentLibrary(BladedModel):
    r"""
    A library of Component definitions. Each Component is added with a unique name, used to reference it from nodes in the Turbine Assembly tree.
    
    Attributes
    ----------
    Notes
    -----
    
    """
    _relative_schema_path: str = PrivateAttr('Turbine/ComponentLibrary/ComponentLibrary.json')


    class Config:
        extra = Extra.allow
        validate_assignment = True
        allow_population_by_field_name = True
        pass


    def items_as_inline(self) -> Iterable[Tuple[str, Union[Blade, DrivetrainAndNacelle, ExternalModuleComponent, FixedSpeedActiveDamper, Flexibility, IndependentPitchHub, Lidar, LinearPassiveDamper, PendulumDamper, PitchSystem, Rotation, Superelement, Tower, Translation, VariableSpeedActiveDamper, VariableSpeedGenerator, YawSystem]]]:
        """
        Returns an iterable of key-value pairs for all of the user-supplied entries currently in the library.
        If any of the values are specified with a '$insert', an error is raised.

        Useful when using type-checking development tools, and the type of every entry in the library is known to not be an insert.

        Returns
        -------
        Iterable[Tuple[str, Union[Blade, DrivetrainAndNacelle, ExternalModuleComponent, FixedSpeedActiveDamper, Flexibility, IndependentPitchHub, Lidar, LinearPassiveDamper, PendulumDamper, PitchSystem, Rotation, Superelement, Tower, Translation, VariableSpeedActiveDamper, VariableSpeedGenerator, YawSystem]]]
            A list of model objects, guaranteed to not be an 'insert'.

        Raises
        ------
        TypeError
            If any of the values are not one of the concrete types of Component; i.e. they are specified with a '$insert'.

        Examples
        --------
        >>> for key, Component_obj in obj.items_as_inline():
                print(f"Entry '{key}' is of type Component_obj.ComponentType}")
        """
        for key, val in self.items():
            if isinstance(val, ComponentInsert) or val.is_insert == True:
                raise TypeError(f"Expected element value to be an in-line object, but it is currently in the '$insert' state.")
            yield (key, val)


    def items_as(self, entry_cls: Type[TComponentOptions]) -> Iterable[Tuple[str, TComponentOptions]]:
        """
        Returns an iterable of key-value pairs for all of the user-supplied entries currently in the library,
        ensuring each value is of the specified type, otherwise an error is raised.

        Useful when using type-checking development tools, and the type of every entry in the library is known to be of the same type.

        Returns
        -------
        Iterable[Tuple[str, TComponentOptions]
            A list of key-value tuples, with each value guaranteed to be of the specified type.

        Raises
        ------
        TypeError
            If any of the values are not one of the specified type.

        Examples
        --------
        Get a reference to each entry in the library when each one is a type of Component:
        >>> for key, Blade_obj in obj.items_as(models.Blade):
                # process object
        >>> for key, DrivetrainAndNacelle_obj in obj.items_as(models.DrivetrainAndNacelle):
                # process object
        >>> for key, ExternalModuleComponent_obj in obj.items_as(models.ExternalModuleComponent):
                # process object
        >>> for key, FixedSpeedActiveDamper_obj in obj.items_as(models.FixedSpeedActiveDamper):
                # process object
        >>> for key, Flexibility_obj in obj.items_as(models.Flexibility):
                # process object
        >>> for key, IndependentPitchHub_obj in obj.items_as(models.IndependentPitchHub):
                # process object
        >>> for key, Lidar_obj in obj.items_as(models.Lidar):
                # process object
        >>> for key, LinearPassiveDamper_obj in obj.items_as(models.LinearPassiveDamper):
                # process object
        >>> for key, PendulumDamper_obj in obj.items_as(models.PendulumDamper):
                # process object
        >>> for key, PitchSystem_obj in obj.items_as(models.PitchSystem):
                # process object
        >>> for key, Rotation_obj in obj.items_as(models.Rotation):
                # process object
        >>> for key, Superelement_obj in obj.items_as(models.Superelement):
                # process object
        >>> for key, Tower_obj in obj.items_as(models.Tower):
                # process object
        >>> for key, Translation_obj in obj.items_as(models.Translation):
                # process object
        >>> for key, VariableSpeedActiveDamper_obj in obj.items_as(models.VariableSpeedActiveDamper):
                # process object
        >>> for key, VariableSpeedGenerator_obj in obj.items_as(models.VariableSpeedGenerator):
                # process object
        >>> for key, YawSystem_obj in obj.items_as(models.YawSystem):
                # process object

        Get a reference to each entry in the library, when each one was specified with a '$insert' and read in from a file:
        >>> for key, insert_obj in obj.items_as(models.ComponentInsert):
                # process object
        """
        for key, val in self.items():
            if not isinstance(val, entry_cls):
                raise ValueError(f"Expected value of type '{entry_cls.__name__}' for key '{key}' but found type '{type(val).__name__}'")
            yield (key, val)


    def Component_as_Blade(self, key: Union[str, int]) -> Blade:
        """
        Retrieves a Component entry from the library, guaranteeing it is a Blade; if it is not, an error is raised.

        Useful when using type-checking development tools, and an entry is expected to be a specific type, and not specified with a '$insert'.

        Parameters
        ----------
        key: Union[str, int]
            The key or index of the entry to retrieve.

        Returns
        -------
        Blade
            A model object guaranteed to be a Blade.

        Raises
        ------
        KeyError
            If the key does not exist in the library.

        TypeError
            If the value is not a Blade.

        Examples
        --------
        >>> Blade_obj = library_obj.Component_as_Blade('my_entry_key')
        """
        return self.Component_as(key, Blade)


    def Component_as_DrivetrainAndNacelle(self, key: Union[str, int]) -> DrivetrainAndNacelle:
        """
        Retrieves a Component entry from the library, guaranteeing it is a DrivetrainAndNacelle; if it is not, an error is raised.

        Useful when using type-checking development tools, and an entry is expected to be a specific type, and not specified with a '$insert'.

        Parameters
        ----------
        key: Union[str, int]
            The key or index of the entry to retrieve.

        Returns
        -------
        DrivetrainAndNacelle
            A model object guaranteed to be a DrivetrainAndNacelle.

        Raises
        ------
        KeyError
            If the key does not exist in the library.

        TypeError
            If the value is not a DrivetrainAndNacelle.

        Examples
        --------
        >>> DrivetrainAndNacelle_obj = library_obj.Component_as_DrivetrainAndNacelle('my_entry_key')
        """
        return self.Component_as(key, DrivetrainAndNacelle)


    def Component_as_ExternalModuleComponent(self, key: Union[str, int]) -> ExternalModuleComponent:
        """
        Retrieves a Component entry from the library, guaranteeing it is a ExternalModuleComponent; if it is not, an error is raised.

        Useful when using type-checking development tools, and an entry is expected to be a specific type, and not specified with a '$insert'.

        Parameters
        ----------
        key: Union[str, int]
            The key or index of the entry to retrieve.

        Returns
        -------
        ExternalModuleComponent
            A model object guaranteed to be a ExternalModuleComponent.

        Raises
        ------
        KeyError
            If the key does not exist in the library.

        TypeError
            If the value is not a ExternalModuleComponent.

        Examples
        --------
        >>> ExternalModuleComponent_obj = library_obj.Component_as_ExternalModuleComponent('my_entry_key')
        """
        return self.Component_as(key, ExternalModuleComponent)


    def Component_as_FixedSpeedActiveDamper(self, key: Union[str, int]) -> FixedSpeedActiveDamper:
        """
        Retrieves a Component entry from the library, guaranteeing it is a FixedSpeedActiveDamper; if it is not, an error is raised.

        Useful when using type-checking development tools, and an entry is expected to be a specific type, and not specified with a '$insert'.

        Parameters
        ----------
        key: Union[str, int]
            The key or index of the entry to retrieve.

        Returns
        -------
        FixedSpeedActiveDamper
            A model object guaranteed to be a FixedSpeedActiveDamper.

        Raises
        ------
        KeyError
            If the key does not exist in the library.

        TypeError
            If the value is not a FixedSpeedActiveDamper.

        Examples
        --------
        >>> FixedSpeedActiveDamper_obj = library_obj.Component_as_FixedSpeedActiveDamper('my_entry_key')
        """
        return self.Component_as(key, FixedSpeedActiveDamper)


    def Component_as_Flexibility(self, key: Union[str, int]) -> Flexibility:
        """
        Retrieves a Component entry from the library, guaranteeing it is a Flexibility; if it is not, an error is raised.

        Useful when using type-checking development tools, and an entry is expected to be a specific type, and not specified with a '$insert'.

        Parameters
        ----------
        key: Union[str, int]
            The key or index of the entry to retrieve.

        Returns
        -------
        Flexibility
            A model object guaranteed to be a Flexibility.

        Raises
        ------
        KeyError
            If the key does not exist in the library.

        TypeError
            If the value is not a Flexibility.

        Examples
        --------
        >>> Flexibility_obj = library_obj.Component_as_Flexibility('my_entry_key')
        """
        return self.Component_as(key, Flexibility)


    def Component_as_IndependentPitchHub(self, key: Union[str, int]) -> IndependentPitchHub:
        """
        Retrieves a Component entry from the library, guaranteeing it is a IndependentPitchHub; if it is not, an error is raised.

        Useful when using type-checking development tools, and an entry is expected to be a specific type, and not specified with a '$insert'.

        Parameters
        ----------
        key: Union[str, int]
            The key or index of the entry to retrieve.

        Returns
        -------
        IndependentPitchHub
            A model object guaranteed to be a IndependentPitchHub.

        Raises
        ------
        KeyError
            If the key does not exist in the library.

        TypeError
            If the value is not a IndependentPitchHub.

        Examples
        --------
        >>> IndependentPitchHub_obj = library_obj.Component_as_IndependentPitchHub('my_entry_key')
        """
        return self.Component_as(key, IndependentPitchHub)


    def Component_as_Lidar(self, key: Union[str, int]) -> Lidar:
        """
        Retrieves a Component entry from the library, guaranteeing it is a Lidar; if it is not, an error is raised.

        Useful when using type-checking development tools, and an entry is expected to be a specific type, and not specified with a '$insert'.

        Parameters
        ----------
        key: Union[str, int]
            The key or index of the entry to retrieve.

        Returns
        -------
        Lidar
            A model object guaranteed to be a Lidar.

        Raises
        ------
        KeyError
            If the key does not exist in the library.

        TypeError
            If the value is not a Lidar.

        Examples
        --------
        >>> Lidar_obj = library_obj.Component_as_Lidar('my_entry_key')
        """
        return self.Component_as(key, Lidar)


    def Component_as_LinearPassiveDamper(self, key: Union[str, int]) -> LinearPassiveDamper:
        """
        Retrieves a Component entry from the library, guaranteeing it is a LinearPassiveDamper; if it is not, an error is raised.

        Useful when using type-checking development tools, and an entry is expected to be a specific type, and not specified with a '$insert'.

        Parameters
        ----------
        key: Union[str, int]
            The key or index of the entry to retrieve.

        Returns
        -------
        LinearPassiveDamper
            A model object guaranteed to be a LinearPassiveDamper.

        Raises
        ------
        KeyError
            If the key does not exist in the library.

        TypeError
            If the value is not a LinearPassiveDamper.

        Examples
        --------
        >>> LinearPassiveDamper_obj = library_obj.Component_as_LinearPassiveDamper('my_entry_key')
        """
        return self.Component_as(key, LinearPassiveDamper)


    def Component_as_PendulumDamper(self, key: Union[str, int]) -> PendulumDamper:
        """
        Retrieves a Component entry from the library, guaranteeing it is a PendulumDamper; if it is not, an error is raised.

        Useful when using type-checking development tools, and an entry is expected to be a specific type, and not specified with a '$insert'.

        Parameters
        ----------
        key: Union[str, int]
            The key or index of the entry to retrieve.

        Returns
        -------
        PendulumDamper
            A model object guaranteed to be a PendulumDamper.

        Raises
        ------
        KeyError
            If the key does not exist in the library.

        TypeError
            If the value is not a PendulumDamper.

        Examples
        --------
        >>> PendulumDamper_obj = library_obj.Component_as_PendulumDamper('my_entry_key')
        """
        return self.Component_as(key, PendulumDamper)


    def Component_as_PitchSystem(self, key: Union[str, int]) -> PitchSystem:
        """
        Retrieves a Component entry from the library, guaranteeing it is a PitchSystem; if it is not, an error is raised.

        Useful when using type-checking development tools, and an entry is expected to be a specific type, and not specified with a '$insert'.

        Parameters
        ----------
        key: Union[str, int]
            The key or index of the entry to retrieve.

        Returns
        -------
        PitchSystem
            A model object guaranteed to be a PitchSystem.

        Raises
        ------
        KeyError
            If the key does not exist in the library.

        TypeError
            If the value is not a PitchSystem.

        Examples
        --------
        >>> PitchSystem_obj = library_obj.Component_as_PitchSystem('my_entry_key')
        """
        return self.Component_as(key, PitchSystem)


    def Component_as_Rotation(self, key: Union[str, int]) -> Rotation:
        """
        Retrieves a Component entry from the library, guaranteeing it is a Rotation; if it is not, an error is raised.

        Useful when using type-checking development tools, and an entry is expected to be a specific type, and not specified with a '$insert'.

        Parameters
        ----------
        key: Union[str, int]
            The key or index of the entry to retrieve.

        Returns
        -------
        Rotation
            A model object guaranteed to be a Rotation.

        Raises
        ------
        KeyError
            If the key does not exist in the library.

        TypeError
            If the value is not a Rotation.

        Examples
        --------
        >>> Rotation_obj = library_obj.Component_as_Rotation('my_entry_key')
        """
        return self.Component_as(key, Rotation)


    def Component_as_Superelement(self, key: Union[str, int]) -> Superelement:
        """
        Retrieves a Component entry from the library, guaranteeing it is a Superelement; if it is not, an error is raised.

        Useful when using type-checking development tools, and an entry is expected to be a specific type, and not specified with a '$insert'.

        Parameters
        ----------
        key: Union[str, int]
            The key or index of the entry to retrieve.

        Returns
        -------
        Superelement
            A model object guaranteed to be a Superelement.

        Raises
        ------
        KeyError
            If the key does not exist in the library.

        TypeError
            If the value is not a Superelement.

        Examples
        --------
        >>> Superelement_obj = library_obj.Component_as_Superelement('my_entry_key')
        """
        return self.Component_as(key, Superelement)


    def Component_as_Tower(self, key: Union[str, int]) -> Tower:
        """
        Retrieves a Component entry from the library, guaranteeing it is a Tower; if it is not, an error is raised.

        Useful when using type-checking development tools, and an entry is expected to be a specific type, and not specified with a '$insert'.

        Parameters
        ----------
        key: Union[str, int]
            The key or index of the entry to retrieve.

        Returns
        -------
        Tower
            A model object guaranteed to be a Tower.

        Raises
        ------
        KeyError
            If the key does not exist in the library.

        TypeError
            If the value is not a Tower.

        Examples
        --------
        >>> Tower_obj = library_obj.Component_as_Tower('my_entry_key')
        """
        return self.Component_as(key, Tower)


    def Component_as_Translation(self, key: Union[str, int]) -> Translation:
        """
        Retrieves a Component entry from the library, guaranteeing it is a Translation; if it is not, an error is raised.

        Useful when using type-checking development tools, and an entry is expected to be a specific type, and not specified with a '$insert'.

        Parameters
        ----------
        key: Union[str, int]
            The key or index of the entry to retrieve.

        Returns
        -------
        Translation
            A model object guaranteed to be a Translation.

        Raises
        ------
        KeyError
            If the key does not exist in the library.

        TypeError
            If the value is not a Translation.

        Examples
        --------
        >>> Translation_obj = library_obj.Component_as_Translation('my_entry_key')
        """
        return self.Component_as(key, Translation)


    def Component_as_VariableSpeedActiveDamper(self, key: Union[str, int]) -> VariableSpeedActiveDamper:
        """
        Retrieves a Component entry from the library, guaranteeing it is a VariableSpeedActiveDamper; if it is not, an error is raised.

        Useful when using type-checking development tools, and an entry is expected to be a specific type, and not specified with a '$insert'.

        Parameters
        ----------
        key: Union[str, int]
            The key or index of the entry to retrieve.

        Returns
        -------
        VariableSpeedActiveDamper
            A model object guaranteed to be a VariableSpeedActiveDamper.

        Raises
        ------
        KeyError
            If the key does not exist in the library.

        TypeError
            If the value is not a VariableSpeedActiveDamper.

        Examples
        --------
        >>> VariableSpeedActiveDamper_obj = library_obj.Component_as_VariableSpeedActiveDamper('my_entry_key')
        """
        return self.Component_as(key, VariableSpeedActiveDamper)


    def Component_as_VariableSpeedGenerator(self, key: Union[str, int]) -> VariableSpeedGenerator:
        """
        Retrieves a Component entry from the library, guaranteeing it is a VariableSpeedGenerator; if it is not, an error is raised.

        Useful when using type-checking development tools, and an entry is expected to be a specific type, and not specified with a '$insert'.

        Parameters
        ----------
        key: Union[str, int]
            The key or index of the entry to retrieve.

        Returns
        -------
        VariableSpeedGenerator
            A model object guaranteed to be a VariableSpeedGenerator.

        Raises
        ------
        KeyError
            If the key does not exist in the library.

        TypeError
            If the value is not a VariableSpeedGenerator.

        Examples
        --------
        >>> VariableSpeedGenerator_obj = library_obj.Component_as_VariableSpeedGenerator('my_entry_key')
        """
        return self.Component_as(key, VariableSpeedGenerator)


    def Component_as_YawSystem(self, key: Union[str, int]) -> YawSystem:
        """
        Retrieves a Component entry from the library, guaranteeing it is a YawSystem; if it is not, an error is raised.

        Useful when using type-checking development tools, and an entry is expected to be a specific type, and not specified with a '$insert'.

        Parameters
        ----------
        key: Union[str, int]
            The key or index of the entry to retrieve.

        Returns
        -------
        YawSystem
            A model object guaranteed to be a YawSystem.

        Raises
        ------
        KeyError
            If the key does not exist in the library.

        TypeError
            If the value is not a YawSystem.

        Examples
        --------
        >>> YawSystem_obj = library_obj.Component_as_YawSystem('my_entry_key')
        """
        return self.Component_as(key, YawSystem)


    def Component_as_inline(self, key: Union[str, int]) -> Union[Blade, DrivetrainAndNacelle, ExternalModuleComponent, FixedSpeedActiveDamper, Flexibility, IndependentPitchHub, Lidar, LinearPassiveDamper, PendulumDamper, PitchSystem, Rotation, Superelement, Tower, Translation, VariableSpeedActiveDamper, VariableSpeedGenerator, YawSystem]:
        """
        Retrieves a Component from the library, if the value is specified with a '$insert', an error is raised.

        Parameters
        ----------
        key: Union[str, int]
            The key or index of the entry to retrieve.

        Returns
        -------
        Union[Blade, DrivetrainAndNacelle, ExternalModuleComponent, FixedSpeedActiveDamper, Flexibility, IndependentPitchHub, Lidar, LinearPassiveDamper, PendulumDamper, PitchSystem, Rotation, Superelement, Tower, Translation, VariableSpeedActiveDamper, VariableSpeedGenerator, YawSystem]
            A model object that could be any of the concrete types of Component specified in-line (and not a '$insert').

        Raises
        ------
        KeyError
            If the key does not exist in the library.

        TypeError
            If the value is not one of the concrete types of Component; i.e. it is specified with a '$insert'.

        Examples
        --------
        >>> Component_obj = library_obj.Component_as_inline('my_entry_key')
        """
        val = self.__getitem__(key)
        if isinstance(val, ComponentInsert) or val.is_insert == True:
            raise TypeError(f"Expected entry value at '{key}' to be an in-line object, but it is currently in the 'insert' state.")
        return val


    def Component_as(self, key: Union[str, int], entry_cls: Type[TComponentOptions]) -> TComponentOptions:
        """
        Retrieves an object from the library, ensuring it is of the specified type.
        The specified type must be one of the valid concrete types of Component, or the '$insert' type
        (in the case the model is defined to be inserted from an external resource).

        Useful when using type-checking development tools, as it provides a concise way to access a value with the correct type.

        Parameters
        ----------
        key: Union[str, int]
            The key or index of the entry to retrieve.

        entry_cls: Type[Union[Blade, DrivetrainAndNacelle, ExternalModuleComponent, FixedSpeedActiveDamper, Flexibility, IndependentPitchHub, Lidar, LinearPassiveDamper, PendulumDamper, PitchSystem, Rotation, Superelement, Tower, Translation, VariableSpeedActiveDamper, VariableSpeedGenerator, YawSystem, ComponentInsert]]
            One of the valid concrete types of Component, or the '$insert' type
            (in the case the model is defined to be inserted from an external resource).

        Returns
        -------
        TComponentOptions
            A model object of the specified type.

        Raises
        ------
        KeyError
            If the key does not exist in the library, or if the index is out of range.

        ValueError
            If the model object for the specified key is not of the specified type.

        Examples
        --------
        Get a reference to an entry as one of the types of Component (including the '$insert' type):
        >>> Blade_obj = library_obj.Component_as('my_entry_key', models.Blade)
        >>> DrivetrainAndNacelle_obj = library_obj.Component_as('my_entry_key', models.DrivetrainAndNacelle)
        >>> ExternalModuleComponent_obj = library_obj.Component_as('my_entry_key', models.ExternalModuleComponent)
        >>> FixedSpeedActiveDamper_obj = library_obj.Component_as('my_entry_key', models.FixedSpeedActiveDamper)
        >>> Flexibility_obj = library_obj.Component_as('my_entry_key', models.Flexibility)
        >>> IndependentPitchHub_obj = library_obj.Component_as('my_entry_key', models.IndependentPitchHub)
        >>> Lidar_obj = library_obj.Component_as('my_entry_key', models.Lidar)
        >>> LinearPassiveDamper_obj = library_obj.Component_as('my_entry_key', models.LinearPassiveDamper)
        >>> PendulumDamper_obj = library_obj.Component_as('my_entry_key', models.PendulumDamper)
        >>> PitchSystem_obj = library_obj.Component_as('my_entry_key', models.PitchSystem)
        >>> Rotation_obj = library_obj.Component_as('my_entry_key', models.Rotation)
        >>> Superelement_obj = library_obj.Component_as('my_entry_key', models.Superelement)
        >>> Tower_obj = library_obj.Component_as('my_entry_key', models.Tower)
        >>> Translation_obj = library_obj.Component_as('my_entry_key', models.Translation)
        >>> VariableSpeedActiveDamper_obj = library_obj.Component_as('my_entry_key', models.VariableSpeedActiveDamper)
        >>> VariableSpeedGenerator_obj = library_obj.Component_as('my_entry_key', models.VariableSpeedGenerator)
        >>> YawSystem_obj = library_obj.Component_as('my_entry_key', models.YawSystem)

        Get a reference to the value, when it was specified with a '$insert' and read in from a file:
        >>> insert_obj = library_obj.Component_as('my_entry_key', models.ComponentInsert)
        """
        val = self.__getitem__(key)
        if not isinstance(val, entry_cls):
            raise ValueError(f"Expected value of type '{entry_cls.__name__}' for key '{key}' but found type '{type(val).__name__}'")
        return val


    def items(self) -> list[tuple[str, Union[Blade, DrivetrainAndNacelle, ExternalModuleComponent, FixedSpeedActiveDamper, Flexibility, IndependentPitchHub, Lidar, LinearPassiveDamper, PendulumDamper, PitchSystem, Rotation, Superelement, Tower, Translation, VariableSpeedActiveDamper, VariableSpeedGenerator, YawSystem, ComponentInsert]]]:
        """
        Returns a list of key-value pairs for all of the user-supplied entries currently in the model.
        """
        return [(k, self.__dict__[k]) for k in self.__dict__ if k not in self.__fields__]


    def keys(self) -> list[str]:
        """
        Returns a list of keys for all of the user-supplied entries currently in the model.
        """
        return [k for k in self.__dict__ if k not in self.__fields__]


    def values(self) -> list[Union[Blade, DrivetrainAndNacelle, ExternalModuleComponent, FixedSpeedActiveDamper, Flexibility, IndependentPitchHub, Lidar, LinearPassiveDamper, PendulumDamper, PitchSystem, Rotation, Superelement, Tower, Translation, VariableSpeedActiveDamper, VariableSpeedGenerator, YawSystem, ComponentInsert]]:
        """
        Returns a list of model objects for all of the user-supplied entries currently in the model.
        """
        return [self.__dict__[k] for k in self.__dict__ if k not in self.__fields__]


    def __len__(self):
        return len([k for k in self.__dict__ if k not in self.__fields__])


    def __contains__(self, item):
        for k in self.__dict__:
            if k not in self.__fields__ and k == item:
                return True
        return False


    def __getitem__(self, key: Union[str, int]) -> Union[Blade, DrivetrainAndNacelle, ExternalModuleComponent, FixedSpeedActiveDamper, Flexibility, IndependentPitchHub, Lidar, LinearPassiveDamper, PendulumDamper, PitchSystem, Rotation, Superelement, Tower, Translation, VariableSpeedActiveDamper, VariableSpeedGenerator, YawSystem, ComponentInsert]:
        if isinstance(key, int):
            keys = self.keys()
            if len(keys) == 0:
                raise KeyError(f"There are currently no entries in the model object.")
            if key < 0 or key >= len(keys):
                raise KeyError(f"Invalid index specified: {key} (0 >= i < {len(keys)})")
            key = keys[key]
        elif isinstance(key, str):
            if key in self.__fields__:
                raise KeyError(f"Item accessors can only be used for custom entries. '{key}' is a pre-defined model property.")
            if not key in self.__dict__:
                raise KeyError(f"There is no entry with key '{key}'.")
        return getattr(self, key)


    def __setitem__(self, key: str, value: Union[Blade, DrivetrainAndNacelle, ExternalModuleComponent, FixedSpeedActiveDamper, Flexibility, IndependentPitchHub, Lidar, LinearPassiveDamper, PendulumDamper, PitchSystem, Rotation, Superelement, Tower, Translation, VariableSpeedActiveDamper, VariableSpeedGenerator, YawSystem, ComponentInsert]):
        if not isinstance(key, str):
            raise KeyError(f"Custom entries can only be added with string keys")
        if key in self.__fields__:
            raise KeyError(f"Item accessors can only be used for custom entries. '{key}' is a pre-defined model property.")
        if not isinstance(value, Component) and not isinstance(value, ComponentInsert):
            raise TypeError(f"Entries must be of type 'Union[Blade, DrivetrainAndNacelle, ExternalModuleComponent, FixedSpeedActiveDamper, Flexibility, IndependentPitchHub, Lidar, LinearPassiveDamper, PendulumDamper, PitchSystem, Rotation, Superelement, Tower, Translation, VariableSpeedActiveDamper, VariableSpeedGenerator, YawSystem, ComponentInsert]'; received '{type(value).__name__}'")
        setattr(self, key, value)


    def __delitem__(self, key: Union[str, int]):
        if isinstance(key, int):
            keys = self.keys()
            if len(keys) == 0:
                raise KeyError(f"There are currently no entries in the model object.")
            if key < 0 or key >= len(keys):
                raise KeyError(f"Invalid index specified: {key} (0 >= i < {len(keys)})")
            key = keys[key]
        elif isinstance(key, str):
            if key in self.__fields__:
                raise KeyError(f"Item accessors can only be used for custom entries. '{key}' is a pre-defined model property.")
            if not key in self.__dict__:
                raise KeyError(f"There is no entry with key '{key}'.")
        delattr(self, key)


    def __setattr__(self, name: str, value: Union[Blade, DrivetrainAndNacelle, ExternalModuleComponent, FixedSpeedActiveDamper, Flexibility, IndependentPitchHub, Lidar, LinearPassiveDamper, PendulumDamper, PitchSystem, Rotation, Superelement, Tower, Translation, VariableSpeedActiveDamper, VariableSpeedGenerator, YawSystem, ComponentInsert]):
        if not name in self.__fields__ and not isinstance(value, Component) and not isinstance(value, ComponentInsert):
            raise TypeError(f"Entries must be of type 'Union[Blade, DrivetrainAndNacelle, ExternalModuleComponent, FixedSpeedActiveDamper, Flexibility, IndependentPitchHub, Lidar, LinearPassiveDamper, PendulumDamper, PitchSystem, Rotation, Superelement, Tower, Translation, VariableSpeedActiveDamper, VariableSpeedGenerator, YawSystem, ComponentInsert]'; received '{type(value).__name__}'")
        super().__setattr__(name, value)



    class __CustomEntries__(BaseModel):
        entries: Dict[str, Annotated[Union[Blade, DrivetrainAndNacelle, ExternalModuleComponent, FixedSpeedActiveDamper, Flexibility, IndependentPitchHub, Lidar, LinearPassiveDamper, PendulumDamper, PitchSystem, Rotation, Superelement, Tower, Translation, VariableSpeedActiveDamper, VariableSpeedGenerator, YawSystem, ComponentInsert], Field(discriminator='ComponentType')]]


    @classmethod
    def __get_validators__(cls):
        yield cls._factory


    @classmethod
    def _factory(cls, data):
        if isinstance(data, ComponentLibrary):
            return data
        if not isinstance(data, dict):
            raise TypeError('An object is required to define ComponentLibrary models')
        return ComponentLibrary.parse_obj(data)


    @classmethod
    def parse_obj(cls: Type['Model'], obj: Any) -> 'Model':
        return custom_entries_parser(cls, obj, dict, ComponentLibrary.__CustomEntries__, lambda entry_key, entry_val: prepare_dict_for_discriminated_insert(cls, entry_key, entry_val, 'ComponentType'))

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
        ComponentLibrary
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = ComponentLibrary.from_file('/path/to/file')
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
        ComponentLibrary
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = ComponentLibrary.from_json('{ ... }')
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
        ComponentLibrary
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


ComponentLibrary.update_forward_refs()
ComponentLibrary.__CustomEntries__.update_forward_refs()
