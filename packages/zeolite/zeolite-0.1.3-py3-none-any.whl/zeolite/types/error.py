from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal

from .validation.threshold import CheckLevel


@dataclass(frozen=True)
class SchemaValidationError:
    schema: str

    error: str
    level: CheckLevel
    message: str
    column: str | None = None
    fraction_failed: str | None = None
    count_failed: str | None = None
    category: Literal["file", "schema", "logic"] = field(init=False, default="unknown")

    # Meta fields
    source: str | None = None
    batch: datetime | None = None
    period: str | None = None
    year: str | None = None

    def with_meta(self, *, source: str, period: str, year: str, batch: datetime):
        object.__setattr__(self, "source", source)
        object.__setattr__(self, "batch", batch)
        object.__setattr__(self, "period", period)
        object.__setattr__(self, "year", year)

        return self


@dataclass(frozen=True)
class UnknownValidationError(SchemaValidationError):
    category = "unknown"
    level: CheckLevel
    column: None = field(init=False, default=None)


@dataclass(frozen=True)
class FileValidationError(SchemaValidationError):
    category = "file"
    level: CheckLevel
    column: None = field(init=False, default=None)


@dataclass(frozen=True)
class StructureValidationError(SchemaValidationError):
    category = "schema_structure"
    level: CheckLevel
    column: str | None = None


@dataclass(frozen=True)
class DataValidationError(SchemaValidationError):
    category = "row_data"
    level: CheckLevel
    column: str

