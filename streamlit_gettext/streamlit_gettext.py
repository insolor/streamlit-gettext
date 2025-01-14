from __future__ import annotations

import gettext as _gettext_module
import re
from pathlib import Path
from typing import TYPE_CHECKING

import streamlit as st

if TYPE_CHECKING:
    from collections.abc import Iterable


def get_preferred_languages() -> list[str]:
    """
    Get preferred languages from the browser
    """
    accept_language = st.context.headers.get("Accept-Language") or ""
    return re.findall(r"([a-zA-Z-]{2,})", accept_language) or []


class GettextWrapper:
    """
    A wrapper for the gettext module
    """
    locale_path: Path
    domain: str

    def __init__(self, locale_path: str | Path, domain: str = "messages") -> None:
        self.locale_path = Path(locale_path)
        self.domain = domain

    def translation(self, languages: Iterable[str] | None = None) -> _gettext_module.NullTranslations:
        return _gettext_module.translation(
            domain=self.domain,
            localedir=self.locale_path,
            languages=languages,
            fallback=True,
        )

    def gettext(self, message: str) -> str:
        """
        Get the translation of a message
        """
        translation = self.translation(get_preferred_languages())
        return translation.gettext(message)

    def ngettext(self, singular: str, plural: str, n: int) -> str:
        """
        Get the plural form of a message
        """
        translation = self.translation(get_preferred_languages())
        return translation.ngettext(singular, plural, n)

    def pgettext(self, context: str, message: str) -> str:
        """
        Get the translation of a message with a context
        """
        translation = self.translation(get_preferred_languages())
        return translation.pgettext(context, message)

    def npgettext(self, context: str, singular: str, plural: str, n: int) -> str:
        """
        Get the plural form of a message with a context
        """
        translation = self.translation(get_preferred_languages())
        return translation.npgettext(context, singular, plural, n)
