'''
=============================================================================
 MODELING A ZERO-ORDER MEASUREMENT SYSTEM
=============================================================================
PHYSICAL ANALOGY: An ideal, perfect sensor with zero "inertia" or "lag".
Imagine a perfect ruler measuring length, or an idealized instant-read
thermometer that jumps to 100°C the exact millisecond it touches boiling water.
It has no thermal mass, no electrical capacitance, and no mechanical friction.

THE DIFFERENTIAL EQUATION:
    y(t) = K * x(t)

    x(t) = The TRUE physical input
    y(t) = The MEASURED output
    K    = Static Sensitivity (a simple multiplication factor)

THE LAPLACE TRANSFER FUNCTION:
    Because there are no derivatives (no rates of change or memory),
    the Transfer Function is just a constant:
    H(s) = Output / Input = K
=============================================================================
'''

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sbn
from scipy import signal

sbn.set_theme(style="darkgrid")

#--------------------------------------------------------------------------------#
# 1. DEFINE THE LTI MEASUREMENT SYSTEM (Zero-Order)
#--------------------------------------------------------------------------------#
# Let's model an ideal sensor with a static sensitivity (K) of 2.0.
# This means it perfectly scales the input by 2, with zero delay.
K = 2.0

# We define H(s) = K / 1 using the coefficients of 's'.
# Numerator: K -> [K]
# Denominator: 1 -> [1]
sys = signal.TransferFunction([K], [1])

# Time array (5 seconds of data)
t = np.linspace(0, 5, 1000)

#--------------------------------------------------------------------------------#
# 2. CREATE THE FOURIER COMPONENTS (Individual Sine Waves)
#--------------------------------------------------------------------------------#
# We use the exact same frequencies as the First-Order script for comparison.
f1, f2, f3 = 1.0, 3.0, 8.0  # Frequencies in Hz (Slow, Medium, Fast)
omega1, omega2, omega3 = 2*np.pi*f1, 2*np.pi*f2, 2*np.pi*f3

x1 = np.sin(omega1 * t)  # 1 Hz
x2 = np.sin(omega2 * t)  # 3 Hz
x3 = np.sin(omega3 * t)  # 8 Hz

#--------------------------------------------------------------------------------#
# 3. CREATE THE "MESSY" REAL-WORLD SIGNAL
#--------------------------------------------------------------------------------#
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
ax1.plot(t, x_complex, color='black', linewidth=2, label='Complex Real-World Input x(t)')
ax1.set_title("Time Domain: The Input Signal (True Physical Phenomenon)", fontsize=14)
ax1.set_ylabel("Amplitude")
ax1.legend(loc='upper right')

# Bottom Plot: The Outputs
ax2.plot(t_out, y_complex, color='red', linewidth=4, alpha=0.5, label='Method A: System Response to Complex Input')
ax2.plot(t_out, y_summed, color='blue', linestyle='--', linewidth=2, label='Method B: Sum of Individual Responses (Superposition)')
ax2.set_title(f"System Output y(t): Zero-Order Response (Scaled by K={K}, Zero Lag)", fontsize=14)
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Sensor Reading")
ax2.legend(loc='upper right')

plt.tight_layout()
plt.show()

'''
=============================================================================
 WHAT TO LOOK FOR IN THE PLOTS (Contrast with First-Order):
=============================================================================
1. THE OVERLAP (Bottom Plot):
    The thick red line and the dashed blue line perfectly overlap.
    This proves that Superposition works! By breaking the black line into simple sine waves (Fourier),
    passing them through the system individually, and adding them up, we bypassed the hard calculus entirely.

2. THE LACK OF FILTERING (The Physics of K):
   Look closely at the output waves compared to the input waves.
   - The 1 Hz, 3 Hz, and 8 Hz waves ALL passed through perfectly.
   - Their amplitudes are exactly doubled (because K = 2.0).
   - There is ZERO phase shift (no left/right time delay).

   WHY? Because a Zero-Order system has no "memory" or "storage elements"
   (no thermal mass, no capacitors). It does NOT act as a Low-Pass Filter.
   It tracks infinitely fast changes perfectly. While physically impossible
   in the real world, it serves as the ideal baseline for static calibration!
=============================================================================
'''
