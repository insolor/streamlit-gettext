from pathlib import Path
from types import SimpleNamespace

import pytest
import streamlit as st

from streamlit_gettext import GettextWrapper


@pytest.mark.parametrize(
    ("entry", "expected"),
    [
        ("en", ("en", 1.0)),
        ("pt-BR", ("pt-BR", 1.0)),
        ("zh-Hant-TW;q=1.000", ("zh-Hant-TW", 1.0)),
        ("es-419;q=0.9", ("es-419", 0.9)),
        ("\tpt-BR ; Q=0.800\t", ("pt-BR", 0.8)),
        ("fr;q=0.001", ("fr", 0.001)),
        ("ru;q=1.", ("ru", 1.0)),
        ("ru;q=0", None),
        ("ru;q=0.000", None),
        ("fr;q=0.", None),
        ("*", None),
        ("*;q=0.5", None),
        ("", None),
        (" \t", None),
        ("ru;q=invalid", None),
        ("ru;q=1.1", None),
        ("ru;q=-0.1", None),
        ("ru;q=0.1234", None),
        ("ru;q=nan", None),
        ("ru;q=inf", None),
        ("ru;q=", None),
        ("en_US", None),
        ("ru--RU", None),
        ("fr;q=0.5;extra=1", None),
        ("fr,de", None),
    ],
)
def test_parse_accept_language_entry(entry: str, expected: tuple[str, float] | None):
    assert GettextWrapper._parse_accept_language_entry(entry) == expected  # noqa: SLF001


@pytest.mark.parametrize(
    ("header", "expected"),
    [
        (None, []),
        ("", []),
        (" , , ", []),
        ("en-US,en;q=0.9,ru;q=0.8", ["en-US", "en", "ru"]),
        ("de;q=0.5,ja;q=1", ["ja", "de"]),
        ("ru;q=0.2,fr,de;q=0.7", ["fr", "de", "ru"]),
        ("de;q=0.5,ja;q=0.5,fr;q=0.5", ["de", "ja", "fr"]),
        ("ru;q=0,ja;q=0.000,fr;q=0.001", ["fr"]),
        ("ru;q=0,fr;q=0", []),
        ("fr;q=0.2,FR;q=0.9,de;q=0.5", ["FR", "de"]),
        ("fr,FR,de", ["fr", "de"]),
        ("*,fr;q=0.8", ["fr"]),
        ("ru;q=invalid,fr", ["fr"]),
    ],
)
def test_browser_languages_parse_quality_values(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    header: str | None,
    expected: list[str],
):
    headers = {"Accept-Language": header} if header is not None else {}
    monkeypatch.setattr(st, "context", SimpleNamespace(headers=headers))

    assert GettextWrapper(tmp_path).get_preferred_languages_from_browser() == expected


@pytest.mark.parametrize(
    ("header", "expected"),
    [
        ("ru;q=0.2,fr;q=0.9", "Ouvrir"),
        ("ru;q=0,fr;q=0.5", "Ouvrir"),
        ("ru;q=0,fr;q=0", "Open"),
        ("ru;q=0.9,fr;q=0.2", "Открыть без контекста"),
    ],
)
def test_browser_weights_select_actual_translation(
    monkeypatch: pytest.MonkeyPatch,
    header: str,
    expected: str,
):
    monkeypatch.setattr(st, "context", SimpleNamespace(headers={"Accept-Language": header}))
    monkeypatch.setattr(st, "session_state", {})
    locale_path = Path(__file__).resolve().parent.parent / "fixtures" / "locale"
    wrapper = GettextWrapper(locale_path, domain="testing")

    assert wrapper.gettext("Open") == expected


def test_language_selector_uses_browser_weights(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    for language in ("ru", "fr"):
        catalog = tmp_path / language / "LC_MESSAGES" / "messages.mo"
        catalog.parent.mkdir(parents=True)
        catalog.touch()
    monkeypatch.setattr(st, "context", SimpleNamespace(headers={"Accept-Language": "ru;q=0.2,fr;q=0.9"}))

    assert GettextWrapper(tmp_path).get_available_languages() == ["fr", "ru", "en"]
