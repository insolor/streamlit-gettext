# streamlit-gettext

[![Tests](https://github.com/insolor/streamlit-gettext/actions/workflows/test.yml/badge.svg)](https://github.com/insolor/streamlit-gettext/actions/workflows/test.yml)
[![Documentation](https://github.com/insolor/streamlit-gettext/actions/workflows/docs.yml/badge.svg)](https://insolor.github.io/streamlit-gettext/)  
[![PyPI](https://img.shields.io/pypi/v/streamlit-gettext)](https://pypi.org/project/streamlit-gettext/)
![Supported Python versions](https://img.shields.io/pypi/pyversions/streamlit-gettext)

> 🚧 WORK IN PROGRESS 🚧

A Streamlit extension that makes it easy to localize your apps. It detects users' preferred languages from their browsers and displays the app in the appropriate language. It avoids a common issue when using gettext in Streamlit: if the browser language is detected only once at startup, all users may see the app in the same language.

When browser detection is active, `streamlit-gettext` checks each user's browser language whenever it translates a message. This lets users sharing the same deployed app see different languages. Calling `set_preferred_languages()` overrides browser detection for that session; passing `None` or an empty iterable restores it.

See a working app that uses `streamlit-gettext`: <https://github.com/dfint/package-build>

Get started with the [complete setup guide](https://insolor.github.io/streamlit-gettext/quick_start/).

TODO:

- [x] [example application](https://github.com/insolor/streamlit-gettext/blob/main/example)  
    [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://st-gettext-example.streamlit.app)
- [x] tests
- [x] documentation
- [x] support for manually switching languages, with the browser's preferred language selected by default
- [x] examples of translations with context
- [ ] ...

Feedback and suggestions are welcome.
