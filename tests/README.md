# Project tests

This standalone uv project tests the local editable `streamlit-gettext` library:

- `unit/`: language discovery, session-scoped preferences, contextual
  translations, plural forms, and fallback using dedicated gettext catalogs.
- `integration/`: the example app's language switcher, plural output, navigation,
  and session isolation through Streamlit `AppTest`.
- `fixtures/`: translation catalogs used by the unit tests.

Run from this directory:

```sh
uv sync --locked
uv run --locked pytest -q
```

To run a single suite, use `uv run --locked pytest unit` or
`uv run --locked pytest integration`.

Integration tests run the source files in `../example/` directly. The example
project keeps only a smoke test that checks application startup:

```sh
cd ../example
uv run pytest -q
```

Compiled fixture catalogs are included, so GNU gettext is only required when
updating them. See [fixture instructions](fixtures/README.md).
