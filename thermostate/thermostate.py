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
            setattr(self, 'Tp', (Q_(300., 'K'), Q_(101325., 'Pa')))

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

    def _set_properties(self, known_props, known_values):
        if len(known_props) != 2 or len(known_values) != 2 or len(known_props) != len(known_values):
            raise StateError('Only specify two properties to _set_properties')

        all_props = 'Tpuvhsx'

        props = []
        vals = []

        for prop, val in zip(known_props, known_values):
            if prop == 'x':
                props.append('Q')
                vals.append(self.to_PropsSI('x', val))
            elif prop == 'v':
                props.append('D')
                vals.append(1.0/self.to_PropsSI('v', val))
            else:
                props.append(prop.upper())
                vals.append(self.to_PropsSI(prop, val))

            setattr(self, '_' + prop, self.to_SI(prop, val))

        unknown_props = all_props.replace(known_props[0], '').replace(known_props[1], '')

        for prop in unknown_props:
            if prop == 'v':
                value = Q_(1.0/PropsSI('D', props[0], vals[0], props[1], vals[1], self.sub),
                           self.SI_units[prop])
            elif prop == 'x':
                value = Q_(PropsSI('Q', props[0], vals[0], props[1], vals[1], self.sub),
                           self.SI_units[prop])
                if value == -1.0:
                    value = None
            else:
                value = Q_(PropsSI(prop.upper(), props[0], vals[0], props[1], vals[1], self.sub),
                           self.SI_units[prop])

            setattr(self, '_' + prop, value)

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
        try:
            PropsSI('Phase',
                    'T', self.to_PropsSI('T', value[0]),
                    'P', self.to_PropsSI('p', value[1]),
                    self.sub)
        except ValueError as e:
            if 'Saturation pressure' in str(e):
                raise StateError('The given values for T and P are not independent.')
            else:
                raise

        self._set_properties(['T', 'p'], value)

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
        self._set_properties(['T', 'u'], value)

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
        self._set_properties(['T', 'h'], value)

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

        self._set_properties(['T', 's'], value)

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
        self._set_properties(['T', 'v'], value)

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
        self._set_properties(['T', 'x'], value)

    @property
    def xT(self):
        return self._x, self._T

    @xT.setter
    def xT(self, value):
        self.Tx = value[1], value[0]

    @property
    def pu(self):
        return self._p, self._u

    @pu.setter
    def pu(self, value):
        self._check_dimensions(['p', 'u'], value)
        self._set_properties(['p', 'u'], value)

    @property
    def up(self):
        return self._u, self._p

    @up.setter
    def up(self, value):
        self.pu = value[1], value[0]

    @property
    def ps(self):
        return self._p, self._s

    @ps.setter
    def ps(self, value):
        self._check_dimensions(['p', 's'], value)
        self._set_properties(['p', 's'], value)

    @property
    def sp(self):
        return self._s, self._p

    @sp.setter
    def sp(self, value):
        self.ps = value[1], value[0]

    @property
    def pv(self):
        return self._p, self._v

    @pv.setter
    def pv(self, value):
        self._check_dimensions(['p', 'v'], value)
        self._set_properties(['p', 'v'], value)

    @property
    def vp(self):
        return self._v, self._p

    @vp.setter
    def vp(self, value):
        self.pv = value[1], value[0]

    @property
    def ph(self):
        return self._p, self._h

    @ph.setter
    def ph(self, value):
        self._check_dimensions(['p', 'h'], value)
        self._set_properties(['p', 'h'], value)

    @property
    def hp(self):
        return self._h, self._p

    @hp.setter
    def hp(self, value):
        self.ph = value[1], value[0]

    @property
    def px(self):
        return self._p, self._x

    @px.setter
    def px(self, value):
        self._check_dimensions(['p', 'x'], value)
        self._set_properties(['p', 'x'], value)

    @property
    def xp(self):
        return self._x, self._p

    @xp.setter
    def xp(self, value):
        self.px = value[1], value[0]

    @property
    def us(self):
        return self._u, self._s

    @us.setter
    def us(self, value):
        raise StateError('Setting s and u simultaneously is not allowed.')
        self._check_dimensions(['u', 's'], value)
        self._set_properties(['u', 's'], value)

    @property
    def su(self):
        return self._s, self._u

    @su.setter
    def su(self, value):
        self.us = value[1], value[0]
