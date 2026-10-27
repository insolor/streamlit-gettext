from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

app_root = Path(__file__).resolve().parent.parent


@pytest.fixture
def apptest() -> AppTest:
    return AppTest.from_file(app_root / "example_with_switcher.py").run()


def test_smoketest(apptest: AppTest):
    assert not apptest.exception, apptest.exception[0].stack_trace
