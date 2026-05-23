'''
The Fourier Series is strictly defined for periodic signals (signals where you know the period T in advance).

The core theorem states that any periodic signal, no matter how complex or jagged,
can be perfectly reconstructed by adding together a series of simple, smooth sine and cosine waves at specific "harmonic" frequencies.

################################################
# Master Formula: y(t) = A0/2 + sum[An*cos(n*w0*t) + Bn*sin(n*w0*t)]

y_t = A0/2 + np.sum(A_n * np.cos(n * omega0 * t) + B_n * np.sin(n * omega0 * t), axis=0), nE[1, infinity]

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


#------------------------------------------------------------------------------------------------------#
#------------------------------------ Fourier series illustration -------------------------------------#
#------------------------------------------------------------------------------------------------------#

T = 4*np.pi # T is a known period of the function
omega0 = (2*np.pi)/T
t = np.linspace(0, T, 1000)

# 1. The True Periodic Square Wave (Anti-symmetric / Odd)
# Using scipy's square wave function for the ground truth
y_t = true_square = signal.square(t)

# Plot the true square wave as a dashed reference line
fig = go.Figure()
fig.add_trace(go.Scatter(x=t, y=true_square, mode="lines", name="True Square signal"))

harmonics = [2, 3, 10, 20, 50]

for n in harmonics:
    n_range = np.arange(1, n+1).reshape(-1, 1)

    A0 = (1/T) * np.trapezoid(y_t, t, axis=0)
    An = (2/T) * np.trapezoid(y_t * np.cos(n_range * omega0 * t), t, axis=1)
    Bn = (2/T) * np.trapezoid(y_t * np.sin(n_range * omega0 * t), t, axis=1)

    # Reshape An and Bn to (n, 1) so they can broadcast against the (n, 2000) time arrays
    An = An.reshape(-1, 1)
    Bn = Bn.reshape(-1, 1)

    y_fs = A0/2 + np.sum((An*np.cos(n_range*omega0*t) + Bn*np.sin(n_range*omega0*t)), axis=0)

    fig.add_trace(go.Scatter(x=t, y=y_fs, mode="lines", name=f"harmonic={n}", showlegend=True))

fig.show()


#----------------------------------------------------------------------------------------#
#------------------------------------ Orthogonality -------------------------------------#
#----------------------------------------------------------------------------------------#

T = 4*np.pi
t = np.linspace(0, T, 10000)

omega0 = 1.5

#####################################
## 1. Sine vs Cosine (always zero) ##
#####################################
'''∫cos(m*ω0*t)*cos(m*ω0*t)*dt = 0'''

m = 2
n = 5

cos_m = np.cos(m*omega0*t)
sin_n = np.sin(n*omega0*t)

integral_0_t = np.trapezoid(cos_m*sin_n, t, axis=0)
print(integral_0_t)
# -1.1102230246251565e-16 = 0

'''
Intuition:
    cos(a) = 0.2
    sin(b) = 0.3

    cos(-a) = 0.2
    sin(-b) = -0.3

=> Integral = cos(a)*sin(b) + cos(-a)*sin(-b) = 0.2*0.3 - 0.2*0.3 = 0
'''

#########################################################
## 2. Cosine/Sine, different frequencies (always zero) ##
#########################################################
'''
∫cos(m*ω0*t)*cos(n*ω0*t)*dt = 0
∫sin(m*ω0*t)*sin(n*ω0*t)*dt = 0
'''

m = 3
n = 7

cos_m = np.cos(m*omega0*t)
cos_n = np.cos(n*omega0*t)

integral_0_t = np.trapezoid(cos_m*cos_n, t)
print(integral_0_t)
# -5.828670879282072e-16

'''
Intuition:

    The Rule: cos(A) * cos(B) = 0.5 * [ cos(A - B) + cos(A + B) ]

    Let A = 3t  (m=3)
    Let B = 7t  (n=7)

    cos(3t) * cos(7t) = 0.5 * [ cos(3t - 7t) + cos(3t + 7t) ]
                      = 0.5 * [ cos(-4t)     + cos(10t) ]
                      = 0.5 * [ cos(4t)      + cos(10t) ]   <-- (since cos(-x) = cos(x))

=> Integral = 0.5 * [ Integral( cos(4t) ) + Integral( cos(10t) ) ]

    Because 4 and 10 are non-zero integers, both of these new waves complete
    an exact, whole number of full cycles over the period T.
    For any pure cosine wave, the positive peaks perfectly cancel out the negative valleys.

 Cycle 1      Cycle 2      Cycle 3      Cycle 4
  __            __            __            __
 /  \          /  \          /  \          /  \
