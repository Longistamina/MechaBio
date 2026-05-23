'''
The Fourier Series is strictly defined for periodic signals (signals where you know the period T in advance).

The core theorem states that any periodic signal, no matter how complex or jagged,
can be perfectly reconstructed by adding together a series of simple, smooth sine and cosine waves at specific "harmonic" frequencies.

################################################
# Master Formula: y(t) = A0/2 + sum[An*cos(n*w0*t) + Bn*sin(n*w0*t)]

y_t = A0/2 + np.sum(A_n * np.cos(n * omega0 * t) + B_n * np.sin(n * omega0 * t), axis=0)

𝐴0: The DC offset (the average static value of the signal).
𝜔0: The fundamental angular frequency, defined as 2𝜋/T
n: The harmonic number (1, 2, 3, ...).
𝐴n: The amplitude (weight) of the cosine wave at harmonic n
Bn: The amplitude (weight) of the sine wave at harmonic n

################################################
# Coefficient Formulas (based on orthogonality)

# A0 = (1/T) * integral(y(t) dt)
A0 = (1 / T) * np.trapezoid(y_t, t)

# An = (2/T) * integral(y(t) * cos(n*w0*t) dt)
A_n = (2 / T) * np.trapezoid(y_t * np.cos(n * omega0 * t), t)

# Bn = (2/T) * integral(y(t) * sin(n*w0*t) dt)
B_n = (2 / T) * np.trapezoid(y_t * np.sin(n * omega0 * t), t)

################################################
# Complex Exponential Form (Engineer's Preference)

# Master Formula: y(t) = sum[Cn * exp(i*n*w0*t)]
y_t = np.sum(C_n * np.exp(1j * n * omega0 * t), axis=0)

# Coefficient Formula
# Cn = (1/T) * integral(y(t) * exp(-i*n*w0*t) dt)
C_n = (1 / T) * np.trapezoid(y_t * np.exp(-1j * n * omega0 * t), t)
'''

import numpy as np
from plotly import graph_objects as go
import plotly.io as pio
from scipy import signal

pio.renderers.default = "browser"

T = 4*np.pi # T is a known period of the function
omega0 = (2*np.pi)/T
t = np.linspace(0, T, 2000)

# 1. The True Periodic Square Wave (Anti-symmetric / Odd)
# Using scipy's square wave function for the ground truth
y_t = true_square = signal.square(t)

# Plot the true square wave as a dashed reference line
fig = go.Figure()
fig.add_trace(go.Scatter(x=t, y=true_square, mode="lines", name="True Square signal"))
fig.show()

harmonics = [1, 3, 10, 20, 50]

for n in harmonics:
    n_range = np.arange(1, n+1).reshape(-1, 1)

    A0 = (1/T) * np.trapezoid(y_t, t)
    An = (2/T) * np.trapezoid(y_t * np.cos(n_range*omega0*t))
    Bn = (2/T) * np.trapezoid(y_t * np.sin(n_range*omega0*t))

    # Reshape An and Bn to (n, 1) so they can broadcast against the (n, 2000) time arrays
    An = An.reshape(-1, 1)
    Bn = Bn.reshape(-1, 1)

    y_fs = A0/2 + np.sum((An*np.cos(n_range*omega0*t) + Bn*np.sin(n_range*omega0*t)), axis=0)

    fig.add_trace(go.Scatter(x=t, y=y_fs, mode="lines", name=f"harmonic={n}", showlegend=True))

fig.show()
