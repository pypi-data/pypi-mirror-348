from dataclasses import dataclass, field, replace
from typing import List, Literal

from polars import LazyFrame

from ._utils.normalise import normalise_column_headers
from ..types import (
    ColumnNode, SourceColDef, ThresholdLevel,
    ValidationResult, ProcessingFailure, ProcessingSuccess
)
from .._utils.args import flatten_args
from .._utils.sanitize import sanitise_column_name
from ..column import ColumnSchema
from ..registry import ColumnRegistry, generate_optimized_stages


@dataclass(frozen=True, kw_only=True)
class _SchemaParams:
    name: str
    is_required: bool = False
    stage: str | None = None
    source_columns: dict[str, SourceColDef] = field(default_factory=dict)
    registry: ColumnRegistry = field(default_factory=ColumnRegistry)


class TableSchema:
    """
    Defines a table schema for data validation and processing.

    Parameters:
        name (str): Name of the schema.
        is_required (bool): Whether the schema is required.
        columns (List[ColumnSchema], optional): List of column schemas.
        stage (str, optional): Processing stage.

    Usage:
        schema = TableSchema("demo", columns=[...])
    """

    def __init__(
            self,
            name: str,
            *,
            is_required: bool = False,
            columns: List[ColumnSchema] | None = None,
            stage: str | None = None,
    ):
        nodes = _cols_to_nodes(schema=name, stage=stage, columns=columns)

        self._params = _SchemaParams(
            name=name,
            is_required=is_required,
            stage=stage,
            registry=ColumnRegistry(nodes),
            source_columns=_cols_to_sources(columns),
        )

    def columns(
            self,
            *args: List[ColumnSchema] | ColumnSchema,
            method: Literal["merge", "replace"] = "merge",
    ) -> "TableSchema":
        columns = flatten_args(args)
        if method == "merge":
            new_nodes = _cols_to_nodes(
                self._params.name, self._params.stage, columns=columns
            )

            new_registry = _reset_registry(self._params.registry.nodes() + new_nodes)

            new_source_columns = {
                **self._params.source_columns,
                **_cols_to_sources(columns),
            }
            return self._replace(
                registry=new_registry, source_columns=new_source_columns
            )

        elif method == "replace":
            new_registry = _reset_registry(
                _cols_to_nodes(self._params.name, self._params.stage, columns=columns)
            )
            new_source_columns = _cols_to_sources(columns)
            return self._replace(
                registry=new_registry, source_columns=new_source_columns
            )
        else:
            raise ValueError(f"Invalid method: {method}")

    def required(self, is_required: bool = True) -> "TableSchema":
        """Set the schema as required"""
        return self._replace(is_required=is_required)

    @property
    def name(self) -> str:
        """Get the name of the table schema"""
        return self._params.name

    @property
    def is_required(self) -> bool:
        """Get the required status of the table schema"""
        return self._params.is_required

    @property
    def stage(self) -> str:
        """Get the stage of the table schema"""
        return self._params.stage

    def step_1_normalise(self, lf: LazyFrame) -> ValidationResult:
        """Normalise the headers of the lazy frame"""
        source_columns = list(self._params.source_columns.values())
        return normalise_column_headers(
            lf.lazy(), schema_name=self._params.name, col_defs=source_columns
        )

    def step_2_prepare(self, lf: LazyFrame) -> ValidationResult:
        prepped = lf

        stages = generate_optimized_stages(self._params.registry.nodes())

        for stage in stages:
            prepped = prepped.with_columns([c.expression for c in stage])

        # TODO: Add a check to see if the processing stages succeed
        return ValidationResult(data=prepped, errors=[], reject=False)

    def step_3_validate(self, lf: LazyFrame) -> ValidationResult:
        validation_errors = []
        for c in self._params.registry.nodes():
            if c.validation_rule is None:
                continue
            check = c.validation_rule.validate(lf)
            if check is not None:
                validation_errors.append(c.validation_rule.validate(lf))

        reject = False
        for e in validation_errors:
            if e.level == ThresholdLevel.REJECT.level:
                reject = True
                break

        return ValidationResult(data=lf, errors=validation_errors, reject=reject)

    def process_data(self, lf: LazyFrame) -> ProcessingFailure | ProcessingSuccess:
        """Process the lazy frame through the schema"""
        errors = []
        normalised = self.step_1_normalise(lf)
        errors.extend(normalised.errors)
        if normalised.reject:
            return ProcessingFailure(
                normalised=normalised.data,
                prepared=None,
                validated=None,
                errors=errors,
                failed_stage="normalise",
            )

        prepped = self.step_2_prepare(normalised.data)
        errors.extend(prepped.errors)
        if prepped.reject:
            return ProcessingFailure(
                normalised=normalised.data,
                prepared=prepped.data,
                validated=None,
                errors=errors,
                failed_stage="prepare"
            )

        valid = self.step_3_validate(prepped.data)
        errors.extend(valid.errors)

        if valid.reject:
            return ProcessingFailure(
                normalised=normalised.data,
                prepared=prepped.data,
                validated=valid.data,
                errors=errors,
                failed_stage="validate",
            )

        # If we get here, the data is valid
        return ProcessingSuccess(
            normalised=normalised.data,
            prepared=prepped.data,
            validated=valid.data,
            errors=errors,
        )

    def _replace(self, **kwargs):
        if "registry" not in kwargs:
            stage = kwargs.get("stage", self._params.stage)
            name = kwargs.get("name", self._params.name)
            kwargs["registry"] = ColumnRegistry(
                [
                    replace(n, stage=stage, schema=name)
                    for n in self._params.registry.nodes()
                ]
            )

        new_params = replace(self._params, **kwargs)
        return TableSchema(name=new_params.name).__set_params(new_params)

    def __set_params(self, params: _SchemaParams) -> "TableSchema":
        self._params = params
        return self


def _cols_to_nodes(
        schema: str, stage: str | None = None, columns: List[ColumnSchema] | None = None
) -> List[ColumnNode]:
    nodes = []
    if columns is None:
        return nodes

    for c in columns:
        assert isinstance(c, ColumnSchema), (
            f"All columns must be a Column Schema definition - {c}"
        )
        nodes.extend(c.get_nodes(schema, stage))

    return nodes


def _cols_to_sources(columns: List[ColumnSchema] | None) -> dict[str, SourceColDef]:
    sources = {}
    aliases = {}
    if columns is None:
        return sources
    for c in columns:
        if c.has_expression:
            # if a column has an expression, it is not a source column
            continue

        ref = c.ref

        if ref.name in sources:
            raise ValueError(f"Duplicate source column name: {ref.name}")
        else:

            col_aliases = {sanitise_column_name(a) for a in c.get_aliases}
            col_aliases.add(sanitise_column_name(ref.name))

            # Check if the alias is already in use
            for a in col_aliases:
                if a in aliases:
                    raise ValueError(
                        f"Duplicate column alias: The sanitized alias `{a}` for column `{ref.name}` already used for `{aliases[a]}`"
                    )
                else:
                    aliases[a] = ref.name

            sources[ref.name] = SourceColDef(
                name=ref.name, aliases=col_aliases, if_missing=c.if_missing, is_meta=c.ref.is_meta
            )

    return sources


def _reset_registry(nodes: List[ColumnNode], **kwargs):
    return ColumnRegistry([replace(n, **kwargs) for n in nodes])
