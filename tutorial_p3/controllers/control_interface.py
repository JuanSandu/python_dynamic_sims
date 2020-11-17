"""
    This code has been developed by Juan Sandubete Lopez and all the rights
    belongs to him.
    Distribution or commercial use of the code is not allowed without previous
    agreement with the author.
"""

import numpy as np
import json
import pathlib
import ctypes


class Controller:
    def __init__(self):
        # Parameters
        self.control_val = []
        self.control_law = None
        self.voltage_sat = None
        self.instance_name = None
        self.store_data = False

    def load_config(self):
        with open("configuration.json") as json_file:
            config_file = json.load(json_file)
        self.voltage_sat = config_file[self.instance_name]["saturation_volt"]
        self.store_data = config_file[self.instance_name]["store_data"]

    def initialize(self, instance_name):
        # Load the name used to find the configuration
        self.instance_name = instance_name
        # Load the configuration
        self.load_config()

        # Import the C++ controller library
        libname = str(pathlib.Path().absolute() / "controllers/libcontrol.so")
        c_lib = ctypes.CDLL(libname)
        # Specify the output data type
        c_lib.nonlinear_control.restype = ctypes.c_double
        # Assign the control law
        self.control_law = c_lib.nonlinear_control

    def run_control(self, meas_sensor, refs):
        # Unzip references
        tau_ref = refs["tau_ref"]
        taup_ref = refs["taup_ref"]
        # Control action calculation
        control_val = self.control_law( ctypes.c_double(meas_sensor),
                                        ctypes.c_double(tau_ref),
                                        ctypes.c_double(taup_ref) )
        # Voltage saturation
        control_val = max( min(control_val, self.voltage_sat),
                          -self.voltage_sat )
        if self.store_data:
            self.control_val.append(control_val)
        return control_val
