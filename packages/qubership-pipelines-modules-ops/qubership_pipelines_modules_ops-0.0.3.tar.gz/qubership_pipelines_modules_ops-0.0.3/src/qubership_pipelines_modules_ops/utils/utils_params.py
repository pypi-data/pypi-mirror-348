import os
import re

import logging
logger = logging.getLogger(__name__)

def cast_string_value(s: str):
    if not s: return s
    try: return int(s)
    except ValueError: pass
    try: return float(s)
    except ValueError: pass
    s_lower = s.lower()
    if s_lower == 'true': return True
    if s_lower == 'false': return False
    return s

def cast_to_string(value, value_for_none=''):
    if isinstance(value, str): return value
    if value is None: return value_for_none
    if isinstance(value, bool): return 'true' if value else 'false'
    return str(value)


VAR_PATTERN = re.compile(
        r'\$\{(?:env:)?([a-zA-Z_]\w*)\}|\$([a-zA-Z_]\w*)')  # handle optional prefix 'env:' as a W/A for gitlab-ci-local
VAR_MAX_NESTING_LEVEL = 100
def substitute_string(known_vars=None, *, var_name=None, expression=None) -> str:
    if known_vars is None:
        known_vars = os.environ

    if var_name is not None:  # calculate variable
        expression = known_vars.get(var_name)
        description = f"variable '{var_name}'"
    else:  # calculate expression
        description = f"expression '{expression}'"

    if not isinstance(expression, str):
        return cast_to_string(expression)
    value = expression
    for _ in range(VAR_MAX_NESTING_LEVEL):
        value, repl_n = re.subn(VAR_PATTERN, lambda m: cast_to_string(known_vars.get(m[1] or m[2])), value)
        if repl_n:
            logger.debug(f"Calculated {description}: {value}")
        else:
            return value
    raise ValueError(f"Variables substitution exceeded {VAR_MAX_NESTING_LEVEL} nesting levels for {description}")

class StringSubstitution:
    def __init__(self, known_vars:dict = None, *,
                cast_string_value:bool = True):
        self.known_vars = known_vars
        self.cast_string_value = cast_string_value

    def _transform_value(self, value):
        if self.cast_string_value:
            value = cast_string_value(value)
        return value

    def calculate_variable(self, var_name: str) -> str:
        return self._transform_value(substitute_string(self.known_vars, var_name=var_name))

    def calculate_expression(self, expression) -> str:
        return self._transform_value(substitute_string(self.known_vars, expression=expression))
