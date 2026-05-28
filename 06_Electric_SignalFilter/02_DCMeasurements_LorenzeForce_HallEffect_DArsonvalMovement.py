'''
=============================================================================
 DC MEASUREMENTS: LORENTZ FORCE, HALL EFFECT, & D'ARSONVAL MOVEMENT
=============================================================================
1. THE LORENTZ FORCE
   When a charged particle moves through an electromagnetic field, it
   experiences the Lorentz force:
   F = q(E + v x B)

   In a standard conductor with no external electric field (E=0), the force
   is purely magnetic: F = q(v x B).
   - q: charge of the particle
   - v: velocity vector of the particle
   - B: magnetic field vector
   - x: cross product (direction determined by the Right-Hand Rule)

2. THE HALL EFFECT (The Professor's "Trick" Question)
   Imagine a flat rectangular conductor.
   - Conventional Current (I) flows to the RIGHT (+x).
   - But physical charge carriers are ELECTRONS (negative charge, q = -e).
   - Therefore, electrons physically drift to the LEFT (-x).

   If we apply a Magnetic Field (B) pointing OUT OF THE PAGE (+z):
   - v is in -x direction.
   - B is in +z direction.
   - The cross product (v x B) points in the +y direction (UP).
   - BUT because the electron has a NEGATIVE charge, the force F = -e(v x B)
     flips direction and points DOWN (-y).

   Result: Electrons are pushed to the BOTTOM edge of the conductor.
   The bottom edge becomes negatively charged, and the top edge becomes
   positively charged. This charge separation creates a transverse electric
   field (Hall Field) and a measurable voltage across the width of the
   conductor, known as the HALL VOLTAGE (V_H).
   This effect physically proves that charge carriers in standard metals are negative!

3. D'ARSONVAL MOVEMENT (The Classic Analog DC Meter)
   How do we use the Lorentz force to measure DC current?
   We place a coil of wire (area A, N turns) inside a permanent magnetic field.
   - When current (I) flows through the coil, the Lorentz force pushes the
     wires up on one side and down on the other, creating a TORQUE.
   - Magnetic Torque: tau_mag = N * I * A * B
   - The coil is attached to a restoring spring: tau_spring = k * theta
   - At equilibrium: k * theta = N * I * A * B  =>  theta = (NAB/k) * I

   The deflection angle (theta) is STRICTLY LINEAR with the current (I).

4. EXTENDING THE RANGE (Shunt Resistors)
   The D'Arsonval coil is delicate and can only handle tiny currents (e.g., 1 mA).
   To measure larger currents (e.g., 10 Amps), we place a "Shunt Resistor"
   (R_sh) in PARALLEL with the meter.
   - The shunt has very low resistance, so it bypasses 99.9% of the current.
   - Only a known, safe fraction flows through the delicate coil.
   - By swapping shunt resistors (like turning the dial on a multimeter),
     you change the measurement range!
=============================================================================
'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sbn

sbn.set_theme(style="whitegrid")

#--------------------------------------------------------------------------------#
# PLOT 1: THE HALL EFFECT GEOMETRY
#--------------------------------------------------------------------------------#
fig1, ax1 = plt.subplots(figsize=(10, 6))

# Draw the Conductor
rect = patches.Rectangle((1, 2), 8, 3, linewidth=2, edgecolor='black', facecolor='lightgray')
ax1.add_patch(rect)

# Conventional Current (I)
ax1.annotate('', xy=(9.5, 4.2), xytext=(0.5, 4.2),
             arrowprops=dict(arrowstyle='->', color='red', lw=3))
ax1.text(5, 4.6, r'Conventional Current ($I$) $\rightarrow$', color='red', fontsize=14, ha='center', fontweight='bold')

# Electron Drift Velocity (v_e)
ax1.annotate('', xy=(0.5, 2.8), xytext=(9.5, 2.8),
             arrowprops=dict(arrowstyle='->', color='blue', lw=3))
ax1.text(5, 2.4, r'Electron Drift Velocity ($v_e$) $\leftarrow$ (Negative Charge)', color='blue', fontsize=14, ha='center', fontweight='bold')

# Magnetic Field B (Out of page)
for x in np.linspace(1.5, 8.5, 6):
    for y in np.linspace(2.5, 4.5, 3):
        ax1.plot(x, y, 'o', color='green', markersize=8, markerfacecolor='none')
        ax1.plot(x, y, '.', color='green', markersize=3)
ax1.text(8.5, 5.5, r'Magnetic Field ($B$) $\odot$ (Out of page)', color='green', fontsize=12, fontweight='bold')

# Lorentz Force on Electron
ax1.annotate('', xy=(5, 2.0), xytext=(5, 3.5),
             arrowprops=dict(arrowstyle='->', color='purple', lw=3))
ax1.text(6.2, 2.8, 'Lorentz Force\non electron ($F_m$)', color='purple', fontsize=12, fontweight='bold')

# Charge accumulation
ax1.text(0.3, 4.2, '+\n+\n+', color='red', fontsize=16, fontweight='bold', ha='center')
ax1.text(0.3, 2.8, '-\n-\n-', color='blue', fontsize=16, fontweight='bold', ha='center')

# Hall Voltage Measurement
ax1.plot([0.2, 0.2], [2.0, 4.8], color='black', lw=2)
ax1.annotate('', xy=(0.2, 4.8), xytext=(0.2, 2.0),
             arrowprops=dict(arrowstyle='<->', color='black', lw=2))
ax1.text(-0.5, 3.4, '$V_H$\n(Hall\nVoltage)', fontsize=12, ha='center', fontweight='bold')

ax1.set_xlim(-1.5, 11)
ax1.set_ylim(1, 6.5)
ax1.axis('off')
ax1.set_title("The Hall Effect: Lorentz Force Separates Charges", fontsize=16, pad=20)
plt.tight_layout()
plt.show()


#--------------------------------------------------------------------------------#
# PLOT 2: D'ARSONVAL MOVEMENT & SHUNT RESISTORS
#--------------------------------------------------------------------------------#
fig2, (ax2, ax3) = plt.subplots(1, 2, figsize=(14, 6))

# Left Plot: Linear Deflection of the Coil
I_coil = np.linspace(0, 1e-3, 100) # 0 to 1 mA
N = 100      # Turns of wire
A = 1e-4     # Area (m^2)
B = 0.1      # Magnetic Field (Tesla)
k = 1e-6     # Spring constant (N*m/rad)

# theta = (N * A * B / k) * I
theta = (N * A * B / k) * I_coil
theta_deg = np.degrees(theta)

ax2.plot(I_coil * 1000, theta_deg, color='darkorange', linewidth=4)
ax2.set_title("D'Arsonval Movement: Linear Deflection", fontsize=14)
ax2.set_xlabel("Current through coil (mA)", fontsize=12)
ax2.set_ylabel("Pointer Deflection Angle (Degrees)", fontsize=12)
ax2.axhline(90, color='red', linestyle='--', label='Max Scale (90°)')
ax2.legend(fontsize=11)

# Right Plot: Shunt Resistor Range Extension
# Meter has internal resistance R_m = 50 Ohms, Full scale I_m = 1 mA
R_m = 50
I_m_fs = 1e-3 # 1 mA full scale
V_m = I_m_fs * R_m # 50 mV (Voltage drop across the meter at full scale)

# We want to measure larger total currents: 10 mA, 100 mA, 1 Amp
I_total_targets = np.array([10e-3, 100e-3, 1.0])

# The shunt resistor must bypass the excess current: I_sh = I_total - I_m
# Since it's in parallel, V_sh = V_m. Therefore, R_sh = V_m / I_sh
R_sh = V_m / (I_total_targets - I_m_fs)

labels = ['10 mA Range', '100 mA Range', '1 Amp Range']
colors = ['green', 'blue', 'purple']

x_pos = np.arange(len(labels))
bars = ax3.bar(x_pos, R_sh, color=colors, edgecolor='black', width=0.5)

for bar, r_val in zip(bars, R_sh):
    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
             rf'{r_val:.3f} $\Omega$', ha='center', va='bottom', fontweight='bold', fontsize=12)

ax3.set_title("Extending Range with Shunt Resistors (Parallel)", fontsize=14)
ax3.set_xticks(x_pos)
ax3.set_xticklabels(labels, fontsize=12)
ax3.set_ylabel("Required Shunt Resistance ($R_{sh}$) in Ohms", fontsize=12)
ax3.set_yscale('log') # Log scale to show the massive drop in resistance
ax3.set_ylim(0.01, 100)

plt.tight_layout()
plt.show()

'''
=============================================================================
 WHAT TO LOOK FOR IN THE PLOTS:
