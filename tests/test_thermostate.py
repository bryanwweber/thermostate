"""Test module for the main ThermoState code."""
import pytest
import numpy as np

from thermostate import State, Q_, set_default_units
from thermostate.thermostate import StateError


class TestState(object):
    """Test the functions of the State object."""

    def test_eq(self):
        """Test equality comparison of states.

        States are equal when their properties are equal and the substances are the
        same.
        """
        st_1 = State(substance="water", T=Q_(400.0, "K"), p=Q_(101325.0, "Pa"))
        st_2 = State(substance="water", T=Q_(400.0, "K"), p=Q_(101325.0, "Pa"))
        assert st_1 == st_2

    def test_eq_not_two_states(self):
        """Test that comparing a state with something else doesn't work."""
        assert not State(substance="water") == 3
        assert not 3 == State(substance="water")

    def test_not_eq(self):
        """States are not equal when properties are not equal."""
        st_1 = State(substance="water", T=Q_(400.0, "K"), p=Q_(101325.0, "Pa"))
        st_2 = State(substance="water", T=Q_(300.0, "K"), p=Q_(101325.0, "Pa"))
        assert not st_1 == st_2

    def test_not_eq_sub(self):
        """States are not equal when substances are not the same."""
        st_1 = State(substance="water", T=Q_(400.0, "K"), p=Q_(101325.0, "Pa"))
        st_2 = State(substance="ammonia", T=Q_(400.0, "K"), p=Q_(101325.0, "Pa"))
        assert not st_1 == st_2

    def test_comparison(self):
        """Greater/less than comparisons are not supported."""
        st_1 = State(substance="water", T=Q_(400.0, "K"), p=Q_(101325.0, "Pa"))
        st_2 = State(substance="water", T=Q_(400.0, "K"), p=Q_(101325.0, "Pa"))
        with pytest.raises(TypeError):
            st_1 < st_2
        with pytest.raises(TypeError):
            st_1 <= st_2
        with pytest.raises(TypeError):
            st_1 > st_2
        with pytest.raises(TypeError):
            st_1 >= st_2

    def test_unit_definitions(self):
        """All of the properties should have units defined."""
        st = State("water")
        props = st._all_props.union(st._read_only_props) - {"phase"}  # type: ignore
        assert all([a in st._SI_units.keys() for a in props])  # type: ignore

    def test_lowercase_input(self):
        """Substances should be able to be specified with lowercase letters."""
        State(substance="water")
        State(substance="r22")
        State(substance="r134a")
        State(substance="ammonia")
        State(substance="propane")
        State(substance="air")
        State(substance="isobutane")
        State(substance="carbondioxide")
        State(substance="oxygen")
        State(substance="nitrogen")

    def test_bad_substance(self):
        """A substance not in the approved list should raise a ValueError."""
        with pytest.raises(ValueError):
            State(substance="bad substance")

    def test_too_many_props(self):
        """Specifying too many properties should raise a ValueError."""
        with pytest.raises(ValueError):
            State(
                substance="water",
                T=Q_(300, "K"),
                p=Q_(101325, "Pa"),
                u=Q_(100, "kJ/kg"),
            )

    def test_too_few_props(self):
        """Specifying too few properties should raise a value error."""
        with pytest.raises(ValueError):
            State(substance="water", T=Q_(300, "K"))

    def test_negative_temperature(self):
        """Negative absolute temperatures should raise a StateError."""
        with pytest.raises(StateError):
            State(substance="water", T=Q_(-100, "K"), p=Q_(101325, "Pa"))

    def test_negative_pressure(self):
        """Negative absolute pressures should raise a StateError."""
        with pytest.raises(StateError):
            State(substance="water", T=Q_(300, "K"), p=Q_(-101325, "Pa"))

    def test_negative_volume(self):
        """Negative absolute specific volumes should raise a StateError."""
        with pytest.raises(StateError):
            State(substance="water", T=Q_(300, "K"), v=Q_(-10.13, "m**3/kg"))

    def test_quality_lt_zero(self):
        """Vapor qualities less than 0.0 should raise a StateError."""
        with pytest.raises(StateError):
            State(substance="water", x=Q_(-1.0, "dimensionless"), p=Q_(101325, "Pa"))

    def test_quality_gt_one(self):
        """Vapor qualities greater than 1.0 should raise a StateError."""
        with pytest.raises(StateError):
            State(substance="water", x=Q_(2.0, "dimensionless"), p=Q_(101325, "Pa"))

    def test_invalid_input_prop(self):
        """Invalid input properties should raise a ValueError."""
        with pytest.raises(ValueError):
            State(
                substance="water", x=Q_(0.5, "dimensionless"), bad_prop=Q_(101325, "Pa")
            )

    @pytest.mark.parametrize("prop", ["T", "p", "v", "u", "s", "h"])
    def test_bad_dimensions(self, prop: str):
        """Setting bad dimensions for the input property raises a StateError."""
        kwargs = {prop: Q_(1.0, "dimensionless")}
        if prop == "v":
            kwargs["T"] = Q_(300.0, "K")
        else:
            kwargs["v"] = Q_(1.0, "m**3/kg")
        with pytest.raises(StateError):
            State(substance="water", **kwargs)

    def test_bad_x_dimensions(self):
        """Setting bad dimensions for quality raises a StateError.

        Must be done in a separate test because the "dimensionless"
        sentinel value used in the other test is actually the correct
        dimension for quality.
        """
        with pytest.raises(StateError):
            State(substance="water", T=Q_(300.0, "K"), x=Q_(1.01325, "K"))

    def test_TP_twophase(self):
        """Setting a two-phase mixture with T and p should raise a StateError."""
        with pytest.raises(StateError):
            State(substance="water", T=Q_(373.1242958476844, "K"), p=Q_(101325.0, "Pa"))

    def test_bad_get_property(self):
        """Accessing attributes that aren't one of the properties or pairs raises."""
        s = State(substance="water", T=Q_(400.0, "K"), p=Q_(101325.0, "Pa"))
        with pytest.raises(AttributeError):
            s.bad_get

    def test_bad_property_setting(self):
        """Regression test that pressure is lowercase p, not uppercase."""
        s = State(substance="water")
        with pytest.raises(AttributeError):
            # Should be lowercase p
            s.TP = Q_(400.0, "K"), Q_(101325.0, "Pa")

    def test_label_cannot_be_converted_to_string(self):
        """Trying to set a label that can't be converted to a string is a TypeError."""

        class NoStr:
            def __str__(self) -> str:
                raise NotImplementedError

        with pytest.raises(TypeError, match="The given label"):
            State("water", label=NoStr())

    def test_unsupported_pair(self):
        """Trying to set with an unsupported property pair raises a StateError."""
        with pytest.raises(StateError, match="The pair of input"):
            State("water", T=Q_(100.0, "degC"), u=Q_(1e6, "J/kg"))

    def test_set_Tp(self):
        """Set a pair of properties of the State and check the properties.

        Also works as a functional/regression test of CoolProp.
        """
        s = State(substance="water")
        s.Tp = Q_(400.0, "K"), Q_(101325.0, "Pa")
        # Pylance does not support NumPy ufuncs
        assert np.isclose(s.T, Q_(400.0, "K"))  # type: ignore
        assert np.isclose(s.p, Q_(101325.0, "Pa"))  # type: ignore
        assert np.isclose(s.Tp[0], Q_(400.0, "K"))  # type: ignore
        assert np.isclose(s.Tp[1], Q_(101325.0, "Pa"))  # type: ignore
        assert np.isclose(s.u, Q_(2547715.3635084038, "J/kg"))  # type: ignore
        assert np.isclose(s.s, Q_(7496.2021523754065, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.cp, Q_(2009.2902478486988, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.cv, Q_(1509.1482452129906, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.v, Q_(1.801983936953226, "m**3/kg"))  # type: ignore
        assert np.isclose(s.h, Q_(2730301.3859201893, "J/kg"))  # type: ignore
        assert s.x is None
        assert s.phase == "gas"

    def test_set_pT(self):
        """Set a pair of properties of the State and check the properties.

        Also works as a functional/regression test of CoolProp.
        """
        s = State(substance="water")
        s.pT = Q_(101325.0, "Pa"), Q_(400.0, "K")
        # Pylance does not support NumPy ufuncs
        assert np.isclose(s.T, Q_(400.0, "K"))  # type: ignore
        assert np.isclose(s.p, Q_(101325.0, "Pa"))  # type: ignore
        assert np.isclose(s.pT[1], Q_(400.0, "K"))  # type: ignore
        assert np.isclose(s.pT[0], Q_(101325.0, "Pa"))  # type: ignore
        assert np.isclose(s.u, Q_(2547715.3635084038, "J/kg"))  # type: ignore
        assert np.isclose(s.s, Q_(7496.2021523754065, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.cp, Q_(2009.2902478486988, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.cv, Q_(1509.1482452129906, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.v, Q_(1.801983936953226, "m**3/kg"))  # type: ignore
        assert np.isclose(s.h, Q_(2730301.3859201893, "J/kg"))  # type: ignore
        assert s.x is None
        assert s.phase == "gas"

    # This set of tests fails because T and u are not valid inputs for PhaseSI
    # in CoolProp 6.1.0
    @pytest.mark.xfail(strict=True, raises=StateError)
    def test_set_uT(self):
        """Set a pair of properties of the State and check the properties.

        Also works as a functional/regression test of CoolProp.
        """
        s = State(substance="water")
        s.uT = Q_(2547715.3635084038, "J/kg"), Q_(400.0, "K")
        # Pylance does not support NumPy ufuncs
        assert np.isclose(s.T, Q_(400.0, "K"))  # type: ignore
        assert np.isclose(s.p, Q_(101325.0, "Pa"))  # type: ignore
        assert np.isclose(s.uT[1], Q_(400.0, "K"))  # type: ignore
        assert np.isclose(s.uT[0], Q_(2547715.3635084038, "J/kg"))  # type: ignore
        assert np.isclose(s.u, Q_(2547715.3635084038, "J/kg"))  # type: ignore
        assert np.isclose(s.s, Q_(7496.2021523754065, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.cp, Q_(2009.2902478486988, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.cv, Q_(1509.1482452129906, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.v, Q_(1.801983936953226, "m**3/kg"))  # type: ignore
        assert np.isclose(s.h, Q_(2730301.3859201893, "J/kg"))  # type: ignore
        assert s.x is None

    @pytest.mark.xfail(strict=True, raises=StateError)
    def test_set_Tu(self):
        """Set a pair of properties of the State and check the properties.

        Also works as a functional/regression test of CoolProp.
        """
        s = State(substance="water")
        s.Tu = Q_(400.0, "K"), Q_(2547715.3635084038, "J/kg")
        # Pylance does not support NumPy ufuncs
        assert np.isclose(s.T, Q_(400.0, "K"))  # type: ignore
        assert np.isclose(s.p, Q_(101325.0, "Pa"))  # type: ignore
        assert np.isclose(s.Tu[0], Q_(400.0, "K"))  # type: ignore
        assert np.isclose(s.Tu[1], Q_(2547715.3635084038, "J/kg"))  # type: ignore
        assert np.isclose(s.u, Q_(2547715.3635084038, "J/kg"))  # type: ignore
        assert np.isclose(s.s, Q_(7496.2021523754065, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.cp, Q_(2009.2902478486988, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.cv, Q_(1509.1482452129906, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.v, Q_(1.801983936953226, "m**3/kg"))  # type: ignore
        assert np.isclose(s.h, Q_(2730301.3859201893, "J/kg"))  # type: ignore
        assert s.x is None

    # This set of tests fails because T and h are not valid inputs for PhaseSI
    # in CoolProp 6.1.0
    @pytest.mark.xfail(strict=True, raises=StateError)
    def test_set_hT(self):
        """Set a pair of properties of the State and check the properties.

        Also works as a functional/regression test of CoolProp.
        """
        s = State(substance="water")
        s.hT = Q_(2730301.3859201893, "J/kg"), Q_(400.0, "K")
        # Pylance does not support NumPy ufuncs
        assert np.isclose(s.T, Q_(400.0, "K"))  # type: ignore
        assert np.isclose(s.p, Q_(101325.0, "Pa"))  # type: ignore
        assert np.isclose(s.hT[1], Q_(400.0, "K"))  # type: ignore
        assert np.isclose(s.hT[0], Q_(2730301.3859201893, "J/kg"))  # type: ignore
        assert np.isclose(s.u, Q_(2547715.3635084038, "J/kg"))  # type: ignore
        assert np.isclose(s.s, Q_(7496.2021523754065, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.cp, Q_(2009.2902478486988, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.cv, Q_(1509.1482452129906, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.v, Q_(1.801983936953226, "m**3/kg"))  # type: ignore
        assert np.isclose(s.h, Q_(2730301.3859201893, "J/kg"))  # type: ignore
        assert s.x is None

    @pytest.mark.xfail(strict=True, raises=StateError)
    def test_set_Th(self):
        """Set a pair of properties of the State and check the properties.

        Also works as a functional/regression test of CoolProp.
        """
        s = State(substance="water")
        s.Th = Q_(400.0, "K"), Q_(2730301.3859201893, "J/kg")
        # Pylance does not support NumPy ufuncs
        assert np.isclose(s.T, Q_(400.0, "K"))  # type: ignore
        assert np.isclose(s.p, Q_(101325.0, "Pa"))  # type: ignore
        assert np.isclose(s.Th[0], Q_(400.0, "K"))  # type: ignore
        assert np.isclose(s.Th[1], Q_(2730301.3859201893, "J/kg"))  # type: ignore
        assert np.isclose(s.u, Q_(2547715.3635084038, "J/kg"))  # type: ignore
        assert np.isclose(s.s, Q_(7496.2021523754065, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.cp, Q_(2009.2902478486988, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.cv, Q_(1509.1482452129906, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.v, Q_(1.801983936953226, "m**3/kg"))  # type: ignore
        assert np.isclose(s.h, Q_(2730301.3859201893, "J/kg"))  # type: ignore
        assert s.x is None

    # This set of tests fails because x and h are not valid inputs for PhaseSI
    # in CoolProp 6.3.0
    @pytest.mark.xfail(strict=True, raises=StateError)
    def test_set_xh(self):
        """Set a pair of properties of the State and check the properties.

        Also works as a functional/regression test of CoolProp.
        """
        s = State(substance="water")
        s.xh = Q_(0.5, "dimensionless"), Q_(1624328.2430353598, "J/kg")
        # Pylance does not support NumPy ufuncs
        assert np.isclose(s.T, Q_(400.0, "K"))  # type: ignore
        assert np.isclose(s.p, Q_(245769.34557103913, "Pa"))  # type: ignore
        assert np.isclose(s.xT[1], Q_(400.0, "K"))  # type: ignore
        assert np.isclose(s.xT[0], Q_(0.5, "dimensionless"))  # type: ignore
        assert np.isclose(s.u, Q_(1534461.5163075812, "J/kg"))  # type: ignore
        assert np.isclose(s.s, Q_(4329.703956664546, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.cp, Q_(4056.471547685226, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.cv, Q_(2913.7307270395363, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.v, Q_(0.3656547423394701, "m**3/kg"))  # type: ignore
        assert np.isclose(s.h, Q_(1624328.2430353598, "J/kg"))  # type: ignore
        assert np.isclose(s.x, Q_(0.5, "dimensionless"))  # type: ignore

    # This set of tests fails because x and h are not valid inputs for PhaseSI
    # in CoolProp 6.3.0
    @pytest.mark.xfail(strict=True, raises=StateError)
    def test_set_hx(self):
        """Set a pair of properties of the State and check the properties.

        Also works as a functional/regression test of CoolProp.
        """
        s = State(substance="water")
        s.hx = Q_(1624328.2430353598, "J/kg"), Q_(0.5, "dimensionless")
        # Pylance does not support NumPy ufuncs
        assert np.isclose(s.T, Q_(400.0, "K"))  # type: ignore
        assert np.isclose(s.p, Q_(245769.34557103913, "Pa"))  # type: ignore
        assert np.isclose(s.xT[1], Q_(400.0, "K"))  # type: ignore
        assert np.isclose(s.xT[0], Q_(0.5, "dimensionless"))  # type: ignore
        assert np.isclose(s.u, Q_(1534461.5163075812, "J/kg"))  # type: ignore
        assert np.isclose(s.s, Q_(4329.703956664546, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.cp, Q_(4056.471547685226, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.cv, Q_(2913.7307270395363, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.v, Q_(0.3656547423394701, "m**3/kg"))  # type: ignore
        assert np.isclose(s.h, Q_(1624328.2430353598, "J/kg"))  # type: ignore
        assert np.isclose(s.x, Q_(0.5, "dimensionless"))  # type: ignore

    def test_set_sT(self):
        """Set a pair of properties of the State and check the properties.

        Also works as a functional/regression test of CoolProp.
        """
        s = State(substance="water")
        s.sT = Q_(7496.2021523754065, "J/(kg*K)"), Q_(400.0, "K")
        # Pylance does not support NumPy ufuncs
        assert np.isclose(s.T, Q_(400.0, "K"))  # type: ignore
        assert np.isclose(s.p, Q_(101325.0, "Pa"))  # type: ignore
        assert np.isclose(s.sT[1], Q_(400.0, "K"))  # type: ignore
        assert np.isclose(s.sT[0], Q_(7496.2021523754065, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.u, Q_(2547715.3635084038, "J/kg"))  # type: ignore
        assert np.isclose(s.s, Q_(7496.2021523754065, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.cp, Q_(2009.2902478486988, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.cv, Q_(1509.1482452129906, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.v, Q_(1.801983936953226, "m**3/kg"))  # type: ignore
        assert np.isclose(s.h, Q_(2730301.3859201893, "J/kg"))  # type: ignore
        assert s.x is None

    def test_set_Ts(self):
        """Set a pair of properties of the State and check the properties.

        Also works as a functional/regression test of CoolProp.
        """
        s = State(substance="water")
        s.Ts = Q_(400.0, "K"), Q_(7496.2021523754065, "J/(kg*K)")
        # Pylance does not support NumPy ufuncs
        assert np.isclose(s.T, Q_(400.0, "K"))  # type: ignore
        assert np.isclose(s.p, Q_(101325.0, "Pa"))  # type: ignore
        assert np.isclose(s.Ts[0], Q_(400.0, "K"))  # type: ignore
        assert np.isclose(s.Ts[1], Q_(7496.2021523754065, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.u, Q_(2547715.3635084038, "J/kg"))  # type: ignore
        assert np.isclose(s.s, Q_(7496.2021523754065, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.cp, Q_(2009.2902478486988, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.cv, Q_(1509.1482452129906, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.v, Q_(1.801983936953226, "m**3/kg"))  # type: ignore
        assert np.isclose(s.h, Q_(2730301.3859201893, "J/kg"))  # type: ignore
        assert s.x is None

    def test_set_vT(self):
        """Set a pair of properties of the State and check the properties.

        Also works as a functional/regression test of CoolProp.
        """
        s = State(substance="water")
        s.vT = Q_(1.801983936953226, "m**3/kg"), Q_(400.0, "K")
        # Pylance does not support NumPy ufuncs
        assert np.isclose(s.T, Q_(400.0, "K"))  # type: ignore
        assert np.isclose(s.p, Q_(101325.0, "Pa"))  # type: ignore
        assert np.isclose(s.vT[1], Q_(400.0, "K"))  # type: ignore
        assert np.isclose(s.vT[0], Q_(1.801983936953226, "m**3/kg"))  # type: ignore
        assert np.isclose(s.u, Q_(2547715.3635084038, "J/kg"))  # type: ignore
        assert np.isclose(s.s, Q_(7496.2021523754065, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.cp, Q_(2009.2902478486988, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.cv, Q_(1509.1482452129906, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.v, Q_(1.801983936953226, "m**3/kg"))  # type: ignore
        assert np.isclose(s.h, Q_(2730301.3859201893, "J/kg"))  # type: ignore
        assert s.x is None

    def test_set_Tv(self):
        """Set a pair of properties of the State and check the properties.

        Also works as a functional/regression test of CoolProp.
        """
        s = State(substance="water")
        s.Tv = Q_(400.0, "K"), Q_(1.801983936953226, "m**3/kg")
        # Pylance does not support NumPy ufuncs
        assert np.isclose(s.T, Q_(400.0, "K"))  # type: ignore
        assert np.isclose(s.p, Q_(101325.0, "Pa"))  # type: ignore
        assert np.isclose(s.Tv[0], Q_(400.0, "K"))  # type: ignore
        assert np.isclose(s.Tv[1], Q_(1.801983936953226, "m**3/kg"))  # type: ignore
        assert np.isclose(s.u, Q_(2547715.3635084038, "J/kg"))  # type: ignore
        assert np.isclose(s.s, Q_(7496.2021523754065, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.cp, Q_(2009.2902478486988, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.cv, Q_(1509.1482452129906, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.v, Q_(1.801983936953226, "m**3/kg"))  # type: ignore
        assert np.isclose(s.h, Q_(2730301.3859201893, "J/kg"))  # type: ignore
        assert s.x is None

    def test_set_xT(self):
        """Set a pair of properties of the State and check the properties.

        Also works as a functional/regression test of CoolProp.
        """
        s = State(substance="water")
        s.xT = Q_(0.5, "dimensionless"), Q_(400.0, "K")
        # Pylance does not support NumPy ufuncs
        assert np.isclose(s.T, Q_(400.0, "K"))  # type: ignore
        assert np.isclose(s.p, Q_(245769.34557103913, "Pa"))  # type: ignore
        assert np.isclose(s.xT[1], Q_(400.0, "K"))  # type: ignore
        assert np.isclose(s.xT[0], Q_(0.5, "dimensionless"))  # type: ignore
        assert np.isclose(s.u, Q_(1534461.5163075812, "J/kg"))  # type: ignore
        assert np.isclose(s.s, Q_(4329.703956664546, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.cp, Q_(4056.471547685226, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.cv, Q_(2913.7307270395363, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.v, Q_(0.3656547423394701, "m**3/kg"))  # type: ignore
        assert np.isclose(s.h, Q_(1624328.2430353598, "J/kg"))  # type: ignore
        assert np.isclose(s.x, Q_(0.5, "dimensionless"))  # type: ignore
        s.xT = Q_(50, "percent"), Q_(400.0, "K")
        assert np.isclose(s.T, Q_(400.0, "K"))  # type: ignore
        assert np.isclose(s.p, Q_(245769.34557103913, "Pa"))  # type: ignore
        assert np.isclose(s.xT[1], Q_(400.0, "K"))  # type: ignore
        assert np.isclose(s.xT[0], Q_(0.5, "dimensionless"))  # type: ignore
        assert np.isclose(s.u, Q_(1534461.5163075812, "J/kg"))  # type: ignore
        assert np.isclose(s.s, Q_(4329.703956664546, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.cp, Q_(4056.471547685226, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.cv, Q_(2913.7307270395363, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.v, Q_(0.3656547423394701, "m**3/kg"))  # type: ignore
        assert np.isclose(s.h, Q_(1624328.2430353598, "J/kg"))  # type: ignore
        assert np.isclose(s.x, Q_(0.5, "dimensionless"))  # type: ignore

    def test_set_Tx(self):
        """Set a pair of properties of the State and check the properties.

        Also works as a functional/regression test of CoolProp.
        """
        s = State(substance="water")
        s.Tx = Q_(400.0, "K"), Q_(0.5, "dimensionless")
        # Pylance does not support NumPy ufuncs
        assert np.isclose(s.T, Q_(400.0, "K"))  # type: ignore
        assert np.isclose(s.p, Q_(245769.34557103913, "Pa"))  # type: ignore
        assert np.isclose(s.Tx[0], Q_(400.0, "K"))  # type: ignore
        assert np.isclose(s.Tx[1], Q_(0.5, "dimensionless"))  # type: ignore
        assert np.isclose(s.u, Q_(1534461.5163075812, "J/kg"))  # type: ignore
        assert np.isclose(s.s, Q_(4329.703956664546, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.cp, Q_(4056.471547685226, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.cv, Q_(2913.7307270395363, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.v, Q_(0.3656547423394701, "m**3/kg"))  # type: ignore
        assert np.isclose(s.h, Q_(1624328.2430353598, "J/kg"))  # type: ignore
        assert np.isclose(s.x, Q_(0.5, "dimensionless"))  # type: ignore
        s.Tx = Q_(400.0, "K"), Q_(50, "percent")
        assert np.isclose(s.T, Q_(400.0, "K"))  # type: ignore
        assert np.isclose(s.p, Q_(245769.34557103913, "Pa"))  # type: ignore
        assert np.isclose(s.Tx[0], Q_(400.0, "K"))  # type: ignore
        assert np.isclose(s.Tx[1], Q_(0.5, "dimensionless"))  # type: ignore
        assert np.isclose(s.u, Q_(1534461.5163075812, "J/kg"))  # type: ignore
        assert np.isclose(s.s, Q_(4329.703956664546, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.cp, Q_(4056.471547685226, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.cv, Q_(2913.7307270395363, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.v, Q_(0.3656547423394701, "m**3/kg"))  # type: ignore
        assert np.isclose(s.h, Q_(1624328.2430353598, "J/kg"))  # type: ignore
        assert np.isclose(s.x, Q_(0.5, "dimensionless"))  # type: ignore

    def test_set_pu(self):
        """Set a pair of properties of the State and check the properties.

        Also works as a functional/regression test of CoolProp.
        """
        s = State(substance="water")
        s.pu = Q_(101325.0, "Pa"), Q_(1013250.0, "J/kg")
        # Pylance does not support NumPy ufuncs
        assert np.isclose(s.T, Q_(373.1242958476843, "K"))  # type: ignore
        assert np.isclose(s.p, Q_(101325.0, "Pa"))  # type: ignore
        assert np.isclose(s.pu[0], Q_(101325.0, "Pa"))  # type: ignore
        assert np.isclose(s.pu[1], Q_(1013250.0, "J/kg"))  # type: ignore
        assert np.isclose(s.u, Q_(1013250.0, "J/kg"))  # type: ignore
        assert np.isclose(s.s, Q_(3028.9867985920914, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.v, Q_(0.4772010021515822, "m**3/kg"))  # type: ignore
        assert np.isclose(s.h, Q_(1061602.391543017, "J/kg"))  # type: ignore
        assert np.isclose(s.x, Q_(0.28475636946248034, "dimensionless"))  # type: ignore
        s.pu = Q_(101325.0, "Pa"), Q_(3013250.0, "J/kg")
        assert np.isclose(s.T, Q_(700.9882316847855, "K"))  # type: ignore
        assert np.isclose(s.p, Q_(101325.0, "Pa"))  # type: ignore
        assert np.isclose(s.pu[0], Q_(101325.0, "Pa"))  # type: ignore
        assert np.isclose(s.pu[1], Q_(3013250.0, "J/kg"))  # type: ignore
        assert np.isclose(s.u, Q_(3013250.0, "J/kg"))  # type: ignore
        assert np.isclose(s.s, Q_(8623.283568815832, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.v, Q_(3.189303132125469, "m**3/kg"))  # type: ignore
        assert np.isclose(s.h, Q_(3336406.139862406, "J/kg"))  # type: ignore
        assert s.x is None

    def test_set_up(self):
        """Set a pair of properties of the State and check the properties.

        Also works as a functional/regression test of CoolProp.
        """
        s = State(substance="water")
        s.up = Q_(1013250.0, "J/kg"), Q_(101325.0, "Pa")
        # Pylance does not support NumPy ufuncs
        assert np.isclose(s.T, Q_(373.1242958476843, "K"))  # type: ignore
        assert np.isclose(s.p, Q_(101325.0, "Pa"))  # type: ignore
        assert np.isclose(s.up[0], Q_(1013250.0, "J/kg"))  # type: ignore
        assert np.isclose(s.up[1], Q_(101325.0, "Pa"))  # type: ignore
        assert np.isclose(s.u, Q_(1013250, "J/kg"))  # type: ignore
        assert np.isclose(s.s, Q_(3028.9867985920914, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.v, Q_(0.4772010021515822, "m**3/kg"))  # type: ignore
        assert np.isclose(s.h, Q_(1061602.391543017, "J/kg"))  # type: ignore
        assert np.isclose(s.x, Q_(0.28475636946248034, "dimensionless"))  # type: ignore
        s.up = Q_(3013250.0, "J/kg"), Q_(101325.0, "Pa")
        assert np.isclose(s.T, Q_(700.9882316847855, "K"))  # type: ignore
        assert np.isclose(s.p, Q_(101325.0, "Pa"))  # type: ignore
        assert np.isclose(s.up[0], Q_(3013250.0, "J/kg"))  # type: ignore
        assert np.isclose(s.up[1], Q_(101325.0, "Pa"))  # type: ignore
        assert np.isclose(s.u, Q_(3013250, "J/kg"))  # type: ignore
        assert np.isclose(s.s, Q_(8623.283568815832, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.v, Q_(3.189303132125469, "m**3/kg"))  # type: ignore
        assert np.isclose(s.h, Q_(3336406.139862406, "J/kg"))  # type: ignore
        assert s.x is None

    def test_set_ps(self):
        """Set a pair of properties of the State and check the properties.

        Also works as a functional/regression test of CoolProp.
        """
        s = State(substance="water")
        s.ps = Q_(101325.0, "Pa"), Q_(3028.9867985920914, "J/(kg*K)")
        # Pylance does not support NumPy ufuncs
        assert np.isclose(s.T, Q_(373.1242958476843, "K"))  # type: ignore
        assert np.isclose(s.p, Q_(101325.0, "Pa"))  # type: ignore
        assert np.isclose(s.ps[0], Q_(101325.0, "Pa"))  # type: ignore
        assert np.isclose(s.ps[1], Q_(3028.9867985920914, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.u, Q_(1013250.0, "J/kg"))  # type: ignore
        assert np.isclose(s.s, Q_(3028.9867985920914, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.v, Q_(0.4772010021515822, "m**3/kg"))  # type: ignore
        assert np.isclose(s.h, Q_(1061602.391543017, "J/kg"))  # type: ignore
        assert np.isclose(s.x, Q_(0.28475636946248034, "dimensionless"))  # type: ignore
        s.ps = Q_(101325.0, "Pa"), Q_(8623.283568815832, "J/(kg*K)")
        assert np.isclose(s.T, Q_(700.9882316847855, "K"))  # type: ignore
        assert np.isclose(s.p, Q_(101325.0, "Pa"))  # type: ignore
        assert np.isclose(s.ps[0], Q_(101325.0, "Pa"))  # type: ignore
        assert np.isclose(s.ps[1], Q_(8623.283568815832, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.u, Q_(3013250.0, "J/kg"))  # type: ignore
        assert np.isclose(s.s, Q_(8623.283568815832, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.v, Q_(3.189303132125469, "m**3/kg"))  # type: ignore
        assert np.isclose(s.h, Q_(3336406.139862406, "J/kg"))  # type: ignore
        assert s.x is None

    def test_set_sp(self):
        """Set a pair of properties of the State and check the properties.

        Also works as a functional/regression test of CoolProp.
        """
        s = State(substance="water")
        s.sp = Q_(3028.9867985920914, "J/(kg*K)"), Q_(101325.0, "Pa")
        # Pylance does not support NumPy ufuncs
        assert np.isclose(s.T, Q_(373.1242958476843, "K"))  # type: ignore
        assert np.isclose(s.p, Q_(101325.0, "Pa"))  # type: ignore
        assert np.isclose(s.sp[0], Q_(3028.9867985920914, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.sp[1], Q_(101325.0, "Pa"))  # type: ignore
        assert np.isclose(s.u, Q_(1013250, "J/kg"))  # type: ignore
        assert np.isclose(s.s, Q_(3028.9867985920914, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.v, Q_(0.4772010021515822, "m**3/kg"))  # type: ignore
        assert np.isclose(s.h, Q_(1061602.391543017, "J/kg"))  # type: ignore
        assert np.isclose(s.x, Q_(0.28475636946248034, "dimensionless"))  # type: ignore
        s.sp = Q_(8623.283568815832, "J/(kg*K)"), Q_(101325.0, "Pa")
        assert np.isclose(s.T, Q_(700.9882316847855, "K"))  # type: ignore
        assert np.isclose(s.p, Q_(101325.0, "Pa"))  # type: ignore
        assert np.isclose(s.sp[0], Q_(8623.283568815832, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.sp[1], Q_(101325.0, "Pa"))  # type: ignore
        assert np.isclose(s.u, Q_(3013250, "J/kg"))  # type: ignore
        assert np.isclose(s.s, Q_(8623.283568815832, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.v, Q_(3.189303132125469, "m**3/kg"))  # type: ignore
        assert np.isclose(s.h, Q_(3336406.139862406, "J/kg"))  # type: ignore
        assert s.x is None

    def test_set_pv(self):
        """Set a pair of properties of the State and check the properties.

        Also works as a functional/regression test of CoolProp.
        """
        s = State(substance="water")
        s.pv = Q_(101325.0, "Pa"), Q_(0.4772010021515822, "m**3/kg")
        # Pylance does not support NumPy ufuncs
        assert np.isclose(s.T, Q_(373.1242958476843, "K"))  # type: ignore
        assert np.isclose(s.p, Q_(101325.0, "Pa"))  # type: ignore
        assert np.isclose(s.pv[0], Q_(101325.0, "Pa"))  # type: ignore
        assert np.isclose(s.pv[1], Q_(0.4772010021515822, "m**3/kg"))  # type: ignore
        assert np.isclose(s.u, Q_(1013250.0, "J/kg"))  # type: ignore
        assert np.isclose(s.s, Q_(3028.9867985920914, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.v, Q_(0.4772010021515822, "m**3/kg"))  # type: ignore
        assert np.isclose(s.h, Q_(1061602.391543017, "J/kg"))  # type: ignore
        assert np.isclose(s.x, Q_(0.28475636946248034, "dimensionless"))  # type: ignore
        s.pv = Q_(101325.0, "Pa"), Q_(3.189303132125469, "m**3/kg")
        assert np.isclose(s.T, Q_(700.9882316847855, "K"))  # type: ignore
        assert np.isclose(s.p, Q_(101325.0, "Pa"))  # type: ignore
        assert np.isclose(s.pv[0], Q_(101325.0, "Pa"))  # type: ignore
        assert np.isclose(s.pv[1], Q_(3.189303132125469, "m**3/kg"))  # type: ignore
        assert np.isclose(s.u, Q_(3013250.0, "J/kg"))  # type: ignore
        assert np.isclose(s.s, Q_(8623.283568815832, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.v, Q_(3.189303132125469, "m**3/kg"))  # type: ignore
        assert np.isclose(s.h, Q_(3336406.139862406, "J/kg"))  # type: ignore
        assert s.x is None

    def test_set_vp(self):
        """Set a pair of properties of the State and check the properties.

        Also works as a functional/regression test of CoolProp.
        """
        s = State(substance="water")
        s.vp = Q_(0.4772010021515822, "m**3/kg"), Q_(101325.0, "Pa")
        # Pylance does not support NumPy ufuncs
        assert np.isclose(s.T, Q_(373.1242958476843, "K"))  # type: ignore
        assert np.isclose(s.p, Q_(101325.0, "Pa"))  # type: ignore
        assert np.isclose(s.vp[0], Q_(0.4772010021515822, "m**3/kg"))  # type: ignore
        assert np.isclose(s.vp[1], Q_(101325.0, "Pa"))  # type: ignore
        assert np.isclose(s.u, Q_(1013250, "J/kg"))  # type: ignore
        assert np.isclose(s.s, Q_(3028.9867985920914, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.v, Q_(0.4772010021515822, "m**3/kg"))  # type: ignore
        assert np.isclose(s.h, Q_(1061602.391543017, "J/kg"))  # type: ignore
        assert np.isclose(s.x, Q_(0.28475636946248034, "dimensionless"))  # type: ignore
        s.vp = Q_(3.189303132125469, "m**3/kg"), Q_(101325.0, "Pa")
        assert np.isclose(s.T, Q_(700.9882316847855, "K"))  # type: ignore
        assert np.isclose(s.p, Q_(101325.0, "Pa"))  # type: ignore
        assert np.isclose(s.vp[0], Q_(3.189303132125469, "m**3/kg"))  # type: ignore
        assert np.isclose(s.vp[1], Q_(101325.0, "Pa"))  # type: ignore
        assert np.isclose(s.u, Q_(3013250, "J/kg"))  # type: ignore
        assert np.isclose(s.s, Q_(8623.283568815832, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.v, Q_(3.189303132125469, "m**3/kg"))  # type: ignore
        assert np.isclose(s.h, Q_(3336406.139862406, "J/kg"))  # type: ignore
        assert s.x is None

    def test_set_ph(self):
        """Set a pair of properties of the State and check the properties.

        Also works as a functional/regression test of CoolProp.
        """
        s = State(substance="water")
        s.ph = Q_(101325.0, "Pa"), Q_(1061602.391543017, "J/kg")
        # Pylance does not support NumPy ufuncs
        assert np.isclose(s.T, Q_(373.1242958476843, "K"))  # type: ignore
        assert np.isclose(s.p, Q_(101325.0, "Pa"))  # type: ignore
        assert np.isclose(s.ph[0], Q_(101325.0, "Pa"))  # type: ignore
        assert np.isclose(s.ph[1], Q_(1061602.391543017, "J/kg"))  # type: ignore
        assert np.isclose(s.u, Q_(1013250.0, "J/kg"))  # type: ignore
        assert np.isclose(s.s, Q_(3028.9867985920914, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.v, Q_(0.4772010021515822, "m**3/kg"))  # type: ignore
        assert np.isclose(s.h, Q_(1061602.391543017, "J/kg"))  # type: ignore
        assert np.isclose(s.x, Q_(0.28475636946248034, "dimensionless"))  # type: ignore
        s.ph = Q_(101325.0, "Pa"), Q_(3336406.139862406, "J/kg")
        assert np.isclose(s.T, Q_(700.9882316847855, "K"))  # type: ignore
        assert np.isclose(s.p, Q_(101325.0, "Pa"))  # type: ignore
        assert np.isclose(s.ph[0], Q_(101325.0, "Pa"))  # type: ignore
        assert np.isclose(s.ph[1], Q_(3336406.139862406, "J/kg"))  # type: ignore
        assert np.isclose(s.u, Q_(3013250.0, "J/kg"))  # type: ignore
        assert np.isclose(s.s, Q_(8623.283568815832, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.v, Q_(3.189303132125469, "m**3/kg"))  # type: ignore
        assert np.isclose(s.h, Q_(3336406.139862406, "J/kg"))  # type: ignore
        assert s.x is None

    def test_set_hp(self):
        """Set a pair of properties of the State and check the properties.

        Also works as a functional/regression test of CoolProp.
        """
        s = State(substance="water")
        s.hp = Q_(1061602.391543017, "J/kg"), Q_(101325.0, "Pa")
        # Pylance does not support NumPy ufuncs
        assert np.isclose(s.T, Q_(373.1242958476843, "K"))  # type: ignore
        assert np.isclose(s.p, Q_(101325.0, "Pa"))  # type: ignore
        assert np.isclose(s.hp[0], Q_(1061602.391543017, "J/kg"))  # type: ignore
        assert np.isclose(s.hp[1], Q_(101325.0, "Pa"))  # type: ignore
        assert np.isclose(s.u, Q_(1013250, "J/kg"))  # type: ignore
        assert np.isclose(s.s, Q_(3028.9867985920914, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.v, Q_(0.4772010021515822, "m**3/kg"))  # type: ignore
        assert np.isclose(s.h, Q_(1061602.391543017, "J/kg"))  # type: ignore
        assert np.isclose(s.x, Q_(0.28475636946248034, "dimensionless"))  # type: ignore
        s.hp = Q_(3336406.139862406, "J/kg"), Q_(101325.0, "Pa")
        assert np.isclose(s.T, Q_(700.9882316847855, "K"))  # type: ignore
        assert np.isclose(s.p, Q_(101325.0, "Pa"))  # type: ignore
        assert np.isclose(s.hp[0], Q_(3336406.139862406, "J/kg"))  # type: ignore
        assert np.isclose(s.hp[1], Q_(101325.0, "Pa"))  # type: ignore
        assert np.isclose(s.u, Q_(3013250, "J/kg"))  # type: ignore
        assert np.isclose(s.s, Q_(8623.283568815832, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.v, Q_(3.189303132125469, "m**3/kg"))  # type: ignore
        assert np.isclose(s.h, Q_(3336406.139862406, "J/kg"))  # type: ignore
        assert s.x is None

    def test_set_px(self):
        """Set a pair of properties of the State and check the properties.

        Also works as a functional/regression test of CoolProp.
        """
        s = State(substance="water")
        s.px = Q_(101325.0, "Pa"), Q_(0.28475636946248034, "dimensionless")
        # Pylance does not support NumPy ufuncs
        assert np.isclose(s.T, Q_(373.1242958476843, "K"))  # type: ignore
        assert np.isclose(s.p, Q_(101325.0, "Pa"))  # type: ignore
        assert np.isclose(s.px[0], Q_(101325.0, "Pa"))  # type: ignore
        assert np.isclose(s.px[1], Q_(0.2847563694624, "dimensionless"))  # type: ignore
        assert np.isclose(s.u, Q_(1013250.0, "J/kg"))  # type: ignore
        assert np.isclose(s.s, Q_(3028.9867985920914, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.v, Q_(0.4772010021515822, "m**3/kg"))  # type: ignore
        assert np.isclose(s.h, Q_(1061602.391543017, "J/kg"))  # type: ignore
        assert np.isclose(s.x, Q_(0.28475636946248034, "dimensionless"))  # type: ignore

    def test_set_xp(self):
        """Set a pair of properties of the State and check the properties.

        Also works as a functional/regression test of CoolProp.
        """
        s = State(substance="water")
        s.xp = Q_(0.28475636946248034, "dimensionless"), Q_(101325.0, "Pa")
        # Pylance does not support NumPy ufuncs
        assert np.isclose(s.T, Q_(373.1242958476843, "K"))  # type: ignore
        assert np.isclose(s.p, Q_(101325.0, "Pa"))  # type: ignore
        assert np.isclose(s.xp[0], Q_(0.2847563694624, "dimensionless"))  # type: ignore
        assert np.isclose(s.xp[1], Q_(101325.0, "Pa"))  # type: ignore
        assert np.isclose(s.u, Q_(1013250, "J/kg"))  # type: ignore
        assert np.isclose(s.s, Q_(3028.9867985920914, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.v, Q_(0.4772010021515822, "m**3/kg"))  # type: ignore
        assert np.isclose(s.h, Q_(1061602.391543017, "J/kg"))  # type: ignore
        assert np.isclose(s.x, Q_(0.28475636946248034, "dimensionless"))  # type: ignore

    # This set of tests fails because s and u are not valid inputs for PhaseSI
    # in CoolProp 6.1.0
    @pytest.mark.xfail(strict=True, raises=StateError)
    def test_set_us(self):
        """Set a pair of properties of the State and check the properties.

        Also works as a functional/regression test of CoolProp.
        """
        s = State(substance="water")
        s.us = Q_(1013250.0, "J/kg"), Q_(3028.9867985920914, "J/(kg*K)")
        # Pylance does not support NumPy ufuncs
        assert np.isclose(s.T, Q_(373.1242958476843, "K"))  # type: ignore
        assert np.isclose(s.p, Q_(101325.0, "Pa"))  # type: ignore
        assert np.isclose(s.us[0], Q_(1013250.0, "J/kg"))  # type: ignore
        assert np.isclose(s.us[1], Q_(3028.9867985920914, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.u, Q_(1013250.0, "J/kg"))  # type: ignore
        assert np.isclose(s.s, Q_(3028.9867985920914, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.v, Q_(0.4772010021515822, "m**3/kg"))  # type: ignore
        assert np.isclose(s.h, Q_(1061602.391543017, "J/kg"))  # type: ignore
        assert np.isclose(s.x, Q_(0.28475636946248034, "dimensionless"))  # type: ignore

    @pytest.mark.xfail(strict=True, raises=StateError)
    def test_set_su(self):
        """Set a pair of properties of the State and check the properties.

        Also works as a functional/regression test of CoolProp.
        """
        s = State(substance="water")
        s.su = Q_(3028.9867985920914, "J/(kg*K)"), Q_(1013250.0, "J/kg")
        # Pylance does not support NumPy ufuncs
        assert np.isclose(s.T, Q_(373.1242958476843, "K"))  # type: ignore
        assert np.isclose(s.p, Q_(101325.0, "Pa"))  # type: ignore
        assert np.isclose(s.su[0], Q_(3028.9867985920914, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.su[1], Q_(1013250.0, "J/kg"))  # type: ignore
        assert np.isclose(s.u, Q_(1013250, "J/kg"))  # type: ignore
        assert np.isclose(s.s, Q_(3028.9867985920914, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.v, Q_(0.4772010021515822, "m**3/kg"))  # type: ignore
        assert np.isclose(s.h, Q_(1061602.391543017, "J/kg"))  # type: ignore
        assert np.isclose(s.x, Q_(0.28475636946248034, "dimensionless"))  # type: ignore

    def test_set_uv(self):
        """Set a pair of properties of the State and check the properties.

        Also works as a functional/regression test of CoolProp.
        """
        s = State(substance="water")
        s.uv = Q_(1013250.0, "J/kg"), Q_(0.4772010021515822, "m**3/kg")
        # Pylance does not support NumPy ufuncs
        assert np.isclose(s.T, Q_(373.1242958476843, "K"))  # type: ignore
        assert np.isclose(s.p, Q_(101325.0, "Pa"))  # type: ignore
        assert np.isclose(s.uv[0], Q_(1013250.0, "J/kg"))  # type: ignore
        assert np.isclose(s.uv[1], Q_(0.4772010021515822, "m**3/kg"))  # type: ignore
        assert np.isclose(s.u, Q_(1013250.0, "J/kg"))  # type: ignore
        assert np.isclose(s.s, Q_(3028.9867985920914, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.v, Q_(0.4772010021515822, "m**3/kg"))  # type: ignore
        assert np.isclose(s.h, Q_(1061602.391543017, "J/kg"))  # type: ignore
        assert np.isclose(s.x, Q_(0.28475636946248034, "dimensionless"))  # type: ignore

    def test_set_vu(self):
        """Set a pair of properties of the State and check the properties.

        Also works as a functional/regression test of CoolProp.
        """
        s = State(substance="water")
        s.vu = Q_(0.4772010021515822, "m**3/kg"), Q_(1013250.0, "J/kg")
        # Pylance does not support NumPy ufuncs
        assert np.isclose(s.T, Q_(373.1242958476843, "K"))  # type: ignore
        assert np.isclose(s.p, Q_(101325.0, "Pa"))  # type: ignore
        assert np.isclose(s.vu[0], Q_(0.4772010021515822, "m**3/kg"))  # type: ignore
        assert np.isclose(s.vu[1], Q_(1013250.0, "J/kg"))  # type: ignore
        assert np.isclose(s.u, Q_(1013250, "J/kg"))  # type: ignore
        assert np.isclose(s.s, Q_(3028.9867985920914, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.v, Q_(0.4772010021515822, "m**3/kg"))  # type: ignore
        assert np.isclose(s.h, Q_(1061602.391543017, "J/kg"))  # type: ignore
        assert np.isclose(s.x, Q_(0.28475636946248034, "dimensionless"))  # type: ignore

    def test_set_sv(self):
        """Set a pair of properties of the State and check the properties.

        Also works as a functional/regression test of CoolProp.
        """
        s = State(substance="water")
        s.sv = Q_(3028.9867985920914, "J/(kg*K)"), Q_(0.4772010021515822, "m**3/kg")
        # Pylance does not support NumPy ufuncs
        assert np.isclose(s.T, Q_(373.1242958476843, "K"))  # type: ignore
        assert np.isclose(s.p, Q_(101325.0, "Pa"))  # type: ignore
        assert np.isclose(s.sv[0], Q_(3028.9867985920914, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.sv[1], Q_(0.4772010021515822, "m**3/kg"))  # type: ignore
        assert np.isclose(s.u, Q_(1013250.0, "J/kg"))  # type: ignore
        assert np.isclose(s.s, Q_(3028.9867985920914, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.v, Q_(0.4772010021515822, "m**3/kg"))  # type: ignore
        assert np.isclose(s.h, Q_(1061602.391543017, "J/kg"))  # type: ignore
        assert np.isclose(s.x, Q_(0.28475636946248034, "dimensionless"))  # type: ignore

    def test_set_vs(self):
        """Set a pair of properties of the State and check the properties.

        Also works as a functional/regression test of CoolProp.
        """
        s = State(substance="water")
        s.vs = Q_(0.4772010021515822, "m**3/kg"), Q_(3028.9867985920914, "J/(kg*K)")
        # Pylance does not support NumPy ufuncs
        assert np.isclose(s.T, Q_(373.1242958476843, "K"))  # type: ignore
        assert np.isclose(s.p, Q_(101325.0, "Pa"))  # type: ignore
        assert np.isclose(s.vs[0], Q_(0.4772010021515822, "m**3/kg"))  # type: ignore
        assert np.isclose(s.vs[1], Q_(3028.9867985920914, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.u, Q_(1013250, "J/kg"))  # type: ignore
        assert np.isclose(s.s, Q_(3028.9867985920914, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.v, Q_(0.4772010021515822, "m**3/kg"))  # type: ignore
        assert np.isclose(s.h, Q_(1061602.391543017, "J/kg"))  # type: ignore
        assert np.isclose(s.x, Q_(0.28475636946248034, "dimensionless"))  # type: ignore

    def test_set_sh(self):
        """Set a pair of properties of the State and check the properties.

        Also works as a functional/regression test of CoolProp.
        """
        s = State(substance="water")
        s.sh = Q_(3028.9867985920914, "J/(kg*K)"), Q_(1061602.391543017, "J/kg")
        # Pylance does not support NumPy ufuncs
        assert np.isclose(s.T, Q_(373.1242958476843, "K"))  # type: ignore
        assert np.isclose(s.p, Q_(101325.0, "Pa"))  # type: ignore
        assert np.isclose(s.sh[0], Q_(3028.9867985920914, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.sh[1], Q_(1061602.391543017, "J/kg"))  # type: ignore
        assert np.isclose(s.u, Q_(1013250.0, "J/kg"))  # type: ignore
        assert np.isclose(s.s, Q_(3028.9867985920914, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.v, Q_(0.4772010021515822, "m**3/kg"))  # type: ignore
        assert np.isclose(s.h, Q_(1061602.391543017, "J/kg"))  # type: ignore
        assert np.isclose(s.x, Q_(0.28475636946248034, "dimensionless"))  # type: ignore

    def test_set_hs(self):
        """Set a pair of properties of the State and check the properties.

        Also works as a functional/regression test of CoolProp.
        """
        s = State(substance="water")
        s.hs = Q_(1061602.391543017, "J/kg"), Q_(3028.9867985920914, "J/(kg*K)")
        # Pylance does not support NumPy ufuncs
        assert np.isclose(s.T, Q_(373.1242958476843, "K"))  # type: ignore
        assert np.isclose(s.p, Q_(101325.0, "Pa"))  # type: ignore
        assert np.isclose(s.hs[0], Q_(1061602.391543017, "J/kg"))  # type: ignore
        assert np.isclose(s.hs[1], Q_(3028.9867985920914, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.u, Q_(1013250, "J/kg"))  # type: ignore
        assert np.isclose(s.s, Q_(3028.9867985920914, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.v, Q_(0.4772010021515822, "m**3/kg"))  # type: ignore
        assert np.isclose(s.h, Q_(1061602.391543017, "J/kg"))  # type: ignore
        assert np.isclose(s.x, Q_(0.28475636946248034, "dimensionless"))  # type: ignore

    def test_set_vh(self):
        """Set a pair of properties of the State and check the properties.

        Also works as a functional/regression test of CoolProp.
        """
        s = State(substance="water")
        s.vh = Q_(0.4772010021515822, "m**3/kg"), Q_(1061602.391543017, "J/kg")
        # Pylance does not support NumPy ufuncs
        assert np.isclose(s.T, Q_(373.1242958476843, "K"))  # type: ignore
        assert np.isclose(s.p, Q_(101325.0, "Pa"))  # type: ignore
        assert np.isclose(s.vh[0], Q_(0.4772010021515822, "m**3/kg"))  # type: ignore
        assert np.isclose(s.vh[1], Q_(1061602.391543017, "J/kg"))  # type: ignore
        assert np.isclose(s.u, Q_(1013250.0, "J/kg"))  # type: ignore
        assert np.isclose(s.s, Q_(3028.9867985920914, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.v, Q_(0.4772010021515822, "m**3/kg"))  # type: ignore
        assert np.isclose(s.h, Q_(1061602.391543017, "J/kg"))  # type: ignore
        assert np.isclose(s.x, Q_(0.28475636946248034, "dimensionless"))  # type: ignore

    def test_set_hv(self):
        """Set a pair of properties of the State and check the properties.

        Also works as a functional/regression test of CoolProp.
        """
        s = State(substance="water")
        s.hv = Q_(1061602.391543017, "J/kg"), Q_(0.4772010021515822, "m**3/kg")
        # Pylance does not support NumPy ufuncs
        assert np.isclose(s.T, Q_(373.1242958476843, "K"))  # type: ignore
        assert np.isclose(s.p, Q_(101325.0, "Pa"))  # type: ignore
        assert np.isclose(s.hv[0], Q_(1061602.391543017, "J/kg"))  # type: ignore
        assert np.isclose(s.hv[1], Q_(0.4772010021515822, "m**3/kg"))  # type: ignore
        assert np.isclose(s.u, Q_(1013250, "J/kg"))  # type: ignore
        assert np.isclose(s.s, Q_(3028.9867985920914, "J/(kg*K)"))  # type: ignore
        assert np.isclose(s.v, Q_(0.4772010021515822, "m**3/kg"))  # type: ignore
        assert np.isclose(s.h, Q_(1061602.391543017, "J/kg"))  # type: ignore
        assert np.isclose(s.x, Q_(0.28475636946248034, "dimensionless"))  # type: ignore

    def test_state_units_EE(self):
        """Set a state with EE units and check the properties."""
        s = State("water", T=Q_(100, "degC"), p=Q_(1.0, "atm"), units="EE")
        assert s.units == "EE"
        assert s.cv.units == "british_thermal_unit / degree_Rankine / pound"
        assert s.cp.units == "british_thermal_unit / degree_Rankine / pound"
        assert s.s.units == "british_thermal_unit / degree_Rankine / pound"
        assert s.h.units == "british_thermal_unit / pound"
        assert s.T.units == "degree_Fahrenheit"
        assert s.u.units == "british_thermal_unit / pound"
        assert s.v.units == "foot ** 3 / pound"
        assert s.p.units == "pound_force_per_square_inch"

    def test_state_units_SI(self):
        """Set a state with SI units and check the properties."""
        s = State("water", T=Q_(100, "degC"), p=Q_(1.0, "atm"), units="SI")
        assert s.units == "SI"
        assert s.cv.units == "kilojoule / kelvin / kilogram"
        assert s.cp.units == "kilojoule / kelvin / kilogram"
        assert s.s.units == "kilojoule / kelvin / kilogram"
        assert s.h.units == "kilojoule / kilogram"
        assert s.T.units == "degree_Celsius"
        assert s.u.units == "kilojoule / kilogram"
        assert s.v.units == "meter ** 3 / kilogram"
        assert s.p.units == "bar"

    def test_default_units(self):
        """Set default units and check for functionality."""
        s = State("water", T=Q_(100, "degC"), p=Q_(1.0, "atm"))
        assert s.units is None
        set_default_units("SI")
        s2 = State("water", T=Q_(100, "degC"), p=Q_(1.0, "atm"))
        assert s2.units == "SI"
        set_default_units("EE")
        s3 = State("water", T=Q_(100, "degC"), p=Q_(1.0, "atm"))
        assert s3.units == "EE"
        set_default_units(None)

    def test_unsupported_units(self):
        """Unsupported unit names should raise TypeError."""
        with pytest.raises(TypeError):
            set_default_units("bad")
        with pytest.raises(TypeError):
            State("water", T=Q_(100, "degC"), p=Q_(1.0, "atm"), units="bad")

    def test_change_units(self):
        """Change state units and check variable units have changed."""
        s = State("water", T=Q_(100, "degC"), p=Q_(1.0, "atm"), units="EE")
        assert s.units == "EE"
        s.units = "SI"
        assert s.units == "SI"
        assert s.cv.units == "kilojoule / kelvin / kilogram"
        assert s.cp.units == "kilojoule / kelvin / kilogram"
        assert s.s.units == "kilojoule / kelvin / kilogram"
        assert s.h.units == "kilojoule / kilogram"
        assert s.T.units == "degree_Celsius"
        assert s.u.units == "kilojoule / kilogram"
        assert s.v.units == "meter ** 3 / kilogram"
        assert s.p.units == "bar"
