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

    def _get_session_state_key(self) -> str:
        return f"streamlit_gettext.preferred_languages:{(str(self.locale_path.resolve()), self.domain)!r}"

    def set_preferred_languages(self, languages: Iterable[str] | None) -> None:
        """
        Set preferred languages for this session. None or an empty iterable restores browser detection.
        """
        preferred_languages = list(languages) if languages is not None else []
        session_state_key = self._get_session_state_key()
        if preferred_languages:
            st.session_state[session_state_key] = preferred_languages
        else:
            st.session_state.pop(session_state_key, None)

    def get_preferred_languages(self) -> list[str]:
        """
        Get preferred languages from the browser if preferred languages are not set explicitly
        """
        preferred_languages = st.session_state.get(self._get_session_state_key())
        if preferred_languages:
            return list(preferred_languages)

        return self.get_preferred_languages_from_browser()

    @staticmethod
    def _normalize_language(language: str) -> str:
        """Normalize a language tag to gettext locale form."""
        return language.replace("-", "_").casefold()

    def get_preferred_languages_from_browser(self) -> list[str]:
        """
        Get concrete browser languages by descending quality, preserving order for ties.
        """
        accept_language = st.context.headers.get("Accept-Language") or ""
        weighted_languages: list[tuple[str, float]] = []
        for entry in accept_language.split(","):
            parsed = self._parse_accept_language_entry(entry)
            if parsed is not None:
                weighted_languages.append(parsed)

        weighted_languages.sort(key=lambda item: item[1], reverse=True)
        languages: list[str] = []
        seen: set[str] = set()
        for language, _weight in weighted_languages:
            normalized = self._normalize_language(language)
            if normalized not in seen:
                seen.add(normalized)
                languages.append(language.replace("-", "_"))
        return languages

    @staticmethod
    def _parse_accept_language_entry(entry: str) -> tuple[str, float] | None:
        """Return a concrete language and weight, or None for unusable entries."""
        match = re.fullmatch(
            r"[ \t]*([a-zA-Z]{1,8}(?:-[a-zA-Z0-9]{1,8})*|\*)[ \t]*"
            r"(?:;[ \t]*[qQ]=(0(?:\.[0-9]{0,3})?|1(?:\.0{0,3})?)[ \t]*)?",
            entry,
        )
        if match is None:
            return None
        language, quality = match.groups()
        weight = float(quality) if quality is not None else 1.0
        # A wildcard does not identify a concrete gettext catalog.
        if language == "*" or weight == 0:
            return None
        return language, weight

    def translation(self, languages: Iterable[str] | None = None) -> _gettext_module.NullTranslations:
        if languages is not None:
            languages = [language.replace("-", "_") for language in languages]
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
            self._normalize_language(language) for language in self.get_preferred_languages_from_browser()
        ]

        def sort_key(language: str) -> tuple[int, int, str]:
            """Prefer exact locale matches, then compatible language fallbacks."""
            normalized = self._normalize_language(language)
            for index, preferred in enumerate(preferred_languages):
                if normalized == preferred:
                    return index, 0, language.casefold()
                if normalized == preferred.split("_")[0] or preferred == normalized.split("_")[0]:
                    return index, 1, language.casefold()
            return len(preferred_languages), 0, language.casefold()

        return sorted(language_codes, key=sort_key)
