from typing import Optional, Tuple

import click
from click import Parameter, Context


class NameEqualsValueType(click.ParamType):
    name = "name_eq_value"

    def convert(
            self,
            value: str,
            param: Optional[Parameter],
            ctx: Optional[Context]
    ) -> Tuple[str, Optional[str]]:
        name, sep, val = value.partition("=")
        if sep == "=":
            return name, val
        else:
            return name, None


NAME_EQ_VALUE = NameEqualsValueType()
