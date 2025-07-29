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

from dnv_bladed_models.applied_load import AppliedLoad

from dnv_bladed_models.applied_load_insert import AppliedLoadInsert

from dnv_bladed_models.blade_point_loading import BladePointLoading

from dnv_bladed_models.bladed_model import BladedModel

from dnv_bladed_models.controller_fault import ControllerFault

from dnv_bladed_models.emergency_stop_operation import EmergencyStopOperation

from dnv_bladed_models.environment import Environment

from dnv_bladed_models.event import Event

from dnv_bladed_models.event_insert import EventInsert

from dnv_bladed_models.external_module import ExternalModule

from dnv_bladed_models.externally_stepped_simulation import ExternallySteppedSimulation

from dnv_bladed_models.gl2010_icing import GL2010Icing

from dnv_bladed_models.grid_loss import GridLoss

from dnv_bladed_models.iec4_icing import IEC4Icing

from dnv_bladed_models.initial_azimuth_position import InitialAzimuthPosition

from dnv_bladed_models.initial_condition import InitialCondition

from dnv_bladed_models.initial_condition_insert import InitialConditionInsert

from dnv_bladed_models.initial_floating_position import InitialFloatingPosition

from dnv_bladed_models.initial_pitch_position import InitialPitchPosition

from dnv_bladed_models.initial_rotor_speed import InitialRotorSpeed

from dnv_bladed_models.initial_yaw_angle import InitialYawAngle

from dnv_bladed_models.network_frequency_disturbance import NetworkFrequencyDisturbance

from dnv_bladed_models.network_voltage_disturbance import NetworkVoltageDisturbance

from dnv_bladed_models.normal_stop_operation import NormalStopOperation

from dnv_bladed_models.permanently_stuck_pitch_system import PermanentlyStuckPitchSystem

from dnv_bladed_models.pitch_fault_constant_rate import PitchFaultConstantRate

from dnv_bladed_models.pitch_fault_constant_torque import PitchFaultConstantTorque

from dnv_bladed_models.pitch_fault_limp import PitchFaultLimp

from dnv_bladed_models.pitch_fault_seizure import PitchFaultSeizure

from dnv_bladed_models.pitch_fault_seizure_at_angle import PitchFaultSeizureAtAngle

from dnv_bladed_models.rotor_idling_control_state import RotorIdlingControlState

from dnv_bladed_models.rotor_in_power_production import RotorInPowerProduction

from dnv_bladed_models.rotor_parked_control_state import RotorParkedControlState

from dnv_bladed_models.short_circuit import ShortCircuit

from dnv_bladed_models.start_up_operation import StartUpOperation

from dnv_bladed_models.time_domain_outputs import TimeDomainOutputs

from dnv_bladed_models.tower_point_loading import TowerPointLoading

from dnv_bladed_models.yaw_fault_constant_rate import YawFaultConstantRate

from dnv_bladed_models.yaw_fault_constant_torque import YawFaultConstantTorque

from dnv_bladed_models.yaw_fault_limp import YawFaultLimp

from dnv_bladed_models.yaw_manoever import YawManoever



from .schema_helper import SchemaHelper 
from .models_impl import *

TAppliedLoadOptions = TypeVar('TAppliedLoadOptions', BladePointLoading, TowerPointLoading, AppliedLoadInsert, AppliedLoad, )
TInitialConditionOptions = TypeVar('TInitialConditionOptions', GL2010Icing, IEC4Icing, InitialAzimuthPosition, InitialFloatingPosition, InitialPitchPosition, InitialRotorSpeed, InitialYawAngle, RotorIdlingControlState, RotorInPowerProduction, RotorParkedControlState, InitialConditionInsert, InitialCondition, )
TEventOptions = TypeVar('TEventOptions', ControllerFault, EmergencyStopOperation, GridLoss, NetworkFrequencyDisturbance, NetworkVoltageDisturbance, NormalStopOperation, PermanentlyStuckPitchSystem, PitchFaultConstantRate, PitchFaultConstantTorque, PitchFaultLimp, PitchFaultSeizure, PitchFaultSeizureAtAngle, ShortCircuit, StartUpOperation, YawFaultConstantRate, YawFaultConstantTorque, YawFaultLimp, YawManoever, EventInsert, Event, )

