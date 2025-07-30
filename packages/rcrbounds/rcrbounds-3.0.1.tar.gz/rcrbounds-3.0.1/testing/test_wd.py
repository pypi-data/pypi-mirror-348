"""
TEST_WD.PY Unit tests for write_details()
"""
import os
import sys
import tempfile


import pytest
import numpy as np

from rcrbounds import write_details


# Basic functionality
def test_wd_basic():
    """write the specified arrays to the specified test file"""
    effectvec = np.zeros(3)
    rcvec = np.zeros(3)
    with tempfile.TemporaryDirectory() as tmp:
        detfile = os.path.join(tmp, 'pdet.txt')
        assert not os.path.exists(detfile)
        write_details(effectvec, rcvec, detfile)
        assert os.path.exists(detfile)


# Exceptions to handle
def test_wd_nofile():
    """do nothing if file name is blank"""
    effectvec = np.zeros(3)
    rcvec = np.zeros(3)
    write_details(effectvec, rcvec, "")


def test_wd_readonly(read_only_file):
    """warn and continue if read-only file"""
    effectvec = np.zeros(3)
    rcvec = np.zeros(3)
    with pytest.warns(UserWarning, match="Cannot write"):
        write_details(effectvec, rcvec, read_only_file)


def test_wd_badfolder():
    """warn and continue if non-existent folder"""
    effectvec = np.zeros(3)
    rcvec = np.zeros(3)
    with pytest.warns(UserWarning, match="Cannot write"):
        write_details(effectvec, rcvec, "nonexistent-path-name/pout.txt")


@pytest.mark.skipif(sys.platform != 'win32', reason="Windows test")
def test_wd_illegalname():
    """warn and continue if illegal file name"""
    effectvec = np.zeros(3)
    rcvec = np.zeros(3)
    with pytest.warns(UserWarning, match="Cannot write"):
        write_details(effectvec, rcvec, "?")
