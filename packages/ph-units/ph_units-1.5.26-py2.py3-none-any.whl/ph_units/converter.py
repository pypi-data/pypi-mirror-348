# -*- coding: utf-8 -*-
# -*- Python Version: 2.7 -*-

"""Functions for converting Values from one unit to another (ie: meter->foot)."""

try:
    from typing import Dict, List, Optional, Tuple, Union
except ImportError:
    pass  # IronPython 2.7

from copy import copy

from ph_units.unit_types import build_unit_type_dicts
from ph_units.unit_types._base import Base_UnitType

unit_type_dict, unit_type_alias_dict = build_unit_type_dicts()


class UnitTypeNameNotFound(Exception):
    def __init__(self, message):
        # type: (str) -> None
        self.message = message
        super(UnitTypeNameNotFound, self).__init__(self.message)


def _find_valid_unit_names_matching_first_letter(_unit_type_alias_dict, _input_string):
    # type: (Dict[str, str], str) -> List[str]
    """Find all valid unit-type names that start with a given letter."""
    matches = []

    try:
        first_letter = str(_input_string).strip()[0].upper()
    except IndexError:
        return matches

    for k in sorted(_unit_type_alias_dict.keys()):
        try:
            if k[0] == first_letter:
                matches.append(k)
        except IndexError:
            pass

    return matches


def _standardize_unit_name(_input, _unit_type_alias_dict):
    # type: (str, Dict[str, str]) -> str
    """Standardize unit nomenclature. ie: 'FT3/M' and 'CFM' both return 'CFM'.
    Arguments:
    ----------
        * _input (str): The input unit-type.
        * _unit_type_alias_dict (Dict[str, str]): The dictionary of unit-type aliases.

    Returns:
    --------
        * (str): The input and output unit-type strings
    """

    _input_string = str(_input).upper()
    try:
        input_unit = _unit_type_alias_dict[_input_string]
    except KeyError:
        if _input_string == "%":
            input_unit = "%"
        else:
            suggested_matches = _find_valid_unit_names_matching_first_letter(
                _unit_type_alias_dict, _input_string
            )
            raise UnitTypeNameNotFound(
                "\nI do not understand the unit: '{}'? "
                "\nPerhaps you meant on of these: '{}'?"
                "\n\nValid formats include only: {}".format(
                    _input_string,
                    suggested_matches,
                    sorted(_unit_type_alias_dict.keys()),
                )
            )

    return input_unit


def _clean_user_inputs(_input_unit, _target_unit, _unit_type_alias_dict):
    # type: (Optional[str], str, Dict[str, str]) -> Tuple[str, str]
    """Clean and standardize the suer-input strings for the unit-types. If no
    input unit-type is designated, the output unit-type will be assumed to
    match the target unit-type.

    Arguments:
    ----------
        * _input_unit (Optional[str]): The input unit-type.
        * _target_unit (str): the output unit-type.
        * _unit_type_alias_dict (Dict[str, str]): The dictionary of unit-type aliases.

    Returns:
    --------
        * (Tuple[str, str]): The input and output unit-type strings
    """
    if not _input_unit:
        _input_unit = copy(_target_unit)

    input_unit = str(_input_unit).upper().strip().replace(" ", "")
    input_unit = _standardize_unit_name(input_unit, _unit_type_alias_dict)
    target_unit = str(_target_unit).upper().strip().replace(" ", "")
    target_unit = _standardize_unit_name(target_unit, _unit_type_alias_dict)

    return input_unit, target_unit


def _conversion_schema(_input_unit, _schemas_dict):
    # type: (str, Dict[str, Base_UnitType]) -> Dict[str, str]
    """Returns the conversion schema dict, given an input unit type.

    ie: _input_unit of "M2" returns the dict: {"SI": "{}*1", "M2": "{}*1", "FT2": "{}*10.76391042"}

    Arguments:
    ----------
        * _input_unit (str): The input unit type
        * _schemas_dict (Dict[str, Base_UnitType]): The dictionary of conversion schema objects.

    Returns:
    --------
        * (Dict[str, str])
    """
    try:
        unit_type = _schemas_dict[_input_unit]
        return unit_type.__factors__
    except KeyError:
        raise Exception(
            "\n\tUnit conversion schema does not include type: '{}'?"
            "\n\tValid input units: {}".format(_input_unit, list(unit_type_dict.keys()))
        )


def _conversion_factor(_schema, _input_unit, _target_unit):
    # type: (Dict[str, str], str, str) -> str
    """Return the correct conversion factor template string for the input and target units.

    The returned string will be a template with a single '{}'. For instance:
        "(1/{})*0.067"

    Arguments:
    ----------
        * _schema (Dict[str, str]): The dictionary of conversion factors.
        * _input_unit (str): The input unit (ie: "FT")
        * _target_unit (str): The output unit (ie: "M")

    Returns:
    --------
        * (str): The conversion factor template string.
    """
    try:
        return _schema[_target_unit]
    except KeyError:
        raise Exception(
            "\n\tUnit conversion schema for '{}' does not include '{}'?"
            "\n\tValid input units: {}".format(
                _input_unit, _target_unit, list(_schema.keys())
            )
        )


def validate_unit_type(_unit_type):
    # type: (str | None) -> str | None
    """Return the valid unit type from the input string.

    examples:
        "in." -> "IN"
        "m" -> "M"
        "Btu/hr-sf-F" -> "BTU/HR-FT2-F"
        None -> None
        "not-a-unit" -> Exception
    """

    if _unit_type is None:
        return None

    return _standardize_unit_name(_unit_type, unit_type_alias_dict)


def convert(_value, _input_unit, _target_unit):
    # type: (Optional[Union[float, int, str]], Optional[str], str) -> Optional[Union[int, float]]
    """Convert a value from a one unit-type to another (ie: "M" -> "FT").

    >>> convert(12.45, "M", "FT") -> 40.85 # FT

    Note that if no input_unit type is provided, it will be assumed to match the
    target_unit type.

    >>> convert(12.45, None, "M") -> 12.45 # M

    Arguments:
    ----------
        * _value (Optional[Union[float, int, str]]): The numeric value to convert.
        * _input_unit (Optional[str]): The input value's starting unit (ie: "M").
        * _target_unit (str): The input value's desired target unit (ie: "FT").

    Returns:
    --------
        * (Optional[Union[float, int]]): The converted value in the target units.
    """

    if _value is None:
        return None

    if str(_value).strip() == "":
        return 0

    input_unit, target_unit = _clean_user_inputs(
        _input_unit, _target_unit, unit_type_alias_dict
    )
    schema = _conversion_schema(input_unit, unit_type_dict)
    conversion_equation = _conversion_factor(schema, input_unit, target_unit)

    return eval("{}".format(conversion_equation).format(float(_value)))
