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

from dnv_bladed_models.extension_pieces import ExtensionPieces

from dnv_bladed_models.hub_connectable_nodes import HubConnectableNodes

from dnv_bladed_models.hub_mass_properties import HubMassProperties

from dnv_bladed_models.hub_output_group_library import HubOutputGroupLibrary

from dnv_bladed_models.mounting_points import MountingPoints

from dnv_bladed_models.spinner import Spinner



class Hub_RotationDirectionEnum(str, Enum):
    CLOCKWISE_VIEWED_FROM_FRONT = "CLOCKWISE_VIEWED_FROM_FRONT"
    ANTICLOCKWISE_VIEWED_FROM_FRONT = "ANTICLOCKWISE_VIEWED_FROM_FRONT"

class Hub_UpwindOrDownwindEnum(str, Enum):
    UPWIND = "UPWIND"
    DOWNWIND = "DOWNWIND"

from .schema_helper import SchemaHelper 
from .models_impl import *


class Hub(Component, ABC):
    r"""
    The common properties shared by all hubs.
    
    Attributes
    ----------
    RotationDirection : Hub_RotationDirectionEnum
        The rotational sense of rotor when viewed from upwind.
    
    UpwindOrDownwind : Hub_UpwindOrDownwindEnum
        Whether the turbine is an upwind turbine (where the rotor is upwind of the nacelle) or a downwind turbine (where the rotor is downwind of the nacelle).
    
    MountingPoints : MountingPoints
    
    ExtensionPieces : ExtensionPieces
    
    MassProperties : HubMassProperties
    
    Spinner : Spinner
    
    ConnectableNodes : HubConnectableNodes, Not supported yet
    
    OutputGroups : HubOutputGroupLibrary, Not supported yet
    
    Notes
    -----
    
    """
    _relative_schema_path: str = PrivateAttr('Components/Hub/common/Hub.json')

    RotationDirection: Hub_RotationDirectionEnum = Field(alias="RotationDirection", default=None)
    UpwindOrDownwind: Hub_UpwindOrDownwindEnum = Field(alias="UpwindOrDownwind", default=None)
    MountingPoints: MountingPoints = Field(alias="MountingPoints", default=None)
    ExtensionPieces: ExtensionPieces = Field(alias="ExtensionPieces", default=None)
    MassProperties: HubMassProperties = Field(alias="MassProperties", default=None)
    Spinner: Spinner = Field(alias="Spinner", default=None)
    ConnectableNodes: HubConnectableNodes = Field(alias="ConnectableNodes", default=HubConnectableNodes()) # Not supported yet
    OutputGroups: HubOutputGroupLibrary = Field(alias="OutputGroups", default=HubOutputGroupLibrary()) # Not supported yet

    @classmethod
    def parse_obj(cls: Type['Model'], obj: Any) -> 'Model':
        discriminated_props = [
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



    def _find_unused_containers(self) -> Set[str]:
        unused_containers: Set[str] = super()._find_unused_containers()
        if self.ConnectableNodes._is_unused():
            unused_containers.add('ConnectableNodes')
        if self.OutputGroups._is_unused():
            unused_containers.add('OutputGroups')
        return unused_containers


    def _is_unused(self) -> bool:
        """
        Returns true if the model has no user-supplied values. This indicates the object should not be rendered in the final JSON output.
        """
        candidate_fields = self.__dict__.values()
        return (len(candidate_fields) == 0 or all(map(lambda f: f is None, candidate_fields))) and super()._is_unused()



Hub.update_forward_refs()
