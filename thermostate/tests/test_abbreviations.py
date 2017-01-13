"""
Test module for the units abbreviations code
"""
from ..abbreviations import EnglishEngineering as EE, SystemInternational as SI


def test_EE():
    assert EE.s == 'BTU/(lb*degR)'
    assert EE.h == 'BTU/lb'
    assert EE.T == 'degF'
    assert EE.u == 'BTU/lb'
    assert EE.v == 'ft**3/lb'
    assert EE.p == 'psi'


def test_SI():
    assert SI.s == 'kJ/(kg*K)'
    assert SI.h == 'kJ/kg'
    assert SI.T == 'degC'
    assert SI.u == 'kJ/kg'
    assert SI.v == 'm**3/kg'
    assert SI.p == 'bar'
