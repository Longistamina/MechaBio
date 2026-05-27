'''
=============================================================================
 REVIEW: MODELING A SECOND-ORDER MEASUREMENT SYSTEM
=============================================================================
PHYSICAL ANALOGY: A mass on a spring with a shock absorber (damper).
Unlike a 1st-order system (which only has one type of "inertia" like thermal mass),
a 2nd-order system has TWO competing storage elements:
1. Potential Energy (the spring's stiffness pulling it back)
2. Kinetic Energy (the mass's momentum pushing it forward)
This competition allows the system to "overshoot" and oscillate (ripple).

THE DIFFERENTIAL EQUATION (Newton's Second Law):
m * y''(t) + c * y'(t) + k * y(t) = F(t)

Normalized Standard Form:
y''(t) + 2*zeta*wn*y'(t) + wn^2 * y(t) = wn^2 * x(t)

wn   = Natural Frequency (sqrt(k/m)) - how fast it "wants" to oscillate.
zeta = Damping Ratio (c / 2*sqrt(m*k)) - how much friction resists the motion.

THE THREE DAMPING REGIMES (Step Response):
1. Underdamped (0 < zeta < 1): Not enough friction. The system overshoots
   the target and oscillates ("wrinkles") before settling.
2. Critically Damped (zeta = 1): The "Goldilocks" zone. The fastest possible
   response to reach the target without any overshoot or oscillation.
3. Overdamped (zeta > 1): Too much friction. The system sluggishly creeps
   to the target, behaving somewhat like a slow 1st-order system.

THE LAPLACE TRANSFER FUNCTION:
H(s) = wn^2 / (s^2 + 2*zeta*wn*s + wn^2)

RESONANCE (The "Beauty" of 2nd Order Systems):
If you drive an UNDERDAMPED system with a periodic input (sine wave) at
exactly its natural frequency (wn), the system absorbs the energy and the
output amplitude is MASSIVELY amplified. This is the core principle behind
dynamic mode mechanical sensors (like cantilevers and SMRs).
=============================================================================
'''

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sbn
from scipy import signal

sbn.set_theme(style="darkgrid")

#--------------------------------------------------------------------------------#
# 1. DEFINE THE SYSTEM PARAMETERS
#--------------------------------------------------------------------------------#

wn = 10.0  # Natural frequency: 10 rad/s (approx 1.59 Hz)

# The three damping scenarios
zeta_under = 0.2   # Underdamped (bouncy, will resonate)
zeta_crit  = 1.0   # Critically damped (optimal for step tracking)
zeta_over  = 2.0   # Overdamped (sluggish)

#--------------------------------------------------------------------------------#
# 2. DEFINE THE TRANSFER FUNCTIONS
#--------------------------------------------------------------------------------#
# H(s) = wn^2 / (s^2 + 2*zeta*wn*s + wn^2)
# Numerator: [wn^2]
# Denominator: [1, 2*zeta*wn, wn^2]

sys_under = signal.TransferFunction([wn**2], [1, 2*zeta_under*wn, wn**2])
sys_crit  = signal.TransferFunction([wn**2], [1, 2*zeta_crit*wn, wn**2])
sys_over  = signal.TransferFunction([wn**2], [1, 2*zeta_over*wn, wn**2])

# Time array for Step Response
t = np.linspace(0, 8, 2000)
x_step = np.ones_like(t)  # Step input of amplitude 1

# Calculate Step Responses
_, y_step_under, _ = signal.lsim(sys_under, x_step, t)
_, y_step_crit, _  = signal.lsim(sys_crit, x_step, t)
_, y_step_over, _  = signal.lsim(sys_over, x_step, t)

#--------------------------------------------------------------------------------#
# 3. CALCULATE FREQUENCY RESPONSE (Bode Plot Data)
#--------------------------------------------------------------------------------#

# We sweep frequencies from 0.1 to 100 rad/s to find the resonance peak
w_sweep = np.logspace(-1, 2, 1000)

