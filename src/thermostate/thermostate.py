"""Base ThermoState module."""
# Needed to support Python < 3.9
from __future__ import annotations
import sys
from typing import TYPE_CHECKING
import enum
from collections import OrderedDict

import CoolProp
from pint import UnitRegistry, DimensionalityError
from pint.unit import UnitsContainer, UnitDefinition
from pint.converters import ScaleConverter
import numpy as np

from .abbreviations import (
    SystemInternational as default_SI,
    EnglishEngineering as default_EE,
)

try:  # pragma: no cover
    from IPython.core.ultratb import AutoFormattedTB

except ImportError:  # pragma: no cover
    AutoFormattedTB = None

if TYPE_CHECKING:  # pragma: no cover
    import pint
    from typing import Union

units = UnitRegistry(autoconvert_offset_to_baseunit=True)
Q_ = units.Quantity
units.define(UnitDefinition("percent", "pct", (), ScaleConverter(1.0 / 100.0)))
units.setup_matplotlib()

default_units = None


def set_default_units(units):
    """Set default units to be used in class initialization."""
    if units is None or units in ("SI", "EE"):
        global default_units
        default_units = units
    else:
        raise TypeError(
            f"The given units '{units!r}' are not supported. Must be 'SI', "
            "'EE', or None."
        )


# Don't add the _render_traceback_ function to DimensionalityError if
# IPython isn't present. This function is only used by the IPython/ipykernel
# anyways, so it doesn't matter if it's missing if IPython isn't available.
if AutoFormattedTB is not None:  # pragma: no cover

    def render_traceback(self: DimensionalityError):
        """Render a minimized version of the DimensionalityError traceback.

        The default Jupyter/IPython traceback includes a lot of
        context from within pint that actually raises the
        DimensionalityError. This context isn't really needed for
        this particular error, since the problem is almost certainly in
        the user code. This function removes the additional context.
        """
        a = AutoFormattedTB(
            mode="Context", color_scheme="Neutral", tb_offset=1
        )  # type: ignore
        etype, evalue, tb = sys.exc_info()
        stb = a.structured_traceback(etype, evalue, tb, tb_offset=1)
        for i, line in enumerate(stb):
            if "site-packages" in line:
                first_line = slice(i)
                break
        else:
            # This is deliberately an "else" on the for loop
            first_line = slice(-1)
        return stb[first_line] + stb[-1:]

    DimensionalityError._render_traceback_ = render_traceback.__get__(  # type: ignore
        DimensionalityError
    )


class CoolPropPhaseNames(enum.Enum):
    """Map the phase names in CoolProp."""

    critical_point = CoolProp.iphase_critical_point
    gas = CoolProp.iphase_gas
    liquid = CoolProp.iphase_liquid
    not_imposed = CoolProp.iphase_not_imposed
    supercritical = CoolProp.iphase_supercritical
    supercritical_gas = CoolProp.iphase_supercritical_gas
    supercritical_liquid = CoolProp.iphase_supercritical_liquid
    twophase = CoolProp.iphase_twophase
    unknown = CoolProp.iphase_unknown


def munge_coolprop_input_prop(prop: str) -> str:
    """Munge an input property pair from CoolProp into our format.

    Example CoolProp input: ``XY_INPUTS``, where ``X`` and ``Y`` are one of
    ``T``, ``P``, ``Dmass``, ``Hmass``, ``Umass``, ``Q``, or ``Smass``. For
    use in ThermoState, we use lower case letters (except for T), replace
    ``D`` with ``v``, and replace ``Q`` with ``x``.

    Examples
    --------
    * ``DmassHmass_INPUTS``: ``vh``
    * ``DmassT_INPUTS``: ``vT``
    * ``PUmass_INPUTS``: ``pu``

    """
    prop = prop.replace("_INPUTS", "").replace("mass", "").replace("D", "V")
    return prop.replace("Q", "X").lower().replace("t", "T")


class StateError(Exception):
    """Errors associated with setting the `State` object."""

    def _render_traceback_(self):  # pragma: no cover
        """Render a minimized version of the `StateError` traceback.

        The default Jupyter/IPython traceback includes a lot of
        context from within `State` where the `StateError` is raised.
        This context isn't really needed, since the problem is almost certainly in
        the user code. This function removes the additional context.
        """
        if AutoFormattedTB is not None:
            a = AutoFormattedTB(mode="Context", color_scheme="Neutral", tb_offset=1)
            etype, evalue, tb = sys.exc_info()
            stb = a.structured_traceback(etype, evalue, tb, tb_offset=1)
            for i, line in enumerate(stb):
                if "site-packages" in line:
                    first_line = slice(i)
                    break
            else:
                first_line = slice(-1)
            return stb[first_line] + stb[-1:]


