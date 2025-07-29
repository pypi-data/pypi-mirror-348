"""
Module to include utils related to transforming
numbers into Spanish literals.
"""
from yta_validation.parameter import ParameterValidator
from typing import Union


def hundred_to_string(
    number: Union[int, float]
) -> str:
    """
    Receives a digit that represents the X00 part of
    a number and returns that number (according to
    its position) in Spanish words, starting with a
    black space.

    This method returns ' novecientos' for 9 input
    and ' cien' for 1 input.
    """
    ParameterValidator.validate_mandatory_number('number', number)
    
    number = {
        9: 'novecientos',
        8: 'ochocientos',
        7: 'setecientos',
        6: 'seiscientos',
        5: 'quinientos',
        4: 'cuatrocientos',
        3: 'trescientos',
        2: 'doscientos',
        1: 'cien'
    }[abs(number)]

    return f' {number}'

def ten_to_string(
    number: Union[int, float]
) -> str:
    """
    Receives a digit that represents the X0 part of
    a number and returns that number (according to
    its position) in Spanish words, starting with a
    black space.

    This method returns ' noventa' for 9 input and
    ' diez' for 1 input.
    """
    ParameterValidator.validate_mandatory_number('number', number)
    
    number = {
        9: 'noventa',
        8: 'ochenta',
        7: 'setenta',
        6: 'sesenta',
        5: 'cincuenta',
        4: 'cuarenta',
        3: 'treinta',
        2: 'veinte',
        1: 'diez'
    }[abs(number)]

    return f' {number}'

def unit_to_string(
    number: Union[int, float]
) -> str:
    """
    Receives a digit that represents the X part of
    a number and returns that number (according to
    its position) in Spanish words, starting with a
    black space.

    This method returns ' nueve' for 9 input, and
    ' uno' for 1 input.
    """
    ParameterValidator.validate_mandatory_number('number', number)
    
    number = {
        9: 'nueve',
        8: 'ocho',
        7: 'siete',
        6: 'seis',
        5: 'cinco',
        4: 'cuatro',
        3: 'tres',
        2: 'dos',
        1: 'uno'
    }[abs(number)]

    return f' {number}'