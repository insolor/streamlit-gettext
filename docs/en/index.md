
# streamlit-gettext documentation

`streamlit-gettext` is a Streamlit extension for localizing apps. It helps display translated text to users based on their browser's preferred language.

If an app reads the browser language only once at startup, that value can be reused for every user: everyone may see the language of the first person who opened the app. `streamlit-gettext` avoids this by checking the current user's browser language whenever it translates a message. This lets users of the same deployed app see different languages.

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

st.write(_("Squirrel application"))

squirrels = st.slider(_("How many squirrels to show?"), 1, 100, 1)

st.write(
    ngettext(
        "There's %(num)d squirrel:",
        "There're %(num)d squirrels:",
        squirrels,
    )
    % {"num": squirrels},
)

st.write("🐿️" * squirrels)
```

In this example, `_()` marks text for translation. `ngettext()` handles singular and plural message forms, and the slider changes the quantity displayed by the app.

This is a usage example, not a complete setup guide. The translation files and project configuration are also needed to run a localized app.

## Switch languages manually

The example below adds a language selector. The selected language is passed to `set_preferred_languages()` so the app uses that translation:

```python
import streamlit as st
from i18n import get_available_languages, ngettext, set_preferred_languages
from i18n import gettext as _

language = st.segmented_control(
    "Language",
    options=get_available_languages(),
    label_visibility="collapsed",
    required=True,
)
if language:
    set_preferred_languages([language])

st.write(_("Squirrel application"))

squirrels = st.slider(_("How many squirrels to show?"), 1, 100, 1)

st.write(
    ngettext(
        "There's %(num)d squirrel:",
        "There're %(num)d squirrels:",
        squirrels,
    )
    % {"num": squirrels},
)

st.write("🐿️" * squirrels)
```

## Try the example

You can try the [hosted Streamlit example](https://st-gettext-example.streamlit.app/) to see the demonstration in action.

For more details, see the [example source code](https://github.com/insolor/streamlit-gettext/tree/main/example).

## API reference

See the [API reference](api.md) for details about the project's documented interfaces.
