"""
    This code has been developed by Juan Sandubete Lopez and all the rights
    belongs to him.
    Distribution or commercial use of the code is not allowed without previous
    agreement with the author.
"""

import numpy as np
import json
import pandas as pd
import scipy
import time

import matplotlib.pyplot as plt

from types import MethodType
from scipy.integrate import odeint, solve_ivp

# Import other classes
from .motorized_pendulum_nonlinear import Pendulum_model
from .motorized_pendulum_tf import Pendulum_tf


class Simulator:
    def __init__(self):
        # Simulation parameters
        self.perfect_sensor = None
        self.init_states = []
        self.sim_time = None
        self.sim_step_cnt = 0
        self.cont_smpls = None  # Continuous samples
        self.sample_period_ms = None
        self.save_data = None
        self.save_figure = None
        self.title = "Title"
        self.instance_name = None

        # Derived simulation parameters
        self.n = None # Discrete simulation points
        self.time_dict = {}
        self.refs_dict = {}
        self.sim_data = {}

        # Submodels
        self.arm_1dof = Pendulum_model()
        self.arm_1dof_tf = Pendulum_tf()

        # Output buffer
        self.perfect_out_states = []
        self.real_out_states = []

    def _load_config(self):
        with open("configuration.json") as json_file:
            config_file = json.load(json_file)
        # Load the parameters from JSON
        self.perfect_sensor = config_file[self.instance_name]["perfect_sensor"]
        self.init_states = config_file[self.instance_name]["initial_states"]
        self.sim_time = config_file[self.instance_name]["sim_time"]
        self.cont_smpls = config_file[self.instance_name]["continuous_samples"]
        self.sample_period_ms = 1000.0 / config_file[self.instance_name]["sampling_freq"]
        self.save_data = config_file[self.instance_name]["save_data"]
        self.save_figure = config_file[self.instance_name]["save_figure"]
        self.title = config_file[self.instance_name]["title"]

    def _load_references(self):
        # TODO automate this to load them from a file or whatever
        self.refs_dict["ref_t_vector"] = np.linspace(0, self.sim_time, self.n-1)
        # self.refs_dict["dc_values"] = np.sin(self.refs_dict["ref_t_vector"])
        self.refs_dict["dc_values"] = [0.0]*(self.n-1)
        for i in range( int((self.n-1) * 0.1), self.n-1 ):
            self.refs_dict["dc_values"][i] = 5.0

    def initialize(self, instance_name):
        # Load the name used to find the configuration
        self.instance_name = instance_name
        # Initialize the simulator itself and all subsystems
        self._load_config()
        self.arm_1dof.initialize("robot_arm1")
        self.arm_1dof_tf.initialize("robot_arm1_tf")

        # Other simulation parameters
        self.n = int((1 / (self.sample_period_ms / 1000.0))*self.sim_time + 1)
        # Data vectors
        # Time vectors for the simulation
        self.time_dict["time_vector"] = np.linspace(0, self.sim_time,
                                        (self.n-self.cont_smpls)*(self.cont_smpls-1)-1)
        self.time_dict["intra_steps"] = list( np.linspace(0, self.sim_time/self.n,
                                                          self.cont_smpls) )
        # References
        self._load_references()

        # Output arrays
        self.sim_data["states"] = []
        self.sim_data["states"].append(self.init_states)
        if not self.perfect_sensor:
            self.sensor.measure( self.init_states[0] )

    def _get_last_sys_outputs(self):
        sys_outputs = []
        if self.perfect_sensor:
            sys_outputs = self.sim_data["states"][-1][0]
        else:
            sys_outputs = self.sensor.measures[-1]
        return sys_outputs

    def _get_refs(self, index):
        refs = {}
        for key, item in self.refs_dict.items():
            refs.update( {key: self.refs_dict[key][index]} )
        return refs

    def _update_states(self, t, states, dc_volts):
        # Input values. Check this with the out_states list
        # In this case it is not necessary to split them

        # Compute motor torque
        out_states = self.arm_1dof.update_states(states, dc_volts)

        # Output for the simulation of the system itself
        self.perfect_out_states = out_states
        return self.perfect_out_states

    def _apply_sensors_effect(self, solution):
        # TODO this method should apply the corresponding sensor to each desired
        # magnitude automatically
        for snap in solution.y.T.tolist()[1:]:
            # Take the sensor signal through the sensor model
            state = [self.sensor.measure( snap[0] )] + snap[1:]

    def simulate_step(self):
        # Load the corresponding voltage for the motor
        dc_vals = self.refs_dict["dc_values"][self.sim_step_cnt]
        # Simulate the system
        solution = solve_ivp( self._update_states, [0, self.sim_time/self.n],
                              self.init_states,
                              t_eval=self.time_dict["intra_steps"],
                              args=(dc_vals,) )

        # Update the init states for the next sim step and store the sim data
        #print(self.init_states)
        self.init_states = [state_vec[-1] for state_vec in solution.y]
        for slice in solution.y.T.tolist()[1:]:
            self.sim_data["states"].append(slice)

        self.sim_step_cnt += 1

    def run_simulation(self):
        print("\n--- SIMULATION Begins ---\n")
        initial_time = time.time()

        t_counter = 0
        for i in range(self.n-self.cont_smpls-1):
            if i >= t_counter * int((self.n-1)/10):
                print("Simulation at {}%".format(t_counter*10))
                t_counter += 1
            # Run the simulation step
            self.simulate_step()

        # Correct the shape of the states
        self.sim_data["states"] = np.array(self.sim_data["states"]).T.tolist()
        # Finish
        elapsed_time = time.time() - initial_time
        print("\nElapsed time: {} sec.".format(elapsed_time))

        print("\n--- SIMULATION Finished. ---\n")

    def run_tf_simulation(self):
        if len(self.refs_dict["ref_t_vector"]) < 1:
            print("Error: load_references() must be run before simulating.")
            exit(-1)
        # Start
        print("\n--- TF SIMULATION Begins ---\n")
        initial_time = time.time()

        self.sim_data["tf_sim"] = \
                    self.arm_1dof_tf.response_sim(self.refs_dict["ref_t_vector"],
                                                  self.refs_dict["dc_values"])
        # Finish
        elapsed_time = time.time() - initial_time
        print("\nElapsed time: {} sec.".format(elapsed_time))
        print("\n--- TF SIMULATION Finished. ---\n")

    def store_data(self):
        # TODO this method must be updated
        print("Saving simulation data...")
        sim_df = pd.DataFrame(self.sim_data["states"])
        sim_df = sim_df.transpose()
        sim_df.rename({0: 'x1', 1: 'x2', 2:'y'}, inplace=True)
        sim_df.to_csv('sim_data/fbck_lin_control_ex3.csv')

    def plot_results(self):
        plt.rcParams['axes.grid'] = True
        fig=plt.figure()
        fig.suptitle("Pendulum Model")

        plt.subplot(3,1,1)
        if not self.perfect_sensor:
            plt.plot( self.time_dict["time_vector"], self.sensor.measures,
                      'b',linewidth=1 )
        plt.plot( self.time_dict["time_vector"], self.sim_data["states"][1],
                  'b',linewidth=1.5 )
        # plt.plot( self.sim_data["tf_sim"][0], self.sim_data["tf_sim"][1],
        #           'k',linewidth=1.0 )
        plt.ylabel('Theta [rad]')

        plt.subplot(3,1,2)
        plt.plot( self.time_dict["time_vector"], self.sim_data["states"][2],
                  'b',linewidth=1.5 )
        plt.ylabel('dtheta [rad/s]')

        plt.subplot(3,1,3)
        plt.plot( self.refs_dict["ref_t_vector"],self.refs_dict["dc_values"],'k--',
                  linewidth=1.2 )
        plt.plot( self.time_dict["time_vector"], self.sim_data["states"][0],
                  'r',linewidth=1 )
        plt.ylabel('Torque [Nm]')
        plt.xlabel('Time [s]')

        if self.save_figure:
            figname = "pictures/" + self.title + ".png"
            plt.savefig(figname)
            plt.show()
        else:
            plt.show()
