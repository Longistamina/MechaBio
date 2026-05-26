import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sbn

sbn.set_theme(style="whitegrid")

'''
=============================================================================
 FICK'S FIRST LAW OF DIFFUSION: FROM RANDOMNESS TO MACROSCOPIC FLUX
=============================================================================
CONCEPT:
Diffusion is driven entirely by random thermal motion (Brownian motion).
Molecules don't "know" where the concentration is lower; they just bounce
around randomly. However, statistically, more molecules will bounce AWAY
from a crowded area than FROM an empty area, creating a NET directional flow.

1. THE MICROSCOPIC DERIVATION (The Random Walk)
   Imagine two adjacent microscopic boxes of volume V = Area * Δx.
   - Left box (at x) has N(x) molecules.
   - Right box (at x+Δx) has N(x+Δx) molecules.
   In a small time step Δt, random chance dictates that half the molecules
   in each box will jump to the other box.

   - Jumps Left to Right: 1/2 * N(x)
   - Jumps Right to Left: 1/2 * N(x+Δx)

   Net Molecules moving Right = 1/2 * [N(x) - N(x+Δx)]

   Flux (J) is defined as (Net Molecules) / (Area * Time):
   J = - (1/2) * [N(x+Δx) - N(x)] / (A * Δt)

   Since Concentration C = N / (A * Δx), we can substitute N = C * A * Δx:
   J = - (1/2) * [C(x+Δx)*A*Δx - C(x)*A*Δx] / (A * Δt)
   J = - (Δx^2 / 2*Δt) * [C(x+Δx) - C(x)] / Δx

   If we define the Diffusion Coefficient D = (Δx^2 / 2*Δt), and take the
   limit as Δx -> 0, the difference quotient becomes a derivative:

   FICK'S FIRST LAW:  J = -D * (dC/dx)
   (The negative sign means flux goes DOWN the concentration gradient).

2. THE MACROSCOPIC APPLICATION (Steady-State Tissue Scaffold)
   Imagine glucose diffusing through a tissue scaffold of thickness L.
   - Boundary conditions: C(0) = C0 (high), C(L) = CL (low).
   - "Steady-State" means the concentration profile is NOT changing over time.
   - For C to remain constant over time, the flux entering any slice of the
     tissue must EXACTLY equal the flux leaving it. Otherwise, molecules
     would accumulate or deplete, violating steady-state.
   - Therefore, J must be CONSTANT across the entire scaffold (dJ/dx = 0).

   If J is constant, and D is constant, then dC/dx must be constant.
   The integral of a constant slope is a STRAIGHT LINE.
   C(x) = C0 - (J/D)*x
=============================================================================
'''

#--------------------------------------------------------------------------------#
# PLOT 1: THE MICROSCOPIC DERIVATION (Random Walk Logic)
#--------------------------------------------------------------------------------#
fig1, ax1 = plt.subplots(figsize=(10, 6))

# Draw Left Box (High Concentration)
rect1 = patches.Rectangle((1, 1), 2.5, 4, fill=False, edgecolor='blue', linewidth=3)
ax1.add_patch(rect1)
ax1.text(2.25, 3, '100\nMolecules', ha='center', va='center', fontsize=14, color='blue', fontweight='bold')
ax1.text(2.25, 0.5, r'Position $x$', ha='center', fontsize=14)

# Draw Right Box (Low Concentration)
rect2 = patches.Rectangle((4.5, 1), 2.5, 4, fill=False, edgecolor='red', linewidth=3)
ax1.add_patch(rect2)
ax1.text(5.75, 3, '40\nMolecules', ha='center', va='center', fontsize=14, color='red', fontweight='bold')
ax1.text(5.75, 0.5, r'Position $x+\Delta x$', ha='center', fontsize=14)

# Arrows for Random Jumps
# Left to Right
ax1.annotate('', xy=(4.3, 4.2), xytext=(3.7, 4.2),
             arrowprops=dict(arrowstyle='->', color='green', lw=3))
ax1.text(4.0, 4.6, '50 move Right\n($1/2 \times 100$)', ha='center', color='green', fontsize=12, fontweight='bold')

# Right to Left
ax1.annotate('', xy=(3.7, 1.8), xytext=(4.3, 1.8),
             arrowprops=dict(arrowstyle='->', color='purple', lw=3))