# signal.bode returns: frequencies (w), magnitude in dB, phase in degrees
w_u, mag_u_dB, phase_u = signal.bode(sys_under, w=w_sweep)
w_c, mag_c_dB, phase_c = signal.bode(sys_crit, w=w_sweep)
w_o, mag_o_dB, phase_o = signal.bode(sys_over, w=w_sweep)

# Convert dB back to Linear Magnitude (Amplification Factor)
# dB = 20 * log10(Linear)  =>  Linear = 10^(dB/20)
mag_u_lin = 10**(mag_u_dB / 20)
mag_c_lin = 10**(mag_c_dB / 20)
mag_o_lin = 10**(mag_o_dB / 20)

#--------------------------------------------------------------------------------#
# 4. PLOT THE RESULTS
#--------------------------------------------------------------------------------#
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12))

# ================= TOP PLOT: STEP RESPONSE =================
ax1.plot(t, x_step, color='black', linestyle=':', linewidth=2, label='Step Input (Target)')
ax1.plot(t, y_step_under, color='red', linewidth=2.5, label=f'Underdamped (ζ={zeta_under}) - Oscillates!')
ax1.plot(t, y_step_crit, color='green', linewidth=2.5, label=f'Critically Damped (ζ={zeta_crit}) - Fastest, No Overshoot')
ax1.plot(t, y_step_over, color='blue', linewidth=2.5, label=f'Overdamped (ζ={zeta_over}) - Sluggish')
ax1.set_title("Second-Order Step Response: The Three Damping Regimes", fontsize=16)
ax1.set_ylabel("Amplitude (y)", fontsize=12)
ax1.legend(loc='right', fontsize=11)
ax1.set_ylim(-0.5, 2.0)
ax1.set_xlim(0, 8)

# ================= BOTTOM PLOT: FREQUENCY RESPONSE (RESONANCE) =================
# Using semilogx because frequency sweeps are best viewed on a logarithmic scale
ax2.semilogx(w_u, mag_u_lin, color='red', linewidth=3, label=f'Underdamped (ζ={zeta_under}) - RESONANCE PEAK!')
ax2.semilogx(w_c, mag_c_lin, color='green', linewidth=2, label=f'Critically Damped (ζ={zeta_crit})')
ax2.semilogx(w_o, mag_o_lin, color='blue', linewidth=2, label=f'Overdamped (ζ={zeta_over})')

# Mark the natural frequency (wn)
ax2.axvline(wn, color='black', linestyle='--', alpha=0.6, label=f'Natural Frequency (ω_n = {wn} rad/s)')

ax2.set_title("Frequency Response: The 'Beauty' of Resonance (Amplitude Amplification)", fontsize=16)
ax2.set_xlabel("Driving Frequency (ω) [rad/s]", fontsize=12)
ax2.set_ylabel("Linear Magnitude (Output / Input)", fontsize=12)
ax2.legend(loc='upper right', fontsize=11)
ax2.set_ylim(0, 3.5) # Cap the y-axis so we can see the other lines clearly

plt.tight_layout()
plt.show()

'''
=============================================================================
 WHAT TO LOOK FOR IN THE PLOTS (Connecting to Lecture 6):
=============================================================================
1. THE STEP RESPONSE (Top Plot):
   - RED (Underdamped): Notice the "wrinkles" (oscillations). The professor
     noted that mechanical sensors like pressure diaphragms and cantilevers
     naturally behave this way when disturbed.
   - GREEN (Critically Damped): The ideal state for a sensor that needs to
     track a changing DC signal quickly without "ringing".

2. THE RESONANCE PEAK (Bottom Plot):
   - Look at the massive RED spike exactly at wn = 10 rad/s!
   - The Y-axis is the "Linear Magnitude" (Output Amplitude / Input Amplitude).
   - A value of 1.0 means Output = Input.
   - The red line spikes to roughly 2.5. This means if you push this system
     with a sine wave of amplitude 1 at 10 rad/s, the system will physically
     oscillate with an amplitude of 2.5!
   - If we lowered zeta to 0.01 (almost zero friction), that peak would shoot
     up to 50x or 100x amplification. This is the exact physics exploited by
     the "Dynamic Mode" cantilevers and the Suspended Microchannel Resonator
     (SMR) discussed in your lecture!
=============================================================================
'''
