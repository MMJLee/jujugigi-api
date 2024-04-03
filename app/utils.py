# standard lib imports
import logging
from typing import Dict, Any, Tuple, Set, List


logger = logging.getLogger("uvicorn.access")


def filter_excluded_keys(mapped_dict: Dict[str, Any], excluded_keys: Set[str]) -> Dict[str, Any]:
    return {k: v for k, v in mapped_dict.items() if k not in excluded_keys}


def build_insert_statement(mapped_dict: Dict[str, Any]) -> Tuple[str, str]:
    values_statement = ", ".join(f":{k}" for k in mapped_dict)
    fields_statement = values_statement.replace(":", "")
    return fields_statement, values_statement


def build_update_statement(mapped_dict: Dict[str, Any]) -> str:
    return ", ".join(f"{k} = :{k}" for k in mapped_dict)


def build_in_statement(filter_list: List[Any]) -> str:
    in_statement = ""
    count = 0
    for val in filter_list:
        if count == 0:
            in_statement += str(val)
        else:
            in_statement += f", {str(val)}"
        count += 1
    return in_statement