=============================================================================
1. THE HALL EFFECT PLOT (Left):
   Notice the purple arrow. The professor's "trick" poll question relied on
   the fact that conventional current (red) flows RIGHT, but physical electrons
   (blue) flow LEFT. When you apply the Right-Hand Rule to the LEFT-pointing
   velocity and the OUT-OF-PAGE magnetic field, the cross product points UP.
   However, because the electron is NEGATIVE, the force flips and pushes the
   electrons DOWN. This creates the transverse Hall Voltage (V_H).

2. THE D'ARSONVAL PLOT (Top Right):
   The orange line is perfectly straight. This proves that the mechanical
   deflection of the needle is strictly proportional to the electrical current.
   This linear relationship is what allows us to print an evenly spaced scale
   on the face of an analog multimeter!

3. THE SHUNT RESISTOR PLOT (Bottom Right):
   Notice the Y-axis is logarithmic. The delicate coil inside the meter can
   only handle 1 mA (and has 50 Ohms of resistance). If you want to measure
   1 Amp (1000 mA), you must place a tiny 0.05 Ohm resistor in parallel.
   This shunt acts as a "bypass valve", allowing 999 mA to flow safely through
   the shunt, while exactly 1 mA flows through the meter to pin the needle
   at the 90-degree mark!
=============================================================================
'''
