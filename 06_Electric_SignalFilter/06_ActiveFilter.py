'''
=============================================================================
 ACTIVE FILTERS & THE SALLEN-KEY TOPOLOGY
=============================================================================
1. THE LIMITATION OF PASSIVE FILTERS
   Passive filters (using only Resistors, Capacitors, and Inductors) have
   two major flaws in modern bio-instrumentation:
   - Flaw 1 (No Amplification): They can only ATTENUATE signals. The maximum
     gain in the passband is always 0 dB (or less). They cannot boost weak
     biological signals.
   - Flaw 2 (Bulky Inductors): To get a sharp 2nd-order (-40 dB/decade) or
     higher roll-off, passive math requires Inductors (L). Inductors are
     essentially coils of wire; they are heavy, physically massive, and
     impossible to miniaturize onto a silicon microchip.

2. THE ACTIVE FILTER SOLUTION
   By introducing Operational Amplifiers (Op-Amps), we can build "Active"
   filters using ONLY tiny Resistors and Capacitors.
   - Advantage 1: Op-Amps have external power supplies, allowing them to
     AMPLIFY the passband (Gain > 0 dB) while simultaneously filtering.
   - Advantage 2: We can achieve sharp, higher-order roll-offs without
     needing a single bulky inductor.

3. THE SALLEN-KEY TOPOLOGY
   The Sallen-Key is the most famous 2nd-order active filter design.
   By using one Op-Amp, two resistors, and two capacitors, it creates a
   2nd-order Low-Pass filter with a sharp -40 dB/decade roll-off.
   (The professor explicitly noted this topology is used on the SMR board).

4. REAL-WORLD APPLICATION: THE SMR PHOTODETECTOR BOARD
   The raw signal from the SMR laser photodiode contains:
   - The Target: ~1 MHz cantilever vibration.
   - Noise 1: 60 Hz power-line interference.
   - Noise 2: ~5 MHz high-frequency electronic noise.
   To isolate the 1 MHz signal, the board cascades a 1st-order High-Pass
   filter (to kill the 60 Hz noise) with a 2nd-order Sallen-Key Low-Pass
   filter (to kill the 5 MHz noise). Together, they form an Active
   BAND-PASS filter that amplifies the target and rejects the noise!
=============================================================================
'''

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sbn
from scipy import signal

sbn.set_theme(style="whitegrid")

#--------------------------------------------------------------------------------#
# 1. DEFINE THE FREQUENCY SWEEP
#--------------------------------------------------------------------------------#
# Sweep from 10 Hz to 100 MHz (Logarithmic scale)
f = np.logspace(1, 8, 5000)
w = 2 * np.pi * f

#--------------------------------------------------------------------------------#
# 2. PLOT 1: PASSIVE VS. ACTIVE LOW-PASS FILTERS
#--------------------------------------------------------------------------------#
fc_lp = 2e6  # Cutoff frequency = 2 MHz
wc_lp = 2 * np.pi * fc_lp

# Passive 1st-Order RC Low-Pass Filter
# H(s) = wc / (s + wc)
sys_passive_lpf = signal.TransferFunction([wc_lp], [1, wc_lp])

# Active 2nd-Order Sallen-Key Low-Pass Filter (Butterworth, Gain = 2 [+6dB])
# H(s) = K * wc^2 / (s^2 + s*(wc/Q) + wc^2)
K = 2.0       # Amplification factor (Active filters can boost the signal!)
Q = 0.707     # Quality factor for a flat Butterworth response
sys_active_lpf = signal.TransferFunction([K * wc_lp**2], [1, wc_lp/Q, wc_lp**2])

# Calculate Bode Magnitudes
_, mag_passive_dB, _ = signal.bode(sys_passive_lpf, w=w)
_, mag_active_dB, _ = signal.bode(sys_active_lpf, w=w)

fig1, ax1 = plt.subplots(figsize=(10, 6))
ax1.semilogx(f, mag_passive_dB, color='blue', linewidth=3, label='1st-Order Passive RC Filter')
ax1.semilogx(f, mag_active_dB, color='red', linewidth=3, label='2nd-Order Active Sallen-Key Filter')

# Annotations for Roll-off slopes
ax1.annotate(r'Passive: -20 dB/decade', xy=(1e7, -20), xytext=(5e7, -10),
             arrowprops=dict(arrowstyle='->', color='blue', lw=2), color='blue', fontweight='bold', fontsize=12)
ax1.annotate(r'Active: -40 dB/decade (Sharper!)', xy=(1e7, -40), xytext=(5e7, -50),
             arrowprops=dict(arrowstyle='->', color='red', lw=2), color='red', fontweight='bold', fontsize=12)

# Annotation for Amplification
ax1.axhline(0, color='black', linestyle=':', alpha=0.5)
ax1.axhline(6.02, color='green', linestyle=':', alpha=0.5)
ax1.text(20, 6.5, r'Active Passband Amplified (+6 dB)', color='green', fontweight='bold', fontsize=12)
ax1.text(20, 0.5, r'Passive Max Gain = 0 dB (No Amplification)', color='blue', fontweight='bold', fontsize=12)

