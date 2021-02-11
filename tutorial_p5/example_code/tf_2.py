from scipy import signal as sig
import matplotlib.pyplot as plt
import numpy as np


k = 0.9
num = [1]
den = [1, 0.65, 1]

Gs = sig.TransferFunction(np.dot(k, num), den)


t, y = sig.step(Gs)

plt.plot(t, y, 'b')
plt.xlabel('Time [s]')
plt.ylabel('Value [Output units]')
plt.title('Step response.')
plt.grid()

plt.show()
