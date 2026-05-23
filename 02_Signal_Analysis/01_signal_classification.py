'''
A signal is a representation of a physical quantity that varies with time, effectively acting as a transmission of information.

Signal classification:
    + Static signal
    + Dynamic signal: periodic, aperiodic

Nondeterministic waveform ~ noise
'''

import numpy as np
import seaborn as sbn
import matplotlib.pyplot as plt

sbn.set_theme(style="darkgrid")

#-----------------------------------------------------------------------------------------------#
#------------------------------------- 1. Static signal ----------------------------------------#
#-----------------------------------------------------------------------------------------------#
'''
Static Signals: These do not change over time and appear as a constant amplitude line.

y(t) = A0
'''

A0 = 3.2
t = np.arange(20)

sbn.lineplot(x=t, y=A0)
plt.xlabel("Time (s)")
plt.ylabel("Signal")
plt.show()

'''One straight line'''

#------------------------------------------------------------------------------------------------#
#------------------------------------- 2. Dynamic signal ----------------------------------------#
#------------------------------------------------------------------------------------------------#
'''Dynamic signals are signals that vary over time'''

##############
## Periodic ##
##############
'''
Repeat after a certain period: y(t+T) = y(t)

Simple waveform: y(t) = A0 + Csin(ωt + ϕ)
Complex waveform: y(t) = A0 + Σn=1_∞C_n*sin(nωt + ϕ_n)
'''

#----- simple waveform -----#

A0 = 2.
C = 1.5
omega = 4
phi = 8

t = np.arange(100)
y = A0 + C*np.sin(omega*t + phi)

plt.figure(figsize=(20, 5))
sbn.lineplot(x=t, y=y)
plt.xlabel("Time (s)")
plt.ylabel("Signal")
plt.show()

#----- complex waveform -----#

A0 = 1.5
omega = 2.5
t = np.arange(100)

n = np.arange(1, 41).reshape(-1, 1) # 40 different waveforms
C_n = np.random.randn(40).reshape(-1, 1)
phi_n = np.random.randn(40).reshape(-1, 1)

y = A0 + np.sum((C_n*np.sin(n*omega*t + phi_n)), axis=0)

plt.figure(figsize=(20, 5))
sbn.lineplot(x=t, y=y)
plt.xlabel("Time (s)")
plt.ylabel("Signal")
plt.show()
