'''
=============================================================================
 MODELING A FIRST-ORDER MEASUREMENT SYSTEM
=============================================================================
PHYSICAL ANALOGY: A sluggish thermometer dipped into boiling water.
It doesn't jump instantly; it has "thermal inertia" and curves up slowly.

THE DIFFERENTIAL EQUATION:
    tau * (dy/dt) + y = x(t)

    x(t) = The TRUE physical input (e.g., actual water temp)
    y(t) = The MEASURED output (e.g., what the thermometer displays)
    dy/dt = How fast the measurement is changing
    tau   = Time Constant (how sluggish the sensor is)

THE LAPLACE TRANSFER FUNCTION (The Engineer's Cheat Code):
    By replacing the derivative (d/dt) with the variable 's', we get:
    H(s) = Output / Input = 1 / (tau*s + 1)
=============================================================================
'''

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sbn
from scipy import signal

sbn.set_theme(style="darkgrid")

#--------------------------------------------------------------------------------#
# 1. DEFINE THE LTI MEASUREMENT SYSTEM (First-Order)
#--------------------------------------------------------------------------------#
# Let's model a slow thermometer with a time constant (tau) of 0.5 seconds.
# The differential equation is: tau * dy/dt + y = x(t)
# In the Laplace domain (Transfer Function), this is: H(s) = 1 / (tau*s + 1)
tau = 0.5

# We define H(s) = 1 / (tau*s + 1) using the coefficients of 's'.
# Numerator: 1           -> [1]
# Denominator: tau*s + 1 -> [tau, 1]
sys = signal.TransferFunction([1], [tau, 1])

# Time array (5 seconds of data)
t = np.linspace(0, 5, 1000)

#--------------------------------------------------------------------------------#
# 2. CREATE THE FOURIER COMPONENTS (Individual Sine Waves)
#--------------------------------------------------------------------------------#
# Let's create 3 simple sine waves of different frequencies
f1, f2, f3 = 1.0, 3.0, 8.0  # Frequencies in Hz
omega1, omega2, omega3 = 2*np.pi*f1, 2*np.pi*f2, 2*np.pi*f3

x1 = np.sin(omega1 * t)  # 1 Hz (Slow)
x2 = np.sin(omega2 * t)  # 3 Hz (Medium)
x3 = np.sin(omega3 * t)  # 8 Hz (Fast)

#--------------------------------------------------------------------------------#
# 3. CREATE THE COMPLEX INPUT SIGNAL
#--------------------------------------------------------------------------------#
# In the real world, the physical variable we are measuring is a messy combination
x_complex = x1 + x2 + x3

#--------------------------------------------------------------------------------#
# 4. SIMULATE THE SYSTEM (The LTI Magic)
#--------------------------------------------------------------------------------#
# Method A: Pass the complex, messy signal through the system all at once
t_out, y_complex, _ = signal.lsim(sys, x_complex, t)

# Method B: Pass each simple sine wave through individually (The Fourier Way)
_, y1, _ = signal.lsim(sys, x1, t)
_, y2, _ = signal.lsim(sys, x2, t)
_, y3, _ = signal.lsim(sys, x3, t)

# Use SUPERPOSITION: Just add the individual outputs together!
y_summed = y1 + y2 + y3

#--------------------------------------------------------------------------------#
# 5. PLOT AND PROVE THEY ARE IDENTICAL
#--------------------------------------------------------------------------------#
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

# Top Plot: The Inputs
ax1.plot(t, x1, alpha=0.5, label='1 Hz Component')
ax1.plot(t, x2, alpha=0.5, label='3 Hz Component')
ax1.plot(t, x3, alpha=0.5, label='8 Hz Component')
ax1.plot(t, x_complex, color='black', linewidth=2, label='Complex Real-World Input')
ax1.set_title("Time Domain: The Input Signal (What we are trying to measure)", fontsize=14)
ax1.set_ylabel("Amplitude")
ax1.legend(loc='upper right')

# Bottom Plot: The Outputs
ax2.plot(t_out, y_complex, color='red', linewidth=4, alpha=0.5, label='System Response to Complex Input')
ax2.plot(t_out, y_summed, color='blue', linestyle='--', linewidth=2, label='Sum of Individual Responses (Superposition)')
ax2.set_title("System Output: Proving the Logical Bridge (Superposition)", fontsize=14)
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Sensor Reading")
ax2.legend(loc='upper right')

plt.tight_layout()
plt.show()

'''
Look at the Top Plot: The black line is a messy, jagged signal. If you had to solve the differential equation
``tau * dy/dt + y = x(t) = black line`` using raw calculus, it would be incredibly difficult.

Look at the Bottom Plot: The thick red line and the dashed blue line perfectly overlap.
This proves that Superposition works! By breaking the black line into simple sine waves (Fourier),
passing them through the system individually, and adding them up, we bypassed the hard calculus entirely.

Notice the Filtering Effect: Look closely at the output (bottom plot).
The 1 Hz wave (slow) passed through with almost full amplitude.
But the 8 Hz wave (fast) was almost completely flattened out!
Because the thermometer (First-Order System) has "thermal inertia,"
it physically cannot react fast enough to catch the 8 Hz fluctuations.
This is exactly why the professor stated that First-Order systems naturally act as Low-Pass Filters.
'''
