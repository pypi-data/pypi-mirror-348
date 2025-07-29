from typing import Any
from dataclasses import dataclass

import numpy as np

from .quantity import Quantity, update_unit

from .units import (
    Unit,
    find_unit,
    m_per_sec_to_km_per_hr,
    knots_to_m_per_sec,
    kelvin_to_celsius,
)


@dataclass(frozen=True)
class Array:
    """
    An ordered collection of data all with the same quantity.
    """

    quantity: Quantity
    data: Any


def append_array(source: Array, new: Array) -> Array:

    return Array(
        quantity=source.quantity, data=np.append(source.data, new.data, axis=0)
    )


def insert_array(source: Array, new: Array, idx: int) -> Array:

    return Array(
        quantity=source.quantity, data=np.insert(source.data, idx, new.data, axis=0)
    )


_CONVERSIONS = {
    "metres_per_second": {"kilometres_per_hour": m_per_sec_to_km_per_hr},
    "knots": {"metres_per_second": knots_to_m_per_sec},
    "kelvin": {"degrees_celsius": kelvin_to_celsius},
}


def convert(source: Array, target_unit: str, units: list[Unit]) -> Array:

    source_unit = source.quantity.unit.name
    if not target_unit or source_unit == target_unit:
        return Array(
            quantity=update_unit(source.quantity, find_unit(source_unit, units)),
            data=source.data,
        )

    if source_unit not in _CONVERSIONS:
        raise ValueError(f"No conversion from {source_unit}")

    if target_unit not in _CONVERSIONS[source_unit]:
        raise ValueError(f"No conversion from {source_unit} to {target_unit}")

    print(f"converting {source_unit} to {target_unit}")
    return Array(
        quantity=update_unit(source.quantity, find_unit(target_unit, units)),
        data=_CONVERSIONS[source_unit][target_unit](source.data),
    )
