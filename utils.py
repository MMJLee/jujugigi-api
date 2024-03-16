# standard lib imports
from copy import deepcopy
import json, logging
from typing import Dict, Any, Tuple, Set, Optional, List
from uuid import UUID

logger = logging.getLogger('uvicorn.access')

def filter_excluded_keys(mapped_dict: Dict[str, Any], excluded_keys: Set[str]) -> Dict[str, Any]:
    return {k: v for k, v in mapped_dict.items() if k not in excluded_keys}

def build_insert_stmts(mapped_dict: Dict[str, Any]) -> Tuple[str, str]:
    values_stmt = ', '.join(f':{k}' for k in mapped_dict)
    fields_stmt = values_stmt.replace(':', '')
    return fields_stmt, values_stmt

def build_update_stmt  (mapped_dict: Dict[str, Any]) -> str:
    return ', '.join(f'{k} = :{k}' for k in mapped_dict)

def build_in_stmt(list: List[Any]) -> str:
    in_stmt = ''
    count = 0
    for val in list:
        if count == 0:
            in_stmt += str(val)
        else:
            in_stmt += f', {str(val)}'
    return in_stmt

def map_dictionary(to_be_mapped: Dict[str, Any], key_map: Dict[str, str], json_fields: Optional[Set[str]] = None, reverse: bool = False) -> Dict[str, Any]:
    mapped_dict = deepcopy(to_be_mapped)
    json_fields = json_fields or set()    

    # perform key mapping
    for key, val in key_map.items():
        if reverse:
            new_val = mapped_dict.pop(val)
            mapped_dict[key] = format_as_uuid(new_val) or new_val
        else:
            new_val = mapped_dict.pop(key)
            mapped_dict[val] = str(new_val) if isinstance(new_val, UUID) else new_val

    # handle any json fields
    for field in json_fields:
        if reverse:
            mapped_dict[field] = json.loads(mapped_dict.get(field) or '{}')
        else:            
            mapped_dict[field] = json.dumps(mapped_dict.get(field) or {}, cls=UUIDEncoder)
    return mapped_dict

def format_as_uuid(val):
    if isinstance(val, UUID):
        return val

    if isinstance(val, str):
        try:
            return UUID(val)
        except: # not a valid uuid value
            pass
    return None

def log(message):
    try:
        logger.info(message)
    except:
        pass
    
class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        return json.JSONEncoder.default(self, obj)