import numpy as np
from scipy import signal as sig


def second_order_tf(gain, omega, zeta):
    num = [omega**2]
    den = [1, 2*zeta*omega, omega**2]
    return [np.dot(gain, num), den]

def param_identification(var_u, var_y, y_peak, y_ss, period_secs):
    # The previous vlaues must be extracted from the step response
    gain = var_y / var_u
    Mp = (y_peak - y_ss) / y_ss
    zeta = np.sqrt( np.log(Mp)**2 / (np.log(Mp)**2 + np.pi**2) )
    omega = (1 / period_secs)*np.pi / np.sqrt(1-zeta**2)
    return [gain, omega, zeta]
