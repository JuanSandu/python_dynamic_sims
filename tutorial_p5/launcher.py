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

from dynamic_models.simulator import Simulator


def launch_simulation():
    # Create and initialize simulator object
    simul = Simulator()
    simul.initialize("simulation_1")

    print("\n--- SIMULATION CONFIG. ---\n")
    print("Simulation time: {} sec".format(simul.sim_time))
    print("Time granulatiry: {}ms".format(simul.sample_period_ms))
    print("Initial states: {}".format(simul.init_states))

    print("\nScipy Version: {}".format(scipy.__version__))

    # Launch the simulation itself
    simul.run_simulation()
    simul.run_tf_simulation()
    # And plot the results
    simul.plot_results()


launch_simulation()
