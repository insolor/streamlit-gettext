# Translation workflow

The example project uses GNU gettext catalog files:

- `locale/messages.pot` is the template extracted from the source code.
- `locale/<language>/LC_MESSAGES/messages.po` contains translations for a language.
- `messages.mo` is the compiled catalog used by the app.

The gettext format is supported by many online translation platforms, including [Crowdin](https://crowdin.com/) and [Transifex](https://www.transifex.com/). You can also edit `.po` files with dedicated software such as [Poedit](https://poedit.net/).

For a more detailed guide to translating apps with gettext, see [Lokalise's tutorial](https://lokalise.com/blog/translating-apps-with-gettext-comprehensive-tutorial/).

The example defines [Poe the Poet](https://poethepoet.natn.io/) tasks for the repetitive steps. Run them from the `example/` directory. These tasks are especially useful when maintaining several languages: they update or compile all existing language catalogs in one go, instead of requiring you to repeat commands for each language.

Before running the tasks, install [GNU gettext](https://www.gnu.org/software/gettext/) and [Poe the Poet](https://poethepoet.natn.io/). If Poe is not installed yet, install it with:

```console
uv tool install poethepoet
```

These are the task definitions used by `example/pyproject.toml`:

```toml
[tool.poe.tasks]
run = "streamlit run app.py"
xgettext.shell = "xgettext -d messages -o ./locale/messages.pot *.py --from-code=UTF-8 --no-location"
msgfmt = "find ./locale -name \\*.po -execdir msgfmt messages.po -o messages.mo \\;"
msgmerge.shell = "find locale -name '*.po' -exec msgmerge -U {} locale/messages.pot \\; && find locale -name '*.po~' -delete"
```

`xgettext` creates one shared template from the Python files. `msgmerge` updates every existing `.po` catalog from that template and removes backup files; `msgfmt` compiles every `.po` catalog into a `.mo` file. These commands are included with GNU gettext, while Poe is only a task runner.

## 1. Mark text for translation

Wrap user-facing strings in `gettext` (usually imported as `_`) or use `ngettext` for singular and plural forms. For example:

```python
st.write(_("Squirrel application"))
ngettext("One squirrel", "%(num)d squirrels", count)
```

## 2. Extract messages

After adding or changing translatable strings, generate the message template:

```console
poe xgettext
```

This runs `xgettext` over the Python files in `example/` and updates `locale/messages.pot`.

## 3. Update and translate catalogs

Merge the latest template into every existing `.po` catalog:

```console
poe msgmerge
```

Open each `locale/<language>/LC_MESSAGES/messages.po` file and translate the entries marked `msgstr`. Keep placeholders such as `%(num)d` unchanged. For plural messages, translate each `msgstr[n]` form required by that language.

When `msgmerge` updates a catalog, it may mark an entry as `fuzzy` if the source text changed but resembles an older entry. The existing translation is carried over as a suggestion, but may no longer be accurate. Review it and remove the `fuzzy` flag; `msgfmt` skips fuzzy entries, so they will not be available in the app.

The task updates existing catalogs; adding a new language requires creating its `.po` catalog first.

## 4. Compile and check

Compile the translated catalogs into `.mo` files:

```console
poe msgfmt
```

Then run the example app to check the translations:

```console
poe run
```

Re-run `poe xgettext` and `poe msgmerge` whenever the source strings change, then translate new or changed entries and compile the catalogs again.
