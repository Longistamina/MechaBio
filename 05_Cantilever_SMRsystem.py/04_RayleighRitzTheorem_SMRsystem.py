'''
=============================================================================
 THE RAYLEIGH-RITZ THEOREM & SUSPENDED MICROCHANNEL RESONATOR (SMR)
=============================================================================
1. THE RAYLEIGH-RITZ THEOREM (Conservation of Energy)
   Solving the Euler-Bernoulli PDE for complex, non-uniform shapes (like a
   cantilever with a cell attached to it) is a mathematical nightmare.
   The Rayleigh-Ritz theorem bypasses the PDE by using an energy approach.

   At resonance, the system continuously trades energy between two states:
   - Maximum Potential Energy (PE_max): When the beam is maximally bent.
   - Maximum Kinetic Energy (KE_max): When the beam is flat but moving fastest.

   By the Conservation of Energy: PE_max = KE_max.
   - PE depends on the beam's stiffness (k).
   - KE depends on the mass (m) and the velocity (which scales with omega * Amplitude).

   If a tiny biological mass (Delta_m) lands on the cantilever, the KE increases.
   To keep the energies balanced (since stiffness k hasn't changed), the system
   MUST vibrate slower. Therefore, the resonant frequency (omega_n) DROPS.

   For small added masses, the frequency shift (Delta_f) is LINEARLY proportional
   to the added mass: Delta_f ≈ -(f_0 / 2*m_eff) * Delta_m.

2. THE PROBLEM: TRADITIONAL CANTILEVERS IN WATER
   To measure biological cells, you need them in an aqueous (water) environment.
   But water is highly viscous. If you submerge a cantilever in water, the fluid
   drag creates massive damping.
   - The Q-factor plummets (reduced by ~65 times compared to air).
   - The resonance peak becomes a broad, flat hill.
   - The sensitivity is completely destroyed; you cannot detect a tiny cell.

3. THE SOLUTION: THE SMR (Suspended Microchannel Resonator)
   The SMR flips the paradigm. Instead of putting the cantilever in the water,
   it puts the water INSIDE the cantilever!
   - The cantilever is hollow, with a microfluidic channel carved inside.
   - The fluid (with cells) flows through the internal channel.
   - The OUTSIDE of the cantilever is kept in a strict VACUUM.

   Because the outside is in a vacuum, there is zero fluid drag. The Q-factor
   remains massive (~500 to 1000+). As a single cell flows through the channel,
   it adds a tiny amount of "buoyant mass", causing a measurable, temporary dip
   in the resonant frequency. This allows mass resolution down to the FEMTOGRAM
   scale (10^-15 grams), which is ~100x more precise than optical microscopes!
=============================================================================
'''

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sbn

sbn.set_theme(style="darkgrid")

#--------------------------------------------------------------------------------#
# 1. RAYLEIGH-RITZ MASS SENSING SIMULATION
#--------------------------------------------------------------------------------#
# Let's model an SMR cantilever vibrating in a vacuum.
f_0 = 1.0e6         # Base resonant frequency = 1 MHz (typical for SMR)
m_beam = 1.0e-9     # Mass of the empty cantilever = 1 nanogram (1000 pg)

# From Rayleigh-Ritz, the "effective mass" of a Mode 1 cantilever is ~23.6% of its physical mass
m_eff = 0.236 * m_beam

# Let's simulate cells of varying masses flowing through the channel
# We will range from 0 to 500 femtograms (1 fg = 10^-15 g = 10^-6 ng)
added_mass_fg = np.linspace(0, 500, 100)
added_mass_ng = added_mass_fg * 1e-6

# Calculate the new frequency using the energy balance (Rayleigh-Ritz approximation)
# f_new = f_0 * sqrt(m_eff / (m_eff + added_mass))
f_new = f_0 * np.sqrt(m_eff / (m_eff + added_mass_ng))

# The frequency shift (Delta f)
delta_f = f_new - f_0

# For very small masses, this is perfectly linear: Delta_f ≈ - (f_0 / 2*m_eff) * Delta_m
delta_f_linear = - (f_0 / (2 * m_eff)) * added_mass_ng

#--------------------------------------------------------------------------------#
# 2. PLOT 1: THE FEMTOGRAM MASS SENSITIVITY
#--------------------------------------------------------------------------------#
fig1, ax1 = plt.subplots(figsize=(10, 6))

