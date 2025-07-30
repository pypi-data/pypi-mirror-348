"""
TEST_DW.PY Unit tests for die() and warn()
"""
import pytest

from rcrbounds import warn, die, set_logfile, get_logfile


# Basic functionality of warn()
def test_warn():
    """write to the logfile and issue a warning"""
    oldlogfile = get_logfile()
    set_logfile(None)
    with pytest.warns(UserWarning, match="Test warning"):
        warn("Test warning")
    set_logfile(oldlogfile)


# Basic functionality of die()
def test_die():
    """issue an exception"""
    oldlogfile = get_logfile()
    set_logfile(None)
    try:
        die("Test dying")
    except RuntimeError:
        pass
    else:
        raise AssertionError
    set_logfile(oldlogfile)
