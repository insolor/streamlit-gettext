from collections.abc import Iterable
from pathlib import Path

import pytest
import streamlit as st

from streamlit_gettext import GettextWrapper


def test_shared_wrapper_keeps_sessions_independent(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    wrapper = GettextWrapper(tmp_path)
    monkeypatch.setattr(wrapper, "get_preferred_languages_from_browser", lambda: ["en"])
    first_session = {}
    second_session = {}

    monkeypatch.setattr(st, "session_state", first_session)
    wrapper.set_preferred_languages(["de"])

    monkeypatch.setattr(st, "session_state", second_session)
    assert wrapper.get_preferred_languages() == ["en"]
    wrapper.set_preferred_languages(["ja"])

    monkeypatch.setattr(st, "session_state", first_session)
    assert wrapper.get_preferred_languages() == ["de"]
    wrapper.set_preferred_languages(None)
    assert wrapper.get_preferred_languages() == ["en"]

    monkeypatch.setattr(st, "session_state", second_session)
    assert wrapper.get_preferred_languages() == ["ja"]


@pytest.mark.parametrize("languages", [None, [], (), iter(())])
def test_reset_restores_browser_detection(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    languages: Iterable[str] | None,
):
    monkeypatch.setattr(st, "session_state", {})
    wrapper = GettextWrapper(tmp_path)
    monkeypatch.setattr(wrapper, "get_preferred_languages_from_browser", lambda: ["fr"])
    wrapper.set_preferred_languages(["de"])
    wrapper.set_preferred_languages(languages)

    assert wrapper.get_preferred_languages() == ["fr"]


def test_preferences_survive_wrapper_recreation_and_are_scoped_to_catalog(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
):
    monkeypatch.setattr(st, "session_state", {})
    wrapper = GettextWrapper(tmp_path)
    languages = ["ja"]
    wrapper.set_preferred_languages(iter(languages))
    languages.append("de")

    recreated = GettextWrapper(str(tmp_path))
    assert recreated.get_preferred_languages() == ["ja"]
    returned_languages = recreated.get_preferred_languages()
    returned_languages.append("fr")
    assert recreated.get_preferred_languages() == ["ja"]
    for other in (GettextWrapper(tmp_path, domain="other"), GettextWrapper(tmp_path / "other")):
        monkeypatch.setattr(other, "get_preferred_languages_from_browser", lambda: ["en"])
        assert other.get_preferred_languages() == ["en"]