class TimeDomainSimulation(BladedModel):
    r"""
    The definition of a time domain analysis - mutually exclusive with 'SteadyCalculation'
    
    Attributes
    ----------
    Duration : float
        The duration of the simulation for which results will be output, excluding the LeadInTime. SI units are seconds.
    
    LeadInTime : float, default=7
        The time that the simulation will run before any outputs are recorded.  This is to allow the simulation to \"settle\", allowing any non-equilibrium initial conditions to converge on their steady state values.  The lead-in time will be added to the duration, meaning that the duration will be the length of time the outputs are recorded for.  Any times specified within the simulation will be measured from the *end* of the lead-in period.
    
    Outputs : TimeDomainOutputs
    
    AdditionalExternalModules : List[ExternalModule], Not supported yet
        A list of external module that will be used for this simulation only.  This could be used to apply loading to the structure, or some other load case specific purpose.  If the external module is seeking to simulate an intrinsic property of the turbine, consider moving it into the GlobalExternalModules, or adding it to the Assembly tree.
    
    ExternallySteppedSimulation : ExternallySteppedSimulation, Not supported yet
    
    Environment : Environment
    
    AppliedLoads : List[Union[BladePointLoading, TowerPointLoading, AppliedLoadInsert]]
        A list of point loading definitions which apply a time history of forces to the structure.
    
    InitialConditions : List[Union[GL2010Icing, IEC4Icing, InitialAzimuthPosition, InitialFloatingPosition, InitialPitchPosition, InitialRotorSpeed, InitialYawAngle, RotorIdlingControlState, RotorInPowerProduction, RotorParkedControlState, InitialConditionInsert]]
        A list of initial conditions to apply at the beginning of the simulation.
    
    Events : List[Union[ControllerFault, EmergencyStopOperation, GridLoss, NetworkFrequencyDisturbance, NetworkVoltageDisturbance, NormalStopOperation, PermanentlyStuckPitchSystem, PitchFaultConstantRate, PitchFaultConstantTorque, PitchFaultLimp, PitchFaultSeizure, PitchFaultSeizureAtAngle, ShortCircuit, StartUpOperation, YawFaultConstantRate, YawFaultConstantTorque, YawFaultLimp, YawManoever, EventInsert]], Not supported yet
        A list of events that occur during the simulation.
    
    Notes
    -----
    
    """
    _relative_schema_path: str = PrivateAttr('TimeDomainSimulation/TimeDomainSimulation.json')

    Duration: float = Field(alias="Duration", default=None)
    LeadInTime: float = Field(alias="LeadInTime", default=None)
    Outputs: TimeDomainOutputs = Field(alias="Outputs", default=None)
    AdditionalExternalModules: List[ExternalModule] = Field(alias="AdditionalExternalModules", default=list()) # Not supported yet
    ExternallySteppedSimulation: ExternallySteppedSimulation = Field(alias="ExternallySteppedSimulation", default=None) # Not supported yet
    Environment: Environment = Field(alias="Environment", default=None)
    AppliedLoads: List[Annotated[Union[BladePointLoading, TowerPointLoading, AppliedLoadInsert], Field(discriminator='AppliedLoadType')]] = Field(alias="AppliedLoads", default=list())
    InitialConditions: List[Annotated[Union[GL2010Icing, IEC4Icing, InitialAzimuthPosition, InitialFloatingPosition, InitialPitchPosition, InitialRotorSpeed, InitialYawAngle, RotorIdlingControlState, RotorInPowerProduction, RotorParkedControlState, InitialConditionInsert], Field(discriminator='InitialConditionType')]] = Field(alias="InitialConditions", default=list())
    Events: List[Annotated[Union[ControllerFault, EmergencyStopOperation, GridLoss, NetworkFrequencyDisturbance, NetworkVoltageDisturbance, NormalStopOperation, PermanentlyStuckPitchSystem, PitchFaultConstantRate, PitchFaultConstantTorque, PitchFaultLimp, PitchFaultSeizure, PitchFaultSeizureAtAngle, ShortCircuit, StartUpOperation, YawFaultConstantRate, YawFaultConstantTorque, YawFaultLimp, YawManoever, EventInsert], Field(discriminator='EventType')]] = Field(alias="Events", default=list()) # Not supported yet

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
            ('AppliedLoads', 'AppliedLoadType'),
            ('InitialConditions', 'InitialConditionType'),
            ('Events', 'EventType'),
        ]
        prepare_model_dict(cls, obj, discriminated_props, discriminated_arrays)
        return super().parse_obj(obj)


    @classmethod
    def __get_validators__(cls):
        yield cls._factory


    @classmethod
    def _factory(cls, data):
        if isinstance(data, TimeDomainSimulation):
            return data
        if not isinstance(data, dict):
            raise TypeError('An object is required to define TimeDomainSimulation models')
        return TimeDomainSimulation.parse_obj(data)


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
    def AppliedLoads_as_inline(self) -> Iterable[Union[BladePointLoading, TowerPointLoading]]:
        """
        Retrieves the value of AppliedLoads as an iterable of model objects; if any of the values are specified with a '$insert', an error is raised.

        Returns
        -------
        Iterable[Union[BladePointLoading, TowerPointLoading]]
            A list of model objects, guaranteed to not be a '$insert'.

        Raises
        ------
        TypeError
            If any of the values are not one of the concrete types of AppliedLoad; i.e. they are specified with an 'insert'.

        Examples
        --------
        >>> for i, AppliedLoad_obj in enumerate(obj.AppliedLoads_as_any):
                print(f"Element {i} is of type AppliedLoad_obj.AppliedLoadType}")

        or

        >>> for AppliedLoad_obj in obj.AppliedLoads_as_any:
                # process object
        """
        for val in self.AppliedLoads:
            if isinstance(val, AppliedLoadInsert) or val.is_insert == True:
                raise TypeError(f"Expected element value to be an in-line object, but it is currently in the '$insert' state.")
            yield val


    def AppliedLoads_element_as_BladePointLoading(self, index: int) -> BladePointLoading:
        """
        Retrieves an object from the AppliedLoads array field, ensuring it is a BladePointLoading.        

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        Returns
        -------
        BladePointLoading
            A model object at the specified index, guaranteed to be a BladePointLoading.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the value at the specified index is not a BladePointLoading.

        Examples
        --------
        Gets a reference to the 2nd element, typed to a BladePointLoading, that is specified in-line:
        >>> entry_obj = obj.AppliedLoads_element_as_BladePointLoading(2)
        """
        return self.AppliedLoads_element_as(index, BladePointLoading)


    def AppliedLoads_element_as_TowerPointLoading(self, index: int) -> TowerPointLoading:
        """
        Retrieves an object from the AppliedLoads array field, ensuring it is a TowerPointLoading.        

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        Returns
        -------
        TowerPointLoading
            A model object at the specified index, guaranteed to be a TowerPointLoading.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the value at the specified index is not a TowerPointLoading.

        Examples
        --------
        Gets a reference to the 2nd element, typed to a TowerPointLoading, that is specified in-line:
        >>> entry_obj = obj.AppliedLoads_element_as_TowerPointLoading(2)
        """
        return self.AppliedLoads_element_as(index, TowerPointLoading)


    def AppliedLoads_element_as_inline(self, index: int) -> Union[BladePointLoading, TowerPointLoading]:
        """
        Retrieves an object from the AppliedLoads array field; if the value is specified with a '$insert', an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        Returns
        -------
        Union[BladePointLoading, TowerPointLoading]
            A model object at the specified index, guaranteed to not be an '$insert'.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the value at the specified index is not one of the concrete types of AppliedLoad; i.e. it is specified with an '$insert'.

        Examples
        --------
        Get a reference to the 2nd element, as any of the concrete types:
        >>> AppliedLoads_obj = obj.AppliedLoads_element_as_inline(2)
        """
        val = self.AppliedLoads[index]
        if isinstance(val, AppliedLoadInsert) or val.is_insert == True:
            raise TypeError(f"Expected element value at '{index}' to be an in-line object, but it is currently in the '$insert' state.")
        return val


    def AppliedLoads_element_as(self, index: int, element_cls: Type[TAppliedLoadOptions]) -> TAppliedLoadOptions:
        """
        Retrieves an object from the AppliedLoads array field, ensuring it is of the specified type.
        The specified type must be one of the valid concrete types of AppliedLoad, or the '$insert' type
        (in the case the model is defined to be inserted from an external resource).

        Useful when using type-checking development tools, as it provides a concise way to access a value with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        element_cls: Type[Union[BladePointLoading, TowerPointLoading, AppliedLoadInsert]]
            One of the valid concrete types of AppliedLoad, or the '$insert' type
            (in the case the model is defined to be inserted from an external resource).

        Returns
        -------
        TAppliedLoadOptions
            A model object of the specified type.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the model object for the specified index is not of the specified type.

        Examples
        --------
        Get a reference to the 2nd element when it was one of the types of AppliedLoad:
        >>> entry_obj = obj.AppliedLoads_element_as(2, models.BladePointLoading)
        >>> entry_obj = obj.AppliedLoads_element_as(2, models.TowerPointLoading)

        Get a reference to the value, when it was specified with a '$insert' and read in from a file:
        >>> insert_obj = obj.AppliedLoads_element_as(2, models.AppliedLoadInsert)
        """
        val = self.AppliedLoads[index]
        if not isinstance(val, element_cls):
            raise TypeError(f"Expected value of type '{element_cls.__name__}' at index {index} but found type '{type(val).__name__}'")
        return val


    @property
    def InitialConditions_as_inline(self) -> Iterable[Union[GL2010Icing, IEC4Icing, InitialAzimuthPosition, InitialFloatingPosition, InitialPitchPosition, InitialRotorSpeed, InitialYawAngle, RotorIdlingControlState, RotorInPowerProduction, RotorParkedControlState]]:
        """
        Retrieves the value of InitialConditions as an iterable of model objects; if any of the values are specified with a '$insert', an error is raised.

        Returns
        -------
        Iterable[Union[GL2010Icing, IEC4Icing, InitialAzimuthPosition, InitialFloatingPosition, InitialPitchPosition, InitialRotorSpeed, InitialYawAngle, RotorIdlingControlState, RotorInPowerProduction, RotorParkedControlState]]
            A list of model objects, guaranteed to not be a '$insert'.

        Raises
        ------
        TypeError
            If any of the values are not one of the concrete types of InitialCondition; i.e. they are specified with an 'insert'.

        Examples
        --------
        >>> for i, InitialCondition_obj in enumerate(obj.InitialConditions_as_any):
                print(f"Element {i} is of type InitialCondition_obj.InitialConditionType}")

        or

        >>> for InitialCondition_obj in obj.InitialConditions_as_any:
                # process object
        """
        for val in self.InitialConditions:
            if isinstance(val, InitialConditionInsert) or val.is_insert == True:
                raise TypeError(f"Expected element value to be an in-line object, but it is currently in the '$insert' state.")
            yield val


    def InitialConditions_element_as_GL2010Icing(self, index: int) -> GL2010Icing:
        """
        Retrieves an object from the InitialConditions array field, ensuring it is a GL2010Icing.        

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        Returns
        -------
        GL2010Icing
            A model object at the specified index, guaranteed to be a GL2010Icing.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the value at the specified index is not a GL2010Icing.

        Examples
        --------
        Gets a reference to the 2nd element, typed to a GL2010Icing, that is specified in-line:
        >>> entry_obj = obj.InitialConditions_element_as_GL2010Icing(2)
        """
        return self.InitialConditions_element_as(index, GL2010Icing)


    def InitialConditions_element_as_IEC4Icing(self, index: int) -> IEC4Icing:
        """
        Retrieves an object from the InitialConditions array field, ensuring it is a IEC4Icing.        

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        Returns
        -------
        IEC4Icing
            A model object at the specified index, guaranteed to be a IEC4Icing.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the value at the specified index is not a IEC4Icing.

        Examples
        --------
        Gets a reference to the 2nd element, typed to a IEC4Icing, that is specified in-line:
        >>> entry_obj = obj.InitialConditions_element_as_IEC4Icing(2)
        """
        return self.InitialConditions_element_as(index, IEC4Icing)


    def InitialConditions_element_as_InitialAzimuthPosition(self, index: int) -> InitialAzimuthPosition:
        """
        Retrieves an object from the InitialConditions array field, ensuring it is a InitialAzimuthPosition.        

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        Returns
        -------
        InitialAzimuthPosition
            A model object at the specified index, guaranteed to be a InitialAzimuthPosition.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the value at the specified index is not a InitialAzimuthPosition.

        Examples
        --------
        Gets a reference to the 2nd element, typed to a InitialAzimuthPosition, that is specified in-line:
        >>> entry_obj = obj.InitialConditions_element_as_InitialAzimuthPosition(2)
        """
        return self.InitialConditions_element_as(index, InitialAzimuthPosition)


    def InitialConditions_element_as_InitialFloatingPosition(self, index: int) -> InitialFloatingPosition:
        """
        Retrieves an object from the InitialConditions array field, ensuring it is a InitialFloatingPosition.        

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        Returns
        -------
        InitialFloatingPosition
            A model object at the specified index, guaranteed to be a InitialFloatingPosition.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the value at the specified index is not a InitialFloatingPosition.

        Examples
        --------
        Gets a reference to the 2nd element, typed to a InitialFloatingPosition, that is specified in-line:
        >>> entry_obj = obj.InitialConditions_element_as_InitialFloatingPosition(2)
        """
        return self.InitialConditions_element_as(index, InitialFloatingPosition)


    def InitialConditions_element_as_InitialPitchPosition(self, index: int) -> InitialPitchPosition:
        """
        Retrieves an object from the InitialConditions array field, ensuring it is a InitialPitchPosition.        

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        Returns
        -------
        InitialPitchPosition
            A model object at the specified index, guaranteed to be a InitialPitchPosition.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the value at the specified index is not a InitialPitchPosition.

        Examples
        --------
        Gets a reference to the 2nd element, typed to a InitialPitchPosition, that is specified in-line:
        >>> entry_obj = obj.InitialConditions_element_as_InitialPitchPosition(2)
        """
        return self.InitialConditions_element_as(index, InitialPitchPosition)


    def InitialConditions_element_as_InitialRotorSpeed(self, index: int) -> InitialRotorSpeed:
        """
        Retrieves an object from the InitialConditions array field, ensuring it is a InitialRotorSpeed.        

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        Returns
        -------
        InitialRotorSpeed
            A model object at the specified index, guaranteed to be a InitialRotorSpeed.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the value at the specified index is not a InitialRotorSpeed.

        Examples
        --------
        Gets a reference to the 2nd element, typed to a InitialRotorSpeed, that is specified in-line:
        >>> entry_obj = obj.InitialConditions_element_as_InitialRotorSpeed(2)
        """
        return self.InitialConditions_element_as(index, InitialRotorSpeed)


    def InitialConditions_element_as_InitialYawAngle(self, index: int) -> InitialYawAngle:
        """
        Retrieves an object from the InitialConditions array field, ensuring it is a InitialYawAngle.        

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        Returns
        -------
        InitialYawAngle
            A model object at the specified index, guaranteed to be a InitialYawAngle.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the value at the specified index is not a InitialYawAngle.

        Examples
        --------
        Gets a reference to the 2nd element, typed to a InitialYawAngle, that is specified in-line:
        >>> entry_obj = obj.InitialConditions_element_as_InitialYawAngle(2)
        """
        return self.InitialConditions_element_as(index, InitialYawAngle)


    def InitialConditions_element_as_RotorIdlingControlState(self, index: int) -> RotorIdlingControlState:
        """
        Retrieves an object from the InitialConditions array field, ensuring it is a RotorIdlingControlState.        

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        Returns
        -------
        RotorIdlingControlState
            A model object at the specified index, guaranteed to be a RotorIdlingControlState.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the value at the specified index is not a RotorIdlingControlState.

        Examples
        --------
        Gets a reference to the 2nd element, typed to a RotorIdlingControlState, that is specified in-line:
        >>> entry_obj = obj.InitialConditions_element_as_RotorIdlingControlState(2)
        """
        return self.InitialConditions_element_as(index, RotorIdlingControlState)


    def InitialConditions_element_as_RotorInPowerProduction(self, index: int) -> RotorInPowerProduction:
        """
        Retrieves an object from the InitialConditions array field, ensuring it is a RotorInPowerProduction.        

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        Returns
        -------
        RotorInPowerProduction
            A model object at the specified index, guaranteed to be a RotorInPowerProduction.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the value at the specified index is not a RotorInPowerProduction.

        Examples
        --------
        Gets a reference to the 2nd element, typed to a RotorInPowerProduction, that is specified in-line:
        >>> entry_obj = obj.InitialConditions_element_as_RotorInPowerProduction(2)
        """
        return self.InitialConditions_element_as(index, RotorInPowerProduction)


    def InitialConditions_element_as_RotorParkedControlState(self, index: int) -> RotorParkedControlState:
        """
        Retrieves an object from the InitialConditions array field, ensuring it is a RotorParkedControlState.        

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        Returns
        -------
        RotorParkedControlState
            A model object at the specified index, guaranteed to be a RotorParkedControlState.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the value at the specified index is not a RotorParkedControlState.

        Examples
        --------
        Gets a reference to the 2nd element, typed to a RotorParkedControlState, that is specified in-line:
        >>> entry_obj = obj.InitialConditions_element_as_RotorParkedControlState(2)
        """
        return self.InitialConditions_element_as(index, RotorParkedControlState)


    def InitialConditions_element_as_inline(self, index: int) -> Union[GL2010Icing, IEC4Icing, InitialAzimuthPosition, InitialFloatingPosition, InitialPitchPosition, InitialRotorSpeed, InitialYawAngle, RotorIdlingControlState, RotorInPowerProduction, RotorParkedControlState]:
        """
        Retrieves an object from the InitialConditions array field; if the value is specified with a '$insert', an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        Returns
        -------
        Union[GL2010Icing, IEC4Icing, InitialAzimuthPosition, InitialFloatingPosition, InitialPitchPosition, InitialRotorSpeed, InitialYawAngle, RotorIdlingControlState, RotorInPowerProduction, RotorParkedControlState]
            A model object at the specified index, guaranteed to not be an '$insert'.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the value at the specified index is not one of the concrete types of InitialCondition; i.e. it is specified with an '$insert'.

        Examples
        --------
        Get a reference to the 2nd element, as any of the concrete types:
        >>> InitialConditions_obj = obj.InitialConditions_element_as_inline(2)
        """
        val = self.InitialConditions[index]
        if isinstance(val, InitialConditionInsert) or val.is_insert == True:
            raise TypeError(f"Expected element value at '{index}' to be an in-line object, but it is currently in the '$insert' state.")
        return val


    def InitialConditions_element_as(self, index: int, element_cls: Type[TInitialConditionOptions]) -> TInitialConditionOptions:
        """
        Retrieves an object from the InitialConditions array field, ensuring it is of the specified type.
        The specified type must be one of the valid concrete types of InitialCondition, or the '$insert' type
        (in the case the model is defined to be inserted from an external resource).

        Useful when using type-checking development tools, as it provides a concise way to access a value with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        element_cls: Type[Union[GL2010Icing, IEC4Icing, InitialAzimuthPosition, InitialFloatingPosition, InitialPitchPosition, InitialRotorSpeed, InitialYawAngle, RotorIdlingControlState, RotorInPowerProduction, RotorParkedControlState, InitialConditionInsert]]
            One of the valid concrete types of InitialCondition, or the '$insert' type
            (in the case the model is defined to be inserted from an external resource).

        Returns
        -------
        TInitialConditionOptions
            A model object of the specified type.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the model object for the specified index is not of the specified type.

        Examples
        --------
        Get a reference to the 2nd element when it was one of the types of InitialCondition:
        >>> entry_obj = obj.InitialConditions_element_as(2, models.GL2010Icing)
        >>> entry_obj = obj.InitialConditions_element_as(2, models.IEC4Icing)
        >>> entry_obj = obj.InitialConditions_element_as(2, models.InitialAzimuthPosition)
        >>> entry_obj = obj.InitialConditions_element_as(2, models.InitialFloatingPosition)
        >>> entry_obj = obj.InitialConditions_element_as(2, models.InitialPitchPosition)
        >>> entry_obj = obj.InitialConditions_element_as(2, models.InitialRotorSpeed)
        >>> entry_obj = obj.InitialConditions_element_as(2, models.InitialYawAngle)
        >>> entry_obj = obj.InitialConditions_element_as(2, models.RotorIdlingControlState)
        >>> entry_obj = obj.InitialConditions_element_as(2, models.RotorInPowerProduction)
        >>> entry_obj = obj.InitialConditions_element_as(2, models.RotorParkedControlState)

        Get a reference to the value, when it was specified with a '$insert' and read in from a file:
        >>> insert_obj = obj.InitialConditions_element_as(2, models.InitialConditionInsert)
        """
        val = self.InitialConditions[index]
        if not isinstance(val, element_cls):
            raise TypeError(f"Expected value of type '{element_cls.__name__}' at index {index} but found type '{type(val).__name__}'")
        return val


    @property
    def Events_as_inline(self) -> Iterable[Union[ControllerFault, EmergencyStopOperation, GridLoss, NetworkFrequencyDisturbance, NetworkVoltageDisturbance, NormalStopOperation, PermanentlyStuckPitchSystem, PitchFaultConstantRate, PitchFaultConstantTorque, PitchFaultLimp, PitchFaultSeizure, PitchFaultSeizureAtAngle, ShortCircuit, StartUpOperation, YawFaultConstantRate, YawFaultConstantTorque, YawFaultLimp, YawManoever]]:
        """
        Retrieves the value of Events as an iterable of model objects; if any of the values are specified with a '$insert', an error is raised.

        Returns
        -------
        Iterable[Union[ControllerFault, EmergencyStopOperation, GridLoss, NetworkFrequencyDisturbance, NetworkVoltageDisturbance, NormalStopOperation, PermanentlyStuckPitchSystem, PitchFaultConstantRate, PitchFaultConstantTorque, PitchFaultLimp, PitchFaultSeizure, PitchFaultSeizureAtAngle, ShortCircuit, StartUpOperation, YawFaultConstantRate, YawFaultConstantTorque, YawFaultLimp, YawManoever]]
            A list of model objects, guaranteed to not be a '$insert'.

        Raises
        ------
        TypeError
            If any of the values are not one of the concrete types of Event; i.e. they are specified with an 'insert'.

        Examples
        --------
        >>> for i, Event_obj in enumerate(obj.Events_as_any):
                print(f"Element {i} is of type Event_obj.EventType}")

        or

        >>> for Event_obj in obj.Events_as_any:
                # process object
        """
        for val in self.Events:
            if isinstance(val, EventInsert) or val.is_insert == True:
                raise TypeError(f"Expected element value to be an in-line object, but it is currently in the '$insert' state.")
            yield val


    def Events_element_as_ControllerFault(self, index: int) -> ControllerFault:
        """
        Retrieves an object from the Events array field, ensuring it is a ControllerFault.        

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        Returns
        -------
        ControllerFault
            A model object at the specified index, guaranteed to be a ControllerFault.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the value at the specified index is not a ControllerFault.

        Examples
        --------
        Gets a reference to the 2nd element, typed to a ControllerFault, that is specified in-line:
        >>> entry_obj = obj.Events_element_as_ControllerFault(2)
        """
        return self.Events_element_as(index, ControllerFault)


    def Events_element_as_EmergencyStopOperation(self, index: int) -> EmergencyStopOperation:
        """
        Retrieves an object from the Events array field, ensuring it is a EmergencyStopOperation.        

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        Returns
        -------
        EmergencyStopOperation
            A model object at the specified index, guaranteed to be a EmergencyStopOperation.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the value at the specified index is not a EmergencyStopOperation.

        Examples
        --------
        Gets a reference to the 2nd element, typed to a EmergencyStopOperation, that is specified in-line:
        >>> entry_obj = obj.Events_element_as_EmergencyStopOperation(2)
        """
        return self.Events_element_as(index, EmergencyStopOperation)


    def Events_element_as_GridLoss(self, index: int) -> GridLoss:
        """
        Retrieves an object from the Events array field, ensuring it is a GridLoss.        

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        Returns
        -------
        GridLoss
            A model object at the specified index, guaranteed to be a GridLoss.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the value at the specified index is not a GridLoss.

        Examples
        --------
        Gets a reference to the 2nd element, typed to a GridLoss, that is specified in-line:
        >>> entry_obj = obj.Events_element_as_GridLoss(2)
        """
        return self.Events_element_as(index, GridLoss)


    def Events_element_as_NetworkFrequencyDisturbance(self, index: int) -> NetworkFrequencyDisturbance:
        """
        Retrieves an object from the Events array field, ensuring it is a NetworkFrequencyDisturbance.        

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        Returns
        -------
        NetworkFrequencyDisturbance
            A model object at the specified index, guaranteed to be a NetworkFrequencyDisturbance.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the value at the specified index is not a NetworkFrequencyDisturbance.

        Examples
        --------
        Gets a reference to the 2nd element, typed to a NetworkFrequencyDisturbance, that is specified in-line:
        >>> entry_obj = obj.Events_element_as_NetworkFrequencyDisturbance(2)
        """
        return self.Events_element_as(index, NetworkFrequencyDisturbance)


    def Events_element_as_NetworkVoltageDisturbance(self, index: int) -> NetworkVoltageDisturbance:
        """
        Retrieves an object from the Events array field, ensuring it is a NetworkVoltageDisturbance.        

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        Returns
        -------
        NetworkVoltageDisturbance
            A model object at the specified index, guaranteed to be a NetworkVoltageDisturbance.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the value at the specified index is not a NetworkVoltageDisturbance.

        Examples
        --------
        Gets a reference to the 2nd element, typed to a NetworkVoltageDisturbance, that is specified in-line:
        >>> entry_obj = obj.Events_element_as_NetworkVoltageDisturbance(2)
        """
        return self.Events_element_as(index, NetworkVoltageDisturbance)


    def Events_element_as_NormalStopOperation(self, index: int) -> NormalStopOperation:
        """
        Retrieves an object from the Events array field, ensuring it is a NormalStopOperation.        

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        Returns
        -------
        NormalStopOperation
            A model object at the specified index, guaranteed to be a NormalStopOperation.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the value at the specified index is not a NormalStopOperation.

        Examples
        --------
        Gets a reference to the 2nd element, typed to a NormalStopOperation, that is specified in-line:
        >>> entry_obj = obj.Events_element_as_NormalStopOperation(2)
        """
        return self.Events_element_as(index, NormalStopOperation)


    def Events_element_as_PermanentlyStuckPitchSystem(self, index: int) -> PermanentlyStuckPitchSystem:
        """
        Retrieves an object from the Events array field, ensuring it is a PermanentlyStuckPitchSystem.        

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        Returns
        -------
        PermanentlyStuckPitchSystem
            A model object at the specified index, guaranteed to be a PermanentlyStuckPitchSystem.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the value at the specified index is not a PermanentlyStuckPitchSystem.

        Examples
        --------
        Gets a reference to the 2nd element, typed to a PermanentlyStuckPitchSystem, that is specified in-line:
        >>> entry_obj = obj.Events_element_as_PermanentlyStuckPitchSystem(2)
        """
        return self.Events_element_as(index, PermanentlyStuckPitchSystem)


    def Events_element_as_PitchFaultConstantRate(self, index: int) -> PitchFaultConstantRate:
        """
        Retrieves an object from the Events array field, ensuring it is a PitchFaultConstantRate.        

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        Returns
        -------
        PitchFaultConstantRate
            A model object at the specified index, guaranteed to be a PitchFaultConstantRate.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the value at the specified index is not a PitchFaultConstantRate.

        Examples
        --------
        Gets a reference to the 2nd element, typed to a PitchFaultConstantRate, that is specified in-line:
        >>> entry_obj = obj.Events_element_as_PitchFaultConstantRate(2)
        """
        return self.Events_element_as(index, PitchFaultConstantRate)


    def Events_element_as_PitchFaultConstantTorque(self, index: int) -> PitchFaultConstantTorque:
        """
        Retrieves an object from the Events array field, ensuring it is a PitchFaultConstantTorque.        

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        Returns
        -------
        PitchFaultConstantTorque
            A model object at the specified index, guaranteed to be a PitchFaultConstantTorque.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the value at the specified index is not a PitchFaultConstantTorque.

        Examples
        --------
        Gets a reference to the 2nd element, typed to a PitchFaultConstantTorque, that is specified in-line:
        >>> entry_obj = obj.Events_element_as_PitchFaultConstantTorque(2)
        """
        return self.Events_element_as(index, PitchFaultConstantTorque)


    def Events_element_as_PitchFaultLimp(self, index: int) -> PitchFaultLimp:
        """
        Retrieves an object from the Events array field, ensuring it is a PitchFaultLimp.        

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        Returns
        -------
        PitchFaultLimp
            A model object at the specified index, guaranteed to be a PitchFaultLimp.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the value at the specified index is not a PitchFaultLimp.

        Examples
        --------
        Gets a reference to the 2nd element, typed to a PitchFaultLimp, that is specified in-line:
        >>> entry_obj = obj.Events_element_as_PitchFaultLimp(2)
        """
        return self.Events_element_as(index, PitchFaultLimp)


    def Events_element_as_PitchFaultSeizure(self, index: int) -> PitchFaultSeizure:
        """
        Retrieves an object from the Events array field, ensuring it is a PitchFaultSeizure.        

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        Returns
        -------
        PitchFaultSeizure
            A model object at the specified index, guaranteed to be a PitchFaultSeizure.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the value at the specified index is not a PitchFaultSeizure.

        Examples
        --------
        Gets a reference to the 2nd element, typed to a PitchFaultSeizure, that is specified in-line:
        >>> entry_obj = obj.Events_element_as_PitchFaultSeizure(2)
        """
        return self.Events_element_as(index, PitchFaultSeizure)


    def Events_element_as_PitchFaultSeizureAtAngle(self, index: int) -> PitchFaultSeizureAtAngle:
        """
        Retrieves an object from the Events array field, ensuring it is a PitchFaultSeizureAtAngle.        

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        Returns
        -------
        PitchFaultSeizureAtAngle
            A model object at the specified index, guaranteed to be a PitchFaultSeizureAtAngle.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the value at the specified index is not a PitchFaultSeizureAtAngle.

        Examples
        --------
        Gets a reference to the 2nd element, typed to a PitchFaultSeizureAtAngle, that is specified in-line:
        >>> entry_obj = obj.Events_element_as_PitchFaultSeizureAtAngle(2)
        """
        return self.Events_element_as(index, PitchFaultSeizureAtAngle)


    def Events_element_as_ShortCircuit(self, index: int) -> ShortCircuit:
        """
        Retrieves an object from the Events array field, ensuring it is a ShortCircuit.        

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        Returns
        -------
        ShortCircuit
            A model object at the specified index, guaranteed to be a ShortCircuit.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the value at the specified index is not a ShortCircuit.

        Examples
        --------
        Gets a reference to the 2nd element, typed to a ShortCircuit, that is specified in-line:
        >>> entry_obj = obj.Events_element_as_ShortCircuit(2)
        """
        return self.Events_element_as(index, ShortCircuit)


    def Events_element_as_StartUpOperation(self, index: int) -> StartUpOperation:
        """
        Retrieves an object from the Events array field, ensuring it is a StartUpOperation.        

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        Returns
        -------
        StartUpOperation
            A model object at the specified index, guaranteed to be a StartUpOperation.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the value at the specified index is not a StartUpOperation.

        Examples
        --------
        Gets a reference to the 2nd element, typed to a StartUpOperation, that is specified in-line:
        >>> entry_obj = obj.Events_element_as_StartUpOperation(2)
        """
        return self.Events_element_as(index, StartUpOperation)


    def Events_element_as_YawFaultConstantRate(self, index: int) -> YawFaultConstantRate:
        """
        Retrieves an object from the Events array field, ensuring it is a YawFaultConstantRate.        

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        Returns
        -------
        YawFaultConstantRate
            A model object at the specified index, guaranteed to be a YawFaultConstantRate.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the value at the specified index is not a YawFaultConstantRate.

        Examples
        --------
        Gets a reference to the 2nd element, typed to a YawFaultConstantRate, that is specified in-line:
        >>> entry_obj = obj.Events_element_as_YawFaultConstantRate(2)
        """
        return self.Events_element_as(index, YawFaultConstantRate)


    def Events_element_as_YawFaultConstantTorque(self, index: int) -> YawFaultConstantTorque:
        """
        Retrieves an object from the Events array field, ensuring it is a YawFaultConstantTorque.        

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        Returns
        -------
        YawFaultConstantTorque
            A model object at the specified index, guaranteed to be a YawFaultConstantTorque.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the value at the specified index is not a YawFaultConstantTorque.

        Examples
        --------
        Gets a reference to the 2nd element, typed to a YawFaultConstantTorque, that is specified in-line:
        >>> entry_obj = obj.Events_element_as_YawFaultConstantTorque(2)
        """
        return self.Events_element_as(index, YawFaultConstantTorque)


    def Events_element_as_YawFaultLimp(self, index: int) -> YawFaultLimp:
        """
        Retrieves an object from the Events array field, ensuring it is a YawFaultLimp.        

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        Returns
        -------
        YawFaultLimp
            A model object at the specified index, guaranteed to be a YawFaultLimp.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the value at the specified index is not a YawFaultLimp.

        Examples
        --------
        Gets a reference to the 2nd element, typed to a YawFaultLimp, that is specified in-line:
        >>> entry_obj = obj.Events_element_as_YawFaultLimp(2)
        """
        return self.Events_element_as(index, YawFaultLimp)


    def Events_element_as_YawManoever(self, index: int) -> YawManoever:
        """
        Retrieves an object from the Events array field, ensuring it is a YawManoever.        

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        Returns
        -------
        YawManoever
            A model object at the specified index, guaranteed to be a YawManoever.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the value at the specified index is not a YawManoever.

        Examples
        --------
        Gets a reference to the 2nd element, typed to a YawManoever, that is specified in-line:
        >>> entry_obj = obj.Events_element_as_YawManoever(2)
        """
        return self.Events_element_as(index, YawManoever)


    def Events_element_as_inline(self, index: int) -> Union[ControllerFault, EmergencyStopOperation, GridLoss, NetworkFrequencyDisturbance, NetworkVoltageDisturbance, NormalStopOperation, PermanentlyStuckPitchSystem, PitchFaultConstantRate, PitchFaultConstantTorque, PitchFaultLimp, PitchFaultSeizure, PitchFaultSeizureAtAngle, ShortCircuit, StartUpOperation, YawFaultConstantRate, YawFaultConstantTorque, YawFaultLimp, YawManoever]:
        """
        Retrieves an object from the Events array field; if the value is specified with a '$insert', an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        Returns
        -------
        Union[ControllerFault, EmergencyStopOperation, GridLoss, NetworkFrequencyDisturbance, NetworkVoltageDisturbance, NormalStopOperation, PermanentlyStuckPitchSystem, PitchFaultConstantRate, PitchFaultConstantTorque, PitchFaultLimp, PitchFaultSeizure, PitchFaultSeizureAtAngle, ShortCircuit, StartUpOperation, YawFaultConstantRate, YawFaultConstantTorque, YawFaultLimp, YawManoever]
            A model object at the specified index, guaranteed to not be an '$insert'.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the value at the specified index is not one of the concrete types of Event; i.e. it is specified with an '$insert'.

        Examples
        --------
        Get a reference to the 2nd element, as any of the concrete types:
        >>> Events_obj = obj.Events_element_as_inline(2)
        """
        val = self.Events[index]
        if isinstance(val, EventInsert) or val.is_insert == True:
            raise TypeError(f"Expected element value at '{index}' to be an in-line object, but it is currently in the '$insert' state.")
        return val


    def Events_element_as(self, index: int, element_cls: Type[TEventOptions]) -> TEventOptions:
        """
        Retrieves an object from the Events array field, ensuring it is of the specified type.
        The specified type must be one of the valid concrete types of Event, or the '$insert' type
        (in the case the model is defined to be inserted from an external resource).

        Useful when using type-checking development tools, as it provides a concise way to access a value with the correct type.

        Parameters
        ----------
        index: int
            The index of the element to retrieve.

        element_cls: Type[Union[ControllerFault, EmergencyStopOperation, GridLoss, NetworkFrequencyDisturbance, NetworkVoltageDisturbance, NormalStopOperation, PermanentlyStuckPitchSystem, PitchFaultConstantRate, PitchFaultConstantTorque, PitchFaultLimp, PitchFaultSeizure, PitchFaultSeizureAtAngle, ShortCircuit, StartUpOperation, YawFaultConstantRate, YawFaultConstantTorque, YawFaultLimp, YawManoever, EventInsert]]
            One of the valid concrete types of Event, or the '$insert' type
            (in the case the model is defined to be inserted from an external resource).

        Returns
        -------
        TEventOptions
            A model object of the specified type.

        Raises
        ------
        IndexError
            If the list index is out of range

        TypeError
            If the model object for the specified index is not of the specified type.

        Examples
        --------
        Get a reference to the 2nd element when it was one of the types of Event:
        >>> entry_obj = obj.Events_element_as(2, models.ControllerFault)
        >>> entry_obj = obj.Events_element_as(2, models.EmergencyStopOperation)
        >>> entry_obj = obj.Events_element_as(2, models.GridLoss)
        >>> entry_obj = obj.Events_element_as(2, models.NetworkFrequencyDisturbance)
        >>> entry_obj = obj.Events_element_as(2, models.NetworkVoltageDisturbance)
        >>> entry_obj = obj.Events_element_as(2, models.NormalStopOperation)
        >>> entry_obj = obj.Events_element_as(2, models.PermanentlyStuckPitchSystem)
        >>> entry_obj = obj.Events_element_as(2, models.PitchFaultConstantRate)
        >>> entry_obj = obj.Events_element_as(2, models.PitchFaultConstantTorque)
        >>> entry_obj = obj.Events_element_as(2, models.PitchFaultLimp)
        >>> entry_obj = obj.Events_element_as(2, models.PitchFaultSeizure)
        >>> entry_obj = obj.Events_element_as(2, models.PitchFaultSeizureAtAngle)
        >>> entry_obj = obj.Events_element_as(2, models.ShortCircuit)
        >>> entry_obj = obj.Events_element_as(2, models.StartUpOperation)
        >>> entry_obj = obj.Events_element_as(2, models.YawFaultConstantRate)
        >>> entry_obj = obj.Events_element_as(2, models.YawFaultConstantTorque)
        >>> entry_obj = obj.Events_element_as(2, models.YawFaultLimp)
        >>> entry_obj = obj.Events_element_as(2, models.YawManoever)

        Get a reference to the value, when it was specified with a '$insert' and read in from a file:
        >>> insert_obj = obj.Events_element_as(2, models.EventInsert)
        """
        val = self.Events[index]
        if not isinstance(val, element_cls):
            raise TypeError(f"Expected value of type '{element_cls.__name__}' at index {index} but found type '{type(val).__name__}'")
        return val



    def _find_unused_containers(self) -> Set[str]:
        unused_containers: Set[str] = super()._find_unused_containers()
        if self.AdditionalExternalModules is not None and len(self.AdditionalExternalModules) == 0: #type: ignore
            unused_containers.add('AdditionalExternalModules')
        if self.AppliedLoads is not None and len(self.AppliedLoads) == 0: #type: ignore
            unused_containers.add('AppliedLoads')
        if self.InitialConditions is not None and len(self.InitialConditions) == 0: #type: ignore
            unused_containers.add('InitialConditions')
        if self.Events is not None and len(self.Events) == 0: #type: ignore
            unused_containers.add('Events')
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
        TimeDomainSimulation
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = TimeDomainSimulation.from_file('/path/to/file')
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
        TimeDomainSimulation
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = TimeDomainSimulation.from_json('{ ... }')
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
        TimeDomainSimulation
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


TimeDomainSimulation.update_forward_refs()
