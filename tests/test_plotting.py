"""Test module for the plotting code."""
import pytest
from thermostate.plotting import VaporDome, IdealGas
from thermostate.thermostate import State, units
import numpy as np


def get_vapordome():
    """Return an instance of the VaporDome Class."""
    return VaporDome("water", ("v", "T"), ("s", "T"))


def test_plot_additon():
    """Test adding a plot."""
    v = VaporDome("CARBONDIOXIDE", ("v", "T"), ("s", "T"))
    v.plot("p", "v")
    assert ("pv") in v.plots


def test_plot_already_added():
    """Test adding a plot that already exists in the instance."""
    v = get_vapordome()
    with pytest.raises(
        ValueError, match="Plot has already been added to this class instance"
    ):
        v.plot("v", "T")


def test_remove_state_no_input():
    """Test error handling of remove_state function with no input."""
    v = get_vapordome()
    with pytest.raises(
        ValueError, match="No state or key was entered. Unable to find state"
    ):
        v.remove_state()


def test_remove_state_no_key():
    """Test ability of remove_state function to work with input of the state."""
    v = get_vapordome()
    state_3 = State("water", T=500 * units.kelvin, v=1 * units.m ** 3 / units.kg)
    v.add_state(state_3)  # test of repr(state)
    v.remove_state(state_3)
    # assert v.states[repr(state_3)] == None


def test_remove_state_key_input():
    """Test ability of remove_state function to work with input of a key."""
    v = get_vapordome()
    state_4 = State("water", T=400 * units.kelvin, v=1 * units.m ** 3 / units.kg)
    v.add_state(state_4, key="st4")  # test of key
    v.remove_state(key="st4")
    # assert state_4 not in v.states #fails whether its "in" or "not in". whats a better
    # way to define this


def test_remove_state_wrong_key_no_state():
    """Test error handling of remove_state function with the wrong key."""
    v = get_vapordome()
    state_5 = State("water", T=700 * units.kelvin, v=1 * units.m ** 3 / units.kg)
    v.add_state(state_5, key="st5")  # test of wrong key and state = none
    with pytest.raises(ValueError, match="Couldn't find key"):
        v.remove_state(key="wrong key")


def test_remove_state_altered_key():
    """Test ability of remove_state function to work with input of an altered key."""
    v = get_vapordome()
    state_6 = State("water", T=700 * units.kelvin, v=0.01 * units.m ** 3 / units.kg)
    v.add_state(state_6, key="st6")  # test of state input with an altered key
    v.remove_state(state_6)


def test_remove_state_state_not_added():
    """Test error handling of remove_state function with the wrong key."""
    v = get_vapordome()
    state_7 = State("water", T=400 * units.kelvin, v=0.01 * units.m ** 3 / units.kg)
    with pytest.raises(ValueError, match="Couldn't find the state"):
        v.remove_state(state_7)  # test of removing a state that was never added


def test_remove_process_without_remove_states():
    """Test ability of remove_process function to remove a line but not the states."""
    v = get_vapordome()
    state_1 = State(
        "water", T=300 * units.degC, s=1.5 * units.kJ / (units.kg * units.K)
    )
    state_2 = State(
        "water", T=300 * units.kelvin, s=3 * units.kJ / (units.K * units.kg)
    )
    v.add_state(state_1)
    v.add_state(state_2)
    v.add_process(state_1, state_2)
    v.remove_process(state_1, state_2, remove_states=False)
    # would like to assert if the states are in v.states and if process was
    # removed from v.states


def test_remove_process_with_remove_states():
    """Test ability of remove_process function to remove a line and the states."""
    v = get_vapordome()
    state_1 = State(
        "water", T=300 * units.degC, s=1.5 * units.kJ / (units.kg * units.K)
    )
    state_2 = State(
        "water", T=300 * units.kelvin, s=3 * units.kJ / (units.K * units.kg)
    )
    v.add_state(state_1)
    v.add_state(state_2)
    v.add_process(state_1, state_2)
    v.remove_process(state_1, state_2, remove_states=True)
    # would like to assert if the states are removed from v.states and if process was
    # removed from v.states


def test_add_process_states_already_added():
    """Test ability of add_process function when states have been previously added."""
    v = get_vapordome()
    state_1 = State(
        "water", T=300 * units.degC, s=1.5 * units.kJ / (units.kg * units.K)
    )
    state_2 = State(
        "water", T=300 * units.kelvin, s=3 * units.kJ / (units.K * units.kg)
    )
    v.add_state(state_1)
    v.add_state(state_2)
    v.add_process(state_1, state_2)


def test_add_process_states_not_added():
    """Test ability of add_process function when states have not been added."""
    v = get_vapordome()
    state_1 = State(
        "water", T=300 * units.degC, s=1.5 * units.kJ / (units.kg * units.K)
    )
    state_2 = State(
        "water", T=300 * units.kelvin, s=3 * units.kJ / (units.K * units.kg)
    )
    v.add_process(state_1, state_2)


