from __future__ import annotations

import gettext as _gettext_module
import re
from pathlib import Path

import streamlit as st


def get_preferred_languages() -> list[str]:
    accept_language = st.context.headers.get("Accept-Language") or ""
    return re.findall(r"([a-zA-Z-]{2,})", accept_language) or []


class GettextWrapper:
    """
    A wrapper for the gettext module
    """

    locale_path: Path

    def __init__(self, locale_path: str | Path) -> None:
        self.locale_path = Path(locale_path)

    def _translation(self) -> _gettext_module.NullTranslations:
        return _gettext_module.translation(
            "messages",
            localedir=self.locale_path,
            languages=get_preferred_languages(),
            fallback=True,
        )

    def gettext(self, message: str) -> str:
        translation = self._translation()
        return translation.gettext(message)

    def ngettext(self, singular: str, plural: str, n: int) -> str:
        translation = self._translation()
        return translation.ngettext(singular, plural, n)
