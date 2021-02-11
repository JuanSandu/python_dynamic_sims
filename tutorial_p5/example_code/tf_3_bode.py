from scipy import signal as sig
import matplotlib.pyplot as plt
import numpy as np


k = -0.9
num_zeros = [ [1, -1.15], [1, 1.3, 0.1] ]
den_poles = [ [1, 0.5], [1, 0.3], [1, 1.8, 0.7] ]

num = [1]
den = [1]
for i in range(len(num_zeros)):
    num = np.polymul(num, num_zeros[i])
for i in range(len(den_poles)):
    den = np.polymul(den, den_poles[i])

Gs = sig.TransferFunction(np.dot(k, num), den)

w, mag, phase = sig.bode(Gs)

plt.subplot(2,1,1)
plt.semilogx(w, mag, 'r')
plt.ylabel('Magnitude [dB]')
plt.title('Bode diagram.')
plt.grid()

plt.subplot(2,1,2)
plt.semilogx(w, phase, 'r')
plt.ylabel('Phase (deg)')

plt.xlabel('freq [rad/s]')
plt.grid()

plt.show()
