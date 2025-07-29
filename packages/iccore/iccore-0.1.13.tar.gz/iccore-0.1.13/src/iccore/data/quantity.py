"""
Module for a measureable quantity
"""

from datetime import date

from pydantic import BaseModel

from .units import Unit, DateRange


class Quantity(BaseModel, frozen=True):
    """
    A measurable quantity, including physical quantities

    :cvar name: A concise name or label
    :cvar unit: A measurement unit, default to dimensionless
    :cvar description: A description of the quantity
    :cvar long_name: A long name as might appear in a plot axis
    :cvar min_value: The minimal value to cutoff at
    :cvar max_value: The max value to cutoff at
    :cvar dates: Date range to cutoff values
    :cvar sensor: Name of the generating sensor
    :cvar schema: Name of the source dataset schema
    """

    name: str
    unit: Unit = Unit(name="")
    description: str = ""
    long_name: str = ""
    min_value: float | None = None
    max_value: float | None = None
    dates: DateRange | None = None
    sensor: str = ""
    schema_name: str = "default"

    @property
    def has_limits(self) -> bool:
        return (self.min_value is not None) and (self.max_value is not None)

    @property
    def limits(self) -> tuple[float | None, ...]:
        if not self.has_limits:
            raise ValueError("Requested limits but none set")

        return self.min_value, self.max_value


def find(name: str, quantities: list[Quantity]) -> Quantity:
    """
    Find the named quantity in a list
    """

    for q in quantities:
        if q.name == name:
            return q
    raise RuntimeError(f"Couldn't find quantity {name}.")


def update_dates(
    quantity: Quantity, start_date: date | None, end_date: date | None
) -> Quantity:
    return quantity.model_copy(
        update={"dates": DateRange(start=start_date, end=end_date)}
    )


def update_unit(quantity: Quantity, unit: Unit) -> Quantity:
    return quantity.model_copy(update={"unit": unit})


def sync(original: Quantity, updated: Quantity) -> Quantity:

    return original.model_copy(
        update={
            "dates": updated.dates,
            "min_value": updated.min_value,
            "max_value": updated.max_value,
        }
    )