class State(object):
    """Basic State manager for thermodyanmic states.

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

    _allowed_subs = [
        "AIR",
        "AMMONIA",
        "WATER",
        "PROPANE",
        "R134A",
        "R22",
        "ISOBUTANE",
        "CARBONDIOXIDE",
        "OXYGEN",
        "NITROGEN",
    ]

    _all_pairs = set(
        munge_coolprop_input_prop(k)
        for k in dir(CoolProp.constants)
        if "INPUTS" in k and "molar" not in k
    )
    _all_pairs.update([k[::-1] for k in _all_pairs])

    _unsupported_pairs = {"Tu", "Th", "us", "hx"}
    _unsupported_pairs.update([k[::-1] for k in _unsupported_pairs])

    _allowed_pairs = _all_pairs - _unsupported_pairs

    _all_props = set("Tpvuhsx")

    _read_only_props = {"cp", "cv", "phase"}

    _dimensions = {
        "T": UnitsContainer({"[temperature]": 1.0}),
        "p": UnitsContainer({"[mass]": 1.0, "[length]": -1.0, "[time]": -2.0}),
        "v": UnitsContainer({"[length]": 3.0, "[mass]": -1.0}),
        "u": UnitsContainer({"[length]": 2.0, "[time]": -2.0}),
        "h": UnitsContainer({"[length]": 2.0, "[time]": -2.0}),
        "s": UnitsContainer({"[length]": 2.0, "[time]": -2.0, "[temperature]": -1.0}),
        "x": UnitsContainer({}),
    }

    _SI_units = {
        "T": "kelvin",
        "p": "pascal",
        "v": "meter**3/kilogram",
        "u": "joules/kilogram",
        "h": "joules/kilogram",
        "s": "joules/(kilogram*kelvin)",
        "x": "dimensionless",
        "cp": "joules/(kilogram*kelvin)",
        "cv": "joules/(kilogram*kelvin)",
    }

    def __setattr__(
        self,
        key: str,
        value: "Union[str, pint.Quantity, tuple[pint.Quantity, pint.Quantity]]",
    ) -> None:
        if key.startswith("_") or key in ("sub", "label", "units"):
            object.__setattr__(self, key, value)
        elif key in self._allowed_pairs:
            if not isinstance(value, tuple):  # pragma: no cover, for typing
                raise ValueError("Must pass a tuple of Quantities")
            self._check_dimensions(key, value)
            self._check_values(key, value)
            self._set_properties(key, value)
        elif key in self._unsupported_pairs:
            raise StateError(
                f"The pair of input properties entered ({key}) isn't supported yet. "
                "Sorry!"
            )
        else:
            raise AttributeError(f"Unknown attribute {key}")

    def __getattr__(
        self, key: str
    ) -> "Union[str, tuple[pint.Quantity, pint.Quantity], pint.Quantity]":
        if key in self._all_props:
            return object.__getattribute__(self, "_" + key)
        elif key in self._all_pairs:
            val_0 = object.__getattribute__(self, "_" + key[0])
            val_1 = object.__getattribute__(self, "_" + key[1])
            return val_0, val_1
        elif key == "phase":
            return object.__getattribute__(self, "_" + key)
        elif key in self._read_only_props:
            return object.__getattribute__(self, "_" + key)
        else:
            raise AttributeError(f"Unknown attribute {key}")

    def __eq__(self, other: object) -> bool:
        """Check if two `State`s are equivalent.

        Check that they are using the same substance and two properties that are
        always independent. Choose T and v because the EOS tends to be defined
        in terms of T and density.
        """
        if not isinstance(other, State):
            return NotImplemented
        if (
            self.sub == other.sub
            # Pylance does not support NumPy ufuncs
            and np.isclose(other.T, self.T)  # type: ignore
            and np.isclose(other.v, self.v)  # type: ignore
        ):
            return True
        return False

    def __le__(self, other: "State"):
        return NotImplemented

    def __lt__(self, other: "State"):
        return NotImplemented

    def __gt__(self, other: "State"):
        return NotImplemented

    def __ge__(self, other: "State"):
        return NotImplemented

    def __init__(
        self, substance: str, label=None, units=None, **kwargs: "pint.Quantity"
    ):

        if units is None:
            units = default_units
        self.units = units

        self.label = label

        if substance.upper() in self._allowed_subs:
            self.sub = substance.upper()
        else:
            raise ValueError(
                f"{substance} is not an allowed substance. "
                f"Choose one of {self._allowed_subs}."
            )

        self._abstract_state = CoolProp.AbstractState("HEOS", self.sub)

        input_props = ""
        for arg in kwargs:
            if arg not in self._all_props:
                raise ValueError(f"The argument {arg} is not allowed.")
            else:
                input_props += arg

        if len(input_props) > 2 or len(input_props) == 1:
            raise ValueError(
                "Incorrect number of properties specified. Must be 2 or 0."
            )

        if len(input_props) > 0 and input_props not in self._allowed_pairs:
            raise StateError(
                f"The pair of input properties entered ({input_props}) isn't supported "
                "yet. Sorry!"
            )

        if len(input_props) > 0:
            setattr(self, input_props, (kwargs[input_props[0]], kwargs[input_props[1]]))

    @property
    def label(self):
        """Get or set the string label for this state, used in plotting."""
        return self._label

    @label.setter
    def label(self, value: str | None):
        if value is None:
            self._label = value
            return
        try:
            label = str(value)
        except Exception:
            raise TypeError(
                f"The given label '{value!r}' could not be converted to a string"
            ) from None
        self._label = label

    @property
    def units(self):
        """Get or set the string units for this state to set attribute units."""
        return self._units

    @units.setter
    def units(self, value: str | None):
        if value is None or value in ("EE", "SI"):
            self._units = value
            if hasattr(self, "T"):
                setattr(self, "Tv", (self.T, self.v))
        else:
            raise TypeError(
                f"The given units '{units!r}' are not supported. Must be 'SI', "
                "'EE', or None."
            )

    def to_SI(self, prop: str, value: "pint.Quantity") -> "pint.Quantity":
        """Convert the input ``value`` to the appropriate SI base units."""
        return value.to(self._SI_units[prop])

    def to_PropsSI(self, prop: str, value: "pint.Quantity") -> float:  # noqa: D403
        """CoolProp can't handle Pint Quantites so return the magnitude only.

        Convert to the appropriate SI units first.
        """  # noqa: D403
        return self.to_SI(prop, value).magnitude

    @staticmethod
    def _check_values(
        properties: str, values: "tuple[pint.Quantity, pint.Quantity]"
    ) -> None:
        for p, v in zip(properties, values):
            if p in "Tvp" and v.to_base_units().magnitude < 0.0:
                raise StateError(f"The value of {p} must be positive in absolute units")
            elif p == "x" and not (0.0 <= v.to_base_units().magnitude <= 1.0):
                raise StateError("The value of the quality must be between 0 and 1")

    def _check_dimensions(
        self, properties: str, values: "tuple[pint.Quantity, pint.Quantity]"
    ) -> None:
        for p, v in zip(properties, values):
            # Dimensionless values are a special case and don't work with
            # the "check" method.
            try:
                valid = v.check(self._SI_units[p])
            except KeyError:
                valid = v.dimensionality == self._dimensions[p]
            if not valid:
                raise StateError(
                    f"The dimensions for {p} must be {self._dimensions[p]}"
                )

    def _set_properties(
        self, known_props: str, known_values: "tuple[pint.Quantity, pint.Quantity]"
    ) -> None:
        known_state: OrderedDict[str, float] = OrderedDict()

        for prop, val in zip(known_props, known_values):
            if prop == "x":
                known_state["Q"] = self.to_PropsSI(prop, val)
            elif prop == "v":
                known_state["Dmass"] = 1.0 / self.to_PropsSI(prop, val)
            else:
                postfix = "" if prop in ["T", "p"] else "mass"
                known_state[prop.upper() + postfix] = self.to_PropsSI(prop, val)

        for key in sorted(known_state):
            known_state.move_to_end(key)

        inputs = getattr(CoolProp, "".join(known_state.keys()) + "_INPUTS")
        try:
            self._abstract_state.update(inputs, *known_state.values())
        except ValueError as e:
            if "Saturation pressure" in str(e):
                raise StateError(
                    f"The given values for {known_props[0]} and {known_props[1]} are "
                    "not independent."
                )
            else:
                raise

        for prop in self._all_props.union(self._read_only_props):
            if prop == "v":
                v = 1.0 / self._abstract_state.keyed_output(CoolProp.iDmass)
                value = v * units(self._SI_units[prop])
            elif prop == "x":
                x = self._abstract_state.keyed_output(CoolProp.iQ)
                if x == -1.0:
                    value = None
                else:
                    value = x * units(self._SI_units[prop])
            elif prop == "phase":
                value = CoolPropPhaseNames(
                    self._abstract_state.keyed_output(CoolProp.iPhase)
                ).name
            else:
                postfix = "" if prop in "Tp" else "mass"
                p = getattr(CoolProp, "i" + prop.title() + postfix)
                value = self._abstract_state.keyed_output(p) * units(
                    self._SI_units[prop]
                )

            set_units = None
            if self.units == "SI":
                set_units = getattr(default_SI, prop, None)
            elif self.units == "EE":
                set_units = getattr(default_EE, prop, None)
            if set_units is not None:
                value.ito(set_units)
            setattr(self, "_" + prop, value)
