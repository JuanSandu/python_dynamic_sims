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

t, y = sig.step(Gs)

plt.plot(t, y, 'b')
plt.xlabel('Time [s]')
plt.ylabel('Value [Output units]')
plt.title('Step response.')
plt.grid()

plt.show()
