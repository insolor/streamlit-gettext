from __future__ import annotations

import gettext as _gettext_module
import re
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

    def __init__(self, locale_path: str | Path, domain: str = "messages") -> None:
        self.locale_path = Path(locale_path)
        self.domain = domain
        self._session_state_key = f"streamlit_gettext.preferred_languages:{(str(self.locale_path.resolve()), domain)!r}"

    def set_preferred_languages(self, languages: Iterable[str] | None) -> None:
        """
        Set preferred languages for this session. None or an empty iterable restores browser detection.
        """
        preferred_languages = list(languages) if languages is not None else []
        if preferred_languages:
            st.session_state[self._session_state_key] = preferred_languages
        else:
            st.session_state.pop(self._session_state_key, None)

    def get_preferred_languages(self) -> list[str]:
        """
        Get preferred languages from the browser if preferred languages are not set explicitly
        """
        preferred_languages = st.session_state.get(self._session_state_key)
        if preferred_languages:
            return list(preferred_languages)

        return self.get_preferred_languages_from_browser()

    def get_preferred_languages_from_browser(self) -> list[str]:
        """
        Get preferred languages from the browser
        """
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
        try:
            locale_directories = list(self.locale_path.iterdir())
        except FileNotFoundError:
            locale_directories = []

        language_codes = {
            path.name
            for path in locale_directories
            if path.is_dir() and (path / "LC_MESSAGES" / f"{self.domain}.mo").is_file()
        }
        language_codes.add("en")

        preferred_languages = [
            language.replace("-", "_").casefold() for language in self.get_preferred_languages_from_browser()
        ]

        def sort_key(language: str) -> tuple[int, int, str]:
            """Prefer exact locale matches, then compatible language fallbacks."""
            normalized = language.replace("-", "_").casefold()
            for index, preferred in enumerate(preferred_languages):
                if normalized == preferred:
                    return index, 0, language.casefold()
                if normalized == preferred.split("_")[0] or preferred == normalized.split("_")[0]:
                    return index, 1, language.casefold()
            return len(preferred_languages), 0, language.casefold()

        return sorted(language_codes, key=sort_key)
