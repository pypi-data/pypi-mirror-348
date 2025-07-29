## All test functions need to start with test_

import Wisdom_Data_Library as wdl

def test_test_function():
    assert callable(wdl.test)

def test_test2_function():
    assert wdl.test2() == "this is a test"