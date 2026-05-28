'''
=============================================================================
 PASSIVE FILTERS: SHAPING FREQUENCY RESPONSE WITH VOLTAGE DIVIDERS
=============================================================================
1. THE CORE CONCEPT: THE AC VOLTAGE DIVIDER
   In DC circuits, a voltage divider splits voltage based on the ratio of
   two static resistors: V_out = V_in * [R2 / (R1 + R2)].
   In AC circuits, we replace resistors with complex Impedances (Z).
   Because the impedance of Capacitors (Z_C = 1/jwC) and Inductors (Z_L = jwL)
   changes with frequency, the voltage divider becomes FREQUENCY-DEPENDENT.

   V_out(jw) = V_in(jw) * [Z2 / (Z1 + Z2)]

   This simple substitution is the mathematical foundation of ALL passive filters!

2. THE TRANSFER FUNCTION & BODE PLOTS
   The Transfer Function H(jw) = V_out / V_in describes the system's behavior.
   We visualize H(jw) using Bode Plots, which consist of two graphs:
   - Magnitude Plot: Gain in Decibels (dB) = 20 * log10(|H(jw)|).
   - Phase Plot: Phase shift in degrees = angle(H(jw)).

3. THE CUTOFF FREQUENCY & THE "-3 dB" RULE
   For a 1st-order RC filter, the cutoff frequency (fc) is where the output
   power drops by exactly half. Because Power is proportional to Voltage squared,
   a half-power drop corresponds to an amplitude drop of 1/sqrt(2) (~0.707).
   In Decibels: 20 * log10(0.707) = -3.01 dB.
   Therefore, the cutoff frequency is universally known as the "-3 dB point".
   fc = 1 / (2 * pi * R * C)

4. THE ROLL-OFF RATE & MECHANICAL ANALOGY
   Beyond the cutoff, a 1st-order filter attenuates the signal at a rate
   of -20 dB per decade (meaning every time frequency increases by 10x,
   the signal amplitude drops by 10x).
   The professor emphasized that a 1st-order RC Low-Pass filter is
   MATHEMATICALLY IDENTICAL to a 1st-order mechanical system (like a
   sluggish thermometer). Both exhibit the exact same -20 dB/decade
   roll-off and 90-degree phase lag at high frequencies!
=============================================================================
'''

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sbn

sbn.set_theme(style="whitegrid")

#--------------------------------------------------------------------------------#
# 1. DEFINE COMPONENTS AND FREQUENCY SWEEP
#--------------------------------------------------------------------------------#
R = 1e3       # 1 kOhm resistor
C = 1e-6      # 1 uF capacitor

# Cutoff frequency (fc) and angular cutoff frequency (wc)
fc = 1 / (2 * np.pi * R * C)  # ~159.15 Hz

# Logarithmic frequency sweep from 1 Hz to 100 kHz
f = np.logspace(0, 5, 1000)
w = 2 * np.pi * f

#--------------------------------------------------------------------------------#
# 2. CALCULATE IMPEDANCES AND TRANSFER FUNCTIONS
#--------------------------------------------------------------------------------#
Z_R = R
Z_C = 1 / (1j * w * C)

# LOW-PASS FILTER (Output taken across the Capacitor)
# At high frequencies, Z_C approaches 0, so V_out approaches 0.
H_LPF = Z_C / (Z_R + Z_C)

# HIGH-PASS FILTER (Output taken across the Resistor)
# At low frequencies, Z_C approaches infinity, so V_out approaches 0.
H_HPF = Z_R / (Z_R + Z_C)

# Calculate Magnitude (in Decibels) and Phase (in Degrees)
mag_LPF_dB = 20 * np.log10(np.abs(H_LPF))
phase_LPF_deg = np.degrees(np.angle(H_LPF))

mag_HPF_dB = 20 * np.log10(np.abs(H_HPF))
phase_HPF_deg = np.degrees(np.angle(H_HPF))

#--------------------------------------------------------------------------------#
# 3. PLOTTING THE BODE PLOTS
#--------------------------------------------------------------------------------#
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# ================= LEFT COLUMN: LOW-PASS FILTER =================
# Magnitude
axes[0, 0].semilogx(f, mag_LPF_dB, color='blue', linewidth=3)
axes[0, 0].axvline(fc, color='red', linestyle='--', label=rf'Cutoff $f_c \approx {fc:.1f}$ Hz')
axes[0, 0].axhline(-3, color='green', linestyle=':', label='-3 dB (Half-Power Point)')
axes[0, 0].set_title(r"1st Order RC Low-Pass Filter (Magnitude)", fontsize=14)
axes[0, 0].set_ylabel("Magnitude (dB)")
axes[0, 0].legend(fontsize=10)
axes[0, 0].set_ylim(-60, 5)

