from dataclasses import dataclass, field, KW_ONLY, replace
from typing import TYPE_CHECKING, Literal, Optional

from polars import Expr

from ...types.validation.threshold import Threshold, CheckThreshold, CheckLevel
from .validation_node import get_validation_node

if TYPE_CHECKING:
    from ...ref import ColumnRef
    from ...types import ColumnNode

type ThresholdType = Threshold | dict[str, CheckThreshold] | None


@dataclass(frozen=True)
class RowCheckBase:
    """Configuration for a row check"""

    _: KW_ONLY
    exclude_row: bool = False
    alias: str | None = None
    check_on_cleaned: bool = False
    message: str = field(default="")
    thresholds: ThresholdType = None
    debug: Optional[CheckThreshold] = None
    warning: Optional[CheckThreshold] = None
    error: Optional[CheckThreshold] = None
    reject: Optional[CheckThreshold] = None

    _label: str | None = field(init=False, default=None)

    @classmethod
    def method_id(cls) -> str:
        return "__check_base__"

    def __post_init__(self):
        object.__setattr__(self, "thresholds", self._get_threshold())

    def _get_threshold(self) -> Threshold | None:
        # If we are excluding the row, we want to reject when all rows fail
        default_reject: Literal["all"] | None = (
            "all" if self.exclude_row is True else None
        )

        # self.thresholds takes precedence over self.warning, self.error, self.reject
        if self.thresholds is None:
            if (
                self.debug is not None
                or self.warning is not None
                or self.error is not None
                or self.reject is not None
            ):
                return Threshold(
                    debug=self.debug,
                    warning=self.warning,
                    error=self.error,
                    reject=self.reject or default_reject,
                )

            if self.exclude_row is True:
                return Threshold(warning=True, reject=default_reject)
            else:
                return None

        elif isinstance(self.thresholds, Threshold):
            return Threshold(
                debug=self.thresholds.debug,
                warning=self.thresholds.warning,
                error=self.thresholds.error,
                reject=self.thresholds.reject or default_reject,
            )
        elif isinstance(self.thresholds, dict):
            # invalid_keys = set(self.thresholds.keys()) - {"warning", "error", "reject"}
            # if invalid_keys:
            #     raise ValueError(f"Invalid keys in thresholds: {invalid_keys}")
            return Threshold(
                debug=self.thresholds.get("debug", None),
                warning=self.thresholds.get("warning", None),
                error=self.thresholds.get("error", None),
                reject=self.thresholds.get("reject", default_reject),
            )
        else:
            raise ValueError(f"Invalid type for thresholds: {type(self.thresholds)}")

    def validation_thresholds(
        self,
        debug: Optional[CheckThreshold] = None,
        warning: Optional[CheckThreshold] = None,
        error: Optional[CheckThreshold] = None,
        reject: Optional[CheckThreshold] = None,
        thresholds: Optional[ThresholdType] = None,
        message: Optional[str] = None,
    ):
        """Configure thresholds for this check"""
        if (
            (thresholds is None)
            and (debug is None)
            and (warning is None)
            and (error is None)
            and (reject is None)
        ):
            raise ValueError(
                "At least one of `thresholds`, `debug`, `warning`, `error`, or `reject` must be provided"
            )

        new_thresholds = (
            thresholds
            if thresholds is not None
            else Threshold(debug=debug, warning=warning, error=error, reject=reject)
        )

        return replace(self, thresholds=new_thresholds, message=message or self.message)

    def get_validation_node(self, source_column: "ColumnRef") -> "ColumnNode":
        """Create a validation node for this check"""
        return get_validation_node(
            check=self,
            source_column=source_column,
            thresholds=self._get_threshold(),
            check_on_cleaned=self.check_on_cleaned,
            alias=self.alias,
            label=self._label,
        )

    def _check_expression(
        self, source_column: str, alias: str, level: CheckLevel
    ) -> Expr:
        """Check expression for this check"""
        raise NotImplementedError("Must be implemented in subclass")
