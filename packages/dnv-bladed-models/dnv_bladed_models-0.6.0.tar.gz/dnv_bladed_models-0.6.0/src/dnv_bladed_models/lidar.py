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

from dnv_bladed_models.circular_lidar_scan import CircularLidarScan

from dnv_bladed_models.component import Component

from dnv_bladed_models.controller_lidar_settings import ControllerLidarSettings

from dnv_bladed_models.lidar_beam import LidarBeam

from dnv_bladed_models.lidar_controller_scan import LidarControllerScan

from dnv_bladed_models.lidar_focal_distance_control import LidarFocalDistanceControl

from dnv_bladed_models.lidar_focal_distance_control_insert import LidarFocalDistanceControlInsert

from dnv_bladed_models.lidar_scanning_pattern import LidarScanningPattern

from dnv_bladed_models.lidar_scanning_pattern_insert import LidarScanningPatternInsert

from dnv_bladed_models.look_up_table_element import LookUpTableElement

from dnv_bladed_models.multiple_lidar_focal_distances import MultipleLidarFocalDistances

from dnv_bladed_models.rosette_lidar_scan import RosetteLidarScan

from dnv_bladed_models.single_lidar_focal_distance import SingleLidarFocalDistance



from .schema_helper import SchemaHelper 
from .models_impl import *

TLidarScanningPatternOptions = TypeVar('TLidarScanningPatternOptions', CircularLidarScan, LidarControllerScan, RosetteLidarScan, LidarScanningPatternInsert, LidarScanningPattern, )
TLidarFocalDistanceControlOptions = TypeVar('TLidarFocalDistanceControlOptions', ControllerLidarSettings, MultipleLidarFocalDistances, SingleLidarFocalDistance, LidarFocalDistanceControlInsert, LidarFocalDistanceControl, )

