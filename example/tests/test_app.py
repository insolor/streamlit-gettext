from pathlib import Path

from streamlit.testing.v1 import AppTest

app_root = Path(__file__).resolve().parent.parent


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
