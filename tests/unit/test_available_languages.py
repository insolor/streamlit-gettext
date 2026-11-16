from pathlib import Path

import pytest

from streamlit_gettext import GettextWrapper


@pytest.mark.parametrize(
    ("preferences", "expected"),
    [
        (["PT-br", "de-DE"], ["pt_BR", "pt", "de", "en", "fr", "pt_PT"]),
        (["pt-PT"], ["pt_PT", "pt", "de", "en", "fr", "pt_BR"]),
        (["pt"], ["pt", "pt_BR", "pt_PT", "de", "en", "fr"]),
        (["fr", "fr", "de"], ["fr", "de", "en", "pt", "pt_BR", "pt_PT"]),
        ([], ["de", "en", "fr", "pt", "pt_BR", "pt_PT"]),
    ],
)
def test_available_languages_locale_preferences(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    preferences: list[str],
    expected: list[str],
):
    for language in ("pt_BR", "pt_PT", "pt", "de", "en", "fr"):
        messages_path = tmp_path / language / "LC_MESSAGES"
        messages_path.mkdir(parents=True)
        (messages_path / "messages.mo").touch()

    wrapper = GettextWrapper(tmp_path)
    monkeypatch.setattr(wrapper, "get_preferred_languages_from_browser", lambda: preferences)

    assert wrapper.get_available_languages() == expected


def test_available_languages_use_configured_domain(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    for language, filename in (("ja", "custom.mo"), ("de", "messages.mo"), ("fr", "custom.po")):
        messages_path = tmp_path / language / "LC_MESSAGES"
        messages_path.mkdir(parents=True)
        (messages_path / filename).touch()
    (tmp_path / "not-a-directory").touch()

    wrapper = GettextWrapper(tmp_path, domain="custom")
    monkeypatch.setattr(wrapper, "get_preferred_languages_from_browser", lambda: ["ja"])

    assert wrapper.get_available_languages() == ["ja", "en"]


@pytest.mark.parametrize("missing", [True, False])
def test_available_languages_without_catalogs(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    *,
    missing: bool,
):
    wrapper = GettextWrapper(tmp_path / "missing" if missing else tmp_path)
    monkeypatch.setattr(wrapper, "get_preferred_languages_from_browser", lambda: ["ja"])

    assert wrapper.get_available_languages() == ["en"]


def test_available_languages_prioritize_browser_preferences_then_sort_alphabetically(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    languages = ("ru", "es", "de", "fr", "pl")
    for language in languages:
        messages_path = tmp_path / language / "LC_MESSAGES"
        messages_path.mkdir(parents=True)
        (messages_path / "messages.mo").touch()

    gettext_wrapper = GettextWrapper(tmp_path)
    monkeypatch.setattr(gettext_wrapper, "get_preferred_languages_from_browser", lambda: ["fr", "de"])

    assert gettext_wrapper.get_available_languages() == ["fr", "de", "en", "es", "pl", "ru"]
