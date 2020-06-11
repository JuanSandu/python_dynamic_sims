"""
    This code has been developed by Juan Sandubete Lopez.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import random
import time
import pandas as pd

# Simulation parametrs
tf = 1.0  # final time
ts_ms = 0.01  # 0.001 = 1us, 1 = 1ms
save_data = True  # Attention: CSV file can be very big
save_fig = True  # If False, figure is showed but not saved
title = "motor_control_a_with_error"

print("Starting motor simulation.")

# Models Parameters
# Motor
a = 1
k = 1
a_model_error = 0.1
k_model_error = 0.5
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
    return y1_m, dx1_m

def motor_controller(tau, tau_ref, taup_ref):
    # Non-Linear control for DC Motor following Dyn ecs: taup + a*k*tau = k*u
    # The controller returns dc_volts
    v = taup_ref - k_c1*(tau - tau_ref)
    return (a+a_model_error)*tau + v/(k+k_model_error)


# The following function puts all ecuations together
def connected_systems_model(states, t, tau_ref, taup_ref):
    # Input values. Check this with the out_states list
    _, x1_m, _, _, _ = states

    # Compute motor controller
    dc_volts = motor_controller(x1_m, tau_ref, taup_ref)
    # Compute motor torque
    tau, taup = dc_motor_model(x1_m, dc_volts)

    # Output
    out_states = [tau, taup, tau_ref, taup_ref, dc_volts]
    return out_states


# Initial conditions
states0 = [0, 0, 0, 0, 0]
n = int((1 / (ts_ms / 1000.0))*tf + 1) # number of time points

# time span for the simulation, cycle every tf/n seconds
time_vector = np.linspace(0,tf,n)
t_sim_step = time_vector[1] - time_vector[0]

# Reference signal and its differentiations
torque_ref = np.sin(3*time_vector)
torquep_ref = [(lambda i: (torque_ref[i+1]-torque_ref[i])/t_sim_step)(i)
          for i in range(len(torque_ref)-1)]
# torquep_ref = np.insert(torquep_ref, 0, 0.0)  # Keep the length, add an initial zero
torquep_ref = np.append(torquep_ref, torquep_ref[-1])  # Clone the last
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
    if i >= t_counter * int((n-1)/10):
        print("Simulation at {}%".format(t_counter*10))
        t_counter += 1
    out_states = odeint(connected_systems_model,states0,[0.0, tf/n],
                        args=(torque_ref[i],torquep_ref[i]))
    #print(out_states)
    states0 = out_states[-1,:]
    #print(out_states)
    states[i] = out_states[-1,:]
elapsed_time = time.time() - initial_time
print("\nElapsed time: {} sec.".format(elapsed_time))

print("\n--- SIMULATION Finished. ---\n")

if save_data:
    print("Saving simulation data...")
    sim_df = pd.DataFrame(states)
    sim_df = sim_df.transpose()
    sim_df.rename({0: 'tau', 1: 'taup', 2: 'tau_ref', 3: 'taup_ref',
                   4: 'dc_volts'}, inplace=True)
    sim_df.to_csv('sim_data/ex4_motor_control.csv')

# Plot results
# States are: tau, taup, tau_ref, taup_ref, dc_volts
plt.rcParams['axes.grid'] = True
plt.figure()
plt.subplot(3,1,1)
plt.plot(time_vector[:-1],states[:,2],'k--',linewidth=3)
plt.plot(time_vector[:-1],states[:,0],'r',linewidth=2)
plt.ylabel('tau [Nm]')
plt.legend(loc=1)
plt.subplot(3,1,3)
plt.plot(time_vector[:-1],states[:,4],'b',linewidth=3)
plt.ylabel('DC Motor [V]')
plt.xlabel('Time (sec)')
plt.legend(loc=1)
plt.subplot(3,1,2)
plt.plot(time_vector[:-1],states[:,3],'k--',linewidth=3)
plt.plot(time_vector[:-1],states[:,1],'r',linewidth=2)
plt.ylabel('taup [Nm/s]')
plt.legend(loc=1)

if save_fig:
    figname = "pictures/" + title + ".png"
    plt.savefig(figname)
else:
    plt.show()
