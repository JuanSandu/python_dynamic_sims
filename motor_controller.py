"""
    This code has been developed by Juan Sandubete Lopez and all the rights
    belongs to him.
    Distribution or commercial use of the code is not allowed without previous
    agreement with the author.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import random
import time
import pandas as pd

# Simulation parametrs
tf = 6.0  # final time
ts_ms = 0.01  # 0.001 = 1us, 1 = 1ms
save_data = False  # Attention: CSV file can be very big
show_fig = True
save_fig = False  # If False, figure is showed but not saved
title = "motor_control_a_with_error_wtf2"

print("Starting motor simulation.")

# Models Parameters
# Motor
a = 1
k = 1
a_model_error = 0.1
k_model_error = 0.3
# Motor Controller (Control1)
k_c1 = 1

print("\n--- PARAMETERS --- \n ")
print("Motor Parameters: a = {}, k = {}".format(a, k))
print("Motor Induced Model Errors: a_error = {}, k_error = {}".
      format(a_model_error, k_model_error))
print("Motor Controller: kc1 = {}".format(k_c1))

# Define models
def dc_motor_model(x1_m, u):
    # DC motor model:
    # taup + a*k*tau = k*u
    # With the change: x1_m = tau (x1_motor)
    dx1_m = -a*k*x1_m + k*u
    y1_m = x1_m
    return dx1_m

def motor_controller(tau, tau_ref, taup_ref):
    # Non-Linear control for DC Motor following Dyn ecs: taup + a*k*tau = k*u
    # The controller returns dc_volts
    v = taup_ref - k_c1*(tau - tau_ref)
    return (a+a_model_error)*tau + v/(k+k_model_error)


# The following function puts all ecuations together
def connected_systems_model(states, t, tau_ref, taup_ref):
    # Input values. Check this with the out_states list
    x1_m, _ = states

    # Compute motor controller
    dc_volts = motor_controller(x1_m, tau_ref, taup_ref)
    # Compute motor torque
    taup = dc_motor_model(x1_m, dc_volts)

    # Output
    out_states = [taup, dc_volts]
    return out_states


# Initial conditions
states0 = [0, 0]
n = int((1 / (ts_ms / 1000.0))*tf + 1) # number of time points

# time span for the simulation, cycle every tf/n seconds
time_vector = np.linspace(0,tf,n)
t_sim_step = time_vector[1] - time_vector[0]

# Reference signal and its differentiations
torque_ref = np.sin(time_vector)
print("Max ref: {}".format(max(torque_ref)))
print("Min ref: {}".format(min(torque_ref)))
torquep_ref = np.cos(time_vector)
print("Max ref: {}".format(max(torquep_ref)))
print("Min ref: {}".format(min(torquep_ref)))
# Output arrays
states = np.zeros( (n-1, len(states0)) ) # States for each timestep

print("\n--- SIMULATION CONFIG. ---\n")
print("Simulation time: {} sec".format(tf))
print("Time granulatiry: {}".format(t_sim_step))
print("Initial states: {}".format(states0))

print("\n--- SIMULATION Begins ---\n")

initial_time = time.time()
# Simulate with ODEINT
t_counter = 0
for i in range(n-1):
    out_states = odeint(connected_systems_model, states0, [0.0, tf/n],
                        args=(torque_ref[i], torquep_ref[i]))
    states0 = out_states[-1,:]
    states[i] = out_states[-1,:]
    if i >= t_counter * int((n-1)/10):
        print("Simulation at {}%".format(t_counter*10))
        t_counter += 1

elapsed_time = time.time() - initial_time
print("\nElapsed time: {} sec.".format(elapsed_time))
print("\n--- SIMULATION Finished. ---\n")

if save_data:
    print("Saving simulation data...")
    sim_df = pd.DataFrame(states)
    sim_df = sim_df.transpose()
    sim_df.rename({0: 'tau', 1: 'tau_ref', 2: 'taup_ref',
                   3: 'dc_volts'}, inplace=True)
    sim_df.to_csv('sim_data/ex4_motor_control.csv')

# Plot results
# States are: tau, tau_ref, taup_ref, dc_volts
plt.rcParams['axes.grid'] = True
plt.figure()
plt.subplot(2,1,1)
plt.plot(time_vector[:-1],torque_ref[:-1],'k--',linewidth=3)
plt.plot(time_vector[:-1],states[:,0],'r',linewidth=2)
plt.ylabel('tau [Nm]')
plt.subplot(2,1,2)
plt.plot(time_vector[:-1],torquep_ref[:-1],'k--',linewidth=3)
plt.ylabel('taup [Nm/s]')

if save_fig:
    figname = "pictures/" + title + ".png"
    plt.savefig(figname)
if show_fig:
    plt.show()
