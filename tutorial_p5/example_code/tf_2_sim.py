from scipy import signal as sig
import matplotlib.pyplot as plt
import numpy as np


k = 12.8
num = [1]
den = [1, 2.65, 2]

Gs = sig.TransferFunction(np.dot(k, num), den)
t = np.linspace(0, 3.5, 600)
u = np.cos(2*np.pi*1.0*t)

tsim, ysim, xsim = sig.lsim2(Gs, U=u, T=t)


plt.subplot(2,1,1)
plt.ylim([-1.3, 1.3])
plt.plot(tsim, ysim, 'r')
plt.ylabel('Output [out. units]')
plt.title('Simulation.')
plt.grid()

plt.subplot(2,1,2)
plt.plot(t, u, 'b')
plt.ylabel('Control signal [control units]')

plt.xlabel('time [s]')
plt.grid()

plt.show()
