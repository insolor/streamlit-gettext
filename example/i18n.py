from pathlib import Path

from streamlit_gettext.streamlit_gettext import GettextWrapper

current_path = Path(__file__).parent
_gettext_wrapper = GettextWrapper(locale_path=current_path / "locale")

gettext = _gettext_wrapper.gettext
ngettext = _gettext_wrapper.ngettext
set_preferred_languages = _gettext_wrapper.set_preferred_languages
get_preferred_languages = _gettext_wrapper.get_preferred_languages
get_available_languages = _gettext_wrapper.get_available_languages
