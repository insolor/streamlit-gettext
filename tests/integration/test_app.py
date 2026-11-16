from pathlib import Path

from streamlit.testing.v1 import AppTest

app_root = Path(__file__).resolve().parents[2] / "example"


def test_navigation_entrypoint():
    apptest = AppTest.from_file(app_root / "app.py").run()

    assert not apptest.exception, apptest.exception[0].stack_trace
    assert len(apptest.slider) == 1
    autodetect_text = apptest.markdown[0].value

    apptest.switch_page("example_with_switcher.py").run()

    assert not apptest.exception, apptest.exception[0].stack_trace
    assert len(apptest.segmented_control) == 1
    apptest.segmented_control[0].set_value("de").run()
    assert apptest.markdown[0].value == "Eichhörnchen-Anwendung"

    apptest.switch_page("autodetect_example.py").run()

    assert not apptest.exception, apptest.exception[0].stack_trace
    assert apptest.markdown[0].value == autodetect_text


def test_example_sessions_do_not_share_manual_language():
    first = AppTest.from_file(app_root / "example_with_switcher.py").run()
    first.segmented_control[0].set_value("de").run()
    assert not first.exception
    assert first.markdown[0].value == "Eichhörnchen-Anwendung"

    second = AppTest.from_file(app_root / "autodetect_example.py").run()
    assert not second.exception
    assert second.markdown[0].value == "Squirrel application"

    second = AppTest.from_file(app_root / "example_with_switcher.py").run()
    second.segmented_control[0].set_value("ja").run()
    assert not second.exception
    assert second.markdown[0].value == "リスのアプリ"

    first.run()
    assert not first.exception
    assert first.markdown[0].value == "Eichhörnchen-Anwendung"