def test_add_process_substance_match():
    """Test error handling of add_process to catch a mismatch of states."""
    v = get_vapordome()
    state_1 = State(
        "water", T=300 * units.degC, s=1.5 * units.kJ / (units.kg * units.K)
    )
    state_2 = State(
        "carbondioxide", T=300 * units.kelvin, s=3 * units.kJ / (units.K * units.kg)
    )
    v.add_state(state_1)
    v.add_state(state_2)
    with pytest.raises(ValueError, match="Substance of input states do not match"):
        v.add_process(state_1, state_2)


def test_add_process_isobaric():
    """Test add_process when process_type = isobaric."""
    v = get_vapordome()
    state_1 = State("water", p=1500 * units.Pa, s=1.5 * units.kJ / (units.kg * units.K))
    state_2 = State("water", p=3500 * units.Pa, s=3 * units.kJ / (units.K * units.kg))
    state_3 = State("water", p=state_2.p, v=100 * units.m ** 3 / units.kg)
    v.add_state(state_1, key="st_1")
    v.add_state(state_2, key="st_2")
    v.add_state(state_3, key="st_3")
    with pytest.raises(ValueError, match="Property: 'p' was not held constant"):
        v.add_process(state_1, state_2, "isobaric")

    v.add_process(state_2, state_3, "isobaric")
    line = v.processes["st_2st_3"]["vT"]
    v_range = (
        np.logspace(np.log10(state_2.v.magnitude), np.log10(state_3.v.magnitude))
        * units.m ** 3
        / units.kg
    )
    assert np.all(np.isclose(line.get_xdata(), v_range))


def test_add_process_isothermal():
    """Test add_process when process_type = isothermal."""
    v = get_vapordome()
    state_1 = State(
        "water", T=300 * units.degC, s=1.5 * units.kJ / (units.kg * units.K)
    )
    state_2 = State(
        "water", T=300 * units.kelvin, s=3 * units.kJ / (units.K * units.kg)
    )
    state_3 = State("water", T=state_2.T, v=100 * units.m ** 3 / units.kg)
    v.add_state(state_1, key="st_1")
    v.add_state(state_2, key="st_2")
    v.add_state(state_3, key="st_3")
    with pytest.raises(ValueError, match="Property: 'T' was not held constant"):
        v.add_process(state_1, state_2, "isothermal")

    v.add_process(state_2, state_3, "isothermal")
    line = v.processes["st_2st_3"]["vT"]
    v_range = (
        np.logspace(np.log10(state_2.v.magnitude), np.log10(state_3.v.magnitude))
        * units.m ** 3
        / units.kg
    )
    assert np.all(np.isclose(line.get_xdata(), v_range))


def test_add_process_isoenergetic():
    """Test add_process when process_type = isoenergetic."""
    v = get_vapordome()
    state_1 = State(
        "water", T=300 * units.degC, s=1.5 * units.kJ / (units.kg * units.K)
    )
    state_2 = State(
        "water", T=300 * units.kelvin, s=3 * units.kJ / (units.K * units.kg)
    )
    state_3 = State("water", u=state_2.u, v=state_2.v + 5 * units.m ** 3 / units.kg)
    v.add_state(state_1, key="st_1")
    v.add_state(state_2, key="st_2")
    v.add_state(state_3, key="st_3")
    with pytest.raises(ValueError, match="Property: 'u' was not held constant"):
        v.add_process(state_1, state_2, "isoenergetic")

    v.add_process(state_2, state_3, "isoenergetic")
    line = v.processes["st_2st_3"]["vT"]
    v_range = (
        np.logspace(np.log10(state_2.v.magnitude), np.log10(state_3.v.magnitude))
        * units.m ** 3
        / units.kg
    )
    assert np.all(np.isclose(line.get_xdata(), v_range))


def test_add_process_isoenthalpic():
    """Test add_process when process_type = isoenthalpic."""
    v = get_vapordome()
    state_1 = State(
        "water", T=300 * units.degC, s=1.5 * units.kJ / (units.kg * units.K)
    )
    state_2 = State(
        "water", T=300 * units.kelvin, s=3 * units.kJ / (units.K * units.kg)
    )
    state_3 = State("water", h=state_2.h, v=state_2.v + 5 * units.m ** 3 / units.kg)
    v.add_state(state_1, key="st_1")
    v.add_state(state_2, key="st_2")
    v.add_state(state_3, key="st_3")
    with pytest.raises(ValueError, match="Property: 'h' was not held constant"):
        v.add_process(state_1, state_2, "isoenthalpic")

    v.add_process(state_2, state_3, "isoenthalpic")
    line = v.processes["st_2st_3"]["vT"]
    v_range = (
        np.logspace(np.log10(state_2.v.magnitude), np.log10(state_3.v.magnitude))
        * units.m ** 3
        / units.kg
    )
    assert np.all(np.isclose(line.get_xdata(), v_range))


