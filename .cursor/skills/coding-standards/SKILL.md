---
name: coding-standards
description: Enforce project coding standards when developing features, refactoring code, or writing tests. Use when the user asks to implement new functionality, refactor existing code, add unit tests, or any task that involves writing or modifying source code.
---

# Coding Standards

## Language & Text

- All comments, error messages, docstrings, and log messages **must be in English**.

## Classes

- Every class must have a docstring immediately below the class name:

```python
class ModelConfig(BaseConfig):
    """Model-level configuration for inference."""
```

## Functions

- Every function (including methods) must have a docstring.
- Add inline comments before each core logic block inside a function body.
- Comment rules:
  - Capitalize the first letter.
  - Describe **what** the following block does, not how.
  - No obvious AI-generated phrasing.
  - One-line comment for simple logic; multi-line or an inline example for complex logic.

```python
def load_weights(self, path: str) -> None:
    """Load model weights from a checkpoint file."""
    # Validate the checkpoint path
    if not os.path.exists(path):
        raise FileNotFoundError(f"Checkpoint not found: {path}")

    # Deserialize weights into the model
    state = torch.load(path)
    self.model.load_state_dict(state)
```

## Type Hints

- Always annotate function parameters, return types, and key variables:

```python
def compute_blocks(num_tokens: int, block_size: int) -> int:
    """Compute the number of KV-cache blocks needed."""
    return (num_tokens + block_size - 1) // block_size
```

## Function Call Style

- **<= 2 args** → positional:

```python
os.path.join(base_dir, filename)
```

- **> 2 args** → keyword:

```python
torch.zeros(
    size=shape,
    dtype=torch.float16,
    device=device,
    requires_grad=False,
)
```

## C/C++ Formatting

When generating or editing C/C++ code, follow the project `.clang-format`:

| Rule | Value |
|------|-------|
| Indent | 4 spaces, no tabs |
| Column limit | 120 |
| Braces | Attach (K&R) |
| Pointer alignment | Left (`int* p`) |
| Bin-pack args/params | No (one per line when wrapped) |
| Trailing comment spacing | 2 spaces |
| Short blocks/functions | Empty body only |

## Python Formatting

Align with the C/C++ style where applicable:

- 4-space indent, no tabs.
- Line length <= 120 characters.
- At most 1 consecutive blank line.

## Refactoring

- Preserve the original code style; do not reformat unchanged lines.
- All rules above still apply to newly written or modified code.

## Unit Tests

- Use the `unittest` module.
- Test class naming: `<Feature>Test`, e.g. `class DeepGemmMaskedExecutorTest(unittest.TestCase)`.
- All test methods start with `test_`.
- End the file with:

```python
if __name__ == "__main__":
    unittest.main()
```

- Example skeleton:

```python
import unittest


class KVCacheAllocatorTest(unittest.TestCase):
    """Tests for the KV-cache block allocator."""

    def test_allocate_single_block(self) -> None:
        """Allocate one block and verify the returned index."""
        allocator = KVCacheAllocator(num_blocks=16)
        block_id = allocator.allocate()
        self.assertIsNotNone(block_id)

    def test_free_block(self) -> None:
        """Free a block and verify it returns to the pool."""
        allocator = KVCacheAllocator(num_blocks=16)
        block_id = allocator.allocate()
        allocator.free(block_id)
        self.assertEqual(allocator.available(), 16)


if __name__ == "__main__":
    unittest.main()
```
