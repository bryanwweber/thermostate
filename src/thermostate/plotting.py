"""Base Plotting module."""
from . import State, units
from CoolProp.CoolProp import PropsSI
import matplotlib.pyplot as plt
import numpy as np
from abc import ABC, abstractmethod

from dataclasses import dataclass, field


@dataclass
class PlottedState:
    """Data class to efficiently store states in the self.states dictionary."""

    key: str
    state: State
    # key: Plot axes string (Tv, pv)
    # value: Line2D instance for that plot of the marker for this state
    markers: dict = field(default_factory=dict)


class PlottingBase(ABC):
    """Basic Plotting manager for thermodynamic states.

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

    axis_units = {
        "v": "m**3/kg",
        "T": "K",
        "s": "J/(kg*K)",
        "p": "pascal",
        "u": "J/kg",
        "h": "J/kg",
        "x": "dimensionless",
    }

    allowed_processes = {
        "isochoric": "v",
        "isovolumetric": "v",
        "isobaric": "p",
        "isothermal": "T",
        "isoenergetic": "u",
        "isoenthalpic": "h",
        "isentropic": "s"
    }

    def __init__(self):
        self.states = {}
        self.plots = {}
        self.processes = {}

    @abstractmethod
    def plot(self, x_axis, y_axis):  # pragma: no cover
        """Hold the place of a plot function that a child class must establish."""
        pass

    def add_state(self, state, key=None):
        """Add a state to the self.states dictionary and plot it."""
        if key is None:
            key = repr(state)

        plotted_state = PlottedState(key=key, state=state)

        for plot_key, value in self.plots.items():
            x_data = []
            y_data = []
            fig, axis = value
            x_axis, y_axis = plot_key
            x_data.append(getattr(state, x_axis).magnitude)
            y_data.append(getattr(state, y_axis).magnitude)
            x_data = np.array(x_data) * getattr(units, self.axis_units[x_axis])
            y_data = np.array(y_data) * getattr(units, self.axis_units[y_axis])
            (line,) = axis.plot(x_data, y_data, marker="o")
            plotted_state.markers[plot_key] = line

        self.states[key] = plotted_state

    def remove_state(self, state=None, key=None):
        """Remove a state from the self.states dictionary and plots."""
        if state is None and key is None:
            raise ValueError("No state or key was entered. Unable to find state")
        if state is not None and repr(state) in self.states:
            state_to_be_removed = self.states[repr(state)]
        elif key is not None and key in self.states:
            state_to_be_removed = self.states[key]
        elif key is not None and key not in self.states and state is None:
            raise ValueError("Couldn't find key")
        else:
            for key, s_2 in self.states.items():
                if state == s_2.state:
                    state_to_be_removed = self.states[key]
                    break
            else:
                raise ValueError("Couldn't find the state")

        for line in state_to_be_removed.markers.values():
            line.remove()
        del self.states[state_to_be_removed.key]

    def remove_process(self, state_1, state_2, remove_states=False):
        """Remove a process from the self.process dictionary.

        The process to be removed is specified by the states that were used to
        initially create the process. It is optional to keep the points associated
        with the states while still removing the line object.
        """
        key_1 = None
        key_2 = None
        for key, plotted_state in self.states.items():
            if state_1 is plotted_state.state:
                key_1 = key
            if state_2 is plotted_state.state:
                key_2 = key

        for line in self.processes[key_1 + key_2].values():
            line.remove()
        del self.processes[key_1 + key_2]

        if remove_states:
            self.remove_state(state_1)
            self.remove_state(state_2)

    def add_process(self, state_1, state_2, process_type=None):
        """Add a thermodynamic process to the self.process dictionary and plots it.

        A property of the states is held constant and all intermediate states are traced
        out in a line between the two states on the graph. The property that is held
        constant is specified by the user with the process_type input.
        If no property is to be held constant then a straight line between the
        two points is drawn.
        """

        if process_type not in self.allowed_processes.keys():
            raise ValueError("Not a supported process type")
        
        if process_type is not None:
            constant1 = getattr(state_1, self.allowed_processes[process_type])
            constant2 = getattr(state_2, self.allowed_processes[process_type])
            if not np.isclose(constant1,constant2):
                raise ValueError("Property was not held constant")

        missing_state_1 = True
        missing_state_2 = True
        key_1 = None
        key_2 = None
        sub1 = state_1.sub
        sub2 = state_2.sub
        if sub1 != sub2:
            raise ValueError("Substance of input states do not match")

        for key, plotted_state in self.states.items():
            if state_1 is plotted_state.state:
                missing_state_1 = False
                key_1 = key
            if state_2 is plotted_state.state:
                missing_state_2 = False
                key_2 = key

        if missing_state_1:
            key_1 = repr(state_1)
            self.add_state(state_1, key_1)

        if missing_state_2:
            key_2 = repr(state_2)
            self.add_state(state_2, key_2)

        plot_key = key_1 + key_2

        self.processes[plot_key] = {}

        if process_type in ("isochoric", "isovolumetric"):
            p_1 = np.log10(state_1.p.magnitude)
            p_2 = np.log10(state_2.p.magnitude)
            v_range = np.logspace(p_1, p_2)*units.pascal
        elif process_type is not None:
            v_1 = np.log10(state_1.v.magnitude)
            v_2 = np.log10(state_2.v.magnitude)
            # Due to numerical approximation by CoolProp, an error occurs
            # if the state is too close to a saturated liquid. Here an
            # imperceptibly small offset is introduced to the specific volume 
            # to avoid this error. 
            if np.isclose(state_1.x.magnitude,0.0):
                v_1 *= 1.0 + 1.0E-14
            if np.isclose(state_2.x.magnitude, 0.0):
                v_2 *= 1.0 + 1.0E-14
            v_range = np.logspace(v_1, v_2) * units("m**3/kg")

        for key, value in self.plots.items():
            x_data = []
            y_data = []
            fig, axis = value
            x_axis, y_axis = key

            if process_type is None:
                x_data.append(getattr(state_1, x_axis).magnitude)
                y_data.append(getattr(state_1, y_axis).magnitude)
                x_data.append(getattr(state_2, x_axis).magnitude)
                y_data.append(getattr(state_2, y_axis).magnitude)

                x_data = np.array(x_data) * getattr(units, self.axis_units[x_axis])
                y_data = np.array(y_data) * getattr(units, self.axis_units[y_axis])
                (line,) = axis.plot(x_data, y_data, marker="None", linestyle="--")
                self.processes[plot_key][key] = line
            else:
                state = State(state_1.substance)
                for v in v_range:
                    if process_type == "isochoric" or process_type == "isovolumetric":
                        state.pv = v, state_1.v
                    elif process_type == "isobaric":
                        state.pv = state_1.p, v
                    elif process_type == "isothermal":
                        state.Tv = state_1.T, v
                    elif process_type == "isoenergetic":
                        state.uv = state_1.u, v
                    elif process_type == "isoenthalpic":
                        state.hv = state_1.h, v
                    elif process_type == "isentropic":
                        state.sv = state_1.s, v

                    x_data.append(getattr(state, x_axis).magnitude)
                    y_data.append(getattr(state, y_axis).magnitude)

                x_data = np.array(x_data) * getattr(units, self.axis_units[x_axis])
                y_data = np.array(y_data) * getattr(units, self.axis_units[y_axis])
                (line,) = axis.plot(x_data, y_data, linestyle="-")
                self.processes[plot_key][key] = line

    def set_xscale(self, x_axis, y_axis, scale="linear"):
        """Acceses a plot in self.plots and changes the scale of its x axis."""
        key = x_axis + y_axis
        fig, axis = self.plots[key]
        axis.set_xscale(scale)

    def set_yscale(self, x_axis, y_axis, scale="linear"):
        """Acceses a plot in self.plots and changes the scale of its y axis."""
        key = x_axis + y_axis
        fig, axis = self.plots[key]
        axis.set_yscale(scale)


class VaporDome(PlottingBase):
    """Class for plotting graphs with a vapor dome."""

    def __init__(self, substance, *args):
        super(VaporDome, self).__init__()
        min_temp = PropsSI("Tmin", substance)
        max_temp = PropsSI("Tcrit", substance)

        T_range = np.logspace(np.log10(min_temp), np.log10(max_temp), 400) * units.K
        self.st_f = [State(substance, T=T, x=0 * units.dimensionless) for T in T_range]
        self.st_g = [State(substance, T=T, x=1 * units.dimensionless) for T in T_range]
        for axes in args:
            self.plot(axes[0], axes[1])

    def plot(self, x_axis, y_axis):
        """Add a plot with a vapor dome to this instance with given x and y axes.

        Parameters
        -----------
        x_axis: 'str'
            The string representing the x axis for this plot. Allowed axes are
            "T", "p", "u", "s", "v", and "h".
        y_axis: 'str'
            The string representing the y axis for this plot. Allowed axes are
            "T", "p", "u", "s", "v", and "h".
        """
        if x_axis + y_axis not in self.plots:
            fig, axis = plt.subplots()
            self.plots[x_axis + y_axis] = (fig, axis)

            x_f = [getattr(st, x_axis).magnitude for st in self.st_f]
            x_f = np.array(x_f) * getattr(units, self.axis_units[x_axis])
            y_f = [getattr(st, y_axis).magnitude for st in self.st_f]
            y_f = np.array(y_f) * getattr(units, self.axis_units[y_axis])
            axis.plot(x_f, y_f)

            x_g = np.array(
                [getattr(st, x_axis).magnitude for st in self.st_g]
            ) * getattr(units, self.axis_units[x_axis])
            y_g = np.array(
                [getattr(st, y_axis).magnitude for st in self.st_g]
            ) * getattr(units, self.axis_units[y_axis])
            axis.plot(x_g, y_g)
            if x_axis in ("p", "v"):
                self.set_xscale(x_axis, y_axis, "log")
            if y_axis in ("p", "v"):
                self.set_yscale(x_axis, y_axis, "log")
        else:
            raise ValueError("Plot has already been added to this class instance")


class IdealGas(PlottingBase):
    """Class for plotting graphs modeled as an Ideal Gas."""

    def __init__(self, *args):
        super(IdealGas, self).__init__()
        for axes in args:
            self.plot(axes[0], axes[1])

    def plot(self, x_axis, y_axis):
        """Add a plot to this instance with given x and y axes.

        Parameters
        -----------
        x_axis: 'str'
            The string representing the x axis for this plot. Allowed axes are
            "T", "p", "u", "s", "v", and "h".
        y_axis: 'str'
            The string representing the y axis for this plot. Allowed axes are
            "T", "p", "u", "s", "v", and "h".
        """
        if x_axis + y_axis not in self.plots:
            fig, axis = plt.subplots()
            self.plots[x_axis + y_axis] = (fig, axis)
        else:
            raise ValueError("Plot has already been added to this class instance")
