'''
=============================================================================
 EULER-BERNOULLI BEAM THEORY: MODELING CANTILEVER DYNAMICS
=============================================================================
1. THE LIMITATION OF THE LUMPED MODEL
   A lumped model treats the cantilever as a single point mass on a spring.
   But in reality, a cantilever is a continuous beam. The base doesn't move
   at all, while the tip moves the most. To capture this "position-dependent
   amplitude", we use Euler-Bernoulli Beam Theory.

2. THE PARTIAL DIFFERENTIAL EQUATION (PDE)
   Instead of F=ma for a single block, we apply Newton's Second Law to
   infinitely small slices of the beam. This yields the PDE:

   E * I * (d^4 w / dx^4) + rho * A * (d^2 w / dt^2) = F(x,t)

   w(x,t) = Deflection at position x and time t
   E      = Young's Modulus (material stiffness)
   I      = Area Moment of Inertia (cross-sectional geometry)
   rho    = Material density
   A      = Cross-sectional area

3. THE FOUR BOUNDARY CONDITIONS (Cantilever)
   To solve this PDE, we need 4 boundary conditions (because of the 4th derivative):
   AT THE BASE (x = 0):
     1. w(0) = 0        (Zero deflection: it's clamped)
     2. dw/dx(0) = 0    (Zero slope: it's clamped flat)
   AT THE FREE TIP (x = L):
     3. d^2w/dx^2(L) = 0 (Zero bending moment: no external torque at the tip)
     4. d^3w/dx^3(L) = 0 (Zero shear force: no external vertical force at the tip)

4. MODE SHAPES AND NODES
   Applying these boundary conditions restricts the beam to only vibrate at
   specific, discrete resonant frequencies (omega_n).
   - Mode 1: The classic "diving board" sweep.
   - Mode 2 & 3: Higher frequencies that create "Nodes" (positions along the
     beam where the amplitude is exactly zero, even while the rest vibrates).

5. THE SCALING LAW (The "Ruler" Analogy)
   For a rectangular beam with width (depth) d and thickness (height) h:
   I = (d * h^3) / 12   and   A = d * h

   Plugging these into the frequency equation reveals that:
   omega_n is proportional to h / L^2.

   CRITICAL TAKEAWAY: The resonant frequency depends linearly on the THICKNESS (h),
   but is COMPLETELY INDEPENDENT of the WIDTH/DEPTH (d).
   (If you bend a flat ruler, it's floppy. If you turn it sideways, it's stiff!)
=============================================================================
'''

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sbn

sbn.set_theme(style="darkgrid")

#--------------------------------------------------------------------------------#
# 1. DEFINE BEAM PROPERTIES & MATHEMATICAL CONSTANTS
#--------------------------------------------------------------------------------#
L = 1.0  # Normalized Length of the cantilever (x goes from 0 to L)
x = np.linspace(0, L, 500)

# The characteristic equation for a cantilever is: cos(beta*L)*cosh(beta*L) + 1 = 0
# The first three roots (beta_n * L) are well-known constants:
beta_L_roots = np.array([1.8751, 4.6941, 7.8548]) # Mode 1, Mode 2, Mode 3

#--------------------------------------------------------------------------------#
# 2. DEFINE THE MODE SHAPE EQUATION
#--------------------------------------------------------------------------------#
def calculate_mode_shape(x, beta_n_L, L):
    """
    Calculates the normalized spatial deflection W(x) for a given mode.
    Derived from applying the 4 boundary conditions to the general PDE solution.
    """
    beta_n = beta_n_L / L

    # Sigma is a constant derived from the tip boundary conditions
    sigma_n = (np.cosh(beta_n_L) + np.cos(beta_n_L)) / \
              (np.sinh(beta_n_L) + np.sin(beta_n_L))

    # The exact analytical mode shape equation
    W_x = (np.cosh(beta_n * x) - np.cos(beta_n * x)) - \
          sigma_n * (np.sinh(beta_n * x) - np.sin(beta_n * x))

    # Normalize so the maximum amplitude is exactly 1.0 for easy visual comparison
    return W_x / np.max(np.abs(W_x))

#--------------------------------------------------------------------------------#
# 3. PLOT 1: THE MODE SHAPES (Visualizing the PDE)
#--------------------------------------------------------------------------------#
fig1, ax1 = plt.subplots(figsize=(10, 6))

