from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

app_root = Path(__file__).resolve().parent.parent


@pytest.fixture
def apptest() -> AppTest:
    return AppTest.from_file(app_root / "example_with_switcher.py").run()


def test_smoketest(apptest: AppTest):
    assert not apptest.exception, apptest.exception[0].stack_trace


def test_language_selection(apptest: AppTest):
    translations = (
        ("de", "Eichhörnchen-Anwendung", "Es gibt 8 Eichhörnchen:"),
        ("fr", "Application sur les écureuils", "Il y a 8 écureuils :"),
        ("zh_TW", "松鼠應用程式", "有 8 隻松鼠："),
        ("zh_CN", "松鼠应用程序", "有 8 只松鼠："),
        ("pt_BR", "Aplicativo sobre esquilos", "Há 8 esquilos:"),
        ("es", "Aplicación de las ardillas", "Hay 8 ardillas:"),
        ("pl", "Aplikacja o wiewiórkach", "Jest 8 wiewiórek:"),
        ("ru", "Беличье приложение", "Здесь 8 белок:"),
        ("uk", "Білячий застосунок", "Тут 8 білок:"),
    )

    for language, text, plural_text in translations:
        apptest.segmented_control[0].set_value(language).run()
        assert apptest.markdown[0].value == text

        apptest.slider[0].set_value(8).run()
        assert apptest.markdown[1].value == plural_text


@pytest.mark.parametrize(
    ("language", "prefix", "count", "form"),
    [
        ("ru", "Здесь", 1, "белка"),
        ("ru", "Здесь", 2, "белки"),
        ("ru", "Здесь", 4, "белки"),
        ("ru", "Здесь", 5, "белок"),
        ("ru", "Здесь", 11, "белок"),
        ("ru", "Здесь", 12, "белок"),
        ("ru", "Здесь", 14, "белок"),
        ("ru", "Здесь", 21, "белка"),
        ("ru", "Здесь", 22, "белки"),
        ("ru", "Здесь", 24, "белки"),
        ("ru", "Здесь", 25, "белок"),
        ("ru", "Здесь", 99, "белок"),
        ("ru", "Здесь", 100, "белок"),
        ("uk", "Тут", 1, "білка"),
        ("uk", "Тут", 2, "білки"),
        ("uk", "Тут", 4, "білки"),
        ("uk", "Тут", 5, "білок"),
        ("uk", "Тут", 11, "білок"),
        ("uk", "Тут", 12, "білок"),
        ("uk", "Тут", 14, "білок"),
        ("uk", "Тут", 21, "білка"),
        ("uk", "Тут", 22, "білки"),
        ("uk", "Тут", 24, "білки"),
        ("uk", "Тут", 25, "білок"),
        ("uk", "Тут", 99, "білок"),
        ("uk", "Тут", 100, "білок"),
        ("pl", "Jest", 1, "wiewiórka"),
        ("pl", "Są", 2, "wiewiórki"),
        ("pl", "Są", 4, "wiewiórki"),
        ("pl", "Jest", 5, "wiewiórek"),
        ("pl", "Jest", 11, "wiewiórek"),
        ("pl", "Jest", 12, "wiewiórek"),
        ("pl", "Jest", 14, "wiewiórek"),
        ("pl", "Jest", 21, "wiewiórek"),
        ("pl", "Są", 22, "wiewiórki"),
        ("pl", "Są", 24, "wiewiórki"),
        ("pl", "Jest", 25, "wiewiórek"),
        ("pl", "Jest", 99, "wiewiórek"),
        ("pl", "Jest", 100, "wiewiórek"),
    ],
)
def test_plural_form_boundaries(
    apptest: AppTest,
    language: str,
    prefix: str,
    count: int,
    form: str,
):
    apptest.segmented_control[0].set_value(language).run()
    apptest.slider[0].set_value(count).run()
    assert apptest.markdown[1].value == f"{prefix} {count} {form}:"
