
# streamlit-gettext documentation

`streamlit-gettext` is a Streamlit extension for localizing apps. It helps display translated text to users based on their browser's preferred language.

The project is a work in progress, so some features and instructions may change.

## What can it do?

- **Translate text:** Mark text for translation using `gettext`, commonly imported as `_`.
- **Handle singular and plural messages:** Use `ngettext` to select the appropriate message form for a quantity.
- **Support different language preferences:** The project aims to show users translations that match their browser language preferences.

## Basic usage

The following example shows how the extension's translation functions can be used in a Streamlit app:

```python
import streamlit as st
from i18n import gettext as _
from i18n import ngettext
from streamlit_gettext import get_preferred_languages

languages = ["en", "ru"]
default_language = next(
    (
        language
        for preferred in get_preferred_languages()
        for language in languages
        if preferred.split("-")[0].lower() == language
    ),
    languages[0],
)
language = st.selectbox(
    "Language", languages, index=languages.index(default_language)
)

st.write(_("Some text", languages=[language]))

squirrels = st.slider(
    _("How many squirrels to show?", languages=[language]), 1, 100, 1
)

st.write(
    ngettext(
        "There's %(num)d squirrel:",
        "There're %(num)d squirrels:",
        squirrels,
        languages=[language],
    )
    % {"num": squirrels},
)

st.write("🐿️" * squirrels)
```

In this example, the language selector defaults to the first supported language
matching the browser's preferences. Passing `languages=[language]` to `_()` and
`ngettext()` uses the selected language instead. Omitting `languages` continues
to use the browser's preferred languages. `_()` marks text for translation,
`ngettext()` handles singular and plural message forms, and the slider changes
the quantity displayed by the app.

This is a usage example, not a complete setup guide. The translation files and project configuration are also needed to run a localized app.

## Try the example

You can try the [hosted Streamlit example](https://st-gettext-example.streamlit.app/) to see the demonstration in action.

For more details, see the [example source code](https://github.com/insolor/streamlit-gettext/tree/main/example).

## API reference

See the [API reference](api.md) for details about the project's documented interfaces.
