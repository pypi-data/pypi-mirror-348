import os
import inspect
import re

import pytest

import pytest_iso

# store docstrings of tests in temp list
_test_details = []


def pytest_runtest_protocol(item, nextitem):
    """

    This hook is executed with each test. It collects the nodeid, which is the path to the pytest script
    and the pytest function, that is tested, the doc, which is the docstring of the test function, and source,
    which is the test function itself (with removed docstring).

    Extracted details are stored in a temporary list (_test_details) and passed to the underlying Rust
    functionality, that creates a PDF file out of these details.

    :param item: A pytest test item
    :param nextitem: The next pytest test item
    :return: None
    """

    if not isinstance(item, pytest.Function):
        return None

    func = item.function
    doc = func.__doc__ or ""

    # extract source code but remove docstring section, since the docstring section is handled separately
    try:
        source = inspect.getsource(func)
        docstring_pattern = r'"""[\s\S]*?"""|\'\'\'[\s\S]*?\'\'\''
        source = re.sub(docstring_pattern, "", source)
    except OSError:
        source = "<source code unavailable>"

    entry = [item.nodeid, doc, source]
    _test_details.append(entry)

    return None


def pytest_sessionfinish(session, exitstatus):
    if _test_details:
        out_pdf = os.path.join(os.getcwd(), "test_protocol.pdf")
        pytest_iso.create_test_pdf(_test_details, out_pdf)
        print(f"\nGenerated PDF report: {out_pdf}")