ax1.text(4.0, 1.4, '20 move Left\n($1/2 \times 40$)', ha='center', color='purple', fontsize=12, fontweight='bold')

# Net Flux Result
ax1.text(4.0, 6.0, r'NET FLUX = 50 - 20 = 30 molecules $\rightarrow$',
         ha='center', fontsize=16, fontweight='bold', color='darkorange',
         bbox=dict(boxstyle="round,pad=0.3", edgecolor="darkorange", facecolor="yellow", alpha=0.5))

ax1.set_xlim(0, 8)
ax1.set_ylim(0, 7)
ax1.axis('off')
ax1.set_title("Microscopic View: Pure Randomness Creates Directional Flux", fontsize=18, pad=20)
plt.tight_layout()
plt.show()


#--------------------------------------------------------------------------------#
# PLOT 2: THE MACROSCOPIC STEADY-STATE (Tissue Scaffold Example)
#--------------------------------------------------------------------------------#
L = 10.0       # Thickness of scaffold
C0 = 10.0      # Concentration at x=0
CL = 2.0       # Concentration at x=L
D = 1.5        # Diffusion Coefficient

x = np.linspace(0, L, 100)
# Linear profile derived from constant J
C_x = C0 - (C0 - CL) * (x / L)

# Calculate the constant Flux J
# J = -D * dC/dx. Since slope is (CL - C0)/L, J = -D * (CL - C0)/L = D * (C0 - CL)/L
J_constant = D * (C0 - CL) / L

fig2, ax2 = plt.subplots(figsize=(10, 6))

# Plot Concentration Profile
ax2.plot(x, C_x, 'b-', linewidth=4, label=r'Concentration $C(x)$')
ax2.fill_between(x, C_x, alpha=0.15, color='blue')

# Mark Boundary Conditions
ax2.plot(0, C0, 'ro', markersize=12, zorder=5)
ax2.text(0.5, C0 - 0.8, r'$C(0) = C_0$ (High)', fontsize=13, color='red', fontweight='bold')
ax2.plot(L, CL, 'ro', markersize=12, zorder=5)
ax2.text(L - 2.5, CL + 0.8, r'$C(L) = C_L$ (Low)', fontsize=13, color='red', fontweight='bold')

# Add the constant Flux line on a secondary y-axis
ax3 = ax2.twinx()
ax3.axhline(J_constant, color='green', linestyle='--', linewidth=4, label=r'Constant Flux $J$')
ax3.set_ylabel(r'Diffusion Flux $J$ (Molecules / Area $\cdot$ Time)', fontsize=14, color='green')
ax3.tick_params(axis='y', labelcolor='green')
ax3.set_ylim(0, J_constant * 3) # Give it some headroom

# Formatting
ax2.set_xlabel('Position across Tissue Scaffold ($x$)', fontsize=14)
ax2.set_ylabel('Concentration $C(x)$', fontsize=14, color='blue')
ax2.tick_params(axis='y', labelcolor='blue')
ax2.set_title("Macroscopic View: Steady-State Diffusion (Poll 2 Example)", fontsize=18)

# Combine legends
lines_1, labels_1 = ax2.get_legend_handles_labels()
lines_2, labels_2 = ax3.get_legend_handles_labels()
ax2.legend(lines_1 + lines_2, labels_1 + labels_2, loc='center right', fontsize=13, framealpha=0.9)

plt.tight_layout()
plt.show()

'''
=============================================================================
 WHAT TO LOOK FOR IN THE PLOTS:
=============================================================================
1. THE MICROSCOPIC PLOT (Top):
   Notice that the molecules are NOT actively trying to move to the right.
   They are just jumping randomly in both directions. But because there are
   MORE molecules on the left, the 50% that jump right outnumber the 50%
   that jump left. This statistical imbalance IS the concentration gradient
   (dC/dx), and it mathematically forces the net flux (J).

2. THE MACROSCOPIC PLOT (Bottom):
   Look at the straight blue line. The professor emphasized in Poll 2 that
   in a STEADY-STATE system, the concentration profile MUST be linear.
   - If the curve bowed outward, it would mean molecules are piling up in
     the middle (violating steady-state).
   - If the curve bowed inward, it would mean molecules are vanishing from
     the middle (violating conservation of mass).
   - Therefore, the slope (dC/dx) must be perfectly constant, resulting in
     a perfectly constant Flux (the green dashed line) from one side to the other.
=============================================================================
'''
