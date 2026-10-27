
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
        "There're %(num)d sqirrels:",
        squirrels,
        languages=[language],
    )
    % {"num": squirrels},
)

st.write("🐿️" * squirrels)
