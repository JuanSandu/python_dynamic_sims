"""
    This code has been developed by Juan Sandubete Lopez and all the rights
    belongs to him.
    Distribution or commercial use of the code is not allowed without previous
    agreement with the author.
"""

import numpy as np
import json

# For the TF
from scipy import signal as sig


class Pendulum_tf:
    def __init__(self):
        self.instance_name = None
        self.first_step = True
        self.tf_2nd_order = True
        # Parameters
        self.k = None
        self.poles = []
        self.zeros = []
        self.w = None
        self.z = None

    def load_config(self):
        with open("configuration.json") as json_file:
            config_file = json.load(json_file)
        # Load the parameters from JSON
        self.tf_2nd_order = config_file[self.instance_name]["def_poles_zeros"]
        if not self.tf_2nd_order:
            self.k = config_file[self.instance_name]["tf"]["k"]
            self.poles = config_file[self.instance_name]["tf"]["poles"]
            self.zeros = config_file[self.instance_name]["tf"]["zeros"]
        else:
            self.k = config_file[self.instance_name]["tf_2nd_order"]["gain"]
            self.w = config_file[self.instance_name]["tf_2nd_order"]["omega"]
            self.z = config_file[self.instance_name]["tf_2nd_order"]["zeta"]

    def initialize(self, instance_name):
        # Load the name used to find the configuration
        self.instance_name = instance_name
        # Load configuration
        self.load_config()
        print( "Pendulum TF Parameters: k={}, \nZeros={}, \nPoles={}, "
                .format(self.k, self.zeros, self.poles) )

    @staticmethod
    def second_order_tf(gain, omega, zeta):
        num = [omega**2]
        den = [1, 2*zeta*omega, omega**2]
        return [np.dot(gain, num), den]

    def response_sim(self, t, inputs):
        # Put together poles and zeros
        num = [1]
        den = [1]
        if not self.tf_2nd_order:
            for i in range(len(self.zeros)):
                num = np.polymul(num, self.zeros[i])
            num = np.dot(self.k, num)
            for i in range(len(self.poles)):
                den = np.polymul(den, self.poles[i])
        else:
            [num, den] = self.second_order_tf(self.k, self.w, self.z)
            print(self.second_order_tf(self.k, self.w, self.z))
        # Create TF object
        Gs = sig.TransferFunction(num, den)
        print(Gs)
        # Return tsim, ysim, xsim
        return sig.lsim2(Gs, U=inputs, T=t)
