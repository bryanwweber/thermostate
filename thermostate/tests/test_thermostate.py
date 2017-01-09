"""
Test module for the main ThermoState code
"""
from pint import UnitRegistry
import pytest
from math import isclose

from ..thermostate import State, StateError


def isclose_quant(a, b, *args, **kwargs):
    return isclose(a.magnitude, b.magnitude, *args, **kwargs)

ureg = UnitRegistry()
Q_ = ureg.Quantity


class TestState(object):
    """
    """
    def test_set_Tp(self):
        s = State(substance='water', T=Q_(400., 'K'), p=Q_(101325., 'Pa'))
        assert isclose_quant(s.T, Q_(400., 'K'))
        assert isclose_quant(s.p, Q_(101325., 'Pa'))
        assert isclose_quant(s.Tp[0], Q_(400., 'K'))
        assert isclose_quant(s.Tp[1], Q_(101325., 'Pa'))
        assert isclose_quant(s.u, Q_(2547715.3635084038, 'J/kg'))
        assert isclose_quant(s.s, Q_(7496.2021523754065, 'J/(kg*K)'))
        assert isclose_quant(s.v, Q_(1.801983936953226, 'm**3/kg'))
        assert isclose_quant(s.h, Q_(2730301.3859201893, 'J/kg'))
        assert s.x is None

    def test_lowercase_input(self):
        State(substance='water')
        State(substance='r22')
        State(substance='r134a')
        State(substance='ammonia')
        State(substance='propane')
        State(substance='air')

    def test_bad_substance(self):
        with pytest.raises(ValueError):
            State(substance='bad substance')

    def test_too_many_props(self):
        with pytest.raises(ValueError):
            State(substance='water', T=Q_(300, 'K'), p=Q_(101325, 'Pa'), u=Q_(100, 'kJ/kg'))

    def test_too_few_props(self):
        with pytest.raises(ValueError):
            State(substance='water', T=Q_(300, 'K'))

    def test_invalid_pair(self):
        with pytest.raises(ValueError):
            State(substance='water', x=Q_(0.5, 'dimensionless'), h=Q_(300, 'kJ/kg'))

    def test_bad_TP_dimensions(self):
        with pytest.raises(StateError):
            State(substance='water', T=Q_(300., 'Pa'), p=Q_(101325., 'Pa'))

        with pytest.raises(StateError):
            State(substance='water', T=Q_(300., 'K'), p=Q_(101325., 'K'))

    def test_TP_twophase(self):
        with pytest.raises(StateError):
            State(substance='water', T=Q_(373.1242958476844, 'K'), p=Q_(101325., 'Pa'))

    # Need to find a pathologically bad set of inputs here to raise a ValueError from
    # CoolProp that isn't related to being too close to the saturation point
    @pytest.mark.xfail
    def test_bad_TP_values(self):
        with pytest.raises(ValueError):
            State(substance='water', T=Q_(10000., 'K'), p=Q_(101325., 'Pa'))

    def test_set_pT(self):
        s = State(substance='water')
        s.pT = Q_(101325., 'Pa'), Q_(400., 'K')
        assert isclose_quant(s.T, Q_(400., 'K'))
        assert isclose_quant(s.p, Q_(101325., 'Pa'))
        assert isclose_quant(s.pT[1], Q_(400., 'K'))
        assert isclose_quant(s.pT[0], Q_(101325., 'Pa'))
        assert isclose_quant(s.u, Q_(2547715.3635084038, 'J/kg'))
        assert isclose_quant(s.s, Q_(7496.2021523754065, 'J/(kg*K)'))
        assert isclose_quant(s.v, Q_(1.801983936953226, 'm**3/kg'))
        assert isclose_quant(s.h, Q_(2730301.3859201893, 'J/kg'))
        assert s.x is None

    # This set of tests fails because T and u are not valid inputs for PhaseSI
    # in CoolProp 6.1.0
    @pytest.mark.xfail(strict=True)
    def test_set_uT(self):
        s = State(substance='water')
        s.uT = Q_(2547715.3635084038, 'J/kg'), Q_(400., 'K')
        assert isclose_quant(s.T, Q_(400., 'K'))
        assert isclose_quant(s.p, Q_(101325., 'Pa'))
        assert isclose_quant(s.uT[1], Q_(400., 'K'))
        assert isclose_quant(s.uT[0], Q_(2547715.3635084038, 'J/kg'))
        assert isclose_quant(s.u, Q_(2547715.3635084038, 'J/kg'))
        assert isclose_quant(s.s, Q_(7496.2021523754065, 'J/(kg*K)'))
        assert isclose_quant(s.v, Q_(1.801983936953226, 'm**3/kg'))
        assert isclose_quant(s.h, Q_(2730301.3859201893, 'J/kg'))
        assert s.x is None

    @pytest.mark.xfail(strict=True)
    def test_set_Tu(self):
        s = State(substance='water')
        s.Tu = Q_(400., 'K'), Q_(2547715.3635084038, 'J/kg')
        assert isclose_quant(s.T, Q_(400., 'K'))
        assert isclose_quant(s.p, Q_(101325., 'Pa'))
        assert isclose_quant(s.Tu[0], Q_(400., 'K'))
        assert isclose_quant(s.Tu[1], Q_(2547715.3635084038, 'J/kg'))
        assert isclose_quant(s.u, Q_(2547715.3635084038, 'J/kg'))
        assert isclose_quant(s.s, Q_(7496.2021523754065, 'J/(kg*K)'))
        assert isclose_quant(s.v, Q_(1.801983936953226, 'm**3/kg'))
        assert isclose_quant(s.h, Q_(2730301.3859201893, 'J/kg'))
        assert s.x is None

    # This set of tests fails because T and h are not valid inputs for PhaseSI
    # in CoolProp 6.1.0
    @pytest.mark.xfail(strict=True)
    def test_set_hT(self):
        s = State(substance='water')
        s.hT = Q_(2730301.3859201893, 'J/kg'), Q_(400., 'K')
        assert isclose_quant(s.T, Q_(400., 'K'))
        assert isclose_quant(s.p, Q_(101325., 'Pa'))
        assert isclose_quant(s.hT[1], Q_(400., 'K'))
        assert isclose_quant(s.hT[0], Q_(2730301.3859201893, 'J/kg'))
        assert isclose_quant(s.u, Q_(2547715.3635084038, 'J/kg'))
        assert isclose_quant(s.s, Q_(7496.2021523754065, 'J/(kg*K)'))
        assert isclose_quant(s.v, Q_(1.801983936953226, 'm**3/kg'))
        assert isclose_quant(s.h, Q_(2730301.3859201893, 'J/kg'))
        assert s.x is None

    @pytest.mark.xfail(strict=True)
    def test_set_Th(self):
        s = State(substance='water')
        s.Th = Q_(400., 'K'), Q_(2730301.3859201893, 'J/kg')
        assert isclose_quant(s.T, Q_(400., 'K'))
        assert isclose_quant(s.p, Q_(101325., 'Pa'))
        assert isclose_quant(s.Tu[0], Q_(400., 'K'))
        assert isclose_quant(s.Th[1], Q_(2730301.3859201893, 'J/kg'))
        assert isclose_quant(s.u, Q_(2547715.3635084038, 'J/kg'))
        assert isclose_quant(s.s, Q_(7496.2021523754065, 'J/(kg*K)'))
        assert isclose_quant(s.v, Q_(1.801983936953226, 'm**3/kg'))
        assert isclose_quant(s.h, Q_(2730301.3859201893, 'J/kg'))
        assert s.x is None