class Lidar(Component):
    r"""
    A Lidar sensor mounted on the structure.
    
    Not supported yet.
    
    Attributes
    ----------
    ComponentType : Literal['Lidar'], default='Lidar', Not supported yet
        Defines the specific type of Component model in use.  For a `Lidar` object, this must always be set to a value of `Lidar`.
    
    LensArea : float, Not supported yet
        The area of the lens.
    
    LaserWavelength : float, Not supported yet
        The wavelength of the laser.
    
    WeightingFunction : List[LookUpTableElement], Not supported yet
        The relationship between the distance from the focal point and the weighting to put on the sample.  Every Lidar sampling point has a finite width, where velocities are collected to either side of the nominal focal distance.  This relationship is used to put more weight on those samples closest to the nominal focal point.
    
    LidarBeams : List[LidarBeam], Not supported yet
        The definition of the lidar beams.
    
    ScanningPattern : Union[CircularLidarScan, LidarControllerScan, RosetteLidarScan, LidarScanningPatternInsert], Not supported yet
    
    FocalDistanceControl : Union[ControllerLidarSettings, MultipleLidarFocalDistances, SingleLidarFocalDistance, LidarFocalDistanceControlInsert], Not supported yet
    
    Notes
    -----
    This model is not supported yet by the Bladed calculation engine.
    """
    _relative_schema_path: str = PrivateAttr('Components/Lidar/Lidar.json')

    ComponentType: Literal['Lidar'] = Field(alias="ComponentType", default='Lidar', allow_mutation=False, const=True) # Not supported yet
    LensArea: float = Field(alias="LensArea", default=None) # Not supported yet
    LaserWavelength: float = Field(alias="LaserWavelength", default=None) # Not supported yet
    WeightingFunction: List[LookUpTableElement] = Field(alias="WeightingFunction", default=list()) # Not supported yet
    LidarBeams: List[LidarBeam] = Field(alias="LidarBeams", default=list()) # Not supported yet
    ScanningPattern: Union[CircularLidarScan, LidarControllerScan, RosetteLidarScan, LidarScanningPatternInsert] = Field(alias="ScanningPattern", default=None, discriminator='ScanningPatternType') # Not supported yet
    FocalDistanceControl: Union[ControllerLidarSettings, MultipleLidarFocalDistances, SingleLidarFocalDistance, LidarFocalDistanceControlInsert] = Field(alias="FocalDistanceControl", default=None, discriminator='FocalDistanceControlType') # Not supported yet

    class Config:
        extra = Extra.forbid
        validate_assignment = True
        allow_population_by_field_name = True
        pass


    @classmethod
    def parse_obj(cls: Type['Model'], obj: Any) -> 'Model':
        discriminated_props = [
            ('ScanningPattern', 'ScanningPatternType'),
            ('FocalDistanceControl', 'FocalDistanceControlType'),
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
        if isinstance(data, Lidar):
            return data
        if not isinstance(data, dict):
            raise TypeError('An object is required to define Lidar models')
        return Lidar.parse_obj(data)


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
    def ScanningPattern_as_CircularLidarScan(self) -> CircularLidarScan:
        """
        Retrieves the value of ScanningPattern guaranteeing it is a CircularLidarScan; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        CircularLidarScan
            A model object, guaranteed to be a CircularLidarScan.

        Raises
        ------
        TypeError
            If the value is not a CircularLidarScan.
        """
        return self.ScanningPattern_as(CircularLidarScan)


    @property
    def ScanningPattern_as_LidarControllerScan(self) -> LidarControllerScan:
        """
        Retrieves the value of ScanningPattern guaranteeing it is a LidarControllerScan; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        LidarControllerScan
            A model object, guaranteed to be a LidarControllerScan.

        Raises
        ------
        TypeError
            If the value is not a LidarControllerScan.
        """
        return self.ScanningPattern_as(LidarControllerScan)


    @property
    def ScanningPattern_as_RosetteLidarScan(self) -> RosetteLidarScan:
        """
        Retrieves the value of ScanningPattern guaranteeing it is a RosetteLidarScan; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        RosetteLidarScan
            A model object, guaranteed to be a RosetteLidarScan.

        Raises
        ------
        TypeError
            If the value is not a RosetteLidarScan.
        """
        return self.ScanningPattern_as(RosetteLidarScan)


    @property
    def ScanningPattern_as_inline(self) -> Union[CircularLidarScan, LidarControllerScan, RosetteLidarScan]:
        """
        Retrieves the value of ScanningPattern as a model object; if the value is specified with a '$insert', an error is raised.

        Returns
        -------
        Union[CircularLidarScan, LidarControllerScan, RosetteLidarScan]
            A model object at the specified index, guaranteed to not be a '$insert'.

        Raises
        ------
        TypeError
            If the value is not one of the concrete types of LidarScanningPattern; i.e. it is specified with a '$insert'.
        """
        if isinstance(self.ScanningPattern, LidarScanningPatternInsert) or self.ScanningPattern.is_insert:
            raise TypeError(f"Expected ScanningPattern value to be an in-line object, but it is currently in the '$insert' state.")
        return self.ScanningPattern


    def ScanningPattern_as(self, cls: Type[TLidarScanningPatternOptions])-> TLidarScanningPatternOptions:
        """
        Retrieves the value of ScanningPattern, ensuring it is of the specified type.
        The specified type must be one of the valid concrete types of LidarScanningPattern, or the '$insert' type
        (in the case the model is defined to be inserted from an external resource).

        Useful when using type-checking development tools, as it provides a concise way to access a value with the correct type.

        Parameters
        ----------
        cls: Type[Union[CircularLidarScan, LidarControllerScan, RosetteLidarScan, LidarScanningPatternInsert]]
            One of the valid concrete types of LidarScanningPattern, or the '$insert' type
            (in the case the model is defined to be inserted from an external resource).

        Returns
        -------
        TLidarScanningPatternOptions
            A model object of the specified type.

        Raises
        ------
        TypeError
            If the value is not of the specified type.

        Examples
        --------
        Get a reference to the value when it is one of the types of LidarScanningPattern:
        >>> val_obj = model_obj.ScanningPattern_as(models.CircularLidarScan)
        >>> val_obj = model_obj.ScanningPattern_as(models.LidarControllerScan)
        >>> val_obj = model_obj.ScanningPattern_as(models.RosetteLidarScan)

        Get a reference to the value, when it was specified with a '$insert' and read in from a file:
        >>> insert_obj = model_obj.ScanningPattern_as(models.LidarScanningPatternInsert)
        """
        if not isinstance(self.ScanningPattern, cls):
            raise TypeError(f"Expected ScanningPattern of type '{cls.__name__}' but was type '{type(self.ScanningPattern).__name__}'")
        return self.ScanningPattern


    @property
    def FocalDistanceControl_as_ControllerLidarSettings(self) -> ControllerLidarSettings:
        """
        Retrieves the value of FocalDistanceControl guaranteeing it is a ControllerLidarSettings; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        ControllerLidarSettings
            A model object, guaranteed to be a ControllerLidarSettings.

        Raises
        ------
        TypeError
            If the value is not a ControllerLidarSettings.
        """
        return self.FocalDistanceControl_as(ControllerLidarSettings)


    @property
    def FocalDistanceControl_as_MultipleLidarFocalDistances(self) -> MultipleLidarFocalDistances:
        """
        Retrieves the value of FocalDistanceControl guaranteeing it is a MultipleLidarFocalDistances; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        MultipleLidarFocalDistances
            A model object, guaranteed to be a MultipleLidarFocalDistances.

        Raises
        ------
        TypeError
            If the value is not a MultipleLidarFocalDistances.
        """
        return self.FocalDistanceControl_as(MultipleLidarFocalDistances)


    @property
    def FocalDistanceControl_as_SingleLidarFocalDistance(self) -> SingleLidarFocalDistance:
        """
        Retrieves the value of FocalDistanceControl guaranteeing it is a SingleLidarFocalDistance; if it is not, an error is raised.

        Useful when using type-checking development tools, as it provides a concise way to retrieve a value and assign a variable with the correct type.

        Returns
        -------
        SingleLidarFocalDistance
            A model object, guaranteed to be a SingleLidarFocalDistance.

        Raises
        ------
        TypeError
            If the value is not a SingleLidarFocalDistance.
        """
        return self.FocalDistanceControl_as(SingleLidarFocalDistance)


    @property
    def FocalDistanceControl_as_inline(self) -> Union[ControllerLidarSettings, MultipleLidarFocalDistances, SingleLidarFocalDistance]:
        """
        Retrieves the value of FocalDistanceControl as a model object; if the value is specified with a '$insert', an error is raised.

        Returns
        -------
        Union[ControllerLidarSettings, MultipleLidarFocalDistances, SingleLidarFocalDistance]
            A model object at the specified index, guaranteed to not be a '$insert'.

        Raises
        ------
        TypeError
            If the value is not one of the concrete types of LidarFocalDistanceControl; i.e. it is specified with a '$insert'.
        """
        if isinstance(self.FocalDistanceControl, LidarFocalDistanceControlInsert) or self.FocalDistanceControl.is_insert:
            raise TypeError(f"Expected FocalDistanceControl value to be an in-line object, but it is currently in the '$insert' state.")
        return self.FocalDistanceControl


    def FocalDistanceControl_as(self, cls: Type[TLidarFocalDistanceControlOptions])-> TLidarFocalDistanceControlOptions:
        """
        Retrieves the value of FocalDistanceControl, ensuring it is of the specified type.
        The specified type must be one of the valid concrete types of LidarFocalDistanceControl, or the '$insert' type
        (in the case the model is defined to be inserted from an external resource).

        Useful when using type-checking development tools, as it provides a concise way to access a value with the correct type.

        Parameters
        ----------
        cls: Type[Union[ControllerLidarSettings, MultipleLidarFocalDistances, SingleLidarFocalDistance, LidarFocalDistanceControlInsert]]
            One of the valid concrete types of LidarFocalDistanceControl, or the '$insert' type
            (in the case the model is defined to be inserted from an external resource).

        Returns
        -------
        TLidarFocalDistanceControlOptions
            A model object of the specified type.

        Raises
        ------
        TypeError
            If the value is not of the specified type.

        Examples
        --------
        Get a reference to the value when it is one of the types of LidarFocalDistanceControl:
        >>> val_obj = model_obj.FocalDistanceControl_as(models.ControllerLidarSettings)
        >>> val_obj = model_obj.FocalDistanceControl_as(models.MultipleLidarFocalDistances)
        >>> val_obj = model_obj.FocalDistanceControl_as(models.SingleLidarFocalDistance)

        Get a reference to the value, when it was specified with a '$insert' and read in from a file:
        >>> insert_obj = model_obj.FocalDistanceControl_as(models.LidarFocalDistanceControlInsert)
        """
        if not isinstance(self.FocalDistanceControl, cls):
            raise TypeError(f"Expected FocalDistanceControl of type '{cls.__name__}' but was type '{type(self.FocalDistanceControl).__name__}'")
        return self.FocalDistanceControl



    def _find_unused_containers(self) -> Set[str]:
        unused_containers: Set[str] = super()._find_unused_containers()
        if self.WeightingFunction is not None and len(self.WeightingFunction) == 0: #type: ignore
            unused_containers.add('WeightingFunction')
        if self.LidarBeams is not None and len(self.LidarBeams) == 0: #type: ignore
            unused_containers.add('LidarBeams')
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
        Lidar
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = Lidar.from_file('/path/to/file')
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
        Lidar
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = Lidar.from_json('{ ... }')
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
        Lidar
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


Lidar.update_forward_refs()
