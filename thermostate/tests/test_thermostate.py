"""
Test module for the main ThermoState code
"""
import pytest

from ..thermostate import State, StateError, Q_, isclose_quant


class TestState(object):
    """
    """
    def test_eq(self):
        st_1 = State(substance='water', T=Q_(400.0, 'K'), p=Q_(101325.0, 'Pa'))
        st_2 = State(substance='water', T=Q_(400.0, 'K'), p=Q_(101325.0, 'Pa'))
        assert st_1 == st_2
        st_2.Tp = Q_(300.0, 'K'), Q_(101325.0, 'Pa')
        assert not st_1 == st_2

    def test_comparison(self):
        st_1 = State(substance='water', T=Q_(400.0, 'K'), p=Q_(101325.0, 'Pa'))
        st_2 = State(substance='water', T=Q_(400.0, 'K'), p=Q_(101325.0, 'Pa'))
        with pytest.raises(TypeError):
            st_1 < st_2
        with pytest.raises(TypeError):
            st_1 <= st_2
        with pytest.raises(TypeError):
            st_1 > st_2
        with pytest.raises(TypeError):
            st_1 >= st_2

    def test_unit_definitions(self):
        st = State('water')
        l = st._all_props[:]
        l.extend(st._read_only_props)
        assert all([a in st._SI_units.keys() for a in l])

    def test_lowercase_input(self):
        State(substance='water')
        State(substance='r22')
        State(substance='r134a')
        State(substance='ammonia')
        State(substance='propane')
        State(substance='air')
        State(substance='isobutane')
        State(substance='carbondioxide')
        State(substance='oxygen')
        State(substance='nitrogen')

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

    def test_invalid_input_prop(self):
        with pytest.raises(ValueError):
            State(substance='water', x=Q_(0.5, 'dimensionless'), bad_prop=Q_(101325, 'Pa'))

    def test_bad_T_dimensions(self):
        with pytest.raises(StateError):
            State(substance='water', T=Q_(300., 'Pa'), p=Q_(101325., 'Pa'))

    def test_bad_p_dimensions(self):
        with pytest.raises(StateError):
            State(substance='water', T=Q_(300., 'K'), p=Q_(101325., 'K'))

    def test_bad_u_dimensions(self):
        with pytest.raises(StateError):
            State(substance='water', v=Q_(3., 'm**3/kg'), u=Q_(101325., 'K'))

    def test_bad_s_dimensions(self):
        with pytest.raises(StateError):
            State(substance='water', T=Q_(300., 'K'), s=Q_(10.1325, 'K'))

    def test_bad_v_dimensions(self):
        with pytest.raises(StateError):
            State(substance='water', T=Q_(300., 'K'), v=Q_(1.01325, 'K'))

    def test_bad_h_dimensions(self):
        with pytest.raises(StateError):
            State(substance='water', h=Q_(300., 'K'), v=Q_(1.01325, 'K'))

    def test_bad_x_dimensions(self):
        with pytest.raises(StateError):
            State(substance='water', T=Q_(300., 'K'), x=Q_(1.01325, 'K'))

    def test_TP_twophase(self):
        with pytest.raises(StateError):
            State(substance='water', T=Q_(373.1242958476844, 'K'), p=Q_(101325., 'Pa'))

    def test_bad_set_properties(self):
        s = State(substance='water')
        with pytest.raises(StateError):
            s._set_properties(['T', 'v', 'h'], [])

    def test_bad_get_property(self):
        s = State(substance='water', T=Q_(400., 'K'), p=Q_(101325., 'Pa'))
        with pytest.raises(AttributeError):
            s.bad_get

    def test_bad_property_setting(self):
        s = State(substance='water')
        with pytest.raises(AttributeError):
            # Should be lowercase p
            s.TP = Q_(400., 'K'), Q_(101325., 'Pa')

    def test_unallowed_pair(self):
        with pytest.raises(StateError):
            State(substance='water', T=Q_(400., 'K'), u=Q_(2547715.3635084038, 'J/kg'))

    def test_set_Tp(self):
        s = State(substance='water')
        s.Tp = Q_(400., 'K'), Q_(101325., 'Pa')
        assert isclose_quant(s.T, Q_(400., 'K'))
        assert isclose_quant(s.p, Q_(101325., 'Pa'))
        assert isclose_quant(s.Tp[0], Q_(400., 'K'))
        assert isclose_quant(s.Tp[1], Q_(101325., 'Pa'))
        assert isclose_quant(s.u, Q_(2547715.3635084038, 'J/kg'))
        assert isclose_quant(s.s, Q_(7496.2021523754065, 'J/(kg*K)'))
        assert isclose_quant(s.cp, Q_(2009.2902478486988, 'J/(kg*K)'))
        assert isclose_quant(s.cv, Q_(1509.1482452129906, 'J/(kg*K)'))
        assert isclose_quant(s.v, Q_(1.801983936953226, 'm**3/kg'))
        assert isclose_quant(s.h, Q_(2730301.3859201893, 'J/kg'))
        assert s.x is None
        assert s.phase == 'gas'

    def test_set_pT(self):
        s = State(substance='water')
        s.pT = Q_(101325., 'Pa'), Q_(400., 'K')
        assert isclose_quant(s.T, Q_(400., 'K'))
        assert isclose_quant(s.p, Q_(101325., 'Pa'))
        assert isclose_quant(s.pT[1], Q_(400., 'K'))
        assert isclose_quant(s.pT[0], Q_(101325., 'Pa'))
        assert isclose_quant(s.u, Q_(2547715.3635084038, 'J/kg'))
        assert isclose_quant(s.s, Q_(7496.2021523754065, 'J/(kg*K)'))
        assert isclose_quant(s.cp, Q_(2009.2902478486988, 'J/(kg*K)'))
        assert isclose_quant(s.cv, Q_(1509.1482452129906, 'J/(kg*K)'))
        assert isclose_quant(s.v, Q_(1.801983936953226, 'm**3/kg'))
        assert isclose_quant(s.h, Q_(2730301.3859201893, 'J/kg'))
        assert s.x is None
        assert s.phase == 'gas'

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
        assert isclose_quant(s.cp, Q_(2009.2902478486988, 'J/(kg*K)'))
        assert isclose_quant(s.cv, Q_(1509.1482452129906, 'J/(kg*K)'))
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
        assert isclose_quant(s.cp, Q_(2009.2902478486988, 'J/(kg*K)'))
        assert isclose_quant(s.cv, Q_(1509.1482452129906, 'J/(kg*K)'))
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
        assert isclose_quant(s.cp, Q_(2009.2902478486988, 'J/(kg*K)'))
        assert isclose_quant(s.cv, Q_(1509.1482452129906, 'J/(kg*K)'))
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
        assert isclose_quant(s.cp, Q_(2009.2902478486988, 'J/(kg*K)'))
        assert isclose_quant(s.cv, Q_(1509.1482452129906, 'J/(kg*K)'))
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
        assert isclose_quant(s.cp, Q_(2009.2902478486988, 'J/(kg*K)'))
        assert isclose_quant(s.cv, Q_(1509.1482452129906, 'J/(kg*K)'))
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
        assert isclose_quant(s.cp, Q_(2009.2902478486988, 'J/(kg*K)'))
        assert isclose_quant(s.cv, Q_(1509.1482452129906, 'J/(kg*K)'))
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
        assert isclose_quant(s.cp, Q_(2009.2902478486988, 'J/(kg*K)'))
        assert isclose_quant(s.cv, Q_(1509.1482452129906, 'J/(kg*K)'))
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
        assert isclose_quant(s.cp, Q_(2009.2902478486988, 'J/(kg*K)'))
        assert isclose_quant(s.cv, Q_(1509.1482452129906, 'J/(kg*K)'))
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
        assert isclose_quant(s.cp, Q_(4056.471547685226, 'J/(kg*K)'))
        assert isclose_quant(s.cv, Q_(2913.7307270395363, 'J/(kg*K)'))
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
        assert isclose_quant(s.cp, Q_(4056.471547685226, 'J/(kg*K)'))
        assert isclose_quant(s.cv, Q_(2913.7307270395363, 'J/(kg*K)'))
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
        assert isclose_quant(s.cp, Q_(4056.471547685226, 'J/(kg*K)'))
        assert isclose_quant(s.cv, Q_(2913.7307270395363, 'J/(kg*K)'))
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
        assert isclose_quant(s.cp, Q_(4056.471547685226, 'J/(kg*K)'))
        assert isclose_quant(s.cv, Q_(2913.7307270395363, 'J/(kg*K)'))
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

    def test_set_uv(self):
        s = State(substance='water')
        s.uv = Q_(1013250., 'J/kg'), Q_(0.4772010021515822, 'm**3/kg')
        assert isclose_quant(s.T, Q_(373.1242958476843, 'K'))
        assert isclose_quant(s.p, Q_(101325., 'Pa'))
        assert isclose_quant(s.uv[0], Q_(1013250., 'J/kg'))
        assert isclose_quant(s.uv[1], Q_(0.4772010021515822, 'm**3/kg'))
        assert isclose_quant(s.u, Q_(1013250., 'J/kg'))
        assert isclose_quant(s.s, Q_(3028.9867985920914, 'J/(kg*K)'))
        assert isclose_quant(s.v, Q_(0.4772010021515822, 'm**3/kg'))
        assert isclose_quant(s.h, Q_(1061602.391543017, 'J/kg'))
        assert isclose_quant(s.x, Q_(0.28475636946248034, 'dimensionless'))

    def test_set_vu(self):
        s = State(substance='water')
        s.vu = Q_(0.4772010021515822, 'm**3/kg'), Q_(1013250., 'J/kg')
        assert isclose_quant(s.T, Q_(373.1242958476843, 'K'))
        assert isclose_quant(s.p, Q_(101325., 'Pa'))
        assert isclose_quant(s.vu[0], Q_(0.4772010021515822, 'm**3/kg'))
        assert isclose_quant(s.vu[1], Q_(1013250., 'J/kg'))
        assert isclose_quant(s.u, Q_(1013250, 'J/kg'))
        assert isclose_quant(s.s, Q_(3028.9867985920914, 'J/(kg*K)'))
        assert isclose_quant(s.v, Q_(0.4772010021515822, 'm**3/kg'))
        assert isclose_quant(s.h, Q_(1061602.391543017, 'J/kg'))
        assert isclose_quant(s.x, Q_(0.28475636946248034, 'dimensionless'))

    def test_set_sv(self):
        s = State(substance='water')
        s.sv = Q_(3028.9867985920914, 'J/(kg*K)'), Q_(0.4772010021515822, 'm**3/kg')
        assert isclose_quant(s.T, Q_(373.1242958476843, 'K'))
        assert isclose_quant(s.p, Q_(101325., 'Pa'))
        assert isclose_quant(s.sv[0], Q_(3028.9867985920914, 'J/(kg*K)'))
        assert isclose_quant(s.sv[1], Q_(0.4772010021515822, 'm**3/kg'))
        assert isclose_quant(s.u, Q_(1013250., 'J/kg'))
        assert isclose_quant(s.s, Q_(3028.9867985920914, 'J/(kg*K)'))
        assert isclose_quant(s.v, Q_(0.4772010021515822, 'm**3/kg'))
        assert isclose_quant(s.h, Q_(1061602.391543017, 'J/kg'))
        assert isclose_quant(s.x, Q_(0.28475636946248034, 'dimensionless'))

    def test_set_vs(self):
        s = State(substance='water')
        s.vs = Q_(0.4772010021515822, 'm**3/kg'), Q_(3028.9867985920914, 'J/(kg*K)')
        assert isclose_quant(s.T, Q_(373.1242958476843, 'K'))
        assert isclose_quant(s.p, Q_(101325., 'Pa'))
        assert isclose_quant(s.vs[0], Q_(0.4772010021515822, 'm**3/kg'))
        assert isclose_quant(s.vs[1], Q_(3028.9867985920914, 'J/(kg*K)'))
        assert isclose_quant(s.u, Q_(1013250, 'J/kg'))
        assert isclose_quant(s.s, Q_(3028.9867985920914, 'J/(kg*K)'))
        assert isclose_quant(s.v, Q_(0.4772010021515822, 'm**3/kg'))
        assert isclose_quant(s.h, Q_(1061602.391543017, 'J/kg'))
        assert isclose_quant(s.x, Q_(0.28475636946248034, 'dimensionless'))

    def test_set_sh(self):
        s = State(substance='water')
        s.sh = Q_(3028.9867985920914, 'J/(kg*K)'), Q_(1061602.391543017, 'J/kg')
        assert isclose_quant(s.T, Q_(373.1242958476843, 'K'))
        assert isclose_quant(s.p, Q_(101325., 'Pa'))
        assert isclose_quant(s.sh[0], Q_(3028.9867985920914, 'J/(kg*K)'))
        assert isclose_quant(s.sh[1], Q_(1061602.391543017, 'J/kg'))
        assert isclose_quant(s.u, Q_(1013250., 'J/kg'))
        assert isclose_quant(s.s, Q_(3028.9867985920914, 'J/(kg*K)'))
        assert isclose_quant(s.v, Q_(0.4772010021515822, 'm**3/kg'))
        assert isclose_quant(s.h, Q_(1061602.391543017, 'J/kg'))
        assert isclose_quant(s.x, Q_(0.28475636946248034, 'dimensionless'))

    def test_set_hs(self):
        s = State(substance='water')
        s.hs = Q_(1061602.391543017, 'J/kg'), Q_(3028.9867985920914, 'J/(kg*K)')
        assert isclose_quant(s.T, Q_(373.1242958476843, 'K'))
        assert isclose_quant(s.p, Q_(101325., 'Pa'))
        assert isclose_quant(s.hs[0], Q_(1061602.391543017, 'J/kg'))
        assert isclose_quant(s.hs[1], Q_(3028.9867985920914, 'J/(kg*K)'))
        assert isclose_quant(s.u, Q_(1013250, 'J/kg'))
        assert isclose_quant(s.s, Q_(3028.9867985920914, 'J/(kg*K)'))
        assert isclose_quant(s.v, Q_(0.4772010021515822, 'm**3/kg'))
        assert isclose_quant(s.h, Q_(1061602.391543017, 'J/kg'))
        assert isclose_quant(s.x, Q_(0.28475636946248034, 'dimensionless'))

    def test_set_vh(self):
        s = State(substance='water')
        s.vh = Q_(0.4772010021515822, 'm**3/kg'), Q_(1061602.391543017, 'J/kg')
        assert isclose_quant(s.T, Q_(373.1242958476843, 'K'))
        assert isclose_quant(s.p, Q_(101325., 'Pa'))
        assert isclose_quant(s.vh[0], Q_(0.4772010021515822, 'm**3/kg'))
        assert isclose_quant(s.vh[1], Q_(1061602.391543017, 'J/kg'))
        assert isclose_quant(s.u, Q_(1013250., 'J/kg'))
        assert isclose_quant(s.s, Q_(3028.9867985920914, 'J/(kg*K)'))
        assert isclose_quant(s.v, Q_(0.4772010021515822, 'm**3/kg'))
        assert isclose_quant(s.h, Q_(1061602.391543017, 'J/kg'))
        assert isclose_quant(s.x, Q_(0.28475636946248034, 'dimensionless'))

    def test_set_hv(self):
        s = State(substance='water')
        s.hv = Q_(1061602.391543017, 'J/kg'), Q_(0.4772010021515822, 'm**3/kg')
        assert isclose_quant(s.T, Q_(373.1242958476843, 'K'))
        assert isclose_quant(s.p, Q_(101325., 'Pa'))
        assert isclose_quant(s.hv[0], Q_(1061602.391543017, 'J/kg'))
        assert isclose_quant(s.hv[1], Q_(0.4772010021515822, 'm**3/kg'))
        assert isclose_quant(s.u, Q_(1013250, 'J/kg'))
        assert isclose_quant(s.s, Q_(3028.9867985920914, 'J/(kg*K)'))
        assert isclose_quant(s.v, Q_(0.4772010021515822, 'm**3/kg'))
        assert isclose_quant(s.h, Q_(1061602.391543017, 'J/kg'))
        assert isclose_quant(s.x, Q_(0.28475636946248034, 'dimensionless'))