# Annotation for Roll-off slope
axes[0, 0].annotate(r'-20 dB/decade Roll-off', xy=(fc*10, -20), xytext=(fc*5, -10),
                    arrowprops=dict(arrowstyle='->', color='purple', lw=2),
                    color='purple', fontweight='bold', fontsize=12)

# Phase
axes[1, 0].semilogx(f, phase_LPF_deg, color='blue', linewidth=3)
axes[1, 0].axvline(fc, color='red', linestyle='--')
axes[1, 0].axhline(-45, color='green', linestyle=':', label=r'-45$^\circ$ at $f_c$')
axes[1, 0].set_title(r"1st Order RC Low-Pass Filter (Phase)", fontsize=14)
axes[1, 0].set_xlabel("Frequency (Hz) [Log Scale]")
axes[1, 0].set_ylabel("Phase (Degrees)")
axes[1, 0].legend(fontsize=10)
axes[1, 0].set_ylim(-100, 10)

# ================= RIGHT COLUMN: HIGH-PASS FILTER =================
# Magnitude
axes[0, 1].semilogx(f, mag_HPF_dB, color='orange', linewidth=3)
axes[0, 1].axvline(fc, color='red', linestyle='--', label=rf'Cutoff $f_c \approx {fc:.1f}$ Hz')
axes[0, 1].axhline(-3, color='green', linestyle=':', label='-3 dB (Half-Power Point)')
axes[0, 1].set_title(r"1st Order RC High-Pass Filter (Magnitude)", fontsize=14)
axes[0, 1].set_ylabel("Magnitude (dB)")
axes[0, 1].legend(fontsize=10)
axes[0, 1].set_ylim(-60, 5)

# Annotation for Roll-off slope
axes[0, 1].annotate(r'+20 dB/decade Roll-off', xy=(fc/10, -20), xytext=(fc/5, -10),
                    arrowprops=dict(arrowstyle='->', color='purple', lw=2),
                    color='purple', fontweight='bold', fontsize=12)

# Phase
axes[1, 1].semilogx(f, phase_HPF_deg, color='orange', linewidth=3)
axes[1, 1].axvline(fc, color='red', linestyle='--')
axes[1, 1].axhline(45, color='green', linestyle=':', label=r'+45$^\circ$ at $f_c$')
axes[1, 1].set_title(r"1st Order RC High-Pass Filter (Phase)", fontsize=14)
axes[1, 1].set_xlabel("Frequency (Hz) [Log Scale]")
axes[1, 1].set_ylabel("Phase (Degrees)")
axes[1, 1].legend(fontsize=10)
axes[1, 1].set_ylim(-10, 100)

plt.tight_layout()
plt.show()

'''
=============================================================================
 WHAT TO LOOK FOR IN THE PLOTS:
=============================================================================
1. THE MAGNITUDE PLOTS (Top Row):
   - Notice how the blue line (LPF) is perfectly flat at 0 dB for low
     frequencies, meaning the signal passes through at 100% amplitude.
     Once it crosses the red dashed line (fc), it plummets.
   - The green dotted line marks exactly -3 dB. Notice how the curve
     crosses the cutoff frequency exactly at this -3 dB mark.
   - The purple arrow highlights the "-20 dB/decade" slope. If you look
     at the x-axis (log scale), moving one "decade" to the right (e.g.,
     from 1 kHz to 10 kHz) results in the signal dropping by exactly 20 dB.

2. THE PHASE PLOTS (Bottom Row):
   - Filters don't just change amplitude; they DELAY the signal.
   - For the LPF, at very high frequencies, the output lags the input by
     a full 90 degrees. Exactly at the cutoff frequency (fc), the phase
     shift is exactly half of that: -45 degrees.
   - The HPF does the exact opposite: it LEADS the phase by +90 degrees
     at low frequencies, crossing +45 degrees at the cutoff.

3. THE LIMITATION OF PASSIVE FILTERS:
   - A -20 dB/decade roll-off is quite "gentle". If you want to block
     60 Hz power-line noise but keep a 70 Hz biological signal, a 1st-order
     passive filter won't cut it; the transition is too slow.
   - To get a sharper cutoff (e.g., -40 dB/decade), you need a 2nd-order
     filter. Doing this passively requires adding an INDUCTOR (L). But as
     the professor noted, inductors are bulky, heavy, and impossible to
     put on a microchip.
   - This exact limitation is what forces engineers to invent ACTIVE FILTERS
     using Operational Amplifiers (Op-Amps)!
=============================================================================
'''
