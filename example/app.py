import streamlit as st
from i18n import set_preferred_languages

autodetect_page = st.Page("autodetect_example.py", title="Autodetect language", default=True)
manual_switcher_page = st.Page("example_with_switcher.py", title="Manual language switcher")

selected_page = st.navigation([autodetect_page, manual_switcher_page], position="sidebar")

if selected_page == autodetect_page:
    set_preferred_languages(None)

selected_page.run()
