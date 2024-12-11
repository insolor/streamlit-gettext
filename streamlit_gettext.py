import gettext as _gettext_module
import re
from functools import lru_cache
from pathlib import Path

import streamlit as st


def get_preferred_languages() -> list[str]:
    accept_language = st.context.headers.get("Accept-Language") or ""
    return re.findall(r"([a-zA-Z-]{2,})", accept_language) or []


_locale_path = None


def set_locale_path(path: str) -> None:
    """
    Set path to the locale directory.
    """
    global _locale_path  # noqa: PLW0603
    _locale_path = Path(path)


@lru_cache(maxsize=128, typed=False)
def _get_translation(languages: tuple[str]) -> _gettext_module.NullTranslations:
    return _gettext_module.translation(
        "messages",
        localedir=_locale_path,
        languages=languages,
        fallback=True,
    )


class GettextWrapper:
    """
    A wrapper for the gettext module
    """

    @staticmethod
    def _get_translation() -> _gettext_module.NullTranslations:
        return _get_translation(tuple(get_preferred_languages()))

    def gettext(self, message: str) -> str:
        translation = self._get_translation()
        return translation.gettext(message)

    def ngettext(self, singular: str, plural: str, n: int) -> str:
        translation = self._get_translation()
        return translation.ngettext(singular, plural, n)


gettext_wrapper = GettextWrapper()
gettext = gettext_wrapper.gettext
ngettext = gettext_wrapper.ngettext
