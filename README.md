# Python Dynamics Simulator
Simple software to simulate dynamic systems with Python and SciPy (mainly).

The purpose of this code is to serve as a template for dynamics simulations with any complexity use ODEInt (first tutorial chapter) and solve_ivp() (from the second on) for the integration of the systems ecuations.
You can play with this code by tuning the controller gain or incrementing the modelling error values (a_error and k_error).

The following is a typical log output:
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

The content of this tutorial is the following:
1. Use of odeint() for simulations with Matlab-like scripts.
https://medium.com/robotics-devs/python-dynamics-simulations-part-1-f89648a35561

2. Simulations using the function solve_ivp() of Scipy. In addition, we run C/C++ controllers in order to be able to test the control laws exactly as they will be implemented in the microcontroller. To know all the details, checkout the tutorial:
https://medium.com/robotics-devs/python-dynamics-simulations-part-2-testing-c-c-controllers-a182a704ca12

3. The creation of a object oriented simulator, more versatile and reusable:
https://medium.com/robotics-devs/python-dynamic-simulations-part-3-object-oriented-simulator-56b2f5190876

4. Use of sockets with Python and C/C++ as a way to interconnect the simulator with other applications:
https://medium.com/robotics-devs/python-dynamics-simulations-part-4-sockets-with-c-and-python-2afb5c62f4b

5. Transfer Functions with Python. An introduction including the simulation of a nonlineal model for a motorized pendulum and a linearization of it.
https://medium.com/robotics-devs/transfer-functions-with-scipy-i-7709f2f1e232


You can check the index of the tutorial here:
https://jsandubete.medium.com/posts-index-44e4f3d987e3


I learnt from these two links mainly to get the core ideas for writing my code:
- https://apmonitor.com/pdc/index.php/Main/ModelSimulation
- https://towardsdatascience.com/on-simulating-non-linear-dynamic-systems-with-python-or-how-to-gain-insights-without-using-ml-353eebf8dcc3
