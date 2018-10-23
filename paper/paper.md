---
title: "ThermoState: A state manager for thermodynamics courses"
tags:
- thermodynamics
- engineering
- coolprop
- pint
authors:
- name: Bryan W. Weber
  ORCID: 0000-0003-0815-9270
  affiliation: 1
affiliations:
- name: Department of Mechanical Engineering, University of Connecticut, Storrs, CT USA 06269
  index: 1
date: 21 September 2018
bibliography: paper.bib
---

# Summary

ThermoState is a Python package that provides easy management of thermodynamic states of simple
compressible systems. ThermoState relies on CoolProp [@coolprop; @cp-article] and Pint [@pint] to
provide the equations of state and units handling, respectively. ThermoState replaces tables that
are typically used in engineering courses to evaluate properties when solving for the behavior of
systems.

# Statement of Need

In traditional engineering thermodynamics courses, properties of simple compressible systems (such
as the temperature, pressure, specific volume, specific enthalpy, etc.) are evaluated from tabulated
data. This process often involves an inordinate number of arithmetic calculations, simply to
determine the appropriate properties at a given state. The length of the simple calculations
inhibits students' ability to recognize patterns in problems; they get lost in the calculations, and
fail to see the larger point of a problem. Aside from calculations from a table, students also often
get stuck performing unit conversions, especially in the so-called "English Engineering" (EE) units
system.

Therefore, there is a need for a software package that simplifies or reduces the number of rote
calculations the students must accomplish and removes the burden of improper unit conversion.
Existing software packages that solve the equation of state for a substance have APIs that are
confusing for students who are learning not only thermodynamics, but Python as well. In addition,
packages such as CoolProp [@coolprop; @cp-article] do not have a facility to automatically manage
units and require all quantities to be in base SI units, which is inconvenient for problems working
with EE units.

ThermoState combines the CoolProp [@coolprop; @cp-article] and Pint [@pint] packages to enable easy
evaluation of equations of state without needing tables as well as automatic unit conversion. In
addition, ThermoState has an easy to understand API that uses instance attributes to store the
properties of interest.

Because of the simplicity of use and because students do not have to perform trivial arithmetic,
ThermoState also enables students to engage in higher levels of learning by evaluating the
performance of systems for a range of input parameters. Packages such as NumPy [@numpy] and
Matplotlib [@matplotlib] can be used to generate ranges of input parameters and plot the output.
Students can interpret the plots and understand the behavior of systems for a range of input values.
This type of analysis would not be possible with traditional table-based techniques because of the
sheer number of calculations required.

# Functionality and Usage

The primary interface for students to the ThermoState package is the `State` class. The `State`
class constructor takes one mandatory argument, the name of the substance, and two optional keyword
arguments, which must be a pair of independent, intensive properties. Two independent, intensive
properties are required to solve the equation of state of the substance. These keyword arguments
must be instances of the `Quantity` class from Pint [@pint], and must have the appropriate
dimensions for the property being set.

```python
from thermostate import State, Q_
T_1 = Q_(100.0, 'degC')
p_1 = Q_(0.5, 'bar')
st_1a = State('water', T=T_1, p=p_1)
```

Alternatively, only the name of the substance can be specified, and the state can be fixed by
assigning a value to an instance attribute representing the appropriate pair of properties.

```python
st_1b = State('water')
st_1b.Tp = T_1, p_1
```

Once the instance of the `State` class is created, the properties of the substance are available as
attributes of the instance. These instance attributes are themselves instances of the `Quantity`
class from Pint [@pint]. Internally, the instance attributes are always in SI base units, to
simplify passing arguments to the appropriate CoolProp [@coolprop; @cp-article] functions. However,
the `Quantity` class has a `to` method that converts the units of the quantity, allowing the
students to use whatever units are natural for a problem.

```python
v_1 = st_1a.v.to('m**3/kg')
u_1 = st_1a.u.to('BTU/lb')
```

Finally, Pint [@pint] `Quantity` instances can be used in arithmetic statements in Python, and
provided that the statement is dimensionally consistent, can be easily used to calculate, e.g., the
work and heat transfer during a process.

# Recent Uses

I originally wrote ThermoState to use in my Applied Thermodynamics course in the Spring 2016
semester at the University of Connecticut. This course covers the major thermodynamic cycles
(Rankine, Brayton, Refrigeration, Otto, Diesel, etc.). Having the students use ThermoState to
evaluate properties allowed me to assign problems that would have been impossible without some
software assistance. In particular, I expect the students to produce 2-3 design reports of systems
that implement one or more of the previously mentioned cycles, and I expect students to perform some
level of analysis of the cycle with respect to varying the input parameters.

Since then, I have used ThermoState in two other Applied Thermodynamics courses (Spring 2017 and
2018). I have also used ThermoState in my Thermodynamic Principles course, a prerequisite for
Applied Thermodynamics. In all the courses, students had positive feedback about the use of
ThermoState, strongly preferring using the software to using tables.

To avoid having to have students install any software on their personal computers, I use a
JupyterHub instance hosted by the University where students can log in and work on their homework
and projects. Using Jupyter Notebooks [@jupyter_notebook], students can combine their code to solve
the problem with Markdown and equations that explains their process.

A tutorial on the basic use of the package and several examples can be found in the `docs` folder
of the [repository](https://github.com/bryanwweber/thermostate) as well as the
[online documentation](https://bryanwweber.github.io/thermostate).

# References
