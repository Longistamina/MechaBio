'''
=============================================================================
 MODELING A SECOND-ORDER MEASUREMENT SYSTEM
=============================================================================
PHYSICAL ANALOGY: A mass on a spring with a shock absorber (damper).
Unlike a first-order system (which only has one type of "inertia"),
a second-order system has TWO storage elements that compete:
1. Potential Energy (the spring's elasticity pulling it back)
2. Kinetic Energy (the mass's momentum pushing it forward)
This competition allows the system to "overshoot" and oscillate.

THE DIFFERENTIAL EQUATION:
(d^2y/dt^2) + 2*zeta*wn*(dy/dt) + wn^2 * y = wn^2 * x(t)

wn   = Natural Frequency (how fast the system "wants" to oscillate naturally)
zeta = Damping Ratio (how much friction/resistance slows it down)

THE THREE DAMPING REGIMES (Step Response):
1. Underdamped (zeta < 1): Not enough friction. The system overshoots the
   target and oscillates (rings) before finally settling.
2. Critically Damped (zeta = 1): The "Goldilocks" zone. The fastest possible
   response to reach the target without any overshoot or oscillation.
3. Overdamped (zeta > 1): Too much friction. The system sluggishly creeps
   to the target, behaving somewhat like a slow first-order system.

THE LAPLACE TRANSFER FUNCTION:
H(s) = wn^2 / (s^2 + 2*zeta*wn*s + wn^2)

RESONANCE (The Danger Zone):
If you input a sine wave whose frequency matches the system's natural
frequency (wn), an UNDERDAMPED system will experience RESONANCE.
The output amplitude will be massively amplified (sometimes 100x or 1000x),
which can physically destroy sensors, bridges, or mechanical structures!
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
zeta_under = 0.2   # Underdamped (bouncy)
zeta_crit  = 1.0   # Critically damped (optimal)
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

# Time array (8 seconds to allow oscillations to play out)
t = np.linspace(0, 8, 2000)

#--------------------------------------------------------------------------------#
# 3. TEST 1: THE STEP RESPONSE (Sudden change in input)
#--------------------------------------------------------------------------------#
x_step = np.ones_like(t)  # Step input of amplitude 1

_, y_step_under, _ = signal.lsim(sys_under, x_step, t)
_, y_step_crit, _  = signal.lsim(sys_crit, x_step, t)
_, y_step_over, _  = signal.lsim(sys_over, x_step, t)

#--------------------------------------------------------------------------------#
# 4. TEST 2: RESONANCE (Sine wave at EXACTLY the natural frequency)
#--------------------------------------------------------------------------------#
# We feed the system a sine wave at exactly wn (10 rad/s).
x_sine = np.sin(wn * t)

_, y_sine_under, _ = signal.lsim(sys_under, x_sine, t)
_, y_sine_crit, _  = signal.lsim(sys_crit, x_sine, t)
_, y_sine_over, _  = signal.lsim(sys_over, x_sine, t)

#--------------------------------------------------------------------------------#
# 5. PLOT THE RESULTS
#--------------------------------------------------------------------------------#
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12), sharex=True)

# Top Plot: Step Response
ax1.plot(t, x_step, color='black', linestyle=':', linewidth=2, label='Step Input (Target)')
ax1.plot(t, y_step_under, color='red', linewidth=2.5, label=f'Underdamped (ζ={zeta_under}) - Oscillates!')
ax1.plot(t, y_step_crit, color='green', linewidth=2.5, label=f'Critically Damped (ζ={zeta_crit}) - Fastest, No Overshoot')
ax1.plot(t, y_step_over, color='blue', linewidth=2.5, label=f'Overdamped (ζ={zeta_over}) - Sluggish')
ax1.set_title("Second-Order Step Response: The Three Damping Regimes", fontsize=16)
ax1.set_ylabel("Amplitude")
ax1.legend(loc='right', fontsize=11)
ax1.set_ylim(-0.5, 2.0)

# Bottom Plot: Resonance (Sinusoidal Input)
ax2.plot(t, x_sine, color='black', alpha=0.5, linewidth=1.5, label='Input Sine Wave (Amplitude = 1)')
ax2.plot(t, y_sine_under, color='red', linewidth=3, label=f'Underdamped Output (RESONANCE AMPLIFIED!)')
ax2.plot(t, y_sine_crit, color='green', linewidth=2, label='Critically Damped Output')
ax2.plot(t, y_sine_over, color='blue', linewidth=2, label='Overdamped Output (Attenuated)')
ax2.set_title(f"Resonance: Input Frequency matches Natural Frequency (ω = {wn} rad/s)", fontsize=16)
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Amplitude")
ax2.legend(loc='upper left', fontsize=11)

plt.tight_layout()
plt.show()

'''
=============================================================================
 WHAT TO LOOK FOR IN THE PLOTS:
=============================================================================
1. THE STEP RESPONSE (Top Plot):
   - RED (Underdamped): It shoots past the target (overshoot), dips below,
     and "rings" back and forth before settling. (Like a bouncy car suspension).
   - GREEN (Critically Damped): It rises as fast as physically possible and
     smoothly locks onto the target without a single bounce. Engineers design
     most sensors to be exactly at this state!
   - BLUE (Overdamped): It acts like a slow First-Order system. It takes
     forever to crawl up to the target.

2. THE RESONANCE DISASTER (Bottom Plot):
   - Look at the RED line! The input sine wave (black) has an amplitude of 1.
     But because the system is Underdamped and the input frequency matches
     its natural "bouncy" frequency, the system absorbs the energy and the
     output amplitude grows MASSIVELY (up to 2.5x in just a few seconds,
     and it would keep growing to infinity in pure math).
   - This is the exact physics behind why soldiers break step when marching
     across a bridge, or why a singer can shatter a wine glass with their voice!
   - The BLUE line (Overdamped) has too much friction to resonate, so it
     safely blocks the high-frequency wave (acting as a low-pass filter).
=============================================================================
'''
