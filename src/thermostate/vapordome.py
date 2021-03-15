get_ipython().run_line_magic('matplotlib', 'notebook')
from thermostate import State, units
from CoolProp.CoolProp import PropsSI
import matplotlib.pyplot as plt
import matplotlib.lines as lines
import numpy as np


from dataclasses import dataclass, field

@dataclass
class PlottedState:
    # https://realpython.com/python-data-classes/
    key: str
    state: State
    # key: Plot axes string (Tv, pv)
    # value: Line2D instance for that plot of the marker for this state
    markers: dict = field(default_factory=dict)

class VaporDome:
    axis_units = {"v": "m**3/kg", "T": "K", "s": "J/(kg*K)", "p": "pascal", "u": "J/kg","h": "J/kg","x": "dimensionless" }
    def __init__(self, *args):
        min_temperature = PropsSI('Tmin','water')
        max_temperature = PropsSI('Tcrit','water')
        T_range = np.logspace(np.log10(min_temperature), np.log10(max_temperature),400)*units.K
        self.st_f = [State("water", T=T, x=0*units.dimensionless) for T in T_range]
        self.st_g = [State("water", T=T, x=1*units.dimensionless) for T in T_range]
        self.states = {}
        self.plots = {}
        self.processes = {}
        for axes in args:
            self.plot(axes[0],axes[1])
    def plot(self, x_axis, y_axis):
        if x_axis + y_axis not in self.plots:
            fig, axis = plt.subplots()
            self.plots[x_axis + y_axis] = (fig, axis)
            
            x_f = [getattr(st, x_axis).magnitude for st in self.st_f]
            x_f = np.array(x_f)*getattr(units, self.axis_units[x_axis])
            y_f = [getattr(st, y_axis).magnitude for st in self.st_f]
            y_f = np.array(y_f)*getattr(units, self.axis_units[y_axis])
            axis.plot(x_f, y_f)

            x_g = np.array([getattr(st, x_axis).magnitude for st in self.st_g])*getattr(units, self.axis_units[x_axis])
            y_g = np.array([getattr(st, y_axis).magnitude for st in self.st_g])*getattr(units, self.axis_units[y_axis])
            axis.plot(x_g, y_g)
            if x_axis == 'p' or x_axis == 'v':
                self.set_xscale(x_axis,y_axis, 'log')
            if y_axis == 'p' or y_axis == 'v':
                self.set_yscale(x_axis,y_axis, 'log')
                

    def add_state(self, state, key=None):
        if not self.plots:
            raise ValueError("Must call .plot first")
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
            line, = axis.plot(x_data, y_data, marker="o")
            plotted_state.markers[plot_key] = line

        self.states[key] = plotted_state

    def remove_state(self, state=None, key=None):
        # https://stackoverflow.com/questions/19569052/matplotlib-how-to-remove-a-specific-line-or-curve
        if state is None and key is None:
            raise ValueError("""Raise a useful error message""")

        # This can be simplified, will have to change for the PlottedState change
        if state is not None and repr(state) in self.states:
            print("found repr")
            state_to_be_removed = self.states[repr(state)]
        elif key is not None and key in self.states:
            print("found key")
            state_to_be_removed = self.states[key]
        elif key is not None and key not in self.states and state is None:
#             print("Couldn't find key")
            raise ValueError("""Couldn't find key""")

        else:
            for key, s_2 in self.states.items():
                if state == s_2.state:
                    print("state found, Altered key:",key)
                    state_to_be_removed = self.states[key]
                    break
            # This is a for/else clause
            # https://book.pythontips.com/en/latest/for_-_else.html
            else:
                raise ValueError("""Couldn't find the state""")
#                 print("Couldn't find the state")

        for line in state_to_be_removed.markers.values():
            line.remove()
        del self.states[state_to_be_removed.key]

    def remove_process(self, state_1, state_2, remove_states=False):
#         for line in self.processes[state_1.key + state_2.key].values():
#             line.remove()
#         del self.processes[state_1.key + state_2.key]
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
        # Need to retrieve or create the PlottedState object for
        # each passed in state

        missing_state_1 = True
        missing_state_2 = True
        key_1 = None
        key_2 = None
        
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

#         plot_key = state_1.key + state_2.key

        self.processes[plot_key] = {}
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

                x_data = np.array(x_data)*getattr(units, self.axis_units[x_axis])
                y_data = np.array(y_data)*getattr(units, self.axis_units[y_axis])
                line, = axis.plot(x_data, y_data, marker='None', linestyle='--')
                self.processes[plot_key][key] = line

            elif process_type == "isobaric":
                if not np.isclose(state_1.p, state_2.p):
                    raise ValueError()
                v_range = np.logspace(np.log10(state_1.v.magnitude), np.log10(state_2.v.magnitude))*units.m**3/units.kg  # might need to use magnitude and multiply by units
                state = State("water", p=state_1.p, v=v_range[0])

            elif process_type == "isothermal":
                if not np.isclose(state_1.T, state_2.T):
                    raise ValueError()
                v_range = np.logspace(np.log10(state_1.v.magnitude), np.log10(state_2.v.magnitude))*units.m**3/units.kg  # might need to use magnitude and multiply by units
                state = State("water", T=state_1.T, v=v_range[0])

            elif process_type == "isoenergetic":
                if not np.isclose(state_1.u, state_2.u):
                    raise ValueError()
                v_range = np.logspace(np.log10(state_1.v.magnitude), np.log10(state_2.v.magnitude))*units.m**3/units.kg  # might need to use magnitude and multiply by units
                state = State("water", u=state_1.u, v=v_range[0])

            elif process_type == "isoenthalpic":
                if not np.isclose(state_1.h, state_2.h):
                    raise ValueError()
                v_range = np.logspace(np.log10(state_1.v.magnitude), np.log10(state_2.v.magnitude))*units.m**3/units.kg  # might need to use magnitude and multiply by units
                state = State("water", h=state_1.h, v=v_range[0])

            elif process_type == "isentropic":
                if not np.isclose(state_1.s, state_2.s):
                    raise ValueError()
                v_range = np.logspace(np.log10(state_1.v.magnitude), np.log10(state_2.v.magnitude))*units.m**3/units.kg  # might need to use magnitude and multiply by units
                state = State("water", s=state_1.s, v=v_range[0])

            elif process_type == "isochoric" or process_type == 'isovolumetric':
                if not np.isclose(state_1.v, state_2.v):
                    raise ValueError()
                v_range = np.logspace(np.log10(state_1.p.magnitude), np.log10(state_2.p.magnitude))*units.m**3/units.kg  # might need to use magnitude and multiply by units
                state = State("water", v=state_1.v, p=v_range[0])
                #pressure is being stored in v_range in the isochoric case

            if process_type is not None:
                for v in v_range:
                    if process_type == 'isochoric' or process_type == 'isovolumetric':
                        state.pv = v, state_1.v
                        #pressure is stored in the variable v for the isochoric case
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

                x_data = np.array(x_data)*getattr(units, self.axis_units[x_axis])
                y_data = np.array(y_data)*getattr(units, self.axis_units[y_axis])
                line, = axis.plot(x_data, y_data, linestyle="-")
                self.processes[plot_key][key] = line
            
    def set_xscale(self, x_axis, y_axis, scale = "linear"):
        key = x_axis + y_axis
        plot = self.plots[key]
        fig, axis = plot
        axis.set_xscale(scale)

    def set_yscale(self, x_axis, y_axis, scale = "linear"):
        key = x_axis + y_axis
        plot = self.plots[key]
        fig, axis = plot
        axis.set_yscale(scale)   
