# streamlit-gettext

[![Tests](https://github.com/insolor/streamlit-gettext/actions/workflows/test.yml/badge.svg)](https://github.com/insolor/streamlit-gettext/actions/workflows/test.yml)
[![Documentation](https://github.com/insolor/streamlit-gettext/actions/workflows/docs.yml/badge.svg)](https://insolor.github.io/streamlit-gettext/)  
[![PyPI](https://img.shields.io/pypi/v/streamlit-gettext)](https://pypi.org/project/streamlit-gettext/)
![Supported Python versions](https://img.shields.io/pypi/pyversions/streamlit-gettext)

> 🚧 WORK IN PROGRESS 🚧

A Streamlit extension that makes it easy to localize your apps. It detects users' preferred languages from their browsers and displays the app in the appropriate language. It avoids a common issue when using gettext in Streamlit: if the browser language is detected only once at startup, all users may see the app in the same language.

When a Streamlit app is deployed, reading the browser language only once at startup can cause every user to see the language detected for the first person who opened the app. `streamlit-gettext` avoids this by checking each user's browser language whenever it translates a message, so users sharing the same app can see it in different languages.

See a working app that uses `streamlit-gettext`: <https://github.com/dfint/package-build>

TODO:

- [x] [example application](https://github.com/insolor/streamlit-gettext/blob/main/example)  
    [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://st-gettext-example.streamlit.app)
- [x] tests
- [x] documentation
- [x] support for manually switching languages, with the browser's preferred language selected by default
- [ ] examples of translations with context
- [ ] ...

Feedback and suggestions are welcome.
