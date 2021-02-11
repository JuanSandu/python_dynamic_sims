"""
    This code has been developed by Juan Sandubete Lopez and all the rights
    belongs to him.
    Distribution or commercial use of the code is not allowed without previous
    agreement with the author.
"""

import numpy as np
import json


class DC_motor_model:
    def __init__(self):
        # Parameters
        self.a = None
        self.k = None
        self.voltage_sat = None # Max. voltage for the motor
        self.store_data = False
        # Internal states
        self._last_x1_m = 0.0
        self._x1_m = 0.0
        self._dx1_m = 0.0
        self._y1_m = 0.0
        self.torque_vals = []
        self.instance_name = None

    def load_config(self):
        with open("configuration.json") as json_file:
            config_file = json.load(json_file)
        # Load the parameters from JSON
        self.a = config_file[self.instance_name]["a"]
        self.k = config_file[self.instance_name]["k"]
        self.store_data = config_file[self.instance_name]["store_data"]

    def initialize(self, instance_name):
        # Load the name used to find the configuration
        self.instance_name = instance_name
        # Load configuration
        self.load_config()
        # For the moment, nothing else here
        print("Motor Parameters: a = {}, k = {}".format(self.a, self.k))

    def update_states(self, x1_m, u):
        # DC motor model:
        # taup + a*k*tau = k*u
        # With the change: x1_m = tau (x1_motor)
        self._last_x1_m = self._x1_m
        self._dx1_m = -self.a*self.k*self._x1_m + self.k*u
        self._y1_m = self._x1_m

        # Update the value
        self._x1_m = x1_m

        if self.store_data:
            self.torque_vals.update(x1_m)
        return self._dx1_m

    def get_torque(self):
        return self._last_x1_m
