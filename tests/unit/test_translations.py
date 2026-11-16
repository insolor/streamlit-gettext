from pathlib import Path

import pytest
import streamlit as st

from streamlit_gettext import GettextWrapper

locale_path = Path(__file__).resolve().parent.parent / "fixtures" / "locale"


@pytest.fixture
def wrapper(monkeypatch: pytest.MonkeyPatch) -> GettextWrapper:
    monkeypatch.setattr(st, "session_state", {})
    result = GettextWrapper(locale_path, domain="testing")
    monkeypatch.setattr(result, "get_preferred_languages_from_browser", lambda: ["ru"])
    return result


def test_pgettext_distinguishes_contexts(wrapper: GettextWrapper):
    assert wrapper.gettext("Open") == "Открыть без контекста"
    assert wrapper.pgettext("action", "Open") == "Открыть"
    assert wrapper.pgettext("state", "Open") == "Открыто"
    assert wrapper.pgettext("unknown", "Open") == "Open"


@pytest.mark.parametrize(
    ("count", "form"),
    [(0, "файлов"), (1, "файл"), (2, "файла"), (5, "файлов"), (11, "файлов"), (21, "файл")],
)
def test_npgettext_distinguishes_contexts_and_plural_forms(wrapper: GettextWrapper, count: int, form: str):
    singular, plural = "%(num)d file", "%(num)d files"
    assert wrapper.ngettext(singular, plural, count) % {"num": count} == f"{count} {form} без контекста"
    assert wrapper.npgettext("download", singular, plural, count) % {"num": count} == f"Скачать {count} {form}"
    assert wrapper.npgettext("delete", singular, plural, count) % {"num": count} == f"Удалить {count} {form}"
    expected = singular if count == 1 else plural
    assert wrapper.npgettext("unknown", singular, plural, count) % {"num": count} == expected % {"num": count}


@pytest.mark.parametrize("count", [0, 1, 2])
def test_missing_messages_fall_back_to_source(wrapper: GettextWrapper, count: int):
    assert wrapper.gettext("Unknown") == "Unknown"
    assert wrapper.pgettext("action", "Unknown") == "Unknown"
    expected = "item" if count == 1 else "items"
    assert wrapper.ngettext("item", "items", count) == expected
    assert wrapper.npgettext("action", "item", "items", count) == expected


@pytest.mark.parametrize("catalog", ["missing-directory", "empty-directory", "missing-language", "missing-domain"])
def test_missing_catalog_falls_back_to_source(
    tmp_path: Path,
    wrapper: GettextWrapper,
    catalog: str,
):
    if catalog == "missing-directory":
        wrapper.locale_path = tmp_path / "missing"
    elif catalog == "empty-directory":
        wrapper.locale_path = tmp_path
    elif catalog == "missing-language":
        wrapper.set_preferred_languages(["xx"])
    else:
        wrapper.domain = "missing"

    assert wrapper.gettext("Open") == "Open"
    assert wrapper.pgettext("action", "Open") == "Open"
    for count, expected in ((0, "files"), (1, "file"), (2, "files")):
        assert wrapper.ngettext("file", "files", count) == expected
        assert wrapper.npgettext("action", "file", "files", count) == expected


@pytest.mark.parametrize("count", [1, 2])
def test_fallback_chain_uses_next_language_for_missing_entries(wrapper: GettextWrapper, count: int):
    wrapper.set_preferred_languages(["xx", "ru", "fr"])

    assert wrapper.gettext("Open") == "Открыть без контекста"
    assert wrapper.pgettext("action", "Open") == "Открыть"
    assert wrapper.gettext("Save") == "Enregistrer"
    assert wrapper.pgettext("action", "Save") == "Sauvegarder"
    singular, plural = "%(num)d backup", "%(num)d backups"
    expected = "sauvegarde" if count == 1 else "sauvegardes"
    assert wrapper.ngettext(singular, plural, count) % {"num": count} == f"{count} {expected}"
    assert wrapper.npgettext("action", singular, plural, count) % {"num": count} == f"Créer {count} {expected}"


def test_context_translations_follow_session_language(wrapper: GettextWrapper):
    wrapper.set_preferred_languages(["fr"])
    assert wrapper.pgettext("action", "Save") == "Sauvegarder"
    wrapper.set_preferred_languages(["ru"])
    assert wrapper.pgettext("action", "Save") == "Save"
    assert wrapper.npgettext("delete", "%(num)d file", "%(num)d files", 2) % {"num": 2} == "Удалить 2 файла"


def test_regional_language_falls_back_to_base_catalog(wrapper: GettextWrapper):
    wrapper.set_preferred_languages(["ru_RU"])

    assert wrapper.gettext("Open") == "Открыть без контекста"
    assert wrapper.pgettext("action", "Open") == "Открыть"
    assert wrapper.npgettext("delete", "%(num)d file", "%(num)d files", 2) % {"num": 2} == "Удалить 2 файла"