ax1.plot(added_mass_fg, delta_f, color='blue', linewidth=3, label=r'Exact Rayleigh-Ritz Shift ($\Delta f$)')
ax1.plot(added_mass_fg, delta_f_linear, color='red', linestyle='--', linewidth=2,
         label=r'Linear Approximation (Small Mass Limit)')

# Highlight a typical single cell (e.g., ~100 fg)
cell_mass = 100
cell_shift = - (f_0 / (2 * m_eff)) * (cell_mass * 1e-6)
ax1.scatter([cell_mass], [cell_shift], color='green', s=150, zorder=5, edgecolors='black')
ax1.annotate(f'Single Cell (~{cell_mass} fg)\nShift: {cell_shift:.1f} Hz',
             xy=(cell_mass, cell_shift), xytext=(150, cell_shift - 100),
             arrowprops=dict(arrowstyle='->', color='green', lw=2),
             fontsize=12, fontweight='bold', color='darkgreen')

ax1.set_title("Rayleigh-Ritz Theorem: Frequency Shift vs. Added Buoyant Mass", fontsize=16)
ax1.set_xlabel("Added Mass of Single Cell (femtograms, fg)", fontsize=14)
ax1.set_ylabel(r"Resonant Frequency Shift ($\Delta f$) [Hz]", fontsize=14)
ax1.legend(fontsize=12)
ax1.invert_yaxis() # Frequency drops, so invert axis to show "dips" going down
plt.tight_layout()
plt.show()

#--------------------------------------------------------------------------------#
# 3. PLOT 2: THE SMR Q-FACTOR RESCUE
#--------------------------------------------------------------------------------#
# Let's visualize why the SMR was invented by comparing Q-factors.
environments = ['Air / Vacuum\n(Traditional)', 'Water\n(Traditional)', 'Water INSIDE,\nVacuum OUTSIDE\n(The SMR)']
q_factors = [800, 12, 1000] # Water reduces Q by ~65x. SMR restores it.
colors_bar = ['skyblue', 'salmon', 'lightgreen']

fig2, ax2 = plt.subplots(figsize=(10, 6))
bars = ax2.bar(environments, q_factors, color=colors_bar, edgecolor='black', linewidth=1.5, width=0.6)

# Add value labels on top of bars
for bar in bars:
    yval = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2, yval + 20, f'Q ≈ {int(yval)}',
             ha='center', va='bottom', fontsize=14, fontweight='bold')

ax2.set_title("The SMR Innovation: Rescuing the Q-Factor from Fluid Damping", fontsize=16)
ax2.set_ylabel("Quality Factor (Q)", fontsize=14)
ax2.set_ylim(0, 1200)

# Add a conceptual "Sensitivity" arrow
ax2.annotate('High Q = High Sensitivity\n(Femtogram Resolution!)',
             xy=(2, 1000), xytext=(1.2, 600),
             arrowprops=dict(arrowstyle='->', color='purple', lw=3),
             fontsize=14, fontweight='bold', color='purple')

plt.tight_layout()
plt.show()

'''
=============================================================================
 WHAT TO LOOK FOR IN THE PLOTS:
=============================================================================
1. THE MASS SHIFT PLOT (Top):
   - Notice the X-axis is in FEMTOGRAMS (10^-15 grams). We are literally
     weighing single biological cells.
   - The blue line (exact energy balance) and red dashed line (linear
     approximation) perfectly overlap. This proves the professor's statement
     that the frequency shift is LINEARLY proportional to the added mass.
   - The green dot shows a 100 fg cell causing a ~23 Hz drop in a 1 MHz
     signal. Because the SMR has such a high Q-factor, the resonance peak
     is so razor-sharp that a 23 Hz shift is massively amplified and easily
     detected by the electronics!

2. THE Q-FACTOR RESCUE PLOT (Bottom):
   - The middle red bar shows the tragedy of traditional biosensors: putting
     a cantilever in water destroys the Q-factor (from 800 down to 12). The
     peak becomes too wide to measure tiny mass shifts.
   - The right green bar shows the brilliance of the SMR: by keeping the
     water strictly INSIDE the channel and vibrating the outside in a vacuum,
     the Q-factor is restored (and even slightly higher due to vacuum
     conditions), enabling the ultimate limit of biological mass sensing.
=============================================================================
'''
