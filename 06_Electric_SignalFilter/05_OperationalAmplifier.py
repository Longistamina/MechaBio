'''
=============================================================================
 OPERATIONAL AMPLIFIERS (OP-AMPS) & THE "GOLDEN RULES"
=============================================================================
1. WHAT IS AN OP-AMP?
   An Op-Amp is a high-gain electronic voltage amplifier with a differential
   input (V+ and V-) and a single-ended output (V_out).
   In open-loop (no feedback), V_out = A * (V+ - V-), where A is massive
   (e.g., 100,000+). This makes it useless on its own because it instantly
   saturates to the power supply rails.

2. THE FOUR "GOLDEN RULES" OF IDEAL OP-AMPS
   To make Op-Amps useful, we use NEGATIVE FEEDBACK (routing the output back
   to the V- input). This triggers four "Golden Rules" that make circuit
   analysis incredibly simple:

   Rule 1: Infinite Open-Loop Gain (A -> infinity).
   Rule 2: Infinite Input Impedance.
           No current flows INTO the input pins (I+ = I- = 0).
           They act as perfect, ideal voltmeters.
   Rule 3: Zero Output Impedance.
           The output acts as a perfect voltage source that can supply
           infinite current without dropping voltage.
   Rule 4: The "Virtual Short" (The Magic Trick).
           Because of the infinite gain and negative feedback, the Op-Amp
           will instantly adjust its V_out to force the voltage difference
           between the inputs to be EXACTLY ZERO.
           Therefore: V+ = V-.

3. THE INVERTING AMPLIFIER
   If we connect V+ to Ground (0V), Rule 4 forces V- to also be 0V.
   This is called a "Virtual Ground".
   Using Kirchhoff's Current Law (KCL) at the V- node:
   I_in + I_f = 0  (because Rule 2 says no current enters the Op-Amp).
   (V_in - 0)/R_in + (V_out - 0)/R_f = 0
   Solving for V_out yields: V_out = - (R_f / R_in) * V_in
   We have created a precise, predictable amplifier using only two resistors!

4. ANALOG COMPUTING: THE INTEGRATOR
   What if we replace the feedback resistor (R_f) with a Capacitor (C)?
   The impedance of the capacitor is Z_C = 1 / (j * omega * C).
   In the time domain, the current through a capacitor is I = C * (dV/dt).
   Applying KCL at the virtual ground:
   (V_in / R) + C * (dV_out / dt) = 0
   Rearranging and integrating:
   V_out(t) = - (1 / RC) * integral[ V_in(t) dt ]
   By simply swapping a component, the Op-Amp now performs CALCULUS in
   real-time! This is the foundation of analog computers and active filters.
=============================================================================
'''

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sbn

sbn.set_theme(style="whitegrid")

#--------------------------------------------------------------------------------#
# PLOT 1: THE INVERTING AMPLIFIER & THE "VIRTUAL GROUND"
#--------------------------------------------------------------------------------#
# Let's simulate an AC signal passing through an Inverting Amplifier.
# R_in = 1 kOhm, R_f = 3 kOhm. Expected Gain = -3.

t = np.linspace(0, 2*np.pi, 1000)
V_in = np.sin(t) * 2.0  # 2V amplitude sine wave

R_in = 1000
R_f = 3000
Gain = - (R_f / R_in)

V_out = Gain * V_in

# Because V+ is tied to ground (0V), Rule 4 forces V- to be 0V (Virtual Ground)
V_minus = np.zeros_like(t)

fig1, ax1 = plt.subplots(figsize=(10, 6))
ax1.plot(t, V_in, color='blue', linewidth=3, label=r'Input Voltage ($V_{in}$)')
ax1.plot(t, V_out, color='red', linewidth=3, linestyle='--', label=r'Output Voltage ($V_{out}$)')
ax1.plot(t, V_minus, color='green', linewidth=4, label=r'Inverting Input ($V_-$) = Virtual Ground')

ax1.set_title(r"Inverting Amplifier: $V_{out} = -\frac{R_f}{R_{in}} V_{in}$", fontsize=16)
ax1.set_xlabel("Time", fontsize=12)
ax1.set_ylabel("Voltage (V)", fontsize=12)
ax1.axhline(0, color='black', linewidth=1)
ax1.legend(fontsize=12, loc='upper right')

