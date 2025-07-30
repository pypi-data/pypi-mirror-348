# cargo-aidoc

`cargo-aidoc` is a Python script that leverages Large Language Models (LLMs) to automatically generate documentation comments for Rust code items like functions, structs, enums, etc.

## Features

*   Analyzes Rust source files using `tree-sitter`.
*   Identifies documentable items (functions, structs, enums, etc.).
*   Uses LLMs (configurable via `mirascope`) to generate documentation comments.
*   Integrates with Git to prevent overwriting uncommitted changes (can be overridden with `--force`).
*   Configurable via `cargo-aidoc.toml`.
*   Supports dry runs to preview generated documentation.

## Installation

This project uses `uv` for package management.

```
uv tool install cargo-aidoc
```

## Usage

Run the script pointing it to the root of your Rust crate:

```bash
cargo aidoc /path/to/your/rust/crate
```

**Options:**

*   `CRATE_PATH`: (Required) The path to the Rust crate directory.
*   `-q`, `--quiet`: Disable verbose output.
*   `--dry-run`: Generate documentation but do not write changes to the files.
*   `--force`: Ignore the Git uncommitted changes check and modify files directly.
*   `-c`, `--clean-cache`: Remove the `.cargo-aidoc` cache directory after execution.

**Example:**

```bash
# Generate docs for a crate, showing verbose output, but don't modify files
cargo aidoc . --quiet --dry-run

# Generate and write docs, forcing overwrite even with uncommitted changes
cargo aidoc . --force
```

## Configuration

The script looks for a `cargo-aidoc.toml` file in the root of the target crate. If it doesn't exist, a default one will be created.

**Default `cargo-aidoc.toml`:**

```toml
[llm]
# Configuration passed to mirascope.llm.call
# See mirascope documentation for options
provider = "openai"
model = "gpt-4o"
call_params = {} # e.g., {"temperature": 0.5}

[doc]
# Glob pattern relative to the crate root for source files
source = ["src/**/*.rs"]
# Types of items to document
item_types = ["fn", "struct", "enum", "union", "trait", "macro", "static"]
```

You can customize the LLM provider, model, call parameters, source file pattern, and the types of Rust items you want to document.

## Dependencies

*   [click](https://pypi.org/project/click/): For creating the command-line interface.
*   [toml](https://pypi.org/project/toml/): For parsing the configuration file.
*   [tree-sitter](https://pypi.org/project/tree-sitter/): The core parsing library.
*   [tree-sitter-rust](https://pypi.org/project/tree-sitter-rust/): Rust grammar for tree-sitter.
*   [mirascope](https://github.com/Mirascope/mirascope): For interacting with LLMs.
*   [termcolor](https://pypi.org/project/termcolor/): For colored terminal output.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

The MIT License (MIT) under Computer-Aided Programming Group at Purdue University, see `LICENCE`

