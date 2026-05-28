'''
=============================================================================
 AC CIRCUITS AND IMPEDANCE: FROM DC RESISTANCE TO AC FREQUENCY DEPENDENCE
=============================================================================
1. THE SHIFT FROM DC TO AC
   In DC circuits, voltage and current are constant, and components simply
   resist the flow of electrons (Ohm's Law: V = I * R).
   In AC (Alternating Current) circuits, voltage and current oscillate as
   sine waves. Because the signals are constantly changing, components that
   store energy (Capacitors and Inductors) react to the *rate of change*
   (the derivative), creating a time delay known as a PHASE SHIFT.

2. IMPEDANCE (Z): The AC Equivalent of Resistance
   Impedance is the total opposition to current flow for time-varying signals.
   It is a complex number that captures both MAGNITUDE (amplitude attenuation)
   and PHASE (time delay).

   - Resistor (R): Z_R = R
     (Opposition is constant. Voltage and Current are perfectly IN PHASE).

   - Capacitor (C): Z_C = 1 / (j * omega * C)
     (Opposition DECREASES as frequency increases. Capacitors block DC but
     pass high-frequency AC. Current LEADS Voltage by 90 degrees).

   - Inductor (L): Z_L = j * omega * L
     (Opposition INCREASES as frequency increases. Inductors pass DC but
     block high-frequency AC. Current LAGS Voltage by 90 degrees).

   *Note: j is the imaginary unit, and omega = 2 * pi * f.

3. THE BRIDGE TO FILTERS (The Voltage Divider)
   Because Impedance depends on frequency (omega), we can replace the static
   resistors in a DC voltage divider with Capacitors and Inductors.
   V_out = V_in * [ Z_2 / (Z_1 + Z_2) ]
   Since Z_1 and Z_2 change depending on the frequency of the input signal,
   the ratio V_out / V_in becomes frequency-dependent. This is the exact
   mathematical foundation of ALL passive electronic filters!
=============================================================================
'''

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sbn

sbn.set_theme(style="whitegrid")

#--------------------------------------------------------------------------------#
# PLOT 1: TIME DOMAIN - VOLTAGE AND CURRENT PHASE RELATIONSHIPS
#--------------------------------------------------------------------------------#
# We use a normalized angular frequency (omega = 1) to clearly visualize the
# phase shifts (time delays) between Voltage and Current.

t = np.linspace(0, 2*np.pi, 1000)
omega = 1.0

# Assume a standard sinusoidal Voltage input
V_t = np.sin(omega * t)

# Resistor: V and I are perfectly in phase (Z = R)
I_R = np.sin(omega * t)

# Capacitor: I = C * dV/dt. The derivative of sin is cos.
# Therefore, Current LEADS Voltage by 90 degrees (pi/2).
I_C = np.sin(omega * t + np.pi/2)

# Inductor: V = L * dI/dt. The integral of sin is -cos.
# Therefore, Current LAGS Voltage by 90 degrees (-pi/2).
I_L = np.sin(omega * t - np.pi/2)

fig, axes = plt.subplots(3, 1, figsize=(10, 12), sharex=True)

# Resistor Plot
axes[0].plot(t, V_t, label=r'Voltage $V(t)$', color='blue', linewidth=2.5)
axes[0].plot(t, I_R, label=r'Current $I_R(t)$', color='red', linestyle='--', linewidth=2.5)
axes[0].set_title(r"Resistor: Voltage and Current are IN PHASE ($Z_R = R$)", fontsize=14)
axes[0].set_ylabel("Amplitude")
axes[0].legend(loc='upper right', fontsize=11)
axes[0].axhline(0, color='black', linewidth=1)

# Capacitor Plot
axes[1].plot(t, V_t, label=r'Voltage $V(t)$', color='blue', linewidth=2.5)
axes[1].plot(t, I_C, label=r'Current $I_C(t)$', color='red', linestyle='--', linewidth=2.5)
axes[1].set_title(r"Capacitor: Current LEADS Voltage by $90^\circ$ ($Z_C = \frac{1}{j\omega C}$)", fontsize=14)
axes[1].set_ylabel("Amplitude")
axes[1].legend(loc='upper right', fontsize=11)
axes[1].axhline(0, color='black', linewidth=1)
# Annotation for phase lead
axes[1].annotate(r'$90^\circ$ Lead', xy=(np.pi/2, 1), xytext=(np.pi/2 + 0.5, 1.2),
                 arrowprops=dict(arrowstyle='->', color='green', lw=2), color='green', fontweight='bold')

# Inductor Plot
axes[2].plot(t, V_t, label=r'Voltage $V(t)$', color='blue', linewidth=2.5)
axes[2].plot(t, I_L, label=r'Current $I_L(t)$', color='red', linestyle='--', linewidth=2.5)
axes[2].set_title(r"Inductor: Current LAGS Voltage by $90^\circ$ ($Z_L = j\omega L$)", fontsize=14)
axes[2].set_xlabel(r"Time ($\omega t$)")
axes[2].set_ylabel("Amplitude")
axes[2].legend(loc='upper right', fontsize=11)
axes[2].axhline(0, color='black', linewidth=1)
# Annotation for phase lag
axes[2].annotate(r'$90^\circ$ Lag', xy=(3*np.pi/2, -1), xytext=(3*np.pi/2 - 0.5, -1.2),
                 arrowprops=dict(arrowstyle='->', color='purple', lw=2), color='purple', fontweight='bold')

plt.tight_layout()
plt.show()


#--------------------------------------------------------------------------------#
# PLOT 2: FREQUENCY DOMAIN - IMPEDANCE MAGNITUDE VS FREQUENCY
#--------------------------------------------------------------------------------#
# Now we look at how the MAGNITUDE of Impedance (|Z|) changes as we sweep
# the frequency of the AC signal from 1 Hz to 10 kHz.

f = np.logspace(0, 4, 1000) # 1 Hz to 10,000 Hz (Logarithmic scale)
omega_f = 2 * np.pi * f

# Component Values
R = 1000        # 1 kOhm
C = 1e-6        # 1 microFarad
L = 10e-3       # 10 milliHenry

# Calculate Magnitude of Impedance (|Z|)
Z_R = np.full_like(f, R)          # Constant
Z_C = 1 / (omega_f * C)           # Inversely proportional to frequency
Z_L = omega_f * L                 # Directly proportional to frequency

plt.figure(figsize=(10, 6))
# We use loglog (logarithmic x and y axes) because impedance spans multiple orders of magnitude
plt.loglog(f, Z_R, label=r'Resistor $|Z_R| = R$', color='orange', linewidth=3)
plt.loglog(f, Z_C, label=r'Capacitor $|Z_C| = \frac{1}{\omega C}$', color='blue', linewidth=3)
plt.loglog(f, Z_L, label=r'Inductor $|Z_L| = \omega L$', color='red', linewidth=3)

plt.title("Impedance Magnitude vs. Frequency (The Origin of Filters)", fontsize=16)
plt.xlabel("Frequency (Hz) [Log Scale]", fontsize=12)
plt.ylabel(r"Impedance Magnitude $|Z|$ ($\Omega$) [Log Scale]", fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, which="both", ls="--", alpha=0.5)

# Conceptual Annotations
plt.text(10, 2e5, "Capacitors block LOW frequencies\n(Act as open circuits at DC)",
         color='blue', fontsize=11, fontweight='bold')
plt.text(2e3, 20, "Inductors block HIGH frequencies\n(Act as open circuits at high AC)",
         color='red', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.show()
