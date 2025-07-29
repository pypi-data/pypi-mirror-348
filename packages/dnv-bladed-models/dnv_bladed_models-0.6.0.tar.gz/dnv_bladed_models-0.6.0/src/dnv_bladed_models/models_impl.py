# *********************************************************************#
# Bladed Python Models API                                             #
# Copyright (c) DNV Services UK Limited (c) 2025. All rights reserved. #
# MIT License (see license file)                                       #
# *********************************************************************#


from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Type, TypeVar, Union
from abc import ABC, abstractmethod
from pydantic import BaseModel, ValidationError, root_validator
from pydantic.error_wrappers import ErrorWrapper
from pydantic.utils import ROOT_KEY

class CommonRoot(BaseModel, ABC):

    def _find_unused_containers(self) -> Set[str]:
        return set()


    def _is_unused(self) -> bool:
        """
        Returns true if the model has no user-supplied values. This indicates the object should not be rendered in the final JSON output.
        """
        return False


    @root_validator(pre=True)
    def _remove_underscore_fields(cls, values: Dict[str, Any]):
        remove_underscore_fields(values)
        return values


class ModelInterface(CommonRoot, ABC):
    @abstractmethod
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
        pass


    @abstractmethod
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
        pass

def remove_underscore_fields(values: Dict[str, Any]):
    to_remove: Set[str] = set()
    for child_name, child in values.items():
        if child_name.startswith('_'):
            to_remove.add(child_name)
        elif isinstance(child, dict):
            remove_underscore_fields(child)
        elif isinstance(child, list):
            for item in child:
                if isinstance(child, dict):
                    remove_underscore_fields(item)
    for x in to_remove:
        del values[x]


def prepare_dict_for_discriminated_insert(cls, field_name: str, field_obj: dict, discriminator_prop: str):
    if isinstance(field_obj, dict) and '$insert' in field_obj:
        if discriminator_prop in field_obj and field_obj[discriminator_prop] is not None and field_obj['$insert'] is not None:
            exc = ValueError(f"Cannot set both {discriminator_prop} and $insert fields.")
            raise ValidationError([ErrorWrapper(exc, loc=field_name)], cls)
        field_obj[discriminator_prop] = '__insert__'


def prepare_list_for_discriminated_insert(cls, field_name: str, field_obj: dict, discriminator_prop: str):
    if isinstance(field_obj, list):
        i = 0
        for item in field_obj:
            if isinstance(item, dict) and '$insert' in item:
                if discriminator_prop in item and item[discriminator_prop] is not None and item['$insert'] is not None:
                    exc = ValueError(f"Cannot set both {discriminator_prop} and $insert fields.")
                    raise ValidationError([ErrorWrapper(exc, loc=f"{field_name}[{i}]")], cls)
                item[discriminator_prop] = '__insert__'
            i += 1
    

def ensure_dict_for_parse(cls, data) -> dict:
    obj = cls._enforce_dict_if_root(data)
    if not isinstance(obj, dict):
        try:
            obj = dict(obj)
        except (TypeError, ValueError) as e:
            exc = TypeError(f'{cls.__name__} expected dict not {obj.__class__.__name__}')
            raise ValidationError([ErrorWrapper(exc, loc=ROOT_KEY)], cls) from e
    return obj


TParsedObj = TypeVar('TParsedObj', bound=BaseModel)
def prepare_model_dict(cls : Type[TParsedObj], obj: Any, discriminated_props: List[Tuple[str, str]], discriminated_arrays: List[Tuple[str, str]]) -> None:
    if any(discriminated_props) or any(discriminated_arrays):
        obj = ensure_dict_for_parse(cls, obj)
        for field_name, discriminator in discriminated_props:
            if field_name in obj:
                prepare_dict_for_discriminated_insert(cls, field_name, obj[field_name], discriminator)
        for field_name, discriminator in discriminated_arrays:
            if field_name in obj:
                prepare_list_for_discriminated_insert(cls, field_name, obj[field_name], discriminator)


TRawContainer = TypeVar('TRawContainer')
def custom_entries_parser(cls, obj, valid_raw_type: Type[TRawContainer], entry_model: Type, prepare_data: Optional[Callable[[str, TRawContainer], None]] = None):
    data_dict = ensure_dict_for_parse(cls, obj)

    ctor_data = {}
    entry_data = {}
    field_keys = set(val.alias or val.name for val in cls.__fields__.values())
    for key, val in data_dict.items():
        if not key in field_keys and not key.startswith('_') and isinstance(val, valid_raw_type):
            if prepare_data is not None:
                prepare_data(key, val)
            entry_data[key] = val
        else:
            ctor_data[key] = val

    instance = cls(**ctor_data)
    try:
        container = entry_model.parse_obj({ 'entries' : entry_data })
        for key, val in container.entries.items():
            setattr(instance, key, val)
    except ValidationError as e:
        raise ValidationError([ErrorWrapper(e, loc=cls.__name__)], cls)
           
    return instance


