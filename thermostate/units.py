"""
This module contains classes with attributes representing the common property units
"""


class EnglishEngineering(object):
    """String representations of common units.

    The attributes of this class are strings that represent the common units for
    thermodynamics calculations.
    """

    s = 'BTU/(lb*degR)'
    h = 'BTU/lb'
    T = 'degF'
    u = 'BTU/lb'
    v = 'ft**3/lb'
    p = 'psi'


class SystemInternational(object):
    """String representations of common units.

    The attributes of this class are strings that represent the common units for
    thermodynamics calculations.
    """

    s = 'kJ/(kg*K)'
    h = 'kJ/kg'
    T = 'degC'
    u = 'kJ/kg'
    v = 'm**3/kg'
    p = 'bar'
