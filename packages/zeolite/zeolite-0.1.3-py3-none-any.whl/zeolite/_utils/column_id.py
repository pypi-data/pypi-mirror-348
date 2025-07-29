from typing import Optional

COLUMN_NAME_DIVIDER = "__"
COLUMN_ID_DIVIDER = "::"


def extract_base_name(name: str) -> tuple[str, str]:
    base_name = name
    prefix = ""
    for p in ["custom_check", "derived", "meta"]:
        if base_name.startswith(f"{p}{COLUMN_NAME_DIVIDER}"):
            base_name = base_name.split(f"{p}{COLUMN_NAME_DIVIDER}")[1]
            prefix = prefix + f"{p}{COLUMN_NAME_DIVIDER}"
    return base_name.split(COLUMN_NAME_DIVIDER)[0], prefix


def make_column_id(
    name: str,
    *,
    schema: str,
    is_clean: bool = False,
    is_derived: bool = False,
    is_meta: bool = False,
    is_custom_check: bool = False,
    check_name: Optional[str] = None,
    stage: Optional[str] = None,
    alias_name: Optional[str] = None,
    include_schema_prefix: bool = True,
) -> str:
    base_name, _ = extract_base_name(name)

    # Build prefix
    prefix_parts = []
    if stage and include_schema_prefix:
        prefix_parts.append(stage)
    if schema and include_schema_prefix:
        prefix_parts.append(schema)
    if is_meta:
        prefix_parts.append("meta")
    if is_derived:
        prefix_parts.append("derived")
    if is_custom_check:
        prefix_parts.append("custom_check")

    prefix_parts.append(base_name)

    # Build type parts
    type_parts = []
    if is_clean:
        type_parts.append("clean")
    if check_name:
        type_parts.append("check")
        type_parts.append(check_name)

    column_id = COLUMN_ID_DIVIDER.join([*prefix_parts, *type_parts])

    # Add alias if specified
    if alias_name:
        column_id = f"{column_id}{COLUMN_ID_DIVIDER}alias{COLUMN_ID_DIVIDER}{alias_name}"

    return column_id