/    \        /    \        /    \        /    \
      \__  __/      \__  __/      \__  __/      \__
         \/            \/            \/            \/

=> Integral = 0.5 * [ 0 + 0 ] = 0

##########################################

The same thing happen for sine:

∫sin(m*w*t)*sin(n*w*t)dt = 0
'''

###############################################
## 3. Cosine/Sine, same frequency (NON-ZERO) ##
###############################################
'''
∫cos(m*ω0*t)*cos(m*ω0*t)*dt = T/2
∫sin(m*ω0*t)*sin(m*ω0*t)*dt = T/2
'''

m = 5

cos_m = np.cos(m*omega0*t)

integral_0_t = np.trapezoid(cos_m*cos_m, t)
print(integral_0_t)
# 6.283185307179586 = 2*np.pi = T/2

'''
Intuition (Same Frequency: cos(3t) * cos(3t)):

    Let A = 3t, B = 3t

    cos(3t) * cos(3t) = 0.5 * [ cos(3t - 3t) + cos(3t + 3t) ]
                      = 0.5 * [ cos(0)       + cos(6t) ]
                      = 0.5 * [ 1            + cos(6t) ]    <-- (since cos(0) = 1)

=> Integral = 0.5 * [ Integral( 1 ) + Integral( cos(6t) ) ]

    The cos(6t) part completes full cycles and cancels out to 0.

    Now look at Integral(1) evaluated from t = 0 to t = T:
    1. 📏 An integral is geometrically just the "Area under the curve".
    2. 🟦 The function y = 1 is a flat, horizontal rectangle with a constant height of 1.
    3. ⏱️ The width of our time window is exactly one period (from 0 to T).
    4. 🧮 Area = Height × Width = 1 × T = T.

=> Final Integral = 0.5 * [ T + 0 ] = T/2

#####################

The same thing happens for sin:

∫sin(n*w*t)*sin(n*w*t)dt = T/2
'''

#-----------------------------------------------------------------------------------------------------------------#
#------------------------------------ Apply orthogonality to Fourrier Series -------------------------------------#
#-----------------------------------------------------------------------------------------------------------------#

##################
## Calculate An ##
##################
'''
y(t) = A0/2 + sum[An*cos(n*w0*t) + Bn*sin(n*w0*t)], nE[1, infinity]
     = A0/2 + A1*cos(1*w0*t) + B1*sin(1*w0*t) + A2*cos(2*w0*t) + B2*sin(2*w0*t) + A3*cos(3*w0*t) + B3*sin(3*w0*t) + ....

Let say, we want to calculate A2, multiply two sides for cos(2*w0*t), then Integrate

=> Based on the 1st and 2nd cases, all the term ``∫sin(...)*cos(...)`` and ``∫cos(n)*cos(m)`` are all canceled out,
   ``∫A0/2*cos(2*w0*t)`` is also canceled (positive and negative valleys canceled out each other)
   only the 3rd case ``A2∫cos(2*w0*t)*cos(2*w0*t)``

=> ∫y(t)cos(2*w0*t)dt = 0 + 0 + A2∫cos(2*w0*t)*cos(2*w0*t)dt + 0 + .....
=> ∫y(t)cos(2*w0*t)dt = A2 * T/2
=> A2 = 2/T * ∫y(t)cos(2*w0*t)dt
=> An = 2/T * ∫y(t)cos(n*w0*t)dt
'''

##################
## Calculate Bn ##
##################
'''
y(t) = A0/2 + sum[An*cos(n*w0*t) + Bn*sin(n*w0*t)], nE[1, infinity]
     = A0/2 + A1*cos(1*w0*t) + B1*sin(1*w0*t) + A2*cos(2*w0*t) + B2*sin(2*w0*t) + A3*cos(3*w0*t) + B3*sin(3*w0*t) + ....

Let say, we want to calculate B2, multiply two sides for sine(2*w0*t), then Integrate

=> Based on the 1st and 2nd cases, all the term ``∫sin(...)*cos(...)`` and ``∫sin(n)*sin(m)`` are all canceled out,
   ``∫A0/2*sin(2*w0*t)`` is also canceled (positive and negative valleys canceled out each other)
   only the 3rd case ``B2∫sin(2*w0*t)*sin(2*w0*t)``

=> ∫y(t)sin(2*w0*t)dt = 0 + 0 + B2∫sin(2*w0*t)*sin(2*w0*t)dt + 0 + .....
=> ∫y(t)sin(2*w0*t)dt = A2 * T/2
=> B2 = 2/T * ∫y(t)sin(2*w0*t)dt
=> Bn = 2/T * ∫y(t)sin(n*w0*t)dt
'''
