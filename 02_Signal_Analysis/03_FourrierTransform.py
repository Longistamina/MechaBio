'''
1. The Limitation of the Fourier Series
# The Fourier Series is incredibly powerful, but it has one strict rule: You must know the period (T) in advance.
# But what if you are measuring a single, isolated event?
# For example, a single rectangular voltage spike, a sudden earthquake, or a single spoken word.
# These are aperiodic signals—they do not repeat. Because they don't repeat, you don't have a period T to plug into your Fourier Series formula.

2. The "Infinite Period" Trick
# Remember how we defined an aperiodic signal earlier?
# We said you can mathematically think of an aperiodic signal as a periodic signal with an infinite period (T→∞).
# Imagine a single rectangular pulse. Now, imagine forcing it to repeat,
# but the next pulse doesn't arrive for 10 seconds. Then 100 seconds. Then 10,000 seconds.
# As the gap between pulses stretches to infinity, the signal effectively stops repeating and becomes a single, isolated aperiodic pulse.

3. From Discrete Bars to a Continuous Spectrum
What happens to the math when T→∞?
# In the Fourier Series, the "step size" between frequencies is ``Δf = 1/T (or Δω = 2π/T)
# As T becomes infinitely large, the step size, Δf becomes infinitesimally small (approaching zero).
# The discrete "bars" or "spikes" of the Fourier Series get closer and closer together until the gaps completely disappear.
# The discrete summation (Σ) turns into a continuous integral (∫).
Instead of asking "What is the amplitude of the exact 3Hz harmonic?",
the Fourier Transform asks "What is the continuous density of frequencies around 3Hz?"
It provides a continuous curve that shows the "weighting" of every possible frequency from −∞ to +∞.

4. The Classic Example: The Rectangular Pulse → Sinc Function (sinc(x) = sin(πx)/πx = sin(x)/x)
# Periodic Square Wave: Its Fourier Series is a set of discrete, shrinking bars (only odd harmonics).
# Single Rectangular Pulse (Aperiodic): Its Fourier Transform is a continuous, wavy curve called the Sinc function

######################################################

Measurement workflow:
    1. Forward Transform: Take a crazy, complex input signal x(t) and break it into simple sine waves X(f)
    2. The System (Transfer Function): Pass those simple sine waves X(f) through your measurement system
       (like a thermometer or an electronic filter). The system changes their amplitudes and phases,
       creating a new modified spectrum, let's call it Y(f)
    3. Inverse Transform: Take that modified spectrum Y(f) and use the Inverse Fourier Transform
       to "rebuild" the final output signal y(t) that your sensor will actually display!
'''

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sbn

sbn.set_theme(style="darkgrid")

#--------------------------------------------------------------------------------------------------------#
#----------------------------------- Fourrier transform demonstration -----------------------------------#
#--------------------------------------------------------------------------------------------------------#

# 1. Create the Aperiodic Signal (A single Rectangular Pulse)
dt = 0.001  # High resolution for smooth continuous math
t = np.arange(-5, 5, dt)

# Pulse is "ON" (Amplitude 1) between t=-1 and t=1, and "OFF" (0) everywhere else
pulse = np.where((t >= -1) & (t <= 1), 1.0, 0.0)

# 2. The Analytical Fourier Transform (The Continuous Sinc Function)
# The mathematical FT of a rect pulse of width 2 is exactly 2 * sinc(f * 2)
# Note: numpy's sinc function is defined as sin(pi*x)/(pi*x)
f = np.linspace(-5, 5, 1000)
continuous_ft = 2 * np.sinc(f * 2)

# 3. Plotting Time Domain vs. Frequency Domain
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 5))

# Left Plot: Time Domain (The Aperiodic Signal)
ax1.fill_between(t, pulse, color='blue', alpha=0.3)
ax1.plot(t, pulse, color='blue', linewidth=2)
ax1.set_title("Time Domain: Single Rectangular Pulse (Aperiodic)", fontsize=14)
ax1.set_xlabel("Time (t)", fontsize=12)
ax1.set_ylabel("Amplitude", fontsize=12)
ax1.set_xlim(-4, 4)
ax1.set_ylim(-0.2, 1.5)

# Right Plot: Frequency Domain (The Continuous Fourier Transform)
ax2.plot(f, continuous_ft, color='red', linewidth=3, label="Continuous FT (Sinc Function)")
ax2.fill_between(f, continuous_ft, where=(continuous_ft > 0), color='green', alpha=0.3, label="Positive Phase")
ax2.fill_between(f, continuous_ft, where=(continuous_ft < 0), color='purple', alpha=0.3, label="Negative Phase")
ax2.axhline(0, color='black', linewidth=1)
ax2.set_title("Frequency Domain: Continuous Spectrum", fontsize=14)
ax2.set_xlabel("Frequency (f)", fontsize=12)
ax2.set_ylabel("Magnitude / Weighting", fontsize=12)
ax2.legend(fontsize=11)

