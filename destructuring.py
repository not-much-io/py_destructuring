from inspect import signature
from uuid import uuid1
from types import GeneratorType

# Just a proof of concept implementation of destructuring in python

_seq_types = [tuple, list, GeneratorType]


def _valid_for_destructuring(param, value):
    # Annotation is either a dict or one of the seq types
    annotation_type = type(param.annotation)
    valid_expr = annotation_type in _seq_types or annotation_type == dict

    # Value that expression applies to must be dictionary
    val_is_dict = type(value) == dict

    return valid_expr and val_is_dict


def destructurable_params(fn, args):
    params = signature(fn).parameters
    for i, param in enumerate(params):
        param = params[param]
        value = args[i]

        if _valid_for_destructuring(param, value):
            yield {"destructuring_expression": param.annotation,
                   "variable_value": value}


def _get_old_values(var_names, fn):
    old_values = []
    uuid = uuid1()  # Signifies no previous value in __globals__
    for name in var_names:
        try:
            old_values.append(fn.__globals__[name])
        except KeyError:
            old_values.append(uuid)  # There was no previous value
    return old_values, uuid


def _assign_vars(var_names, var_values, fn):
    for i, var_name in enumerate(var_names):
        new_value = var_values[i]
        fn.__globals__[var_name] = new_value


def _revert_vars(var_names, old_values, fn, uuid):
    for i, var_name in enumerate(var_names):
        old_value = old_values[i]
        if old_value == uuid:  # There was no previous value
            del fn.__globals__[var_name]
        else:
            fn.__globals__[var_name] = old_values[old_value]


def _store_assign_run_revert(var_names, var_values, fn, args):
    old_values, uuid = _get_old_values(var_names, fn)
    _assign_vars(var_names, var_values, fn)
    res = fn(*args)
    _revert_vars(var_names, old_values, fn, uuid)
    return res


def seq_destruct(expr, target_dict, fn, args):
    var_names = expr
    var_values = [target_dict[key] for key in expr]
    return _store_assign_run_revert(var_names, var_values, fn, args)


def dict_destructure(expr, target_dict, fn, args):
    var_names = []
    var_values = []
    for var_name, var_key in expr.items():
        var_names.append(var_name)
        var_values.append(target_dict[var_key])
    return _store_assign_run_revert(var_names, var_values, fn, args)


def destructure(fn):
    def wrapper(*args, **kwargs):
        params_to_destructure = destructurable_params(fn, args)
        for param in params_to_destructure:

            destruct_expression = param["destructuring_expression"]
            target_dict = param["variable_value"]

            if type(destruct_expression) in _seq_types:
                return seq_destruct(destruct_expression, target_dict, fn, args)
            if type(destruct_expression) == dict:
                return dict_destructure(destruct_expression, target_dict, fn, args)

    return wrapper
