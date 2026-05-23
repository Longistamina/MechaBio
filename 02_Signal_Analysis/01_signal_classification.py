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
plt.title("Static signal")
plt.xlabel("Time (s)")
plt.ylabel("Signal amplitude")
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
plt.title("Simple waveform")
plt.xlabel("Time (s)")
plt.ylabel("Signal amplitude")
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
plt.title("Complex waveform (combination of 40 simple waveforms)")
plt.xlabel("Time (s)")
plt.ylabel("Signal amplitude")
plt.show()

#########################
## Aperiodic waveforms ##
#########################
'''
Aperiodic signals do not repeat over time.
Can mathematically think of an aperiodic signal as a periodic signal with an INFINITE period (T -> ∞).

Common examples from the slides: Step, Ramp, and Pulse.
'''

# Using a higher resolution time array to capture sharp, sudden changes accurately
t = np.linspace(0, 20, 1000)

#----- 1. Step Function -----#
'''
A sudden jump in amplitude that stays constant.
y(t) = 0 for t < t0
y(t) = A for t >= t0
'''
t0_step = 5.0
A_step = 5.0
# np.where is great for piecewise functions: np.where(condition, value_if_true, value_if_false)
y_step = np.where(t >= t0_step, A_step, 0.0)

plt.figure(figsize=(20, 5))
sbn.lineplot(x=t, y=y_step, linewidth=2.5, color='blue')
plt.title("Step Function (Aperiodic)")
plt.xlabel("Time (s)")
plt.ylabel("Signal Amplitude")
plt.ylim(-1, 7)
plt.show()

#----- 2. Ramp Function -----#
'''
A signal that increases linearly with time after a certain point.
y(t) = 0 for t < t0
y(t) = K * (t - t0) for t >= t0
'''
t0_ramp = 5.0
K_ramp = 1.5 # Slope of the ramp
y_ramp = np.where(t >= t0_ramp, K_ramp * (t - t0_ramp), 0.0)

plt.figure(figsize=(20, 5))
sbn.lineplot(x=t, y=y_ramp, linewidth=2.5, color='green')
plt.title("Ramp Function (Aperiodic)")
plt.xlabel("Time (s)")
plt.ylabel("Signal Amplitude")
plt.ylim(-1, 25)
plt.show()

#----- 3. Pulse Function (Rectangular Pulse) -----#
'''
A signal that jumps to a certain amplitude for a finite duration and then returns to zero.
y(t) = A for t1 <= t < t2
y(t) = 0 otherwise
'''
t1_pulse = 6.0
t2_pulse = 12.0
A_pulse = 4.0
# Using logical AND (&) for multiple conditions
y_pulse = np.where((t >= t1_pulse) & (t < t2_pulse), A_pulse, 0.0)

plt.figure(figsize=(20, 5))
sbn.lineplot(x=t, y=y_pulse, linewidth=2.5, color='purple')
plt.title("Rectangular Pulse Function (Aperiodic)")
plt.xlabel("Time (s)")
plt.ylabel("Signal Amplitude")
plt.ylim(-1, 6)
plt.show()


#-------------------------------------------------------------------------------------------------------------------#
#------------------------------------- 3. Nondeterministic waveform - noise ----------------------------------------#
#-------------------------------------------------------------------------------------------------------------------#

#------------------------------------------------------------------------------------------------#
#--------------------------------- 3. Nondeterministic Signals ----------------------------------#
#------------------------------------------------------------------------------------------------#
'''
Nondeterministic signals are stochastic (random) and lack a specific,
explainable mathematical pattern. The classic example is NOISE.
'''

# Using a high-resolution time array so the random fluctuations look continuous
t = np.linspace(0, 10, 1000)

#----- 1. Pure White Noise (Classic Nondeterministic) -----#
'''
White noise has equal intensity across all frequencies.
It looks like random static and is completely unpredictable.
'''
white_noise = np.random.randn(1000) * 1.5

plt.figure(figsize=(20, 5))
# Using alpha=0.8 to make the dense overlapping lines look like a "fuzzy" band
sbn.lineplot(x=t, y=white_noise, linewidth=1, color='red', alpha=0.8)
plt.title("Pure Nondeterministic Signal: White Noise (Environmental Interference)")
plt.xlabel("Time (s)")
plt.ylabel("Signal Amplitude")
plt.show()


#----- 2. Random Walk / Brownian Noise (Realistic Sensor Drift) -----#
'''
In real biological/mechanical instruments, noise isn't always pure static.
Often it's a "random walk" (low-frequency noise) caused by thermal drift
in sensors, which wanders unpredictably over time.
'''
brownian_noise = np.cumsum(np.random.randn(1000)) * 0.1

plt.figure(figsize=(20, 5))
sbn.lineplot(x=t, y=brownian_noise, linewidth=2.5, color='darkorange')
plt.title("Nondeterministic Signal: Random Walk (Sensor Thermal Drift)")
plt.xlabel("Time (s)")
plt.ylabel("Signal Amplitude")
plt.show()