plt.tight_layout()
plt.show()


#----------------------------------------------------------------------------------------------------------------------#
#---------------------------- Step 1: The "Testing" Formula (Forward Fourier Transform) -------------------------------#
#----------------------------------------------------------------------------------------------------------------------#
'''
In the Fourier Series, we multiplied our signal by cos(nω0t) to "test" if a specific frequency was present (Orthogonality).

In the Fourier Transform, because the period is infinite and frequencies are continuous,
we replace the discrete sum with a continuous integral from −∞ to +∞,
and we use the complex exponential with a negative sign as our "testing" wave.

X(f) = integral[x(t) * e^(-i * 2*pi*f*t) * dt]
'''

#--------------------------------------------------------------------------------#
# 1. THE TIME DOMAIN (The continuous signal we are analyzing)
#--------------------------------------------------------------------------------#
# We just need a high-resolution time window to approximate the continuous integral
dt = 0.001
t = np.arange(-10, 10, dt)

# Let's use the Aperiodic Rectangular Pulse from earlier
x_t = np.where((t >= -1) & (t <= 1), 1.0, 0.0)


#--------------------------------------------------------------------------------#
# 2. THE FREQUENCY DOMAIN (The continuous "probe" points)
#--------------------------------------------------------------------------------#
# Instead of using a fake T and np.arange, we just define a smooth, dense grid
# that spans both NEGATIVE and POSITIVE frequencies.
# 2000 points is more than enough to draw a perfectly smooth continuous curve.
f = np.linspace(-20, 20, 2000)

# Reshape to column vector for broadcasting: shape becomes (2000, 1)
f_col = f.reshape(-1, 1)


#--------------------------------------------------------------------------------#
# 3. THE CONTINUOUS FOURIER TRANSFORM INTEGRAL
#--------------------------------------------------------------------------------#
# Formula: X(f) = integral[ x(t) * e^(-i * 2*pi*f*t) ] dt

# Create the complex exponential testing wave
complex_wave = np.exp(-1j * 2 * np.pi * f_col * t)

# Multiply and integrate over time (axis=1)
# np.trapezoid handles the continuous time integration beautifully
X_f = np.trapezoid(x_t * complex_wave, x=t, axis=1)


#--------------------------------------------------------------------------------#
# 4. EXTRACTING MAGNITUDE AND PHASE
#--------------------------------------------------------------------------------#
# Because X_f is complex, we extract the physical meaning:
magnitude = np.abs(X_f)      # How much of frequency f is present?
phase = np.angle(X_f)        # What is the time-shift (phase) of frequency f?

# (Optional) Print to prove it worked without crashing!
print(f"Frequency array shape: {f.shape}")
print(f"Transformed X(f) shape: {X_f.shape}")
print(f"Magnitude at 0 Hz (DC area): {magnitude[np.argmin(np.abs(f))]:.2f}")
# Frequency array shape: (2000,)
# Transformed X(f) shape: (2000,)
# Magnitude at 0 Hz (DC area): 2.00


#-----------------------------------------------------------------------------------------------------------------------#
#---------------------------- Step 2: The "Building" Formula (Inverse Fourier Transform) -------------------------------#
#-----------------------------------------------------------------------------------------------------------------------#
'''
The Forward Transform analyzed a recorded song and gave you a list of settings:
"To make this song, you need 10% of a 50Hz bass wave, 40% of a 440Hz guitar wave, etc."
This list of settings is your frequency spectrum X(f).

The Inverse Transform is the act of actually turning on all those oscillators at the exact specified volumes and phases,
and letting them play together in the room to recreate the original song, x(t).
'''

dt = 0.001
t = np.arange(-10, 10, dt)
t_col = t.reshape(-1, 1)

f = np.linspace(-20, 20, 2000)

#--------------------------------------------------------------------------------#
# INVERSE FOURIER TRANSFORM (Frequency Domain -> Time Domain)
#--------------------------------------------------------------------------------#
# Formula: x(t) = integral[ X(f) * e^(+i * 2*pi*f*t) ] df

# 1. Create the complex exponential "building" wave (Notice the POSITIVE sign and '1j')
# Shape becomes (num_time_points, num_frequencies)
complex_wave_inverse = np.exp(1j * 2 * np.pi * t_col * f)

# 2. Multiply by the spectrum X(f) and integrate over frequency (axis=1)
# X_f broadcasts across the rows, and we integrate along the columns (the f axis)
x_t_reconstructed = np.trapezoid(X_f * complex_wave_inverse, x=f, axis=1)

# 3. Extract the physical signal
# The math guarantees the imaginary parts cancel out, but floating-point math
# might leave microscopic noise (e.g., 1e-16j). We take the real part to clean it.
x_t_final = np.real(x_t_reconstructed)
