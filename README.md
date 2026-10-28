# streamlit-gettext

[![Tests](https://github.com/insolor/streamlit-gettext/actions/workflows/test.yml/badge.svg)](https://github.com/insolor/streamlit-gettext/actions/workflows/test.yml)
[![Documentation](https://github.com/insolor/streamlit-gettext/actions/workflows/docs.yml/badge.svg)](https://insolor.github.io/streamlit-gettext/)  
[![PyPI](https://img.shields.io/pypi/v/streamlit-gettext)](https://pypi.org/project/streamlit-gettext/)
![Supported Python versions](https://img.shields.io/pypi/pyversions/streamlit-gettext)

> 🚧 WORK IN PROGRESS 🚧

A Streamlit extension for easy localization of your apps. Gets preferred languages from the browser, shows the the translated app to a user (it can be different translations for different users connected to the same app).

When a Streamlit app is deployed, reading the browser language only once at startup can cause every user to see the language of the first user who opened the app. `streamlit-gettext` avoids this by checking the current user's browser language each time it translates a message, so users sharing the same app can see it in different languages.

See a working app using `streamlit-gettext`: <https://github.com/dfint/package-build>

TODO:

- [x] [example application](https://github.com/insolor/streamlit-gettext/blob/main/example)  
    [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://st-gettext-example.streamlit.app)
- [x] tests
- [x] documentation
- [x] support of manual switching with default language selected from the browser preferred languages
- [ ] examples of translations with context
- [ ] ...

Feedback and suggestions are highly appreciated.
