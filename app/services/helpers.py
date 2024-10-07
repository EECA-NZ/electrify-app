"""
Module for generic helper functions.
"""

def answer_options(object, field):
    """
    For a given field on a pydantic model, return the possible answer options.
    """
    return type(object).model_fields[field].annotation.__args__
