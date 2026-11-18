# streamlit-gettext

[![Tests](https://github.com/insolor/streamlit-gettext/actions/workflows/test.yml/badge.svg)](https://github.com/insolor/streamlit-gettext/actions/workflows/test.yml)
[![Documentation](https://github.com/insolor/streamlit-gettext/actions/workflows/docs.yml/badge.svg)](https://insolor.github.io/streamlit-gettext/)  
[![PyPI](https://img.shields.io/pypi/v/streamlit-gettext)](https://pypi.org/project/streamlit-gettext/)
![Supported Python versions](https://img.shields.io/pypi/pyversions/streamlit-gettext)

A Streamlit extension that lets users of the same app see its interface in different languages. It uses browser language preferences by default and supports a language override for each session.

## Minimal example

Install `streamlit-gettext` with Python 3.11 or newer.

```sh
python -m pip install streamlit-gettext
```

Add this to your Streamlit app:

```python
from pathlib import Path

import streamlit as st
from streamlit_gettext import GettextWrapper

translations = GettextWrapper(Path(__file__).parent / "locale")
_ = translations.gettext
st.title(_("File manager"))
```

Supply translations as compiled `.mo` catalogs, for example `locale/de/LC_MESSAGES/messages.mo` for German. This README uses German as an example. You can replace `de` with the language code for any language you provide translations for. The [complete setup guide](https://insolor.github.io/streamlit-gettext/quick_start/) walks through extracting messages, editing `.po` files, and compiling them into `.mo` catalogs.

## How language selection works

By default, the library selects catalogs using the browser's `Accept-Language` header. If no translation is found, it displays the original message.

To override the browser preference for the current session, pass the language code selected in your app's language switcher to `translations.set_preferred_languages([language])`. For example, if the user selects German, `language` is `"de"`. Passing `None` or an empty iterable restores automatic detection.

## What is gettext?

`streamlit-gettext` is built on [GNU gettext](https://www.gnu.org/software/gettext/), a localization system with tools for extracting translatable messages and compiling translation catalogs. It uses the `gettext` module from Python’s standard library to load the compiled catalogs and look up translations at runtime.

GNU gettext is a de facto standard for translating user-facing strings in many open-source projects, including GNU command-line tools and Linux desktop projects such as GNOME and KDE. Its `.po` catalogs are widely supported by desktop editors such as [Lokalize](https://apps.kde.org/lokalize/) and [Poedit](https://poedit.net/), and by web-based translation platforms such as [Weblate](https://docs.weblate.org/en/latest/formats/gettext.html), [Crowdin](https://store.crowdin.com/gnu-gettext), and [Transifex](https://help.transifex.com/en/articles/6220794-gettext-po).

The `.po` format is also used in commercial software. For example, [Epic Games recommends importing and exporting `.po` files](https://dev.epicgames.com/documentation/en-us/unreal-engine/localization-tools-in-unreal-engine) when translating Unreal Engine projects with external tools.

## Examples

- [Example source code](https://github.com/insolor/streamlit-gettext/tree/main/example)
- [Live example app](https://st-gettext-example.streamlit.app) (it may take a moment to start)
- [dfint/package-build](https://github.com/dfint/package-build), an app that uses `streamlit-gettext`

![streamlit-gettext demo](https://github.com/insolor/streamlit-gettext/blob/main/assets/screencast.gif)
