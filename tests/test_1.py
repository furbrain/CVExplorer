"""Performs general tests."""
import amodule
from sampleproject.libs import samplemodule as sm


def test_amodule():
    """Test amodule.hello()."""
    amodule.hello()


def test_true():
    """Just asserts True."""
    assert True


def test_sampleclass():
    """Test samplemodule SampleClass true method."""
    s = sm.SampleClass()
    assert s.true() is True


def test_sampleclass_false():
    """Test samplemodule SampleClass false classmethod."""
    assert sm.SampleClass.false() is False
