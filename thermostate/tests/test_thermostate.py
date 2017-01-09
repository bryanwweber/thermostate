"""
Test module for the main ThermoState code
"""
import pytest
from math import isclose

from ..thermostate import State, StateError, Q_


def isclose_quant(a, b, *args, **kwargs):
    return isclose(a.magnitude, b.magnitude, *args, **kwargs)


class TestState(object):
    """
    """
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
    @pytest.mark.xfail(strict=True, raises=StateError)
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

    @pytest.mark.xfail(strict=True, raises=StateError)
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
    @pytest.mark.xfail(strict=True, raises=StateError)
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

    @pytest.mark.xfail(strict=True, raises=StateError)
    def test_set_Th(self):
        s = State(substance='water')
        s.Th = Q_(400., 'K'), Q_(2730301.3859201893, 'J/kg')
        assert isclose_quant(s.T, Q_(400., 'K'))
        assert isclose_quant(s.p, Q_(101325., 'Pa'))
        assert isclose_quant(s.Th[0], Q_(400., 'K'))
        assert isclose_quant(s.Th[1], Q_(2730301.3859201893, 'J/kg'))
        assert isclose_quant(s.u, Q_(2547715.3635084038, 'J/kg'))
        assert isclose_quant(s.s, Q_(7496.2021523754065, 'J/(kg*K)'))
        assert isclose_quant(s.v, Q_(1.801983936953226, 'm**3/kg'))
        assert isclose_quant(s.h, Q_(2730301.3859201893, 'J/kg'))
        assert s.x is None

    def test_set_sT(self):
        s = State(substance='water')
        s.sT = Q_(7496.2021523754065, 'J/(kg*K)'), Q_(400., 'K')
        assert isclose_quant(s.T, Q_(400., 'K'))
        assert isclose_quant(s.p, Q_(101325., 'Pa'))
        assert isclose_quant(s.sT[1], Q_(400., 'K'))
        assert isclose_quant(s.sT[0], Q_(7496.2021523754065, 'J/(kg*K)'))
        assert isclose_quant(s.u, Q_(2547715.3635084038, 'J/kg'))
        assert isclose_quant(s.s, Q_(7496.2021523754065, 'J/(kg*K)'))
        assert isclose_quant(s.v, Q_(1.801983936953226, 'm**3/kg'))
        assert isclose_quant(s.h, Q_(2730301.3859201893, 'J/kg'))
        assert s.x is None

    def test_set_Ts(self):
        s = State(substance='water')
        s.Ts = Q_(400., 'K'), Q_(7496.2021523754065, 'J/(kg*K)')
        assert isclose_quant(s.T, Q_(400., 'K'))
        assert isclose_quant(s.p, Q_(101325., 'Pa'))
        assert isclose_quant(s.Ts[0], Q_(400., 'K'))
        assert isclose_quant(s.Ts[1], Q_(7496.2021523754065, 'J/(kg*K)'))
        assert isclose_quant(s.u, Q_(2547715.3635084038, 'J/kg'))
        assert isclose_quant(s.s, Q_(7496.2021523754065, 'J/(kg*K)'))
        assert isclose_quant(s.v, Q_(1.801983936953226, 'm**3/kg'))
        assert isclose_quant(s.h, Q_(2730301.3859201893, 'J/kg'))
        assert s.x is None

    def test_set_vT(self):
        s = State(substance='water')
        s.vT = Q_(1.801983936953226, 'm**3/kg'), Q_(400., 'K')
        assert isclose_quant(s.T, Q_(400., 'K'))
        assert isclose_quant(s.p, Q_(101325., 'Pa'))
        assert isclose_quant(s.vT[1], Q_(400., 'K'))
        assert isclose_quant(s.vT[0], Q_(1.801983936953226, 'm**3/kg'))
        assert isclose_quant(s.u, Q_(2547715.3635084038, 'J/kg'))
        assert isclose_quant(s.s, Q_(7496.2021523754065, 'J/(kg*K)'))
        assert isclose_quant(s.v, Q_(1.801983936953226, 'm**3/kg'))
        assert isclose_quant(s.h, Q_(2730301.3859201893, 'J/kg'))
        assert s.x is None

    def test_set_Tv(self):
        s = State(substance='water')
        s.Tv = Q_(400., 'K'), Q_(1.801983936953226, 'm**3/kg')
        assert isclose_quant(s.T, Q_(400., 'K'))
        assert isclose_quant(s.p, Q_(101325., 'Pa'))
        assert isclose_quant(s.Tv[0], Q_(400., 'K'))
        assert isclose_quant(s.Tv[1], Q_(1.801983936953226, 'm**3/kg'))
        assert isclose_quant(s.u, Q_(2547715.3635084038, 'J/kg'))
        assert isclose_quant(s.s, Q_(7496.2021523754065, 'J/(kg*K)'))
        assert isclose_quant(s.v, Q_(1.801983936953226, 'm**3/kg'))
        assert isclose_quant(s.h, Q_(2730301.3859201893, 'J/kg'))
        assert s.x is None

    def test_set_xT(self):
        s = State(substance='water')
        s.xT = Q_(0.5, 'dimensionless'), Q_(400., 'K')
        assert isclose_quant(s.T, Q_(400., 'K'))
        assert isclose_quant(s.p, Q_(245769.34557103913, 'Pa'))
        assert isclose_quant(s.xT[1], Q_(400., 'K'))
        assert isclose_quant(s.xT[0], Q_(0.5, 'dimensionless'))
        assert isclose_quant(s.u, Q_(1534461.5163075812, 'J/kg'))
        assert isclose_quant(s.s, Q_(4329.703956664546, 'J/(kg*K)'))
        assert isclose_quant(s.v, Q_(0.3656547423394701, 'm**3/kg'))
        assert isclose_quant(s.h, Q_(1624328.2430353598, 'J/kg'))
        assert isclose_quant(s.x, Q_(0.5, 'dimensionless'))
        s.xT = Q_(50, 'percent'), Q_(400., 'K')
        assert isclose_quant(s.T, Q_(400., 'K'))
        assert isclose_quant(s.p, Q_(245769.34557103913, 'Pa'))
        assert isclose_quant(s.xT[1], Q_(400., 'K'))
        assert isclose_quant(s.xT[0], Q_(0.5, 'dimensionless'))
        assert isclose_quant(s.u, Q_(1534461.5163075812, 'J/kg'))
        assert isclose_quant(s.s, Q_(4329.703956664546, 'J/(kg*K)'))
        assert isclose_quant(s.v, Q_(0.3656547423394701, 'm**3/kg'))
        assert isclose_quant(s.h, Q_(1624328.2430353598, 'J/kg'))
        assert isclose_quant(s.x, Q_(0.5, 'dimensionless'))

    def test_set_Tx(self):
        s = State(substance='water')
        s.Tx = Q_(400., 'K'), Q_(0.5, 'dimensionless')
        assert isclose_quant(s.T, Q_(400., 'K'))
        assert isclose_quant(s.p, Q_(245769.34557103913, 'Pa'))
        assert isclose_quant(s.Tx[0], Q_(400., 'K'))
        assert isclose_quant(s.Tx[1], Q_(0.5, 'dimensionless'))
        assert isclose_quant(s.u, Q_(1534461.5163075812, 'J/kg'))
        assert isclose_quant(s.s, Q_(4329.703956664546, 'J/(kg*K)'))
        assert isclose_quant(s.v, Q_(0.3656547423394701, 'm**3/kg'))
        assert isclose_quant(s.h, Q_(1624328.2430353598, 'J/kg'))
        assert isclose_quant(s.x, Q_(0.5, 'dimensionless'))
        s.Tx = Q_(400., 'K'), Q_(50, 'percent')
        assert isclose_quant(s.T, Q_(400., 'K'))
        assert isclose_quant(s.p, Q_(245769.34557103913, 'Pa'))
        assert isclose_quant(s.Tx[0], Q_(400., 'K'))
        assert isclose_quant(s.Tx[1], Q_(0.5, 'dimensionless'))
        assert isclose_quant(s.u, Q_(1534461.5163075812, 'J/kg'))
        assert isclose_quant(s.s, Q_(4329.703956664546, 'J/(kg*K)'))
        assert isclose_quant(s.v, Q_(0.3656547423394701, 'm**3/kg'))
        assert isclose_quant(s.h, Q_(1624328.2430353598, 'J/kg'))
        assert isclose_quant(s.x, Q_(0.5, 'dimensionless'))

    def test_set_pu(self):
        s = State(substance='water')
        s.pu = Q_(101325., 'Pa'), Q_(1013250., 'J/kg')
        assert isclose_quant(s.T, Q_(373.1242958476843, 'K'))
        assert isclose_quant(s.p, Q_(101325., 'Pa'))
        assert isclose_quant(s.pu[0], Q_(101325., 'Pa'))
        assert isclose_quant(s.pu[1], Q_(1013250., 'J/kg'))
        assert isclose_quant(s.u, Q_(1013250., 'J/kg'))
        assert isclose_quant(s.s, Q_(3028.9867985920914, 'J/(kg*K)'))
        assert isclose_quant(s.v, Q_(0.4772010021515822, 'm**3/kg'))
        assert isclose_quant(s.h, Q_(1061602.391543017, 'J/kg'))
        assert isclose_quant(s.x, Q_(0.28475636946248034, 'dimensionless'))
        s.pu = Q_(101325., 'Pa'), Q_(3013250., 'J/kg')
        assert isclose_quant(s.T, Q_(700.9882316847855, 'K'))
        assert isclose_quant(s.p, Q_(101325., 'Pa'))
        assert isclose_quant(s.pu[0], Q_(101325., 'Pa'))
        assert isclose_quant(s.pu[1], Q_(3013250., 'J/kg'))
        assert isclose_quant(s.u, Q_(3013250., 'J/kg'))
        assert isclose_quant(s.s, Q_(8623.283568815832, 'J/(kg*K)'))
        assert isclose_quant(s.v, Q_(3.189303132125469, 'm**3/kg'))
        assert isclose_quant(s.h, Q_(3336406.139862406, 'J/kg'))
        assert s.x is None

    def test_set_up(self):
        s = State(substance='water')
        s.up = Q_(1013250., 'J/kg'), Q_(101325., 'Pa')
        assert isclose_quant(s.T, Q_(373.1242958476843, 'K'))
        assert isclose_quant(s.p, Q_(101325., 'Pa'))
        assert isclose_quant(s.up[0], Q_(1013250., 'J/kg'))
        assert isclose_quant(s.up[1], Q_(101325., 'Pa'))
        assert isclose_quant(s.u, Q_(1013250, 'J/kg'))
        assert isclose_quant(s.s, Q_(3028.9867985920914, 'J/(kg*K)'))
        assert isclose_quant(s.v, Q_(0.4772010021515822, 'm**3/kg'))
        assert isclose_quant(s.h, Q_(1061602.391543017, 'J/kg'))
        assert isclose_quant(s.x, Q_(0.28475636946248034, 'dimensionless'))
        s.up = Q_(3013250., 'J/kg'), Q_(101325., 'Pa')
        assert isclose_quant(s.T, Q_(700.9882316847855, 'K'))
        assert isclose_quant(s.p, Q_(101325., 'Pa'))
        assert isclose_quant(s.up[0], Q_(3013250., 'J/kg'))
        assert isclose_quant(s.up[1], Q_(101325., 'Pa'))
        assert isclose_quant(s.u, Q_(3013250, 'J/kg'))
        assert isclose_quant(s.s, Q_(8623.283568815832, 'J/(kg*K)'))
        assert isclose_quant(s.v, Q_(3.189303132125469, 'm**3/kg'))
        assert isclose_quant(s.h, Q_(3336406.139862406, 'J/kg'))
        assert s.x is None

    def test_set_ps(self):
        s = State(substance='water')
        s.ps = Q_(101325., 'Pa'), Q_(3028.9867985920914, 'J/(kg*K)')
        assert isclose_quant(s.T, Q_(373.1242958476843, 'K'))
        assert isclose_quant(s.p, Q_(101325., 'Pa'))
        assert isclose_quant(s.ps[0], Q_(101325., 'Pa'))
        assert isclose_quant(s.ps[1], Q_(3028.9867985920914, 'J/(kg*K)'))
        assert isclose_quant(s.u, Q_(1013250., 'J/kg'))
        assert isclose_quant(s.s, Q_(3028.9867985920914, 'J/(kg*K)'))
        assert isclose_quant(s.v, Q_(0.4772010021515822, 'm**3/kg'))
        assert isclose_quant(s.h, Q_(1061602.391543017, 'J/kg'))
        assert isclose_quant(s.x, Q_(0.28475636946248034, 'dimensionless'))
        s.ps = Q_(101325., 'Pa'), Q_(8623.283568815832, 'J/(kg*K)')
        assert isclose_quant(s.T, Q_(700.9882316847855, 'K'))
        assert isclose_quant(s.p, Q_(101325., 'Pa'))
        assert isclose_quant(s.ps[0], Q_(101325., 'Pa'))
        assert isclose_quant(s.ps[1], Q_(8623.283568815832, 'J/(kg*K)'))
        assert isclose_quant(s.u, Q_(3013250., 'J/kg'))
        assert isclose_quant(s.s, Q_(8623.283568815832, 'J/(kg*K)'))
        assert isclose_quant(s.v, Q_(3.189303132125469, 'm**3/kg'))
        assert isclose_quant(s.h, Q_(3336406.139862406, 'J/kg'))
        assert s.x is None

    def test_set_sp(self):
        s = State(substance='water')
        s.sp = Q_(3028.9867985920914, 'J/(kg*K)'), Q_(101325., 'Pa')
        assert isclose_quant(s.T, Q_(373.1242958476843, 'K'))
        assert isclose_quant(s.p, Q_(101325., 'Pa'))
        assert isclose_quant(s.sp[0], Q_(3028.9867985920914, 'J/(kg*K)'))
        assert isclose_quant(s.sp[1], Q_(101325., 'Pa'))
        assert isclose_quant(s.u, Q_(1013250, 'J/kg'))
        assert isclose_quant(s.s, Q_(3028.9867985920914, 'J/(kg*K)'))
        assert isclose_quant(s.v, Q_(0.4772010021515822, 'm**3/kg'))
        assert isclose_quant(s.h, Q_(1061602.391543017, 'J/kg'))
        assert isclose_quant(s.x, Q_(0.28475636946248034, 'dimensionless'))
        s.sp = Q_(8623.283568815832, 'J/(kg*K)'), Q_(101325., 'Pa')
        assert isclose_quant(s.T, Q_(700.9882316847855, 'K'))
        assert isclose_quant(s.p, Q_(101325., 'Pa'))
        assert isclose_quant(s.sp[0], Q_(8623.283568815832, 'J/(kg*K)'))
        assert isclose_quant(s.sp[1], Q_(101325., 'Pa'))
        assert isclose_quant(s.u, Q_(3013250, 'J/kg'))
        assert isclose_quant(s.s, Q_(8623.283568815832, 'J/(kg*K)'))
        assert isclose_quant(s.v, Q_(3.189303132125469, 'm**3/kg'))
        assert isclose_quant(s.h, Q_(3336406.139862406, 'J/kg'))
        assert s.x is None

    def test_set_pv(self):
        s = State(substance='water')
        s.pv = Q_(101325., 'Pa'), Q_(0.4772010021515822, 'm**3/kg')
        assert isclose_quant(s.T, Q_(373.1242958476843, 'K'))
        assert isclose_quant(s.p, Q_(101325., 'Pa'))
        assert isclose_quant(s.pv[0], Q_(101325., 'Pa'))
        assert isclose_quant(s.pv[1], Q_(0.4772010021515822, 'm**3/kg'))
        assert isclose_quant(s.u, Q_(1013250., 'J/kg'))
        assert isclose_quant(s.s, Q_(3028.9867985920914, 'J/(kg*K)'))
        assert isclose_quant(s.v, Q_(0.4772010021515822, 'm**3/kg'))
        assert isclose_quant(s.h, Q_(1061602.391543017, 'J/kg'))
        assert isclose_quant(s.x, Q_(0.28475636946248034, 'dimensionless'))
        s.pv = Q_(101325., 'Pa'), Q_(3.189303132125469, 'm**3/kg')
        assert isclose_quant(s.T, Q_(700.9882316847855, 'K'))
        assert isclose_quant(s.p, Q_(101325., 'Pa'))
        assert isclose_quant(s.pv[0], Q_(101325., 'Pa'))
        assert isclose_quant(s.pv[1], Q_(3.189303132125469, 'm**3/kg'))
        assert isclose_quant(s.u, Q_(3013250., 'J/kg'))
        assert isclose_quant(s.s, Q_(8623.283568815832, 'J/(kg*K)'))
        assert isclose_quant(s.v, Q_(3.189303132125469, 'm**3/kg'))
        assert isclose_quant(s.h, Q_(3336406.139862406, 'J/kg'))
        assert s.x is None

    def test_set_vp(self):
        s = State(substance='water')
        s.vp = Q_(0.4772010021515822, 'm**3/kg'), Q_(101325., 'Pa')
        assert isclose_quant(s.T, Q_(373.1242958476843, 'K'))
        assert isclose_quant(s.p, Q_(101325., 'Pa'))
        assert isclose_quant(s.vp[0], Q_(0.4772010021515822, 'm**3/kg'))
        assert isclose_quant(s.vp[1], Q_(101325., 'Pa'))
        assert isclose_quant(s.u, Q_(1013250, 'J/kg'))
        assert isclose_quant(s.s, Q_(3028.9867985920914, 'J/(kg*K)'))
        assert isclose_quant(s.v, Q_(0.4772010021515822, 'm**3/kg'))
        assert isclose_quant(s.h, Q_(1061602.391543017, 'J/kg'))
        assert isclose_quant(s.x, Q_(0.28475636946248034, 'dimensionless'))
        s.vp = Q_(3.189303132125469, 'm**3/kg'), Q_(101325., 'Pa')
        assert isclose_quant(s.T, Q_(700.9882316847855, 'K'))
        assert isclose_quant(s.p, Q_(101325., 'Pa'))
        assert isclose_quant(s.vp[0], Q_(3.189303132125469, 'm**3/kg'))
        assert isclose_quant(s.vp[1], Q_(101325., 'Pa'))
        assert isclose_quant(s.u, Q_(3013250, 'J/kg'))
        assert isclose_quant(s.s, Q_(8623.283568815832, 'J/(kg*K)'))
        assert isclose_quant(s.v, Q_(3.189303132125469, 'm**3/kg'))
        assert isclose_quant(s.h, Q_(3336406.139862406, 'J/kg'))
        assert s.x is None

    def test_set_ph(self):
        s = State(substance='water')
        s.ph = Q_(101325., 'Pa'), Q_(1061602.391543017, 'J/kg')
        assert isclose_quant(s.T, Q_(373.1242958476843, 'K'))
        assert isclose_quant(s.p, Q_(101325., 'Pa'))
        assert isclose_quant(s.ph[0], Q_(101325., 'Pa'))
        assert isclose_quant(s.ph[1], Q_(1061602.391543017, 'J/kg'))
        assert isclose_quant(s.u, Q_(1013250., 'J/kg'))
        assert isclose_quant(s.s, Q_(3028.9867985920914, 'J/(kg*K)'))
        assert isclose_quant(s.v, Q_(0.4772010021515822, 'm**3/kg'))
        assert isclose_quant(s.h, Q_(1061602.391543017, 'J/kg'))
        assert isclose_quant(s.x, Q_(0.28475636946248034, 'dimensionless'))
        s.ph = Q_(101325., 'Pa'), Q_(3336406.139862406, 'J/kg')
        assert isclose_quant(s.T, Q_(700.9882316847855, 'K'))
        assert isclose_quant(s.p, Q_(101325., 'Pa'))
        assert isclose_quant(s.ph[0], Q_(101325., 'Pa'))
        assert isclose_quant(s.ph[1], Q_(3336406.139862406, 'J/kg'))
        assert isclose_quant(s.u, Q_(3013250., 'J/kg'))
        assert isclose_quant(s.s, Q_(8623.283568815832, 'J/(kg*K)'))
        assert isclose_quant(s.v, Q_(3.189303132125469, 'm**3/kg'))
        assert isclose_quant(s.h, Q_(3336406.139862406, 'J/kg'))
        assert s.x is None

    def test_set_hp(self):
        s = State(substance='water')
        s.hp = Q_(1061602.391543017, 'J/kg'), Q_(101325., 'Pa')
        assert isclose_quant(s.T, Q_(373.1242958476843, 'K'))
        assert isclose_quant(s.p, Q_(101325., 'Pa'))
        assert isclose_quant(s.hp[0], Q_(1061602.391543017, 'J/kg'))
        assert isclose_quant(s.hp[1], Q_(101325., 'Pa'))
        assert isclose_quant(s.u, Q_(1013250, 'J/kg'))
        assert isclose_quant(s.s, Q_(3028.9867985920914, 'J/(kg*K)'))
        assert isclose_quant(s.v, Q_(0.4772010021515822, 'm**3/kg'))
        assert isclose_quant(s.h, Q_(1061602.391543017, 'J/kg'))
        assert isclose_quant(s.x, Q_(0.28475636946248034, 'dimensionless'))
        s.hp = Q_(3336406.139862406, 'J/kg'), Q_(101325., 'Pa')
        assert isclose_quant(s.T, Q_(700.9882316847855, 'K'))
        assert isclose_quant(s.p, Q_(101325., 'Pa'))
        assert isclose_quant(s.hp[0], Q_(3336406.139862406, 'J/kg'))
        assert isclose_quant(s.hp[1], Q_(101325., 'Pa'))
        assert isclose_quant(s.u, Q_(3013250, 'J/kg'))
        assert isclose_quant(s.s, Q_(8623.283568815832, 'J/(kg*K)'))
        assert isclose_quant(s.v, Q_(3.189303132125469, 'm**3/kg'))
        assert isclose_quant(s.h, Q_(3336406.139862406, 'J/kg'))
        assert s.x is None

    def test_set_px(self):
        s = State(substance='water')
        s.px = Q_(101325., 'Pa'), Q_(0.28475636946248034, 'dimensionless')
        assert isclose_quant(s.T, Q_(373.1242958476843, 'K'))
        assert isclose_quant(s.p, Q_(101325., 'Pa'))
        assert isclose_quant(s.px[0], Q_(101325., 'Pa'))
        assert isclose_quant(s.px[1], Q_(0.28475636946248034, 'dimensionless'))
        assert isclose_quant(s.u, Q_(1013250., 'J/kg'))
        assert isclose_quant(s.s, Q_(3028.9867985920914, 'J/(kg*K)'))
        assert isclose_quant(s.v, Q_(0.4772010021515822, 'm**3/kg'))
        assert isclose_quant(s.h, Q_(1061602.391543017, 'J/kg'))
        assert isclose_quant(s.x, Q_(0.28475636946248034, 'dimensionless'))

    def test_set_xp(self):
        s = State(substance='water')
        s.xp = Q_(0.28475636946248034, 'dimensionless'), Q_(101325., 'Pa')
        assert isclose_quant(s.T, Q_(373.1242958476843, 'K'))
        assert isclose_quant(s.p, Q_(101325., 'Pa'))
        assert isclose_quant(s.xp[0], Q_(0.28475636946248034, 'dimensionless'))
        assert isclose_quant(s.xp[1], Q_(101325., 'Pa'))
        assert isclose_quant(s.u, Q_(1013250, 'J/kg'))
        assert isclose_quant(s.s, Q_(3028.9867985920914, 'J/(kg*K)'))
        assert isclose_quant(s.v, Q_(0.4772010021515822, 'm**3/kg'))
        assert isclose_quant(s.h, Q_(1061602.391543017, 'J/kg'))
        assert isclose_quant(s.x, Q_(0.28475636946248034, 'dimensionless'))

    # This set of tests fails because s and u are not valid inputs for PhaseSI
    # in CoolProp 6.1.0
    @pytest.mark.xfail(strict=True, raises=StateError)
    def test_set_us(self):
        s = State(substance='water')
        s.us = Q_(1013250., 'J/kg'), Q_(3028.9867985920914, 'J/(kg*K)')
        assert isclose_quant(s.T, Q_(373.1242958476843, 'K'))
        assert isclose_quant(s.p, Q_(101325., 'Pa'))
        assert isclose_quant(s.us[0], Q_(1013250., 'J/kg'))
        assert isclose_quant(s.us[1], Q_(3028.9867985920914, 'J/(kg*K)'))
        assert isclose_quant(s.u, Q_(1013250., 'J/kg'))
        assert isclose_quant(s.s, Q_(3028.9867985920914, 'J/(kg*K)'))
        assert isclose_quant(s.v, Q_(0.4772010021515822, 'm**3/kg'))
        assert isclose_quant(s.h, Q_(1061602.391543017, 'J/kg'))
        assert isclose_quant(s.x, Q_(0.28475636946248034, 'dimensionless'))

    @pytest.mark.xfail(strict=True, raises=StateError)
    def test_set_su(self):
        s = State(substance='water')
        s.su = Q_(3028.9867985920914, 'J/(kg*K)'), Q_(1013250., 'J/kg')
        assert isclose_quant(s.T, Q_(373.1242958476843, 'K'))
        assert isclose_quant(s.p, Q_(101325., 'Pa'))
        assert isclose_quant(s.su[0], Q_(3028.9867985920914, 'J/(kg*K)'))
        assert isclose_quant(s.su[1], Q_(1013250., 'J/kg'))
        assert isclose_quant(s.u, Q_(1013250, 'J/kg'))
        assert isclose_quant(s.s, Q_(3028.9867985920914, 'J/(kg*K)'))
        assert isclose_quant(s.v, Q_(0.4772010021515822, 'm**3/kg'))
        assert isclose_quant(s.h, Q_(1061602.391543017, 'J/kg'))
        assert isclose_quant(s.x, Q_(0.28475636946248034, 'dimensionless'))
