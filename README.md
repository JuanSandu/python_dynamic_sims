# Python Dynamics Simulator
Simple software to simulate dynamic systems with Python and SciPy (mainly).

The purpose of this code is to serve as a template for dynamics simulations with any complexity use ODEInt (first tutorial chapter) and solve_ivp() (from the second on) for the integration of the systems ecuations.
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

In the second part of the tutorial, we make simulations using the function solve_ivp() of Scipy. In addition, we run C/C++ controllers in order to be able to test the control laws exactly as they will be implemented in the microcontroller. To know all the details, checkout the tutorial:
https://medium.com/robotics-devs/python-dynamics-simulations-part-2-testing-c-c-controllers-a182a704ca12

The third part is about the creation of a object oriented simulator, more versatile and reusable:
https://medium.com/robotics-devs/python-dynamic-simulations-part-3-object-oriented-simulator-56b2f5190876

You can check the index of the tutorial here:
https://jsandubete.medium.com/posts-index-44e4f3d987e3


I learnt from these two links mainly to get the core ideas for writing my code:
- https://apmonitor.com/pdc/index.php/Main/ModelSimulation
- https://towardsdatascience.com/on-simulating-non-linear-dynamic-systems-with-python-or-how-to-gain-insights-without-using-ml-353eebf8dcc3
