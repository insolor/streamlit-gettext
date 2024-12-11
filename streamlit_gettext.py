import gettext as gettext_module
import re
from functools import lru_cache
from pathlib import Path

import streamlit as st


def get_preferred_languages() -> list[str]:
    accept_language = st.context.headers.get("Accept-Language") or ""
    return re.findall(r"([a-zA-Z-]{2,})", accept_language) or []


@lru_cache(maxsize=128, typed=False)
def _get_lang(languages: tuple[str]) -> gettext_module.NullTranslations:
    locale_dir = Path(__file__).parent / "locale"

    return gettext_module.translation(
        "messages",
        localedir=locale_dir,
        languages=languages,
        fallback=True,
    )


class LanguageWrapper:
    @staticmethod
    def _get_lang() -> gettext_module.NullTranslations:
        return _get_lang(tuple(get_preferred_languages()))

    def gettext(self, message: str) -> str:
        lang = self._get_lang()
        return lang.gettext(message)

    def ngettext(self, singular: str, plural: str, n: int) -> str:
        lang = self._get_lang()
        return lang.ngettext(singular, plural, n)


lang = LanguageWrapper()
gettext = lang.gettext
ngettext = lang.ngettext
