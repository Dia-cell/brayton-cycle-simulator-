# Brayton Cycle Simulator
A python based thermodynamic simulation tool for analyzing the performance of an ideal brayton cycle used in gas-turbine engines.
## Project Overview
This project simulates the major processes of a brayton cycle and evaluates how engine performance changes with compressor pressure ratio.

The simulator calculates:

- Compressor outlet temperature
- Turbine outlet temperature
- Turbine work
- Compressor work
- Net specific work
- Heat added & rejected
- Thermal efficiency
- Fuel flow rate
- Specific power
- Optimum pressure ratio
- Maximum net work
- Maximum power

it also performs pressure ratio studies and generates performance plots.

## Engineering Model
The simulator is based on the Brayton cycle:
1. Isentropic compression.
2. Constant ratio analysis.
3. Isentropic expansion.
4. Constant pressure heat rejection.

## Main features
- Interactive user inputs.
- Compressor and turbine efficiency modelling
- pressure-ratio analysis.
- Thermal efficiency analysis.
- Net work analysis.
- power analysis.
- T-s diagram
- Energy-balance validation.
- Gas property validation.
- CSV result validation.
- Automated performance plots.

## Assumptions
- Ideal gas
- Constant state operation.
- Constant specific heat.
- Negligible pressure losses.
- Specified compressor efficiency.
- Specified turbine efficiency.

## Technologies
- python
- Numpy
- Matplotlib
- CSV

## Example Analysis
The simulator can determine the pressure ratio that produces maximum thermal efficiency, maximum net specific work, and maximum power for a given set of operating conditions.

## Project Purpose
This project was developed as an aerospace engineering portfolio project to apply thermodynamics, gas-turbine cycle analysis, numerical computation, and engineering data visualization using python.