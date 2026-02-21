import unittest
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from capri_llm.config.config_modules.base_config import BaseConfig


@dataclass
class InnerConfig(BaseConfig):
    """Nested config used to test recursive serialization."""

    block_size: int = 64
    max_num_blocks: int = 1024


@dataclass
class SampleConfig(BaseConfig):
    """Top-level config containing primitives, collections, and a nested config."""

    model_name: str = "Qwen3-Coder"
    model_type: str = "qwen_3_moe"
    num_layers: int = 32
    learning_rate: float = 1e-4
    enabled: bool = True
    tags: List[str] = field(default_factory=lambda: ["a", "b"])
    meta: Dict[str, int] = field(default_factory=lambda: {"x": 1})
    optional_field: Optional[str] = None
    inner: InnerConfig = field(default_factory=InnerConfig)


class BaseConfigTest(unittest.TestCase):
    """Tests for BaseConfig.__str__ hierarchical serialization."""

    def test_primitive_fields(self) -> None:
        """Primitive fields appear as 'key: value' lines."""
        cfg = SampleConfig()
        output: str = str(cfg)
        self.assertIn("model_name: Qwen3-Coder", output)
        self.assertIn("num_layers: 32", output)
        self.assertIn("learning_rate: 0.0001", output)
        self.assertIn("enabled: True", output)

    def test_none_field(self) -> None:
        """None values are rendered as the string 'None'."""
        cfg = SampleConfig()
        output: str = str(cfg)
        self.assertIn("optional_field: None", output)

    def test_list_and_dict_fields(self) -> None:
        """List and dict fields are rendered on a single line via repr."""
        cfg = SampleConfig()
        output: str = str(cfg)
        self.assertIn("tags: ['a', 'b']", output)
        self.assertIn("meta: {'x': 1}", output)

    def test_nested_config(self) -> None:
        """Nested BaseConfig subclass is recursively serialized."""
        cfg = SampleConfig()
        output: str = str(cfg)
        self.assertIn("InnerConfig: {", output)
        self.assertIn("block_size: 64", output)
        self.assertIn("max_num_blocks: 1024", output)

    def test_primitives_before_nested(self) -> None:
        """Primitive/collection fields appear before nested config blocks."""
        cfg = SampleConfig()
        output: str = str(cfg)
        model_name_pos: int = output.index("model_name:")
        inner_pos: int = output.index("InnerConfig:")
        self.assertLess(model_name_pos, inner_pos)

    def test_indentation(self) -> None:
        """Each nesting level indents by two additional spaces."""
        cfg = SampleConfig()
        lines: List[str] = str(cfg).splitlines()

        # Top-level class opens at column 0
        self.assertTrue(lines[0].startswith("SampleConfig: {"))

        # First-level fields indented by 2 spaces
        field_lines: List[str] = [l for l in lines if "model_name:" in l]
        self.assertEqual(len(field_lines), 1)
        self.assertTrue(field_lines[0].startswith("  model_name:"))

        # Nested config header indented by 2 spaces
        inner_lines: List[str] = [l for l in lines if "InnerConfig: {" in l]
        self.assertEqual(len(inner_lines), 1)
        self.assertTrue(inner_lines[0].startswith("  InnerConfig:"))

        # Nested config fields indented by 4 spaces
        block_lines: List[str] = [l for l in lines if "block_size:" in l]
        self.assertEqual(len(block_lines), 1)
        self.assertTrue(block_lines[0].startswith("    block_size:"))

    def test_closing_braces(self) -> None:
        """Opening and closing braces are present at correct indentation."""
        cfg = SampleConfig()
        lines: List[str] = str(cfg).splitlines()

        # Top-level closing brace at column 0
        self.assertEqual(lines[-1], "}")

        # Nested closing brace at 2-space indent
        inner_close_found: bool = any(l == "  }" for l in lines)
        self.assertTrue(inner_close_found)

    def test_full_output_format(self) -> None:
        """Exact match of the full serialized output."""
        cfg = SampleConfig()
        expected: str = (
            "SampleConfig: {\n"
            "  model_name: Qwen3-Coder\n"
            "  model_type: qwen_3_moe\n"
            "  num_layers: 32\n"
            "  learning_rate: 0.0001\n"
            "  enabled: True\n"
            "  tags: ['a', 'b']\n"
            "  meta: {'x': 1}\n"
            "  optional_field: None\n"
            "  InnerConfig: {\n"
            "    block_size: 64\n"
            "    max_num_blocks: 1024\n"
            "  }\n"
            "}"
        )
        self.assertEqual(str(cfg), expected)

    def test_inner_config_standalone(self) -> None:
        """Nested config can be serialized independently."""
        cfg = InnerConfig()
        expected: str = (
            "InnerConfig: {\n"
            "  block_size: 64\n"
            "  max_num_blocks: 1024\n"
            "}"
        )
        self.assertEqual(str(cfg), expected)

    def test_custom_values(self) -> None:
        """Non-default field values are reflected in the output."""
        cfg = SampleConfig(
            model_name="LLaMA-70B",
            num_layers=80,
            tags=["x"],
            inner=InnerConfig(block_size=128, max_num_blocks=2048),
        )
        output: str = str(cfg)
        self.assertIn("model_name: LLaMA-70B", output)
        self.assertIn("num_layers: 80", output)
        self.assertIn("tags: ['x']", output)
        self.assertIn("block_size: 128", output)
        self.assertIn("max_num_blocks: 2048", output)


if __name__ == "__main__":
    unittest.main()