ax1.set_title("Why Active Filters? Amplification & Sharp Roll-off (No Inductors Needed)", fontsize=16)
ax1.set_xlabel("Frequency (Hz) [Log Scale]", fontsize=12)
ax1.set_ylabel("Magnitude (dB)", fontsize=12)
ax1.legend(fontsize=12, loc='lower left')
ax1.set_ylim(-80, 15)
plt.tight_layout()
plt.show()


#--------------------------------------------------------------------------------#
# 3. PLOT 2: THE SMR PHOTODETECTOR BOARD (CASCADING TO CREATE A BAND-PASS)
#--------------------------------------------------------------------------------#

# 1st-Order High-Pass Filter (To block 60 Hz power-line noise)
fc_hp = 100e3  # Cutoff = 100 kHz
wc_hp = 2 * np.pi * fc_hp
# H(s) = s / (s + wc)
sys_hpf = signal.TransferFunction([1, 0], [1, wc_hp])

# 2nd-Order Active Low-Pass Filter (To block 5 MHz electronic noise)
# (Using the same Sallen-Key defined above, fc = 2 MHz)

# CASCADE: Multiply the Transfer Functions (Convolve the polynomials)
num_smr = np.convolve(sys_hpf.num, sys_active_lpf.num)
den_smr = np.convolve(sys_hpf.den, sys_active_lpf.den)
sys_smr_bandpass = signal.TransferFunction(num_smr, den_smr)

# Calculate Bode Magnitudes
_, mag_hpf_dB, _ = signal.bode(sys_hpf, w=w)
_, mag_lpf_dB, _ = signal.bode(sys_active_lpf, w=w)
_, mag_smr_dB, _ = signal.bode(sys_smr_bandpass, w=w)

fig2, ax2 = plt.subplots(figsize=(10, 6))
ax2.semilogx(f, mag_hpf_dB, color='orange', linestyle='--', linewidth=2, alpha=0.6, label='Stage 1: 1st-Order High-Pass')
ax2.semilogx(f, mag_lpf_dB, color='purple', linestyle='--', linewidth=2, alpha=0.6, label='Stage 2: 2nd-Order Sallen-Key Low-Pass')
ax2.semilogx(f, mag_smr_dB, color='black', linewidth=4, label='Combined: SMR Band-Pass Response')

# Mark the Target and Noise Frequencies
# 60 Hz Noise
ax2.axvline(60, color='red', linestyle=':', linewidth=2)
ax2.plot(60, np.interp(60, f, mag_smr_dB), 'rx', markersize=15, markeredgewidth=3)
ax2.text(80, -60, '60 Hz Noise\n(BLOCKED)', color='red', fontweight='bold', fontsize=12)

# 1 MHz Target Signal
ax2.axvline(1e6, color='green', linestyle=':', linewidth=2)
ax2.plot(1e6, np.interp(1e6, f, mag_smr_dB), 'g*', markersize=20)
ax2.text(1.2e6, 0, '1 MHz Cantilever\n(PASSED & AMPLIFIED!)', color='green', fontweight='bold', fontsize=12)

# 5 MHz Noise
ax2.axvline(5e6, color='red', linestyle=':', linewidth=2)
ax2.plot(5e6, np.interp(5e6, f, mag_smr_dB), 'rx', markersize=15, markeredgewidth=3)
ax2.text(6e6, -40, '5 MHz Noise\n(BLOCKED)', color='red', fontweight='bold', fontsize=12)

ax2.set_title("Real-World Application: The SMR Photodetector Board Pipeline", fontsize=16)
ax2.set_xlabel("Frequency (Hz) [Log Scale]", fontsize=12)
ax2.set_ylabel("Magnitude (dB)", fontsize=12)
ax2.legend(fontsize=11, loc='lower left')
ax2.set_ylim(-80, 15)
plt.tight_layout()
plt.show()

'''
=============================================================================
 WHAT TO LOOK FOR IN THE PLOTS:
=============================================================================
1. THE PASSIVE VS. ACTIVE PLOT (Top):
   - Notice the BLUE line (Passive). It peaks at 0 dB and slowly rolls off
     at -20 dB/decade. It cannot amplify, and the transition to the "stop
     band" is very gentle.
   - Notice the RED line (Active Sallen-Key). It peaks at +6 dB (meaning it
     is actively AMPLIFYING the biological signal using external power).
     Furthermore, because it is 2nd-order, it plummets at -40 dB/decade.
     It achieves this sharp cutoff using only tiny resistors and capacitors
     on a microchip—no bulky inductors required!

2. THE SMR BOARD PLOT (Bottom):
   - The black line is the final "Band-Pass" filter created by cascading
     the orange High-Pass and purple Low-Pass filters.
   - Look at the RED X's: The 60 Hz power-line noise is completely
     destroyed by the High-Pass filter. The 5 MHz electronic noise is
     completely destroyed by the Sallen-Key Low-Pass filter.
   - Look at the GREEN STAR: The 1 MHz mechanical cantilever vibration
     sits perfectly in the "passband". It passes through the filter and is
     amplified, allowing the FPGA board to easily track the femtogram-scale
     mass changes of single cells!
=============================================================================
'''
