# Best Practices for Readable and Maintainable Code

Use this page as a project checklist. You do not need to satisfy every item perfectly, but your code should reflect these principles where applicable.

## General

### Keep code easy to read

- Use clear names (`input_file`, `bucket_name`, `results_df`) instead of short names (`x`, `tmp`, `data1`) unless in short loops.
- Keep functions and scripts focused on one task.
- Prefer simple control flow over clever one-liners.
- Avoid copy-paste blocks; create a reusable function instead.

### Comment with purpose

- Write comments that explain **why**, not obvious **what**.
- You shouldn't comment each line of code. Add short comments before non-obvious logic.
- Keep comments current; remove stale comments when code changes.

### Organize project files

- Keep source code, data, and outputs in separate folders.
- Do not commit large generated output files to GitHub unless required.
- Do not commit secrets (keys, passwords, `.env` files with credentials).
- Use .gitignore to exclude sensitive files from being tracked. This avoids accidental leakage into public repositories. 

### Make your project reproducible

- Include a clear `README.md` with:
  - project goal
  - setup instructions
  - how to run
  - expected outputs
- List all Python packages used in a `requirements.txt` file. This file should reside at the top level of your repository.
- Document assumptions (input paths, expected schema, required environment variables).

## Python

### Use functions

- Organize code into functions where each function has a single responsibility.
- Use meaningful function names.
- Add a docstring to each function (at least one sentence).
- Use:

```python
if __name__ == "__main__":
    main()
```

### Prefer a `main()` workflow

- Parse inputs once.
- For your app script(s), call helper functions from `main()`.

### Handle external calls with `try/except`

Wrap calls to external services (e.g. boto3.client(), database clients, requests to URLs, file I/O) with `try/except` blocks so failures are understandable.

- Catch specific exceptions when possible.
- Log useful context in the error message.
- Exit with non-zero status on unrecoverable errors.

### Use command-line arguments

Use command line arguments to allow users to pass configurables to the script. You can use `sys.argv` for this, or explore `argparse` ([docs](https://docs.python.org/3/library/argparse.html)).

### Use logging (not only `print`)

- Use `logging` for status, warnings, and errors.
- Include a command-line option to control log level (`INFO`, `DEBUG`, etc.) for larger scripts.
- Keep user-facing output concise; avoid noisy logs by default.

### Keep imports clean

- Remove unused imports.
- Group imports in this order: standard library, third-party, local modules.
- Avoid importing inside functions unless necessary.

## Bash

### Safer shell scripts

Start scripts with:

```bash
set -euo pipefail
```

- Quote variable expansions (`"$FILE"` not `$FILE`).
- Validate positional arguments before use.
- Print a usage message for incorrect invocation.
- Use exit codes (`exit 1`) on failure.

### Write portable commands

- Avoid hard-coding user-specific paths unless necessary.
- Add short comments for non-obvious commands.

### Validate inputs early

- Check that files/folders exist before processing.
- Validate expected columns/fields in datasets and databases before running heavy logic.
- Fail fast with clear messages when assumptions are violated.

### Be explicit with cloud resources

- Name resources consistently (`ds2002-<computing_id>-...` when required).
- Keep region settings explicit when relevant (`us-east-1` in this course context).
- Clean up cloud resources after testing to avoid charges.

## Testing and verification

### Test small, then full

- Run on a tiny sample first.
- Add at least one negative test (missing file, bad argument, permission issue).
- Verify output format and counts, not just "script runs."
