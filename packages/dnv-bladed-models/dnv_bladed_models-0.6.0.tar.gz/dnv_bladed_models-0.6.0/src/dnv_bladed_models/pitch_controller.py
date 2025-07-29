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

from dnv_bladed_models.pitch_actuation_limited import PitchActuationLimited

from dnv_bladed_models.pitch_constant_rate_safety_system import PitchConstantRateSafetySystem

from dnv_bladed_models.pitch_position_demand import PitchPositionDemand

from dnv_bladed_models.pitch_rate_demand import PitchRateDemand

from dnv_bladed_models.pitch_rate_demand_set_by_external_controller import PitchRateDemandSetByExternalController

from dnv_bladed_models.pitch_rate_varies_with_position import PitchRateVariesWithPosition

from dnv_bladed_models.pitch_rate_varies_with_time import PitchRateVariesWithTime

from dnv_bladed_models.pitch_safety_system import PitchSafetySystem

from dnv_bladed_models.pitch_safety_system_insert import PitchSafetySystemInsert

from dnv_bladed_models.pitch_system_demand import PitchSystemDemand

from dnv_bladed_models.pitch_system_demand_insert import PitchSystemDemandInsert

from dnv_bladed_models.pitch_torque_set_by_external_controller import PitchTorqueSetByExternalController



from .schema_helper import SchemaHelper 
from .models_impl import *

TPitchSystemDemandOptions = TypeVar('TPitchSystemDemandOptions', PitchPositionDemand, PitchRateDemand, PitchSystemDemandInsert, PitchSystemDemand, )
TPitchSafetySystemOptions = TypeVar('TPitchSafetySystemOptions', PitchActuationLimited, PitchConstantRateSafetySystem, PitchRateDemandSetByExternalController, PitchRateVariesWithPosition, PitchRateVariesWithTime, PitchTorqueSetByExternalController, PitchSafetySystemInsert, PitchSafetySystem, )

