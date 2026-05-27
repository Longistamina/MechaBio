'''
=============================================================================
 THE QUALITY FACTOR (Q-FACTOR) & DYNAMIC MODE SENSING
=============================================================================
1. WHAT IS THE Q-FACTOR?
   The Q-factor measures the "sharpness" of the resonance peak in an
   underdamped second-order system.
   - High Q: Very little friction/damping. The resonance peak is razor-sharp.
   - Low Q: High friction/damping. The resonance peak is broad and flat.

   Mathematically, it is directly tied to the damping ratio (zeta):
   Q = 1 / (2 * zeta)

2. THE TWO WAYS TO MEASURE Q (Experimental Determination)
   A. Frequency Sweep (Bandwidth Method):
      You drive the system with sine waves of varying frequencies. The Q-factor
      is the center resonant frequency divided by the "Full Width at Half Maximum"
      (FWHM), also known as the -3dB bandwidth.
      Q = f_center / Delta_f

   B. Step Response (Ring-Down Method):
      You hit the system with a single impulse (step) and watch it "ring" like
      a bell. The Q-factor is determined by how slowly the oscillation decays.
      The decay envelope follows: exp(-zeta * wn * t).
      Q = (wn * tau_decay) / 2

3. WHY DO WE CARE? (Dynamic Mode Sensing)
   In "Static Mode", you measure physical bending (deflection).
   In "Dynamic Mode", you vibrate the cantilever exactly at its resonant peak.
   Because a High Q peak is so sharp, if a tiny biological mass (like a single
   cell) binds to the cantilever, the resonant frequency shifts slightly. This
   tiny shift causes a MASSIVE drop in amplitude, making the sensor incredibly
   sensitive (down to the femtogram scale!).

4. THE WATER PROBLEM & THE SMR SOLUTION
   If you submerge a cantilever in water to measure biological cells, the fluid
   friction (damping) kills the Q-factor (reducing it by ~65x).
   The Suspended Microchannel Resonator (SMR) solves this by making the
   cantilever hollow. The fluid flows INSIDE the channel, while the outside
   of the cantilever vibrates in a VACUUM, preserving a massive Q-factor (~1000).
=============================================================================
'''

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sbn
from scipy import signal

sbn.set_theme(style="darkgrid")

#--------------------------------------------------------------------------------#
# 1. DEFINE THE SYSTEM
#--------------------------------------------------------------------------------#
wn = 100.0       # Natural frequency (rad/s)
zeta = 0.05      # Damping ratio (Underdamped, very low friction)
Q_theoretical = 1 / (2 * zeta) # True Q = 10

# Transfer Function: H(s) = wn^2 / (s^2 + 2*zeta*wn*s + wn^2)
sys = signal.TransferFunction([wn**2], [1, 2*zeta*wn, wn**2])

#--------------------------------------------------------------------------------#
# 2. METHOD A: FREQUENCY SWEEP (BANDWIDTH METHOD)
#--------------------------------------------------------------------------------#
# High resolution frequency sweep to accurately find the peak and bandwidth
w = np.logspace(0.5, 2.5, 10000)
w, mag_dB, phase = signal.bode(sys, w=w)

# Find the resonant peak
peak_idx = np.argmax(mag_dB)
peak_dB = mag_dB[peak_idx]
w_peak = w[peak_idx]

# Find the -3dB points (Half-Power Bandwidth)
threshold_dB = peak_dB - 3.01

# Find left and right crossings
left_idx = np.where(mag_dB[:peak_idx] >= threshold_dB)[0][-1]
right_idx = np.where(mag_dB[peak_idx:] <= threshold_dB)[0][0] + peak_idx

w_left = w[left_idx]
w_right = w[right_idx]
delta_w = w_right - w_left

# Calculate Q from Bandwidth
Q_bandwidth = w_peak / delta_w

#--------------------------------------------------------------------------------#
# 3. METHOD B: STEP RESPONSE (RING-DOWN METHOD)
#--------------------------------------------------------------------------------#
t = np.linspace(0, 3, 2000)
t_step, y_step = signal.step(sys, T=t)

# The oscillation decays according to an exponential envelope
# Envelope = 1 +/- (1/sqrt(1-zeta^2)) * exp(-zeta * wn * t)
decay_rate = zeta * wn
tau_decay = 1 / decay_rate  # Time constant of the envelope

# Calculate Q from Ring-Down
Q_ringdown = (wn * tau_decay) / 2

# Theoretical Envelope Curves
amp_factor = 1 / np.sqrt(1 - zeta**2)
env_upper = 1 + amp_factor * np.exp(-decay_rate * t_step)
env_lower = 1 - amp_factor * np.exp(-decay_rate * t_step)

