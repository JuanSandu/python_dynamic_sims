"""
    This code has been developed by Juan Sandubete Lopez and all the rights
    belongs to him.
    Distribution or commercial use of the code is not allowed without previous
    agreement with the author.
"""

import numpy as np
import json

# Import other classes
from .dc_motor_model import DC_motor_model


class Pendulum_model:
    def __init__(self):
        self.instance_name = None
        self.first_step = True
        # Parameters
        self.mass = None
        self.arm_L = None
        self.theta_init = None
        self.drag = None
        self.g = None
        # Internal states
        self._theta = 0.0
        self._dtheta = 0.0
        self._d2theta = 0.0
        self._dp = 0.0
        # Storage
        self.d2theta_values = []
        self.dtheta_values = []
        # Other subsystems
        self.motor = DC_motor_model()

    def load_config(self):
        with open("configuration.json") as json_file:
            config_file = json.load(json_file)
        # Load the parameters from JSON
        if "g" in config_file.keys():
            self.g = config_file["g"]
        else:
            self.g = 9.81
        self.mass = config_file[self.instance_name]["mass"]
        self.arm_L = config_file[self.instance_name]["length"]
        self.drag = config_file[self.instance_name]["drag_coef"]
        self._theta = config_file[self.instance_name]["theta_init"]
        self.store_data = config_file[self.instance_name]["store_data"]

    def initialize(self, instance_name):
        # Load the name used to find the configuration
        self.instance_name = instance_name
        # Load configuration
        self.load_config()
        print("Pendulum Parameters: Mass={}, L={}, Drag Coef.={}, "
                "Theta init={}".format(self.mass, self.arm_L, self.drag,
                                        self._theta))
        self.motor.initialize("dc_motor_model1")
        print("Motor Parameters: a = {}, k = {}".format(self.motor.a, self.motor.k))

    def update_states(self, inputs, dc_volts):
        # Extract the inputs
        torque = inputs[0]
        self._theta = inputs[1]
        self._dtheta = inputs[2]
        self._dp = inputs[4]  # velocity

        # Motor dynamics update
        dtorque = self.motor.update_states(torque, dc_volts)
        # Pendulum nonlinear model
        self._d2theta = -(self.g / self.arm_L)*np.sin(self._theta) + (torque - \
                        self.drag * self._dtheta) / self.mass
        self._dv = self.arm_L * self._dtheta

        # Store data
        if self.store_data:
            self.d2theta_values.append(self._d2theta)
            self.dtheta_values.append(self._dtheta)
        return [dtorque, self._dtheta, self._d2theta, self._dp, self._dv]
