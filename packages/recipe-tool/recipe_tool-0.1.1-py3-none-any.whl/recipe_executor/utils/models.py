"""
Utility functions for generating Pydantic models from JSON-Schema object definitions.
"""
from typing import Any, Dict, List, Optional, Tuple, Type

from pydantic import BaseModel, create_model

__all__ = ["json_object_to_pydantic_model"]


def json_object_to_pydantic_model(
    schema: Dict[str, Any], model_name: str = "SchemaModel"
) -> Type[BaseModel]:
    """
    Convert a JSON-Schema object fragment into a Pydantic BaseModel subclass.

    Args:
        schema: A JSON-Schema fragment describing an object (type must be "object").
        model_name: Name for the generated Pydantic model class.

    Returns:
        A subclass of pydantic.BaseModel corresponding to the schema.

    Raises:
        ValueError: If the schema is invalid or unsupported.
    """
    # Validate top-level schema
    if not isinstance(schema, dict):
        raise ValueError("Schema must be a dictionary.")
    if "type" not in schema:
        raise ValueError('Schema missing required "type" property.')
    if schema["type"] != "object":
        raise ValueError('Root schema type must be "object".')

    properties = schema.get("properties", {})
    required_fields = schema.get("required", [])
    if not isinstance(properties, dict):
        raise ValueError('Schema "properties" must be a dictionary if present.')
    if not isinstance(required_fields, list):
        raise ValueError('Schema "required" must be a list if present.')

    # Counter for naming nested models deterministically
    class _Counter:
        def __init__(self) -> None:
            self._cnt = 0

        def next(self) -> int:
            self._cnt += 1
            return self._cnt

    counter = _Counter()

    def _parse_field(
        field_schema: Dict[str, Any], field_name: str, parent_name: str
    ) -> Tuple[Any, Any]:
        # Ensure valid schema fragment
        if not isinstance(field_schema, dict):
            raise ValueError(f"Schema for field '{field_name}' must be a dictionary.")
        if "type" not in field_schema:
            raise ValueError(f"Schema for field '{field_name}' missing required 'type'.")

        ftype = field_schema["type"]
        # Primitive types
        if ftype == "string":
            return str, ...
        if ftype == "integer":
            return int, ...
        if ftype == "number":
            return float, ...
        if ftype == "boolean":
            return bool, ...
        # Nested object
        if ftype == "object":
            nested_name = f"{parent_name}_{field_name.capitalize()}Obj{counter.next()}"
            nested_model = _build_model(field_schema, nested_name)
            return nested_model, ...
        # Array / list
        if ftype in ("array", "list"):
            items = field_schema.get("items")
            if not isinstance(items, dict):
                raise ValueError(
                    f"Array field '{field_name}' missing valid 'items' schema."
                )
            item_type, _ = _parse_field(items, f"{field_name}_item", parent_name)
            return List[item_type], ...
        # Fallback
        return Any, ...

    def _wrap_optional(
        field_schema: Dict[str, Any], is_required: bool, field_name: str, parent_name: str
    ) -> Tuple[Any, Any]:
        type_hint, default = _parse_field(field_schema, field_name, parent_name)
        if not is_required:
            type_hint = Optional[type_hint]  # type: ignore
            default = None
        return type_hint, default

    def _build_model(obj_schema: Dict[str, Any], name: str) -> Type[BaseModel]:
        # Validate object schema
        if not isinstance(obj_schema, dict):
            raise ValueError(f"Nested schema '{name}' must be a dictionary.")
        if obj_schema.get("type") != "object":
            raise ValueError(f"Nested schema '{name}' type must be 'object'.")

        props = obj_schema.get("properties", {})
        req = obj_schema.get("required", [])
        if not isinstance(props, dict):
            raise ValueError(f"Nested schema '{name}' properties must be a dictionary.")
        if not isinstance(req, list):
            raise ValueError(f"Nested schema '{name}' required must be a list.")

        fields: Dict[str, Tuple[Any, Any]] = {}
        for prop, subschema in props.items():
            is_req = prop in req
            hint, default = _wrap_optional(subschema, is_req, prop, name)
            fields[prop] = (hint, default)

        return create_model(name, **fields)  # type: ignore

    # Build and return the top-level model
    return _build_model(schema, model_name)
