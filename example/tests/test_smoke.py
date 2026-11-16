from pathlib import Path

from streamlit.testing.v1 import AppTest

app_root = Path(__file__).resolve().parent.parent


def test_app_starts():
    app = AppTest.from_file(app_root / "app.py").run()

    assert not app.exception, app.exception[0].stack_trace
    assert len(app.slider) == 1
