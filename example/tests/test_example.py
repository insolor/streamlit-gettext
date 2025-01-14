import pytest
from streamlit.testing.v1 import AppTest


@pytest.fixture
def apptest() -> AppTest:
    return AppTest.from_file("example.py").run()


def test_smoketest(apptest: AppTest):
    assert not apptest.exception, apptest.exception[0].stack_trace
