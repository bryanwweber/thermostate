"""
Base ThermoState module
"""
from CoolProp.CoolProp import PropsSI
from pint import UnitRegistry
from pint.unit import UnitsContainer, UnitDefinition
from pint.converters import ScaleConverter

units = UnitRegistry()
Q_ = units.Quantity
units.define(UnitDefinition('percent', 'pct', (), ScaleConverter(1.0/100.0)))


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
        'Tp', 'Ts', 'Tv', 'Tx',
        'pT', 'pu', 'ps', 'pv', 'ph', 'px',
        'up', 'us', 'uv',
        'sT', 'sp', 'su', 'sv', 'sh',
        'vT', 'vp', 'vu', 'vs', 'vh',
        'hp', 'hs', 'hv',
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

    SI_units = {
        'T': 'kelvin',
        'p': 'pascal',
        'u': 'joules/kilogram',
        's': 'joules/(kilogram*kelvin)',
        'v': 'meter**3/kilogram',
        'h': 'joules/kilogram',
        'x': 'dimensionless',
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

    def to_SI(self, prop, value):
        return value.to(self.SI_units[prop])

    def to_PropsSI(self, prop, value):
        return self.to_SI(prop, value).magnitude

    def _check_dimensions(self, properties, value):
        if value[0].dimensionality != self.dimensions[properties[0]]:
            raise StateError('The dimensions for {props[0]} must be {dim}'.format(
                props=properties,
                dim=self.dimensions[properties[0]]))
        elif value[1].dimensionality != self.dimensions[properties[1]]:
            raise StateError('The dimensions for {props[1]} must be {dim}'.format(
                props=properties,
                dim=self.dimensions[properties[1]]))

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
        self._check_dimensions(['T', 'p'], value)
        PropsSI_T = self.to_PropsSI('T', value[0])
        PropsSI_p = self.to_PropsSI('p', value[1])
        try:
            PropsSI('Phase', 'T', PropsSI_T, 'P', PropsSI_p, self.sub)
        except ValueError as e:
            if 'Saturation pressure' in str(e):
                raise StateError('The given values for T and P are not independent.')
            else:
                raise

        self._T = self.to_SI('T', value[0])
        self._p = self.to_SI('p', value[1])
        self._u = Q_(PropsSI('U', 'T', PropsSI_T, 'P', PropsSI_p, self.sub), self.SI_units['u'])
        self._s = Q_(PropsSI('S', 'T', PropsSI_T, 'P', PropsSI_p, self.sub), self.SI_units['s'])
        self._v = Q_(1.0/PropsSI('D', 'T', PropsSI_T, 'P', PropsSI_p, self.sub), self.SI_units['v'])
        self._h = Q_(PropsSI('H', 'T', PropsSI_T, 'P', PropsSI_p, self.sub), self.SI_units['h'])
        self._x = None

    @property
    def pT(self):
        return self._p, self._T

    @pT.setter
    def pT(self, value):
        self.Tp = value[1], value[0]

    @property
    def Tu(self):
        return self._T, self._u

    @Tu.setter
    def Tu(self, value):
        raise StateError('Setting T and u simultaneously is not allowed.')
        self._check_dimensions(['T', 'u'], value)
        PropsSI_T = self.to_PropsSI('T', value[0])
        PropsSI_u = self.to_PropsSI('u', value[1])

        self._T = self.to_SI('T', value[0])
        self._u = self.to_SI('u', value[1])
        self._p = Q_(PropsSI('P', 'T', PropsSI_T, 'U', PropsSI_u, self.sub), self.SI_units['p'])
        self._s = Q_(PropsSI('S', 'T', PropsSI_T, 'U', PropsSI_u, self.sub), self.SI_units['s'])
        self._v = Q_(1.0/PropsSI('D', 'T', PropsSI_T, 'U', PropsSI_u, self.sub), self.SI_units['v'])
        self._h = Q_(PropsSI('H', 'T', PropsSI_T, 'U', PropsSI_u, self.sub), self.SI_units['h'])
        self._x = Q_(PropsSI('Q', 'T', PropsSI_T, 'U', PropsSI_u, self.sub), self.SI_units['x'])
        if self._x == -1.0:
            self._x = None

    @property
    def uT(self):
        return self._u, self._T

    @uT.setter
    def uT(self, value):
        self.Tu = value[1], value[0]

    @property
    def Th(self):
        return self._T, self._h

    @Th.setter
    def Th(self, value):
        raise StateError('Setting T and h simultaneously is not allowed.')
        self._check_dimensions(['T', 'h'], value)
        PropsSI_T = self.to_PropsSI('T', value[0])
        PropsSI_h = self.to_PropsSI('h', value[1])

        self._T = self.to_SI('T', value[0])
        self._h = self.to_SI('h', value[1])
        self._p = Q_(PropsSI('P', 'T', PropsSI_T, 'H', PropsSI_h, self.sub), self.SI_units['p'])
        self._s = Q_(PropsSI('S', 'T', PropsSI_T, 'H', PropsSI_h, self.sub), self.SI_units['s'])
        self._v = Q_(1.0/PropsSI('D', 'T', PropsSI_T, 'H', PropsSI_h, self.sub), self.SI_units['v'])
        self._u = Q_(PropsSI('U', 'T', PropsSI_T, 'H', PropsSI_h, self.sub), self.SI_units['u'])
        self._x = Q_(PropsSI('Q', 'T', PropsSI_T, 'H', PropsSI_h, self.sub), self.SI_units['x'])
        if self._x == -1.0:
            self._x = None

    @property
    def hT(self):
        return self._h, self._T

    @hT.setter
    def hT(self, value):
        self.Th = value[1], value[0]

    @property
    def Ts(self):
        return self._T, self._s

    @Ts.setter
    def Ts(self, value):
        self._check_dimensions(['T', 's'], value)
        PropsSI_T = self.to_PropsSI('T', value[0])
        PropsSI_s = self.to_PropsSI('s', value[1])

        self._T = self.to_SI('T', value[0])
        self._s = self.to_SI('s', value[1])
        self._p = Q_(PropsSI('P', 'T', PropsSI_T, 'S', PropsSI_s, self.sub), self.SI_units['p'])
        self._h = Q_(PropsSI('H', 'T', PropsSI_T, 'S', PropsSI_s, self.sub), self.SI_units['h'])
        self._v = Q_(1.0/PropsSI('D', 'T', PropsSI_T, 'S', PropsSI_s, self.sub), self.SI_units['v'])
        self._u = Q_(PropsSI('U', 'T', PropsSI_T, 'S', PropsSI_s, self.sub), self.SI_units['u'])
        self._x = Q_(PropsSI('Q', 'T', PropsSI_T, 'S', PropsSI_s, self.sub), self.SI_units['x'])
        if self._x == -1.0:
            self._x = None

    @property
    def sT(self):
        return self._s, self._T

    @sT.setter
    def sT(self, value):
        self.Ts = value[1], value[0]

    @property
    def Tv(self):
        return self._T, self._v

    @Tv.setter
    def Tv(self, value):
        self._check_dimensions(['T', 'v'], value)
        PropsSI_T = self.to_PropsSI('T', value[0])
        PropsSI_v = self.to_PropsSI('v', value[1])
        PropsSI_d = 1.0/PropsSI_v

        self._T = self.to_SI('T', value[0])
        self._v = self.to_SI('v', value[1])
        self._p = Q_(PropsSI('P', 'T', PropsSI_T, 'D', PropsSI_d, self.sub), self.SI_units['p'])
        self._h = Q_(PropsSI('H', 'T', PropsSI_T, 'D', PropsSI_d, self.sub), self.SI_units['h'])
        self._s = Q_(PropsSI('S', 'T', PropsSI_T, 'D', PropsSI_d, self.sub), self.SI_units['s'])
        self._u = Q_(PropsSI('U', 'T', PropsSI_T, 'D', PropsSI_d, self.sub), self.SI_units['u'])
        self._x = Q_(PropsSI('Q', 'T', PropsSI_T, 'D', PropsSI_d, self.sub), self.SI_units['x'])
        if self._x == -1.0:
            self._x = None

    @property
    def vT(self):
        return self._v, self._T

    @vT.setter
    def vT(self, value):
        self.Tv = value[1], value[0]

    @property
    def Tx(self):
        return self._T, self._x

    @Tx.setter
    def Tx(self, value):
        self._check_dimensions(['T', 'x'], value)
        PropsSI_T = self.to_PropsSI('T', value[0])
        PropsSI_x = self.to_PropsSI('x', value[1])

        self._T = self.to_SI('T', value[0])
        self._x = self.to_SI('x', value[1])
        self._p = Q_(PropsSI('P', 'T', PropsSI_T, 'Q', PropsSI_x, self.sub), self.SI_units['p'])
        self._h = Q_(PropsSI('H', 'T', PropsSI_T, 'Q', PropsSI_x, self.sub), self.SI_units['h'])
        self._s = Q_(PropsSI('S', 'T', PropsSI_T, 'Q', PropsSI_x, self.sub), self.SI_units['s'])
        self._u = Q_(PropsSI('U', 'T', PropsSI_T, 'Q', PropsSI_x, self.sub), self.SI_units['u'])
        self._v = Q_(1.0/PropsSI('D', 'T', PropsSI_T, 'Q', PropsSI_x, self.sub), self.SI_units['v'])

    @property
    def xT(self):
        return self._x, self._T

    @xT.setter
    def xT(self, value):
        self.Tx = value[1], value[0]
