from random import randint

import streamlit as st
from i18n import gettext as _
from i18n import ngettext

st.write(_("Some text"))

squirrels = randint(1, 100)

st.write(
    ngettext(
        "There's %(num)d squirrel:",
        "There're %(num)d sqirrels:",
        squirrels,
    )
    % {"num": squirrels},
)

st.write("🐿️" * squirrels)
