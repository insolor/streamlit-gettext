# Quick start

Build a small app with English source text, German translations, a language selector, and context-aware plural messages.

## 1. Install the tools

Use Python 3.11 or newer. In a terminal, create a project and install the Python packages:

```sh
mkdir localized-app
cd localized-app
python -m venv .venv
source .venv/bin/activate
python -m pip install streamlit streamlit-gettext poethepoet
```

These shell commands use Bash on Linux or macOS. On Windows, run the entire guide inside WSL, including virtual environment setup, so `poe` and the shell tasks use the same Linux environment.

Install GNU gettext separately; it provides `xgettext` and `msgfmt`. For example, on Ubuntu or Debian:

```sh
sudo apt-get install gettext
```

On macOS with Homebrew:

```sh
brew install gettext
```

For other systems, see the [GNU gettext installation instructions](https://www.gnu.org/software/gettext/). Run the remaining commands from `localized-app/` with the virtual environment activated.

## 2. Create the translation module

Save the following as `i18n.py` next to `app.py`. This module belongs to your app; it is not installed by the library.

```python
from pathlib import Path

from streamlit_gettext import GettextWrapper

wrapper = GettextWrapper(Path(__file__).parent / "locale")

gettext = wrapper.gettext
ngettext = wrapper.ngettext
pgettext = wrapper.pgettext
npgettext = wrapper.npgettext
get_available_languages = wrapper.get_available_languages
set_preferred_languages = wrapper.set_preferred_languages
```

The catalog path is relative to `i18n.py`, so it does not depend on the working directory. The default catalog domain is `messages`, corresponding to `messages.po` and `messages.mo`.

## 3. Create the app

Save this as `app.py`:

```python
import streamlit as st
from i18n import (
    get_available_languages,
    ngettext,
    npgettext,
    pgettext,
    set_preferred_languages,
)
from i18n import gettext as _

language = st.selectbox(
    "Language",
    options=["auto", *get_available_languages()],
    format_func=lambda code: "Browser language" if code == "auto" else code,
)
set_preferred_languages(None if language == "auto" else [language])

st.title(_("File manager"))
count = st.slider(_("Number of files"), 1, 30, 1)
st.write(ngettext("%(num)d file", "%(num)d files", count) % {"num": count})

st.button(pgettext("action", "Open"))
st.write(pgettext("state", "Open"))
st.write(
    npgettext(
        "download",
        "Download %(num)d file",
        "Download %(num)d files",
        count,
    )
    % {"num": count}
)
```

`gettext` translates a single message. `ngettext` chooses a plural form. `pgettext` distinguishes the action “Open” from the state “Open” through its context argument. `npgettext` combines context with plural selection.

Select `auto` to follow the browser language, or a language code to override it. Passing `None` restores browser detection. Manual preferences are stored separately for each Streamlit session. The source text in this example is English, so `en` uses the original messages when no English catalog is present.

## 4. Extract and translate messages

Create `pyproject.toml` in the project root with these tasks (or add the section to an existing file):

```toml
[tool.poe.tasks]
extract_pot = """
xgettext
    --keyword=pgettext:1c,2
    --keyword=npgettext:1c,2,3
    --no-location
    --output=locale/messages.pot
    app.py
"""

[tool.poe.tasks.update_po]
shell = """
find locale -type f -name '*.po' -exec sh -c '
    for po do
        msgmerge --update --backup=none "$po" locale/messages.pot || exit
    done
' sh {} +
"""

[tool.poe.tasks.compile_mo]
shell = """
find locale -type f -name '*.po' -exec sh -c '
    for po do
        msgfmt --check-format "$po" -o "${po%.po}.mo" || exit
    done
' sh {} +
"""

[tool.poe.tasks.init_po]
shell = """
mkdir -p "locale/${language}/LC_MESSAGES" &&
msginit --input=locale/messages.pot --output-file="locale/${language}/LC_MESSAGES/messages.po" --locale="${language}" --no-translator
"""
args = [{ name = "language", positional = true, required = true }]
```

[Poe the Poet](https://poethepoet.natn.io/) runs the commands stored in this file. You write the options once; subsequent runs use short task names. GNU gettext still needs to be installed.

`xgettext` detects Python from the `.py` extension, handles Python source encoding, and recognizes `_`, `gettext`, and `ngettext` by default. Context-aware calls require the additional `--keyword` options.

The extraction options:

| Option | Purpose |
|---|---|
| `--keyword=pgettext:1c,2` | Argument 1 is the context (`c`); argument 2 is the message. |
| `--keyword=npgettext:1c,2,3` | Argument 1 is the context; arguments 2 and 3 are the singular and plural messages. |
| `--no-location` | Omit source file locations from the catalog to reduce changes when code moves. |
| `--output=locale/messages.pot` | Write the shared message template to this file. |
| `app.py` | The source file to scan; add other source files here when the app grows. |

`init_po` accepts a required positional language argument. It creates `locale/<language>/LC_MESSAGES` and passes the language to `msginit`. Run `poe init_po de` for German or `poe init_po ja` for Japanese; you do not need to edit the tasks when adding languages.

`update_po` and `compile_mo` use `find` to process every `.po` file under `locale/`. The first updates all catalogs from the shared template without backup files; the second checks format placeholders and creates a `.mo` next to each `.po`. `${po%.po}` removes the `.po` suffix before adding `.mo`. `for po do` processes the paths passed by `find`, and `|| exit` propagates any gettext failure. With `-exec … +`, `find` also returns an error if a batch fails, so Poe and CI can detect the failure. Paths are quoted to support directory names containing spaces.

These shell tasks require a POSIX shell and `find`, available on Linux and macOS. On Windows, run the guide inside WSL.

Create the common catalog directory and extract the messages:

```sh
mkdir -p locale
poe extract_pot
```

Create the `.po` file from the template:

```sh
poe init_po de
```

This task runs `msginit`: `--input` selects the template, `--output-file` selects the new translation catalog, `--locale=de` sets the language, and `--no-translator` disables interactive prompts for translator details. The command creates entries with empty translations and initializes the header, including `Language` and `Plural-Forms`.

Run `poe init_po <language>` once for each new language. Subsequent `poe update_po` and `poe compile_mo` runs process all added languages together.

You can fill in translations with a dedicated editor such as [Poedit](https://poedit.com/), which provides an interface for editing messages and plural forms. Many online translation services, including [Crowdin](https://support.crowdin.com/developer/configuration-file/#gettext-project) and [Transifex](https://help.transifex.com/en/articles/6220794-gettext-po), support `.po` natively, without conversion to another format.

You can configure a repository integration with these services to send updated source messages and receive completed translations, for example through [Crowdin's GitHub integration](https://support.crowdin.com/github-integration/) or [Transifex's GitHub integration](https://help.transifex.com/en/articles/6265125-github-installation-and-configuration). After receiving updated `.po` files, run `poe compile_mo` so the app uses the new translations.

Open `locale/de/LC_MESSAGES/messages.po` and fill in `msgstr` and `msgstr[n]`. In the metadata header (`msgid ""`), set UTF-8 as the charset and save the file in that encoding:

```po
"Content-Type: text/plain; charset=UTF-8\n"
```

Keep the other generated header fields, including `Plural-Forms`. The translated entries should look like this:

```po
msgid "File manager"
msgstr "Dateimanager"

msgid "Number of files"
msgstr "Anzahl der Dateien"

#, python-format
msgid "%(num)d file"
msgid_plural "%(num)d files"
msgstr[0] "%(num)d Datei"
msgstr[1] "%(num)d Dateien"

msgctxt "action"
msgid "Open"
msgstr "Öffnen"

msgctxt "state"
msgid "Open"
msgstr "Geöffnet"

#, python-format
msgctxt "download"
msgid "Download %(num)d file"
msgid_plural "Download %(num)d files"
msgstr[0] "%(num)d Datei herunterladen"
msgstr[1] "%(num)d Dateien herunterladen"
```

`.pot` is the extracted template, `.po` is the editable translation, and `.mo` is the compiled catalog loaded by the app. `msgctxt` must match the context in the Python call. Keep `%(num)d` unchanged and translate every plural form required by the language. German has two forms; other languages can require a different number and a different `Plural-Forms` expression.

## 5. Compile and run

```sh
poe compile_mo
```

Your project now has this structure:

```text
localized-app/
├── app.py
├── i18n.py
├── pyproject.toml
└── locale/
    ├── messages.pot
    └── de/
        └── LC_MESSAGES/
            ├── messages.po
            └── messages.mo
```

Start the app:

```sh
python -m streamlit run app.py
```

Choose `de`: the title should become “Dateimanager”. Set the slider to 1, 2, and 5 to see “1 Datei”, “2 Dateien”, and “5 Dateien”. The button reads “Öffnen”, while the state reads “Geöffnet”. Choose `en` to return to the English source text, or `auto` to use the browser language.

If a message stays in English, check the selected language, catalog location, domain, and whether the `.mo` was recompiled after editing the `.po`. Entries marked `fuzzy` are skipped by `msgfmt`; review the translation and remove that flag before compiling. Restart Streamlit after recompiling catalogs to clear cached translations.

## Keep translations up to date

After changing source messages, extract them again and update the translation catalog:

```sh
poe extract_pot
poe update_po
```

Translate new or changed entries, review any `fuzzy` entries, run `poe compile_mo`, and restart the app. See the [translation workflow](translation_workflow.md) for the repository example's tasks, or the [API reference](api.md) for the library interfaces.
