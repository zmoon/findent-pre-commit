# findent-pre-commit

Use [findent](https://www.ratrabbit.nl/ratrabbit/findent/)
as a [pre-commit](https://pre-commit.com/) hook.


## Requirements

[pre-commit](https://pre-commit.com/#install), and:

* The `wfindent-conda` and `findent-conda` hooks require `conda` available on `PATH`
  (or `mamba`, with `PRE_COMMIT_USE_MAMBA=1`).
* The `wfindent-system` hook requires `wfindent` available on `PATH`.
* The `findent-system` hook requires `findent` available on `PATH`.


## Usage

Add one of the hooks defined in [`.pre-commit-hooks.yaml`](./.pre-commit-hooks.yaml)
to your `.pre-commit-config.yaml` file.

For example:
```yaml
repos:
  - repo: https://github.com/zmoon/findent-pre-commit
    rev: main
    hooks:
      - id: wfindent-system
```

To control which files get formatted, set
```yaml
        files: <regex>
```
to match them.
The current setting (`\.[fF](90|95|03|08)$`) matches free-form sources files
[according to GCC](https://gcc.gnu.org/onlinedocs/gfortran/GNU-Fortran-and-GCC.html).

To pass args to `findent`, use, for example:
```yaml
        args: [--indent=4, -r0]
```


## Wrapper

To install the Python wrapper `findent-wrapper` with [`pipx`](https://pypa.github.io/pipx/):

```
pipx install https://github.com/zmoon/findent-pre-commit/archive/main.zip
```

Note that the `wfindent` tool distributed with findent and referenced above provides in-place editing
using shell scripting.
`findent-wrapper` adds a `--diff` option (and maybe more options in the future...).


## Another way

As an alternative to the `wfindent-system` hook defined in this repo, it is possible
to use a [local hook](https://pre-commit.com/#repository-local-hooks) setup.

```yaml
# .pre-commit-config.yaml

- repo: local
  hooks:
    - id: wfindent
      name: Format Fortran code using findent
      entry: wfindent
      description: Uses system copy of wfindent available on PATH.
      language: system
      pass_filenames: true
      files: \.[fF](90|95|03|08)$
      types: [text]
      require_serial: true
```

Note that `findent` cannot be used in this way, since it only reads from STDIN.
