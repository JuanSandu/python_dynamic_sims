# Python Dynamics Simulator
Simple software to simulate dynamic systems with Python and SciPy (mainly).

The purpose of this code is to serve as a template for dynamics simulations with any complexity use ODEInt for the integration of the systems ecuations.
You can play with this code by tuning the controller gain or incrementing the modelling error values (a_error and k_error).

The following is the usual log output:
```
Starting motor simulation.

--- PARAMETERS --- 
 
Motor Parameters: a = 1, k = 1
Motor Induced Model Errors: a_error = 0, k_error = 0
Motor Controller: kc1 = 1

--- SIMULATION CONFIG. ---

Simulation time: 3.0 sec
Time granulatiry: 1.00000333334e-05
Initial states: [0, 0, 0, 0, 0]

--- SIMULATION Begins ---

Simulation at 0%
Simulation at 10%
Simulation at 20%
Simulation at 30%
Simulation at 40%
Simulation at 50%
Simulation at 60%
Simulation at 70%
Simulation at 80%
Simulation at 90%
Simulation at 100%

Elapsed time: 15.2205140591 sec.

--- SIMULATION Finished. ---

```