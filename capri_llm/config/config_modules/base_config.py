from dataclasses import dataclass, fields


@dataclass
class BaseConfig:
    """Config base; subclasses get hierarchical __str__ of all fields."""

    def _is_primitive_or_collection(self, value) -> bool:
        """Primitive, list, or dict (not BaseConfig)."""
        if value is None:
            return True
        if isinstance(value, (int, float, str, bool)):
            return True
        if isinstance(value, (list, dict)):
            return True
        return False

    def _format_value(self, value, indent: str) -> str:
        """Primitives as str; list/dict one line; BaseConfig recursed."""
        if isinstance(value, BaseConfig):
            return value._to_str(indent)
        if isinstance(value, (list, dict)):
            return repr(value)
        if value is None:
            return "None"
        return str(value)

    def _to_str(self, base_indent: str = "") -> str:
        inner_indent = base_indent + "  "
        class_name = self.__class__.__name__
        lines = [f"{base_indent}{class_name}: {{"]

        # Primitives first, then BaseConfig subclasses
        primitives = []
        config_objs = []
        for f in fields(self):
            if not f.repr:
                continue
            name = f.name
            value = getattr(self, name, None)
            if self._is_primitive_or_collection(value):
                primitives.append((name, value))
            else:
                config_objs.append((name, value))

        for name, value in primitives:
            formatted = self._format_value(value, inner_indent)
            lines.append(f"{inner_indent}{name}: {formatted}")

        for name, value in config_objs:
            formatted = self._format_value(value, inner_indent)
            lines.append(formatted)

        lines.append(f"{base_indent}}}")
        return "\n".join(lines)

    def __str__(self) -> str:
        return self._to_str("")
