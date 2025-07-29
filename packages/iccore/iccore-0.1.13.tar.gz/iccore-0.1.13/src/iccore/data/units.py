"""
Module for handling units and quantities
"""

from pathlib import Path
import json
from dataclasses import dataclass
from datetime import date, datetime, timedelta

from pydantic import BaseModel


@dataclass(frozen=True)
class Unit:
    """
    A unit of measurement

    :cvar name: A short name for the unit
    :cvar long_name: A longer name for the unit, as might be shown in a plot
    :cvar symbol: A symbol for the unit
    """

    name: str
    long_name: str = ""
    symbol: str = ""

    @property
    def unset(self) -> bool:
        return not self.name

    def get_long_name(self) -> str:
        if self.long_name:
            return self.long_name
        return self.name

    def get_symbol(self) -> str:
        if self.symbol:
            return self.symbol
        return self.name


def load_default_units() -> list[Unit]:
    return load_units(Path(__file__).parent / "units.json")


def load_units(path: Path) -> list[Unit]:
    """
    Load a unit definition file from the provided path
    """
    with open(path, "r", encoding="utf8") as f:
        data = json.load(f)

    return [Unit(**u) for u in data["items"]]


def find_unit(name: str, units: list[Unit]) -> Unit:
    for unit in units:
        if unit.name == name:
            return unit
    raise ValueError(f"Requested unit {name} not found")


class DateRange(BaseModel, frozen=True):
    """
    A date range, useful for defining the extents of a time series
    """

    start: date | None
    end: date | None

    def as_tuple(self) -> tuple[date | None, ...]:
        return self.start, self.end


def m_per_sec_to_km_per_hr(value):
    return value * (3600.0) / (1000.0)


def knots_to_m_per_sec(value):
    return (value * 1852.0) / (3600.0)


def kelvin_to_celsius(value):
    return value - 273.1


def timestamp_from_seconds_since(count, relative_to: str):
    reference = datetime.fromisoformat(relative_to)
    reference += timedelta(seconds=count)
    return reference


def to_date_str(date_item: date):
    return f"{date_item.year}-{date_item.month}-{date_item.day}"


def to_timestamps(times, since: str):
    return [timestamp_from_seconds_since(int(t), since) for t in times]
