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

from dnv_bladed_models.angle_vs_stiffness_torque import AngleVsStiffnessTorque

from dnv_bladed_models.damper import Damper

from dnv_bladed_models.pendulum_damper_mounting_position import PendulumDamperMountingPosition

from dnv_bladed_models.velocity_vs_damping_torque import VelocityVsDampingTorque



from .schema_helper import SchemaHelper 
from .models_impl import *


class PendulumDamper(Damper):
    r"""
    A \"pendulum\" or \"tuned mass\" damper, which uses a suspended mass to damp oscillations in a tower.
    
    Not supported yet.
    
    Attributes
    ----------
    ComponentType : Literal['PendulumDamper'], default='PendulumDamper', Not supported yet
        Defines the specific type of Component model in use.  For a `PendulumDamper` object, this must always be set to a value of `PendulumDamper`.
    
    Length : float, Not supported yet
        The length of the (rigid) pendulum arm.
    
    Mass : float, Not supported yet
        The mass suspended at the end of the pendulum arm.
    
    Inertia : float, Not supported yet
        Any added inertia for the pendulum.
    
    Stiffness : float, Not supported yet
        The constant stiffness term for the hinge of the pendulum.  This is in addition to the non-linear terms defined in the AngleVsStiffnessTorque parameter.
    
    Damping : float, Not supported yet
        The constant damping term for the hinge of the pendulum.  This is in addition to the non-linear terms defined in the VelocityVsDampingTorque parameter.
    
    InitialAngle : float, Not supported yet
        The initial angle of the pendulum at the beginning of the simulation.
    
    ConstantFriction : float, Not supported yet
        The constant friction torque applied to rotational hinge.  Any other friction contributions will be in addition to this.
    
    AngleVsStiffnessTorque : List[AngleVsStiffnessTorque], Not supported yet
        A look-up table of additional stiffnesses that vary with the pendulum's position.
    
    VelocityVsDampingTorque : List[VelocityVsDampingTorque], Not supported yet
        A look-up table of additional damping that vary with the pendulum's velocity.
    
    MountingPosition : PendulumDamperMountingPosition, Not supported yet
    
    Notes
    -----
    This model is not supported yet by the Bladed calculation engine.
    """
    _relative_schema_path: str = PrivateAttr('Components/Damper/PendulumDamper.json')

    ComponentType: Literal['PendulumDamper'] = Field(alias="ComponentType", default='PendulumDamper', allow_mutation=False, const=True) # Not supported yet
    Length: float = Field(alias="Length", default=None) # Not supported yet
    Mass: float = Field(alias="Mass", default=None) # Not supported yet
    Inertia: float = Field(alias="Inertia", default=None) # Not supported yet
    Stiffness: float = Field(alias="Stiffness", default=None) # Not supported yet
    Damping: float = Field(alias="Damping", default=None) # Not supported yet
    InitialAngle: float = Field(alias="InitialAngle", default=None) # Not supported yet
    ConstantFriction: float = Field(alias="ConstantFriction", default=None) # Not supported yet
    AngleVsStiffnessTorque: List[AngleVsStiffnessTorque] = Field(alias="AngleVsStiffnessTorque", default=list()) # Not supported yet
    VelocityVsDampingTorque: List[VelocityVsDampingTorque] = Field(alias="VelocityVsDampingTorque", default=list()) # Not supported yet
    MountingPosition: PendulumDamperMountingPosition = Field(alias="MountingPosition", default=None) # Not supported yet

    class Config:
        extra = Extra.forbid
        validate_assignment = True
        allow_population_by_field_name = True
        pass


    @classmethod
    def parse_obj(cls: Type['Model'], obj: Any) -> 'Model':
        discriminated_props = [
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
        if isinstance(data, PendulumDamper):
            return data
        if not isinstance(data, dict):
            raise TypeError('An object is required to define PendulumDamper models')
        return PendulumDamper.parse_obj(data)


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
        if self.AngleVsStiffnessTorque is not None and len(self.AngleVsStiffnessTorque) == 0: #type: ignore
            unused_containers.add('AngleVsStiffnessTorque')
        if self.VelocityVsDampingTorque is not None and len(self.VelocityVsDampingTorque) == 0: #type: ignore
            unused_containers.add('VelocityVsDampingTorque')
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
        PendulumDamper
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = PendulumDamper.from_file('/path/to/file')
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
        PendulumDamper
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = PendulumDamper.from_json('{ ... }')
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
        PendulumDamper
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


PendulumDamper.update_forward_refs()