# Annotation explaining the Virtual Ground
ax1.annotate(r'Golden Rule #4 forces $V_- = V_+ = 0V$' + '\n(No current enters Op-Amp, Rule #2)',
             xy=(np.pi, 0), xytext=(np.pi + 0.5, 3),
             arrowprops=dict(arrowstyle='->', color='green', lw=2),
             color='green', fontweight='bold', fontsize=12,
             bbox=dict(boxstyle="round,pad=0.3", edgecolor="green", facecolor="lightgreen", alpha=0.5))

plt.tight_layout()
plt.show()


#--------------------------------------------------------------------------------#
# PLOT 2: ANALOG COMPUTING - THE OP-AMP INTEGRATOR
#--------------------------------------------------------------------------------#
# Let's feed a Square Wave into an Op-Amp Integrator.
# The mathematical integral of a constant (flat top of square wave) is a linear ramp.
# Therefore, a Square Wave input should result in a Triangle Wave output!

# Generate a Square Wave

freq = 1.0
V_in_sq = np.sign(np.sin(2 * np.pi * freq * t)) * 2.0

# Simulate the RC Integrator using numerical integration (Euler method)
R_int = 1000  # 1 kOhm
C_int = 1e-3  # 1 mF
RC = R_int * C_int
dt = t[1] - t[0]

V_out_int = np.zeros_like(t)
for i in range(1, len(t)):
    # V_out(t) = V_out(t-dt) - (dt / RC) * V_in(t)
    V_out_int[i] = V_out_int[i-1] - (dt / RC) * V_in_sq[i]

fig2, (ax2_top, ax2_bot) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

# Top Plot: Input
ax2_top.plot(t, V_in_sq, color='blue', linewidth=3)
ax2_top.set_title(r"Op-Amp Integrator Input: Square Wave ($V_{in}$)", fontsize=14)
ax2_top.set_ylabel("Voltage (V)", fontsize=12)
ax2_top.set_ylim(-3, 3)
ax2_top.axhline(0, color='black', linewidth=1)

# Bottom Plot: Output
ax2_bot.plot(t, V_out_int, color='purple', linewidth=3)
ax2_bot.set_title(r"Op-Amp Integrator Output: Triangle Wave ($V_{out} = -\frac{1}{RC} \int V_{in} dt$)", fontsize=14)
ax2_bot.set_xlabel("Time", fontsize=12)
ax2_bot.set_ylabel("Voltage (V)", fontsize=12)
ax2_bot.axhline(0, color='black', linewidth=1)

# Annotation explaining the Calculus
ax2_bot.annotate(r'Integral of a constant' + '\nis a linear ramp!',
                 xy=(np.pi/2, V_out_int[np.argmin(np.abs(t - np.pi/2))]),
                 xytext=(np.pi/2 + 0.5, 0.05),
                 arrowprops=dict(arrowstyle='->', color='darkorange', lw=2),
                 color='darkorange', fontweight='bold', fontsize=12)

plt.tight_layout()
plt.show()

'''
=============================================================================
 WHAT TO LOOK FOR IN THE PLOTS:
=============================================================================
1. THE INVERTING AMPLIFIER (Top Plot):
   - Notice the green line flatlining at exactly 0V. This is the "Virtual
     Ground". Even though it is not physically connected to the ground, the
     Op-Amp's negative feedback actively drives the V- pin to match the V+
     pin (which is grounded).
   - The red dashed output wave is exactly 3 times larger than the blue
     input wave, and it is flipped upside down (inverted), perfectly matching
     the -Rf/Rin ratio.

2. THE INTEGRATOR (Bottom Plots):
   - The professor explicitly stated that Op-Amps can perform "mathematical
     integration or differentiation". Look at the bottom plot!
   - When the blue square wave is HIGH (a positive constant), the purple
     output line ramps DOWN linearly.
   - When the blue square wave is LOW (a negative constant), the purple
     output line ramps UP linearly.
   - The Op-Amp has literally solved the calculus integral in real-time
     using nothing but a resistor, a capacitor, and the Golden Rules. This
     exact circuit topology is the building block of the Active Filters
     (like the Sallen-Key) used on the SMR photodetector board!
=============================================================================
'''
