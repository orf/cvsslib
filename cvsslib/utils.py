import inspect
from functools import partial
from .base_enum import BaseEnum, NotDefined


def get_enums(obj, only_classes=True):
    module_members = inspect.getmembers(obj)

    for name, obj in module_members:
        if inspect.isclass(obj):
            process = issubclass(obj, BaseEnum)
        elif not only_classes:
            process = isinstance(obj, BaseEnum)
        else:
            continue

        if process and obj is not BaseEnum:
            yield name, obj


def run_calc(function, *args, getter=None, override=None, _parent_override=None, **kwargs):
    if getter is None:
        raise RuntimeError("Must supply a getter argument!")

    override = override or {}

    if _parent_override:
        _parent_override.update(override)
        override = _parent_override

    def argument_getter(*args, **kwargs):
        res = getter(*args, **kwargs)
        if isinstance(res, NotDefined):
            return res.value
        return res

    default_args = {
        "run_calculation": partial(run_calc, getter=getter, _parent_override=override),
        "get": getter
    }

    extra_args = list(args)
    call_args = []
    argspec = inspect.getfullargspec(function)

    for func_arg in argspec.args:
        if func_arg not in argspec.annotations:
            if func_arg in default_args:
                call_args.append(default_args[func_arg])
            elif len(extra_args) == 0:
                raise RuntimeError("Not enough arguments passed to {0} ({1})".format(function.__name__, func_arg))
            else:
                call_args.append(extra_args.pop())
            continue

        annotated_type = argspec.annotations[func_arg]

        if override and annotated_type in override:
            value = override[annotated_type]
        else:
            value = argument_getter(annotated_type)

        call_args.append(
            value
        )

    result = function(*call_args, **kwargs)
    return result