class PitchController(BladedModel):
    r"""
    The definition of the pitch controller.  The pitch system generally has its own independent controller (usually physically separate) which received position or rate demands from the main controller.
    
    Attributes
    ----------
    Demand : Union[PitchPositionDemand, PitchRateDemand, PitchSystemDemandInsert]
    
    SafetySystem : Union[PitchActuationLimited, PitchConstantRateSafetySystem, PitchRateDemandSetByExternalController, PitchRateVariesWithPosition, PitchRateVariesWithTime, PitchTorqueSetByExternalController, PitchSafetySystemInsert]
    
    Notes
    -----
    
    """
    _relative_schema_path: str = PrivateAttr('Components/PitchSystem/PitchController/PitchController.json')

    Demand: Union[PitchPositionDemand, PitchRateDemand, PitchSystemDemandInsert] = Field(alias="Demand", default=None, discriminator='PitchSystemDemandType')
    SafetySystem: Union[PitchActuationLimited, PitchConstantRateSafetySystem, PitchRateDemandSetByExternalController, PitchRateVariesWithPosition, PitchRateVariesWithTime, PitchTorqueSetByExternalController, PitchSafetySystemInsert] = Field(alias="SafetySystem", default=None, discriminator='PitchSafetySystemType')

    class Config:
        extra = Extra.forbid
        validate_assignment = True
        allow_population_by_field_name = True
        pass


    @classmethod
    def parse_obj(cls: Type['Model'], obj: Any) -> 'Model':
        discriminated_props = [
            ('Demand', 'PitchSystemDemandType'),
            ('SafetySystem', 'PitchSafetySystemType'),
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
        if isinstance(data, PitchController):
            return data
        if not isinstance(data, dict):
            raise TypeError('An object is required to define PitchController models')
        return PitchController.parse_obj(data)


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
    def Demand_as_PitchPositionDemand(self) -> PitchPositionDemand:
        """
        Retrieves the value of Demand guaranteeing it is a PitchPositionDemand; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        PitchPositionDemand
            A model object, guaranteed to be a PitchPositionDemand.

        Raises
        ------
        TypeError
            If the value is not a PitchPositionDemand.
        """
        return self.Demand_as(PitchPositionDemand)


    @property
    def Demand_as_PitchRateDemand(self) -> PitchRateDemand:
        """
        Retrieves the value of Demand guaranteeing it is a PitchRateDemand; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        PitchRateDemand
            A model object, guaranteed to be a PitchRateDemand.

        Raises
        ------
        TypeError
            If the value is not a PitchRateDemand.
        """
        return self.Demand_as(PitchRateDemand)


    @property
    def Demand_as_inline(self) -> Union[PitchPositionDemand, PitchRateDemand]:
        """
        Retrieves the value of Demand as a model object; if the value is specified with a '$insert', an error is raised.

        Returns
        -------
        Union[PitchPositionDemand, PitchRateDemand]
            A model object at the specified index, guaranteed to not be a '$insert'.

        Raises
        ------
        TypeError
            If the value is not one of the concrete types of PitchSystemDemand; i.e. it is specified with a '$insert'.
        """
        if isinstance(self.Demand, PitchSystemDemandInsert) or self.Demand.is_insert:
            raise TypeError(f"Expected Demand value to be an in-line object, but it is currently in the '$insert' state.")
        return self.Demand


    def Demand_as(self, cls: Type[TPitchSystemDemandOptions])-> TPitchSystemDemandOptions:
        """
        Retrieves the value of Demand, ensuring it is of the specified type.
        The specified type must be one of the valid concrete types of PitchSystemDemand, or the '$insert' type
        (in the case the model is defined to be inserted from an external resource).

        Useful when using type-checking development tools, as it provides a concise way to access a value with the correct type.

        Parameters
        ----------
        cls: Type[Union[PitchPositionDemand, PitchRateDemand, PitchSystemDemandInsert]]
            One of the valid concrete types of PitchSystemDemand, or the '$insert' type
            (in the case the model is defined to be inserted from an external resource).

        Returns
        -------
        TPitchSystemDemandOptions
            A model object of the specified type.

        Raises
        ------
        TypeError
            If the value is not of the specified type.

        Examples
        --------
        Get a reference to the value when it is one of the types of PitchSystemDemand:
        >>> val_obj = model_obj.Demand_as(models.PitchPositionDemand)
        >>> val_obj = model_obj.Demand_as(models.PitchRateDemand)

        Get a reference to the value, when it was specified with a '$insert' and read in from a file:
        >>> insert_obj = model_obj.Demand_as(models.PitchSystemDemandInsert)
        """
        if not isinstance(self.Demand, cls):
            raise TypeError(f"Expected Demand of type '{cls.__name__}' but was type '{type(self.Demand).__name__}'")
        return self.Demand


    @property
    def SafetySystem_as_PitchActuationLimited(self) -> PitchActuationLimited:
        """
        Retrieves the value of SafetySystem guaranteeing it is a PitchActuationLimited; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        PitchActuationLimited
            A model object, guaranteed to be a PitchActuationLimited.

        Raises
        ------
        TypeError
            If the value is not a PitchActuationLimited.
        """
        return self.SafetySystem_as(PitchActuationLimited)


    @property
    def SafetySystem_as_PitchConstantRateSafetySystem(self) -> PitchConstantRateSafetySystem:
        """
        Retrieves the value of SafetySystem guaranteeing it is a PitchConstantRateSafetySystem; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        PitchConstantRateSafetySystem
            A model object, guaranteed to be a PitchConstantRateSafetySystem.

        Raises
        ------
        TypeError
            If the value is not a PitchConstantRateSafetySystem.
        """
        return self.SafetySystem_as(PitchConstantRateSafetySystem)


    @property
    def SafetySystem_as_PitchRateDemandSetByExternalController(self) -> PitchRateDemandSetByExternalController:
        """
        Retrieves the value of SafetySystem guaranteeing it is a PitchRateDemandSetByExternalController; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        PitchRateDemandSetByExternalController
            A model object, guaranteed to be a PitchRateDemandSetByExternalController.

        Raises
        ------
        TypeError
            If the value is not a PitchRateDemandSetByExternalController.
        """
        return self.SafetySystem_as(PitchRateDemandSetByExternalController)


    @property
    def SafetySystem_as_PitchRateVariesWithPosition(self) -> PitchRateVariesWithPosition:
        """
        Retrieves the value of SafetySystem guaranteeing it is a PitchRateVariesWithPosition; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        PitchRateVariesWithPosition
            A model object, guaranteed to be a PitchRateVariesWithPosition.

        Raises
        ------
        TypeError
            If the value is not a PitchRateVariesWithPosition.
        """
        return self.SafetySystem_as(PitchRateVariesWithPosition)


    @property
    def SafetySystem_as_PitchRateVariesWithTime(self) -> PitchRateVariesWithTime:
        """
        Retrieves the value of SafetySystem guaranteeing it is a PitchRateVariesWithTime; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        PitchRateVariesWithTime
            A model object, guaranteed to be a PitchRateVariesWithTime.

        Raises
        ------
        TypeError
            If the value is not a PitchRateVariesWithTime.
        """
        return self.SafetySystem_as(PitchRateVariesWithTime)


    @property
    def SafetySystem_as_PitchTorqueSetByExternalController(self) -> PitchTorqueSetByExternalController:
        """
        Retrieves the value of SafetySystem guaranteeing it is a PitchTorqueSetByExternalController; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        PitchTorqueSetByExternalController
            A model object, guaranteed to be a PitchTorqueSetByExternalController.

        Raises
        ------
        TypeError
            If the value is not a PitchTorqueSetByExternalController.
        """
        return self.SafetySystem_as(PitchTorqueSetByExternalController)


    @property
    def SafetySystem_as_inline(self) -> Union[PitchActuationLimited, PitchConstantRateSafetySystem, PitchRateDemandSetByExternalController, PitchRateVariesWithPosition, PitchRateVariesWithTime, PitchTorqueSetByExternalController]:
        """
        Retrieves the value of SafetySystem as a model object; if the value is specified with a '$insert', an error is raised.

        Returns
        -------
        Union[PitchActuationLimited, PitchConstantRateSafetySystem, PitchRateDemandSetByExternalController, PitchRateVariesWithPosition, PitchRateVariesWithTime, PitchTorqueSetByExternalController]
            A model object at the specified index, guaranteed to not be a '$insert'.

        Raises
        ------
        TypeError
            If the value is not one of the concrete types of PitchSafetySystem; i.e. it is specified with a '$insert'.
        """
        if isinstance(self.SafetySystem, PitchSafetySystemInsert) or self.SafetySystem.is_insert:
            raise TypeError(f"Expected SafetySystem value to be an in-line object, but it is currently in the '$insert' state.")
        return self.SafetySystem


    def SafetySystem_as(self, cls: Type[TPitchSafetySystemOptions])-> TPitchSafetySystemOptions:
        """
        Retrieves the value of SafetySystem, ensuring it is of the specified type.
        The specified type must be one of the valid concrete types of PitchSafetySystem, or the '$insert' type
        (in the case the model is defined to be inserted from an external resource).

        Useful when using type-checking development tools, as it provides a concise way to access a value with the correct type.

        Parameters
        ----------
        cls: Type[Union[PitchActuationLimited, PitchConstantRateSafetySystem, PitchRateDemandSetByExternalController, PitchRateVariesWithPosition, PitchRateVariesWithTime, PitchTorqueSetByExternalController, PitchSafetySystemInsert]]
            One of the valid concrete types of PitchSafetySystem, or the '$insert' type
            (in the case the model is defined to be inserted from an external resource).

        Returns
        -------
        TPitchSafetySystemOptions
            A model object of the specified type.

        Raises
        ------
        TypeError
            If the value is not of the specified type.

        Examples
        --------
        Get a reference to the value when it is one of the types of PitchSafetySystem:
        >>> val_obj = model_obj.SafetySystem_as(models.PitchActuationLimited)
        >>> val_obj = model_obj.SafetySystem_as(models.PitchConstantRateSafetySystem)
        >>> val_obj = model_obj.SafetySystem_as(models.PitchRateDemandSetByExternalController)
        >>> val_obj = model_obj.SafetySystem_as(models.PitchRateVariesWithPosition)
        >>> val_obj = model_obj.SafetySystem_as(models.PitchRateVariesWithTime)
        >>> val_obj = model_obj.SafetySystem_as(models.PitchTorqueSetByExternalController)

        Get a reference to the value, when it was specified with a '$insert' and read in from a file:
        >>> insert_obj = model_obj.SafetySystem_as(models.PitchSafetySystemInsert)
        """
        if not isinstance(self.SafetySystem, cls):
            raise TypeError(f"Expected SafetySystem of type '{cls.__name__}' but was type '{type(self.SafetySystem).__name__}'")
        return self.SafetySystem



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
        PitchController
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = PitchController.from_file('/path/to/file')
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
        PitchController
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = PitchController.from_json('{ ... }')
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
        PitchController
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


PitchController.update_forward_refs()
