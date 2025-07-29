import pytest_iso


def test_runtest_protocol_hook_is_called(pytester):
    """
    This is the docstring of a pytest test function. You can add your test explanation here and
    pytest-iso will print this section in the top frame of the PDF.

    Pytest hooks will be tested by the pytest plugin "pytester". Pytester creates isolated
    environments to test pytest functionalities.

    In this test example conftests and example functions are created that interact with pytest hooks
    defined in pytest-iso.

    Finally, it will be evaluated if the hook was called and the function name is properly provided.
    """
    # hook needs to be exposed via conftest
    pytester.makeconftest("""
    import pytest_iso
    pytest_runtest_protocol = pytest_iso.pytest_runtest_protocol
    """)

    # example test
    pytester.makepyfile("""
    def test_example():
        '''docstring for test_example'''
        assert 1 + 1 == 2
    """)

    # hook recorder
    hookrec = pytester.inline_run("-q")
    hookrec.assertoutcome(passed=1)

    # assert that hook was called (one example function so one call)
    calls = hookrec.getcalls("pytest_runtest_protocol")
    assert len(calls) == 1

    # check that function name is provided with nodeid
    call = calls[0]
    assert call.item.nodeid.endswith("::test_example")

    # only one item to test so nextiitem is none
    assert call.nextitem is None


def test_runtest_protocol_skips_non_function_items():
    class NotAPytestFunction:
        pass

    dummy = NotAPytestFunction()
    ret = pytest_iso.pytest_runtest_protocol(dummy, nextitem=None)
    assert ret is None


def test_sessionfinish_hook_creates_pdf(pytester):
    pytester.makepyfile("""
    def test_dummy():
        '''dummy docstring'''
        assert True
    """)

    pytester.makeconftest("""
    import pytest_iso
    pytest_runtest_protocol = pytest_iso.pytest_runtest_protocol
    pytest_sessionfinish = pytest_iso.pytest_sessionfinish
    """)

    pytester.runpytest("-q")

    pdf_path = pytester.path / "test_protocol.pdf"
    assert pdf_path.exists()
    assert pdf_path.stat().st_size > 0


# the tests above just test pytest_iso as a pytest plugin, so if the hooks work
# but we also need to test the direct import
def test_direct_import_pytest_iso():
    import importlib

    importlib.reload(pytest_iso)
    assert isinstance(pytest_iso.plugin._test_details, list)
