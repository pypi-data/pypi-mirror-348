"""
A data source, such as a feed or sensor
"""

import logging
from pathlib import Path
import json

from pydantic import BaseModel

from iccore.filesystem import get_json_files

from .schema import Schema
from .units import Unit, find_unit

logger = logging.getLogger(__name__)


def load_model(path: Path, model_type):
    with open(path, "r", encoding="utf8") as f:
        data = json.load(f)
    return model_type(**data)


class Source(BaseModel, frozen=True):
    """
    A sensor has one or more datasources, it may be a piece of measurement equipment
    """

    name: str
    dataset_schemas: list[Schema] = []

    def get_schema(self, name: str) -> Schema:
        for s in self.dataset_schemas:
            if s.name == name:
                return s
        raise ValueError(f"Source schema {name} not found.")


def find_source(name: str, sources: list[Source]) -> Source:
    """
    Find a named sensor in the provided list
    """

    for s in sources:
        if s.name == name:
            return s
    raise ValueError(f"Source with name {name} not found.")


def _validate_units(source: Source, units: list[Unit]):

    for schema in source.dataset_schemas:
        for array in schema.values:
            if array.quantity.unit:
                try:
                    find_unit(array.quantity.unit.name, units)
                except Exception as e:
                    raise RuntimeError(
                        f"Unit {array.quantity.unit.name} in {array.quantity.name} "
                        f"not found. {e}"
                    )


def load(path: Path, units: list[Unit]) -> Source:
    """
    Load a source description from a json file.

    :param path: Path to the loading python source file.
    """
    logger.info("Loading %s", path)
    model = load_model(path.parent / (path.stem + ".json"), Source)
    _validate_units(model, units)
    return model


def load_all(path: Path, units: list[Unit]) -> list[Source]:
    """
    Load all sensor definition json files found in the provided
    directory.
    """
    return [load(f, units) for f in get_json_files(path)]
