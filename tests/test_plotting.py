import pytest
from src.thermostate.plotting import PlottedState, VaporDome
from src.thermostate.thermostate import State, Q_, units


def get_vapordome():
    return VaporDome(("v", "T"), ("s", "T"))


def test_remove_state_no_input():
    v = get_vapordome()
    with pytest.raises(ValueError):
        v.remove_state()


def test_remove_state_no_key():
    v = get_vapordome()
    state_3 = State("water", T=500 * units.kelvin, v=1 * units.m ** 3 / units.kg)
    v.add_state(state_3)  # test of repr(state)
    v.remove_state(state_3)
    # assert v.states[repr(state_3)] == None


def test_remove_state_key_input():
    v = get_vapordome()
    state_4 = State("water", T=400 * units.kelvin, v=1 * units.m ** 3 / units.kg)
    v.add_state(state_4, key="st4")  # test of key
    v.remove_state(key="st4")


def test_remove_state_wrong_key_no_state():
    v = get_vapordome()
    state_5 = State("water", T=700 * units.kelvin, v=1 * units.m ** 3 / units.kg)
    v.add_state(state_5, key="st5")  # test of wrong key and state = none
    with pytest.raises(ValueError):
        v.remove_state(key="wrong key")


def test_remove_state_altered_key():
    v = get_vapordome()
    state_6 = State("water", T=700 * units.kelvin, v=0.01 * units.m ** 3 / units.kg)
    v.add_state(state_6, key="st6")  # test of state input with an altered key
    v.remove_state(state_6)


def test_remove_state_state_not_added():
    v = get_vapordome()
    state_7 = State("water", T=400 * units.kelvin, v=0.01 * units.m ** 3 / units.kg)
    with pytest.raises(ValueError):
        v.remove_state(state_7)  # test of removing a state that was never added


def test_add_process_states_already_added():
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


def test_add_process_isobaric():
    v = get_vapordome()
    state_1 = State(
        "water", T=300 * units.degC, s=1.5 * units.kJ / (units.kg * units.K)
    )
    state_2 = State(
        "water", T=300 * units.kelvin, s=3 * units.kJ / (units.K * units.kg)
    )
    state_3 = State("water", p=state_2.p, v=100 * units.m ** 3 / units.kg)
    with pytest.raises(ValueError):
        v.add_process(state_1, state_2, "isobaric")

    v.add_process(state_2, state_3, "isobaric")


def test_add_process_isothermal():
    v = get_vapordome()
    state_1 = State(
        "water", T=300 * units.degC, s=1.5 * units.kJ / (units.kg * units.K)
    )
    state_2 = State(
        "water", T=300 * units.kelvin, s=3 * units.kJ / (units.K * units.kg)
    )
    state_3 = State("water", T=state_2.T, v=100 * units.m ** 3 / units.kg)
    with pytest.raises(ValueError):
        v.add_process(state_1, state_2, "isothermal")

    v.add_process(state_2, state_3, "isothermal")


def test_add_process_isoenergetic():
    v = get_vapordome()
    state_1 = State(
        "water", T=300 * units.degC, s=1.5 * units.kJ / (units.kg * units.K)
    )
    state_2 = State(
        "water", T=300 * units.kelvin, s=3 * units.kJ / (units.K * units.kg)
    )
    state_3 = State("water", u=state_2.u, v=state_2.v + 5 * units.m ** 3 / units.kg)
    with pytest.raises(ValueError):
        v.add_process(state_1, state_2, "isoenergetic")

    v.add_process(state_2, state_3, "isoenergetic")


def test_add_process_isoenthalpic():
    v = get_vapordome()
    state_1 = State(
        "water", T=300 * units.degC, s=1.5 * units.kJ / (units.kg * units.K)
    )
    state_2 = State(
        "water", T=300 * units.kelvin, s=3 * units.kJ / (units.K * units.kg)
    )
    state_3 = State("water", h=state_2.h, v=state_2.v + 5 * units.m ** 3 / units.kg)
    with pytest.raises(ValueError):
        v.add_process(state_1, state_2, "isoenthalpic")

    v.add_process(state_2, state_3, "isoenthalpic")


def test_add_process_isentropic():
    v = get_vapordome()
    state_1 = State(
        "water", T=300 * units.degC, s=1.5 * units.kJ / (units.kg * units.K)
    )
    state_2 = State(
        "water", T=300 * units.kelvin, s=3 * units.kJ / (units.K * units.kg)
    )
    state_3 = State("water", s=state_2.s, T=450 * units.kelvin)
    with pytest.raises(ValueError):
        v.add_process(state_1, state_2, "isentropic")

    v.add_process(state_2, state_3, "isentropic")


def test_add_process_isochoric():
    v = get_vapordome()
    state_1 = State(
        "water", T=300 * units.degC, s=1.5 * units.kJ / (units.kg * units.K)
    )
    state_2 = State(
        "water", T=300 * units.kelvin, s=3 * units.kJ / (units.K * units.kg)
    )
    state_3 = State("water", v=state_2.v, T=450 * units.kelvin)
    with pytest.raises(ValueError):
        v.add_process(state_1, state_2, "isochoric")

    v.add_process(state_2, state_3, "isochoric")
