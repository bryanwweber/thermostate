"""
Base ThermoState module
"""
from CoolProp.CoolProp import PropsSI
from pint import UnitRegistry
from pint.unit import UnitsContainer

units = UnitRegistry()
Q_ = units.Quantity


class StateError(Exception):
    pass


class State(object):
    """Basic State manager for thermodyanmic states

    Parameters
    ----------
    substance : `str`
        One of the substances supported by CoolProp
    T : `pint.UnitRegistry.Quantity`
        Temperature
    p : `pint.UnitRegistry.Quantity`
        Pressure
    u : `pint.UnitRegistry.Quantity`
        Mass-specific internal energy
    s : `pint.UnitRegistry.Quantity`
        Mass-specific entropy
    v : `pint.UnitRegistry.Quantity`
        Mass-specific volume
    h : `pint.UnitRegistry.Quantity`
        Mass-specific enthalpy
    x : `pint.UnitRegistry.Quantity`
        Quality
    """
    allowed_subs = ['AIR', 'AMMONIA', 'WATER', 'PROPANE', 'R134A', 'R22']

    allowed_pairs = [
        'Tp', 'Tu', 'Ts', 'Tv', 'Th', 'Tx',
        'pT', 'pu', 'ps', 'pv', 'ph', 'px',
        'uT', 'up', 'us', 'uv',
        'sT', 'sp', 'su', 'sv', 'sh',
        'vT', 'vp', 'vu', 'vs', 'vh',
        'hT', 'hp', 'hs', 'hv',
    ]

    dimensions = {
        'T': UnitsContainer({'[temperature]': 1.0}),
        'p': UnitsContainer({'[mass]': 1.0, '[length]': -1.0, '[time]': -2.0}),
        'u': UnitsContainer({'[length]': 2.0, '[time]': -2.0}),
        's': UnitsContainer({'[length]': 2.0, '[time]': -2.0, '[temperature]': -1.0}),
        'v': UnitsContainer({'[length]': 3.0, '[mass]': -1.0}),
        'h': UnitsContainer({'[length]': 2.0, '[time]': -2.0}),
        'x': UnitsContainer({}),
    }

    def __init__(self, substance, **kwargs):  # T=None, p=None, u=None, s=None, v=None, h=None, x=None):  # noqa
        if substance.upper() in self.allowed_subs:
            self.sub = substance.upper()
        else:
            raise ValueError('{} is not an allowed substance. Choose one of {}.'.format(
                substance, self.allowed_subs,
            ))

        input_props = ''
        if len(kwargs) != 0:
            for prop in 'Tpusvhx':
                if kwargs.get(prop, None) is not None:
                    input_props += prop

        if len(input_props) > 2 or len(input_props) == 1:
            raise ValueError('Incorrect number of properties specified. Must be 2 or 0.')

        if len(input_props) > 0 and input_props not in self.allowed_pairs:
            raise ValueError('The supplied pair of properties, {props[0]} and {props[1]} is not a'
                             'valid set of independent properties.'.format(props=input_props))

        if len(input_props) > 0:
            setattr(self, input_props, (kwargs[input_props[0]], kwargs[input_props[1]]))
        else:
            setattr(self, 'TP', (Q_(300., 'K'), Q_(101325., 'Pa')))

    def to_SI(self, value):
        return value.to_base_units()

    def to_PropsSI(self, value):
        return self.to_SI(value).magnitude

    @property
    def T(self):
        return self._T

    @property
    def p(self):
        return self._p

    @property
    def u(self):
        return self._u

    @property
    def s(self):
        return self._s

    @property
    def v(self):
        return self._v

    @property
    def h(self):
        return self._h

    @property
    def x(self):
        return self._x

    @property
    def Tp(self):
        return self._T, self._p

    @Tp.setter
    def Tp(self, value):
        if value[0].dimensionality != self.dimensions['T']:
            raise StateError('The dimensions for temperature must be {}'.format(
                self.dimensions['T']))
        elif value[1].dimensionality != self.dimensions['p']:
            raise StateError('The dimensions for pressure must be {}'.format(
                self.dimensions['p']))

        PropsSI_T = self.to_PropsSI(value[0])
        PropsSI_p = self.to_PropsSI(value[1])
        try:
            PropsSI('Phase', 'T', PropsSI_T, 'P', PropsSI_p, self.sub)
        except ValueError as e:
            if 'Saturation pressure' in str(e):
                raise StateError('The given values for T and P are not independent.')
            else:
                raise

        self._T = self.to_SI(value[0])
        self._p = self.to_SI(value[1])
        self._u = Q_(PropsSI('U', 'T', PropsSI_T, 'P', PropsSI_p, self.sub), 'J/kg')
        self._s = Q_(PropsSI('S', 'T', PropsSI_T, 'P', PropsSI_p, self.sub), 'J/(kg*K)')
        self._v = Q_(1.0/PropsSI('D', 'T', PropsSI_T, 'P', PropsSI_p, self.sub), 'm**3/kg')
        self._h = Q_(PropsSI('H', 'T', PropsSI_T, 'P', PropsSI_p, self.sub), 'J/kg')
        self._x = None

    @property
    def pT(self):
        return self._p, self._T

    @pT.setter
    def pT(self, value):
        self.Tp = value[1], value[0]
