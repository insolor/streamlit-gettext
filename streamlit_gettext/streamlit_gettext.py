from __future__ import annotations

import gettext as _gettext_module
import re
import sys
from pathlib import Path
from typing import TYPE_CHECKING

import streamlit as st

if TYPE_CHECKING:
    from collections.abc import Iterable


class GettextWrapper:
    """
    A wrapper for the gettext module
    """

    locale_path: Path
    domain: str

    preferred_languages: list[str] | None = None

    def __init__(self, locale_path: str | Path, domain: str = "messages") -> None:
        self.locale_path = Path(locale_path)
        self.domain = domain

    def set_preferred_languages(self, languages: Iterable[str] | None) -> None:
        """
        Manually set preferred languages. If not None then it overrides detected languages.
        """
        self.preferred_languages = list(languages) if languages else None

    def get_preferred_languages(self) -> list[str]:
        """
        Get preferred languages from the browser if preferred languages are not set explicitly
        """
        if self.preferred_languages is not None:
            return self.preferred_languages

        accept_language = st.context.headers.get("Accept-Language") or ""
        return re.findall(r"([a-zA-Z-]{2,})", accept_language) or []

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
        translation = self.translation(self.get_preferred_languages())
        return translation.gettext(message)

    def ngettext(self, singular: str, plural: str, n: int) -> str:
        """
        Get the plural form of a message
        """
        translation = self.translation(self.get_preferred_languages())
        return translation.ngettext(singular, plural, n)

    def pgettext(self, context: str, message: str) -> str:
        """
        Get the translation of a message with a context
        """
        translation = self.translation(self.get_preferred_languages())
        return translation.pgettext(context, message)

    def npgettext(self, context: str, singular: str, plural: str, n: int) -> str:
        """
        Get the plural form of a message with a context
        """
        translation = self.translation(self.get_preferred_languages())
        return translation.npgettext(context, singular, plural, n)

    def get_available_languages(self) -> list[str]:
        """
        Get languages available in the locale directory
        """
        language_codes = [
            path.name
            for path in self.locale_path.iterdir()
            if path.is_dir()
            and (path / "LC_MESSAGES" / "messages.mo").is_file()
        ]
        language_codes.insert(0, "en")

        preferred_languages = self.get_preferred_languages()
        index_map = {
            language: i for i, language in enumerate(preferred_languages)
        }
        def key_function(language: str) -> int:
            return index_map.get(language) or sys.maxsize

        language_codes.sort(
            key=key_function
        )

        return language_codes
