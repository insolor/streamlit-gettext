
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

st.write(_("Some text"))

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

## Try the example

You can try the [hosted Streamlit example](https://st-gettext-example.streamlit.app/) to see the demonstration in action.

For more details, see the [example source code](https://github.com/insolor/streamlit-gettext/tree/main/example).

## API reference

See the [API reference](api.md) for details about the project's documented interfaces.