#--------------------------------------------------------------------------------#
# 4. PLOTTING THE RESULTS
#--------------------------------------------------------------------------------#
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12))

# ================= TOP PLOT: FREQUENCY SWEEP =================
ax1.semilogx(w, mag_dB, color='blue', linewidth=3, label='Magnitude Response')
ax1.axvline(w_peak, color='red', linestyle='--', label=rf'Resonant Peak ($\omega_n \approx {w_peak:.1f}$ rad/s)')
ax1.axhline(threshold_dB, color='green', linestyle=':', label='-3dB (Half-Power) Threshold')
ax1.axvline(w_left, color='green', linestyle='--', alpha=0.6)
ax1.axvline(w_right, color='green', linestyle='--', alpha=0.6)

# Highlight the Bandwidth (Delta W)
ax1.annotate('', xy=(w_left, threshold_dB - 2), xytext=(w_right, threshold_dB - 2),
             arrowprops=dict(arrowstyle='<->', color='green', lw=2))
ax1.text(np.sqrt(w_left*w_right), threshold_dB - 4, r'$\Delta \omega$ (Bandwidth)',
         ha='center', color='green', fontsize=12, fontweight='bold')

ax1.set_title(f"Method A: Frequency Sweep (Q = {Q_bandwidth:.2f})", fontsize=16)
ax1.set_ylabel("Magnitude (dB)", fontsize=12)
ax1.legend(loc='lower left', fontsize=11)
ax1.set_ylim(-20, peak_dB + 5)

# ================= BOTTOM PLOT: STEP RESPONSE =================
ax2.plot(t_step, y_step, color='blue', linewidth=2, label='Step Response (Ring-Down)')
ax2.plot(t_step, env_upper, color='red', linestyle='--', linewidth=2, label=r'Decay Envelope ($e^{-\zeta \omega_n t}$)')
ax2.plot(t_step, env_lower, color='red', linestyle='--', linewidth=2)
ax2.axhline(1, color='black', linestyle=':', alpha=0.5, label='Steady State')

# Highlight the Time Constant (tau)
ax2.axvline(tau_decay, color='purple', linestyle='-.', linewidth=2, label=f'Time Constant ($\\tau = {tau_decay:.3f}$ s)')
ax2.scatter([tau_decay], [1 + amp_factor * np.exp(-1)], color='purple', s=100, zorder=5)
ax2.text(tau_decay + 0.05, 1.5, r'Amplitude drops to $1/e$ (37%)', color='purple', fontsize=12)

ax2.set_title(f"Method B: Step Response Ring-Down (Q = {Q_ringdown:.2f})", fontsize=16)
ax2.set_xlabel("Time (s)", fontsize=12)
ax2.set_ylabel("Amplitude", fontsize=12)
ax2.legend(loc='upper right', fontsize=11)
ax2.set_ylim(0, 2.5)

plt.tight_layout()
plt.show()

print(f"Theoretical Q (1 / 2*zeta):      {Q_theoretical:.2f}")
print(f"Q from Frequency Bandwidth:      {Q_bandwidth:.2f}")
print(f"Q from Step Response Ring-Down:  {Q_ringdown:.2f}")

'''
=============================================================================
 WHAT TO LOOK FOR IN THE PLOTS:
=============================================================================
1. THE RAZOR-SHARP PEAK (Top Plot):
   Because zeta is only 0.05, the system has very little friction. The blue
   line shoots up to a massive +20 dB amplification! The green arrows show
   the "Full Width at Half Maximum" (Delta W). Because the peak is so narrow,
   Delta W is very small, resulting in a High Q (Q = 10).

2. THE RING-DOWN ENVELOPE (Bottom Plot):
   When you hit a high-Q system with a step input, it doesn't just settle; it
   "rings" like a struck tuning fork. The red dashed lines show the exponential
   decay envelope. The purple line marks the "Time Constant" (tau). A high Q
   system takes a long time to die out (large tau), which mathematically
   translates to a high Q-factor.

3. THE BIOSENSOR CONNECTION:
   Imagine the blue line in the top plot is your cantilever vibrating in a
   vacuum. If a single cancer cell binds to it, the mass increases, and the
   entire blue curve shifts slightly to the LEFT (lower frequency). Because
   the peak is so steep and sharp (High Q), that tiny shift causes the amplitude
   at your driving frequency to plummet drastically. You easily detect the cell!
   If you did this in water (Low Q), the peak would be a broad, flat hill, and
   that same tiny shift would be completely invisible.
=============================================================================
'''