def test_add_process_isentropic():
    """Test add_process when process_type = isentropic."""
    v = get_vapordome()
    state_1 = State(
        "water", T=300 * units.degC, s=1.5 * units.kJ / (units.kg * units.K)
    )
    state_2 = State(
        "water", T=300 * units.kelvin, s=3 * units.kJ / (units.K * units.kg)
    )
    state_3 = State("water", s=state_2.s, T=450 * units.kelvin)
    v.add_state(state_1, key="st_1")
    v.add_state(state_2, key="st_2")
    v.add_state(state_3, key="st_3")
    with pytest.raises(ValueError, match="Property: 's' was not held constant"):
        v.add_process(state_1, state_2, "isentropic")

    v.add_process(state_2, state_3, "isentropic")
    line = v.processes["st_2st_3"]["vT"]
    v_range = (
        np.logspace(np.log10(state_2.v.magnitude), np.log10(state_3.v.magnitude))
        * units.m ** 3
        / units.kg
    )
    assert np.all(np.isclose(line.get_xdata(), v_range))


def test_add_process_isochoric():
    """Test add_process when process_type = isochoric."""
    v = get_vapordome()
    state_1 = State(
        "water", T=300 * units.degC, s=1.5 * units.kJ / (units.kg * units.K)
    )
    state_2 = State(
        "water", T=300 * units.kelvin, s=3 * units.kJ / (units.K * units.kg)
    )
    state_3 = State("water", v=state_2.v, T=450 * units.kelvin)
    v.add_state(state_1, key="st_1")
    v.add_state(state_2, key="st_2")
    v.add_state(state_3, key="st_3")
    with pytest.raises(ValueError, match="Property: 'v' was not held constant"):
        v.add_process(state_1, state_2, "isochoric")

    v.add_process(state_2, state_3, "isochoric")
    line = v.processes["st_2st_3"]["vT"]
    v_range = (
        np.logspace(np.log10(state_2.v.magnitude), np.log10(state_3.v.magnitude))
        * units.m ** 3
        / units.kg
    )
    assert np.all(np.isclose(line.get_xdata(), v_range))


def test_add_process_invalid_process_type():
    """Test error handling of add_process when process_type is not an accepted form."""
    v = get_vapordome()
    state_1 = State(
        "water", T=300 * units.degC, s=1.5 * units.kJ / (units.kg * units.K)
    )
    state_2 = State(
        "water", T=300 * units.kelvin, s=3 * units.kJ / (units.K * units.kg)
    )
    v.add_state(state_1, key="st_1")
    v.add_state(state_2, key="st_2")
    with pytest.raises(ValueError, match="Not a supported process type"):
        v.add_process(state_1, state_2, "hogwash")


def test_IdealGas_plot_additon():
    """Test adding a plot."""
    g = IdealGas(("v", "T"), ("s", "T"))
    g.plot("p", "v")
    assert ("pv") in g.plots


def test_IdealGas_plot_already_added():
    """Test adding a plot that already exists in the instance."""
    g = IdealGas("air", ("v", "T"))
    with pytest.raises(
        ValueError, match="Plot has already been added to this class instance"
    ):
        g.plot("v", "T")


def test_label_add_state():
    """Test using a label in add_state."""
    vd = VaporDome("water", ("v", "T"))
    st_1 = State("water", x=1.0 * units.dimensionless, T=100 * units.degC)
    st_2 = State("water", x=0.0 * units.dimensionless, T=100 * units.degC)
    assert st_1.label is None
    assert st_2.label is None
    vd.add_state(st_1, label=1)
    vd.add_state(st_2, label="2")
    assert st_1.label == "1"
    assert st_2.label == "2"


def test_label_add_process():
    """Test using label in add_process."""
    vd = VaporDome("water", ("v", "T"))
    st_1 = State("water", x=1.0 * units.dimensionless, T=100 * units.degC)
    st_2 = State("water", x=0.0 * units.dimensionless, T=100 * units.degC)
    assert st_1.label is None
    assert st_2.label is None
    vd.add_process(st_1, st_2, label_1=1, label_2="2")
    assert st_1.label == "1"
    assert st_2.label == "2"


@pytest.mark.xfail(strict=True)
def test_multiple_processes_with_the_same_states():
    """Test adding multiple processes with the same states.

    This expected failure is because no ValueError is raised.
    """
    g = IdealGas("air", ("v", "T"))
    state_1 = State("air", T=300 * units.K, s=1.5 * units("kJ/kg/K"))
    state_2 = State("air", T=300 * units.K, s=3.0 * units("kJ/kg/K"))
    g.add_process(state_1, state_2)
    with pytest.raises(ValueError):
        g.add_process(state_1, state_2, "isothermal")
    with pytest.raises(ValueError):
        g.remove_process(state_1, state_2)
