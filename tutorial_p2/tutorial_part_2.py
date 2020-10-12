"""
    This code has been developed by Juan Sandubete Lopez and all the rights
    belongs to him.
    Distribution or commercial use of the code is not allowed without previous
    agreement with the author.
"""

import numpy as np
import scipy
import random
import time

import ctypes
import pathlib

import pandas as pd

import matplotlib.pyplot as plt
from scipy.integrate import odeint, solve_ivp

# Simulation parametrs
tf = 6.0  # Final time
smpls = 3  # Continuous steps between control actions
save_data = False  # Attention: CSV file can be very big
save_fig = True  # If False, figure is showed but not saved
title = "motor_control_part2"

print("Realistic motor control simulation.")

# Models Parameters
# Motor
a = 1
k = 1
voltage_sat = 7  # Maximum voltage for the motor
# Sensorization Effect
perfect_sensor = False
mean_white_noise = 0.0
dev_white_noise = 0.05
sensor_bits = 8
torque_range = 10
ts_ms = 5.0  # 0.001 = 1us, 1 = 1ms

print("\n--- PARAMETERS --- \n ")
print("Motor Parameters: a = {}, k = {}".format(a, k))

# Import the C++ controller library
libname = str(pathlib.Path().absolute() / "libcontrol.so")
c_lib = ctypes.CDLL(libname)
# Specify the output data type
c_lib.nonlinear_control.restype = ctypes.c_double

# Sensor parameters calculation
n_steps = 2**sensor_bits
sensor_steps = 2*torque_range / n_steps
print("Sensor bit step: {}[N·m/V]".format(sensor_steps))


# Define models
def dc_motor_model(x1_m, u):
    # DC motor model:
    # taup + a*k*tau = k*u
    # With the change: x1_m = tau (x1_motor)
    dx1_m = -a*k*x1_m + k*u
    y1_m = x1_m
    return dx1_m

def torque_sensor(torque):
    # Noise injection
    gauss_noise = np.random.normal(mean_white_noise, dev_white_noise)
    noisy_torque = torque + gauss_noise
    # Signal quantization
    dig_torque = sensor_steps * np.round(noisy_torque/sensor_steps)
    return dig_torque

# The following function puts all ecuations together
def connected_systems_model(t, states, dc_volts):
    # Input values. Check this with the out_states list
    _, tau, _ = states

    # Compute motor torque
    taup = dc_motor_model(tau, dc_volts)

    # Output
    out_states = [tau, taup, dc_volts]
    return out_states


# Initial conditions
states0 = [0.0, 0.0, 0.0]
n = int((1 / (ts_ms / 1000.0))*tf + 1) # number of time points

# Time vectors for the simulation
time_vector = np.linspace(0,tf,(n-smpls)*(smpls-1)-1)
t_sim_step = time_vector[1] - time_vector[0]
intra_steps = list( np.linspace(0, tf/n, smpls) )

# Reference signal and its differentiations
ref_t_vector = np.linspace(0,tf,n-1)
tau_ref = np.sin(ref_t_vector)
taup_ref = np.cos(ref_t_vector)

# Output arrays
states = np.zeros( ( len(time_vector), len(states0)) ) # States for each timestep
if not perfect_sensor:
    meas_sensor = np.zeros( n - 1 )
control_val = np.zeros( n-smpls-1 )

print("\n--- SIMULATION CONFIG. ---\n")
print("Simulation time: {} sec".format(tf))
print("Time granulatiry: {}".format(t_sim_step))
print("Initial states: {}".format(states0))

print("\nScipy Version: {}".format(scipy.__version__))



print("\n--- SIMULATION Begins ---\n")
initial_time = time.time()

t_counter = 0
for i in range(n-smpls-1):
    if i >= t_counter * int((n-1)/10):
        print("Simulation at {}%".format(t_counter*10))
        t_counter += 1
    if perfect_sensor:
        meas_sensor[i] = states0[0]
    else:
        meas_sensor[i] = torque_sensor( states0[0] )
    # Control action calculation
    control_val[i] = c_lib.nonlinear_control(ctypes.c_double(meas_sensor[i]),
                                             ctypes.c_double(tau_ref[i]),
                                             ctypes.c_double(taup_ref[i]) )
    # Voltage saturation
    control_val[i] = max(min(control_val[i], voltage_sat), -voltage_sat)
    # Model Simulation
    solution = solve_ivp( connected_systems_model, [0, tf/n], states0,
                          t_eval=intra_steps, args=(control_val[i],) )
    states0 = [state_vec[-1] for state_vec in solution.y]
    # Store the output data
    if i>0:
        states[smpls+(i-1)*(smpls-1):smpls+i*(smpls-1)] = \
                                                    solution.y.T.tolist()[1:]
    else:
        states[0:smpls] = solution.y.T.tolist()

elapsed_time = time.time() - initial_time
print("\nElapsed time: {} sec.".format(elapsed_time))

print("\n--- SIMULATION Finished. ---\n")



if save_data:
    print("Saving simulation data...")
    sim_df = pd.DataFrame(states)
    sim_df = sim_df.transpose()
    sim_df.rename({0: 'x1', 1: 'x2', 2:'y'}, inplace=True)
    sim_df.to_csv('sim_data/fbck_lin_control_ex3.csv')

# Plot results
plt.rcParams['axes.grid'] = True
fig=plt.figure()
fig.suptitle("Motor Control. Sampling Freq.:{0:.2f}Hz".format(1000/ts_ms))
plt.subplot(3,1,1)
plt.plot(ref_t_vector,tau_ref,'k--',linewidth=3)
if not perfect_sensor:
    plt.plot(ref_t_vector,meas_sensor,'b',linewidth=1)
plt.plot(time_vector,states[:,0],'r',linewidth=1.5)
plt.ylabel('tau [N·m]')
plt.subplot(3,1,2)
plt.plot(ref_t_vector,taup_ref,'k--',linewidth=3)
plt.plot(time_vector,states[:,1],'r',linewidth=1)
plt.ylabel('taup [N·m/s]')
plt.subplot(3,1,3)
plt.plot(np.linspace(0,tf,len(control_val)) ,control_val,'r',linewidth=1)
plt.ylabel('u_val [V]')
plt.xlabel('Time [s]')

if save_fig:
    figname = "pictures/" + title + ".png"
    plt.savefig(figname)
    plt.show()
else:
    plt.show()
