"""Test module for the units abbreviations code."""
from thermostate import EnglishEngineering as EE
from thermostate import SystemInternational as SI


def test_EE():
    """Test the English Engineering abbreviations."""
    assert EE.s == "BTU/(lb*degR)"
    assert EE.h == "BTU/lb"
    assert EE.T == "degF"
    assert EE.u == "BTU/lb"
    assert EE.v == "ft**3/lb"
    assert EE.p == "psi"


def test_SI():
    """Test the Système Internationale d'Unités abbreviations."""
    assert SI.s == "kJ/(kg*K)"
    assert SI.h == "kJ/kg"
    assert SI.T == "degC"
    assert SI.u == "kJ/kg"
    assert SI.v == "m**3/kg"
    assert SI.p == "bar"
