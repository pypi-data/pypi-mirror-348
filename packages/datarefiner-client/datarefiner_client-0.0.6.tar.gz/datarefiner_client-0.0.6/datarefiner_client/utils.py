from dataclasses import fields, is_dataclass
from typing import List


def _jupyter_repr_pretty_(obj) -> List[str]:
    repr_lines: List[str] = [f"{obj.__class__.__name__}"]
    for f in fields(obj):
        field_value = getattr(obj, f.name)
        if isinstance(field_value, (list, tuple, set)):
            repr_lines.append(f"\t{f.name}:")
            repr_lines.extend(f"\t\t{v}" for v in field_value)
        elif isinstance(field_value, dict):
            repr_lines.append(f"\t{f.name}:")
            repr_lines.extend(f"\t\t{k}: {v}" for k, v in field_value.items())
        elif is_dataclass(field_value):
            field_value_lines: List[str] = _jupyter_repr_pretty_(field_value)
            repr_lines.append(f"\t{f.name}: {field_value_lines[0]}")
            repr_lines.extend([f"\t{line}" for line in field_value_lines[1:]])
        else:
            repr_lines.append(f"\t{f.name}: {field_value}")
    return repr_lines


class JupyterDataclass(type):
    def __init__(cls, clsname, superclasses, attributedict):
        cls._repr_pretty_ = lambda obj, p, cycle: p.text("\n".join(_jupyter_repr_pretty_(obj)))


def is_notebook() -> bool:
    try:
        shell = get_ipython().__class__.__name__
        if shell == "ZMQInteractiveShell":
            return True  # Jupyter notebook or qtconsole
        elif shell == "TerminalInteractiveShell":
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False  # Probably standard Python interpreter
