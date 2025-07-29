"""
A schema to describe a dataset. Its specification allows loading the
dataset in a standard format.
"""

from pydantic import BaseModel

from .quantity import Quantity


class ArraySchema(BaseModel, frozen=True):
    """
    A description of a dataset entry corresponding to a measurable
    quantity. This might be a column in a csv or a variable in a netcdf.

    This includes information useful for extracting the quantity's values
    from the dataset.

    :cvar quantity: The measurement quantity
    :cvar name: The name of the quantity as it appears in the dataset if different
    from quantity name.
    :cvar column: If dealing with columnar data this is the column index
    :cvar dimension: The dimensionality of the data
    """

    quantity: Quantity
    name: str = ""
    column: int = 0
    dimension: int = 1

    def get_name(self) -> str:
        if self.name:
            return self.name
        return self.quantity.name


class Schema(BaseModel, frozen=True):
    """
    A schema for a dataset to allow loading its content into a standard format.

    :cvar name: A concise name or label
    :cvar format: The format such as an extension for a file source
    :cvar items: A list of expected quantities
    :cvar type_specs: Type hints for csv loader performance
    :cvar x: Description of the x or index values
    :cvar y: Optional 'y' values for 2d datasets
    """

    name: str
    format: str
    description: str = ""
    values: list[ArraySchema]
    x: ArraySchema
    y: ArraySchema | None
    type_specs: dict[str, str] = {}
    group_prefix: str = ""
    path_excludes: list[str] = []

    def get_quantity(self, name: str) -> Quantity:

        for v in self.values:
            if v.quantity.name == name:
                return v.quantity
        raise ValueError(f"No quantity {name} in schema {self.name}")


def get_quantity(name: str, schema: Schema) -> Quantity:

    for v in schema.values:
        if v.quantity.name == name:
            return v.quantity
    raise ValueError(f"No quantity {name} in schema {schema.name}")