colors = ['blue', 'red', 'green']
mode_labels = ['Mode 1 (Fundamental)', 'Mode 2 (First Overtone)', 'Mode 3 (Second Overtone)']

for i, beta_L in enumerate(beta_L_roots):
    W = calculate_mode_shape(x, beta_L, L)
    ax1.plot(x, W, color=colors[i], linewidth=3, label=mode_labels[i])

    # Find and mark the "Nodes" (where amplitude crosses zero, excluding the base)
    # We look for sign changes in the array
    zero_crossings = np.where(np.diff(np.sign(W)))[0]
    for zc in zero_crossings:
        # Only mark nodes that are not at the clamped base (x=0)
        if x[zc] > 0.05:
            ax1.plot(x[zc], 0, 'ko', markersize=8, zorder=5)
            ax1.text(x[zc], 0.15, 'Node', ha='center', fontsize=10, fontweight='bold')

ax1.axhline(0, color='black', linewidth=1, linestyle='-')
ax1.set_title("Euler-Bernoulli Cantilever Mode Shapes (Solving the PDE)", fontsize=16)
ax1.set_xlabel("Position along beam (x / L)", fontsize=12)
ax1.set_ylabel("Normalized Deflection Amplitude", fontsize=12)
ax1.legend(fontsize=11, loc='upper left')
ax1.set_ylim(-1.5, 1.5)

# Draw the "clamped" wall at the base
ax1.plot([0, 0], [-1.5, 1.5], color='black', linewidth=8, solid_capstyle='butt')
ax1.text(-0.05, 0, 'Clamped\nBase', ha='right', va='center', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.show()

#--------------------------------------------------------------------------------#
# 4. PLOT 2: THE SCALING LAW (Thickness vs. Width)
#--------------------------------------------------------------------------------#
# Let's prove the professor's "Ruler" analogy mathematically.
# omega_n is proportional to (h / L^2) * sqrt(E / rho)
# We will hold E, rho, and L constant and vary h (thickness) and d (width/depth)

h_vals = np.linspace(0.5, 5.0, 100) # Varying thickness
d_vals = np.linspace(0.5, 5.0, 100) # Varying width/depth

# Frequency scaling factor (ignoring constant material properties for visualization)
# omega is proportional to h
freq_vs_h = h_vals

# omega is completely independent of d (it cancels out in I/A)
freq_vs_d = np.ones_like(d_vals) * 2.5 # Arbitrary constant line

fig2, ax2 = plt.subplots(figsize=(10, 5))
ax2.plot(h_vals, freq_vs_h, color='purple', linewidth=4, label=r'Resonant Frequency vs. Thickness ($h$)')
ax2.plot(d_vals, freq_vs_d, color='orange', linewidth=4, linestyle='--', label=r'Resonant Frequency vs. Width/Depth ($d$)')

ax2.set_title("The Scaling Law: Why turning a ruler sideways makes it stiff", fontsize=16)
ax2.set_xlabel("Dimension Multiplier", fontsize=12)
ax2.set_ylabel("Relative Resonant Frequency ($\omega_n$)", fontsize=12)
ax2.legend(fontsize=12)

plt.tight_layout()
plt.show()

'''
=============================================================================
 WHAT TO LOOK FOR IN THE PLOTS:
=============================================================================
1. THE MODE SHAPES (Top Plot):
   - MODE 1 (Blue): The entire beam sweeps up and down together. This is the
     mode used in almost all biological mass sensing (like the SMR).
   - MODE 2 (Red) & MODE 3 (Green): Notice the black dots labeled "Node".
     These are physical locations on the vibrating beam that are completely
     stationary! The professor noted that as you increase the driving frequency,
     the beam breaks into complex shapes with multiple stationary nodes.
   - THE BASE: Notice how all lines perfectly flatten out horizontally at x=0.
     This is the mathematical enforcement of the "Zero Deflection" and
     "Zero Slope" boundary conditions.

2. THE SCALING LAW (Bottom Plot):
   - The PURPLE line shows that if you double the thickness (h) of your
     cantilever, the resonant frequency doubles.
   - The ORANGE dashed line shows that if you double the width (d) of your
     cantilever, the frequency DOES NOT CHANGE.
   - WHY? Because adding width adds stiffness (I), but it adds an exactly
     proportional amount of mass (A). The two effects perfectly cancel out!
     But adding thickness adds stiffness to the 3rd power (h^3), while only
     adding mass linearly (h). Therefore, thickness dominates!
=============================================================================
'''
