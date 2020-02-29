"""
This module contains classes with attributes representing the common property units.

Example
-------
These classes are shortcuts to the units for common properties::

    >>> st = State("water", T=Q_(300.0, "K"), p=Q_(101325, "Pa"))
    >>> h = st.h.to(SI.h)
    >>> u = st.u.to(EE.u)

"""


class EnglishEngineering(object):
    """String representations of common units.

    The attributes of this class are strings that represent the common units for
    thermodynamics calculations.

    Attributes
    ----------
    h : `str`
        BTU/lb
    p : `str`
        psi
    s : `str`
        BTU/(lb*degR)
    T : `str`
        degF
    u : `str`
        BTU/lb
    v : `str`
        ft**3/lb

    """

    s = "BTU/(lb*degR)"
    h = "BTU/lb"
    T = "degF"
    u = "BTU/lb"
    v = "ft**3/lb"
    p = "psi"


class SystemInternational(object):
    """String representations of common units.

    The attributes of this class are strings that represent the common units for
    thermodynamics calculations.

    Attributes
    ----------
    h : `str`
        kJ/kg
    p : `str`
        bar
    s : `str`
        kJ/(kg*K)
    T : `str`
        degC
    u : `str`
        kJ/kg
    v : `str`
        m**3/lb

    """

    s = "kJ/(kg*K)"
    h = "kJ/kg"
    T = "degC"
    u = "kJ/kg"
    v = "m**3/kg"
    p = "bar"
