"""
A collection of values of type described by an associated quantity.
"""

from pydantic import BaseModel

from .array import Array, append_array, insert_array


class Series(BaseModel):
    """
    A collection of arrays, each with the same quantity.

    :cvar x: The x axis values correspond to the values
    :cvar y: Optional extra values for 2d series (e.g. height)
    """

    values: list[Array] = []
    x: Array | None = None
    y: Array | None = None
    name: str = ""
    components: list["Series"] = []

    @property
    def is_compound(self) -> bool:
        return not self.x

    def get_array(self, quantity_name: str) -> Array:

        for a in self.values:
            if a.quantity.name == quantity_name:
                return a
        raise ValueError(f"No array found with quantity name {quantity_name}")


def insert_compound_series(source: Series, new: Series) -> Series:

    return Series(
        components=[
            insert_series(s, n) for s, n in zip(source.components, new.components)
        ]
    )


def insert_series(source: Series, new: Series) -> Series:

    if source.is_compound:
        return insert_compound_series(source, new)

    if not source.x:
        raise RuntimeError("Attempting to insert series with no source value")

    if not new.x:
        raise RuntimeError("Attempting to insert series with no target value")

    if new.x.data[0] > source.x.data[-1]:
        return Series(
            x=append_array(source.x, new.x),
            y=source.y,
            name=source.name,
            values=[
                append_array(source.values[idx], new.values[idx])
                for idx in range(len(source.values))
            ],
        )

    if new.x.data[0] < source.x.data[0]:
        return Series(
            x=append_array(new.x, source.x),
            y=source.y,
            name=source.name,
            values=[
                append_array(new.values[idx], source.values[idx])
                for idx in range(len(source.values))
            ],
        )
    for jdx, x in enumerate(source.x.data):
        if new.x.data[0] < x:
            return Series(
                x=insert_array(source.x, new.x, jdx),
                y=source.y,
                name=source.name,
                values=[
                    insert_array(source.values[idx], new.values[idx], jdx)
                    for idx in range(len(source.values))
                ],
            )
    raise RuntimeError("Unexpected source and target series overlap")
