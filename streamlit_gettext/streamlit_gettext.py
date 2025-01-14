from __future__ import annotations

import gettext as _gettext_module
import re
from pathlib import Path
from typing import TYPE_CHECKING

import streamlit as st

if TYPE_CHECKING:
    from collections.abc import Iterable


def get_preferred_languages() -> list[str]:
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
        translation = self.translation(get_preferred_languages())
        return translation.gettext(message)

    def ngettext(self, singular: str, plural: str, n: int) -> str:
        translation = self.translation(get_preferred_languages())
        return translation.ngettext(singular, plural, n)
