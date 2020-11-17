"""
    This code has been developed by Juan Sandubete Lopez and all the rights
    belongs to him.
    Distribution or commercial use of the code is not allowed without previous
    agreement with the author.
"""

import numpy as np
import json


class Torque_sensor:
    def __init__(self):
        # Parameters
        self.mean_white_noise = None
        self.dev_white_noise = None
        self.sensor_bits = None
        self.torque_range = None
        self.sensor_steps = None
        self.instance_name = None
        self.store_data = False
        self.measures = []

    def load_config(self):
        with open("configuration.json") as json_file:
            config_file = json.load(json_file)
        # Load the parameters from JSON
        self.mean_white_noise = config_file[self.instance_name]["mean_white_noise"]
        self.dev_white_noise = config_file[self.instance_name]["dev_white_noise"]
        self.sensor_bits = config_file[self.instance_name]["sensor_bits"]
        self.torque_range = config_file[self.instance_name]["torque_range"]
        self.store_data = config_file[self.instance_name]["store_data"]

    def initialize(self, instance_name):
        # Load the name used to find the configuration
        self.instance_name = instance_name
        # Load configuration
        self.load_config()
        # Initialize the sensor steps
        n_steps = 2**self.sensor_bits
        self.sensor_steps = 2*self.torque_range / n_steps
        print("Sensor bit step: {}[N·m/V]".format(self.sensor_steps))

    def measure(self, torque):
        # Noise injection
        gauss_noise = np.random.normal(self.mean_white_noise, self.dev_white_noise)
        noisy_torque = torque + gauss_noise
        # Signal quantization
        dig_torque = self.sensor_steps * np.round(noisy_torque/self.sensor_steps)

        if self.store_data:
            self.measures.append( dig_torque )
        return dig_torque
