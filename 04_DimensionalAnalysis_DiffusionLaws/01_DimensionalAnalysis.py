import numpy as np
import matplotlib.pyplot as plt
import seaborn as sbn

sbn.set_theme(style="darkgrid")

'''
=============================================================================
 DIMENSIONAL ANALYSIS & DIFFUSION LAWS
=============================================================================
Dimensional analysis simplifies physical problems by enforcing "Dimensional
Homogeneity"—meaning both sides of a valid physical equation must have the
exact same fundamental dimensions (Length [L], Mass [M], Time [T]).

1. DERIVING THE DIFFUSION COEFFICIENT (D)
   Fick's First Law: J = -D * (dC/dx)

   Let's break down the dimensions of each term:
   - Flux (J): Molecules passing per Area per Time
               -> 1 / ([L]^2 * [T])
   - Concentration (C): Molecules per Volume
               -> 1 / [L]^3
   - Gradient (dC/dx): Change in C over distance [L]
               -> (1 / [L]^3) / [L] = 1 / [L]^4

   Plugging these into Fick's Law:
   [J] = [D] * [dC/dx]
   1 / ([L]^2 * [T]) = [D] * (1 / [L]^4)

   Solving for [D]:
   [D] = (1 / ([L]^2 * [T])) * [L]^4
   [D] = [L]^2 / [T]   <-- (e.g., m^2/s or um^2/s)

2. THE PORE FLOW RATE PUZZLE (Radius vs. Area)
   Imagine a membrane with a small hole of radius 'a'. Molecules diffuse
   through it. What is the net flow rate (molecules per second)?

   Naive Intuition: Flow should scale with the Area of the hole (a^2).
   Dimensional Logic:
   - Flow Rate = Molecules / Time -> 1 / [T]
   - Assume Flow Rate is proportional to D, C, and a^k:
     [Flow] = [D] * [C] * [a]^k
     1/[T]  = ([L]^2/[T]) * (1/[L]^3) * [L]^k
     1/[T]  = [L]^(k-1) / [T]

   For the dimensions to match, the [L] terms must cancel out (L^0).
   Therefore: k - 1 = 0  =>  k = 1.

   CONCLUSION: Flow rate scales linearly with RADIUS (a^1), NOT area (a^2)!

   PHYSICAL REASON: A "local depletion zone" forms around the hole. Because
   molecules are instantly absorbed, the concentration right at the hole is
   zero. Molecules from far away must funnel inward, creating a bottleneck
   that limits the maximum uptake rate regardless of the surface area.
=============================================================================
'''

#--------------------------------------------------------------------------------#
# 1. VISUALIZING THE SCALING LAW (The Poll 4 Question)
#--------------------------------------------------------------------------------#
# Let's compare the true physical scaling (a^1) vs the naive intuition (a^2)
a = np.linspace(0.1, 5, 100)  # Radius of the pore
D = 1.0                       # Arbitrary Diffusion Coefficient
C0 = 1.0                      # Arbitrary Bulk Concentration

# True physical scaling (Derived via Dimensional Analysis: Q = 4 * pi * D * C0 * a)
flow_true = 4 * np.pi * D * C0 * a

# Naive intuitive scaling (Assuming it scales with Area: Q = k * a^2)
flow_naive = a**2

plt.figure(figsize=(10, 5))
plt.plot(a, flow_true, label=r'True Scaling (Flow $\propto a^1$)', color='blue', linewidth=3)
plt.plot(a, flow_naive, label=r'Naive Intuition (Flow $\propto a^2$)', color='red', linestyle='--', linewidth=3)
plt.title("Dimensional Analysis: Pore Flow Rate Scaling", fontsize=14)
plt.xlabel("Pore Radius (a)", fontsize=12)
plt.ylabel("Net Flow Rate (molecules / sec)", fontsize=12)
plt.legend(fontsize=12)
plt.tight_layout()
plt.show()


#--------------------------------------------------------------------------------#
# 2. VISUALIZING THE "LOCAL DEPLETION ZONE"
#--------------------------------------------------------------------------------#
# Why does it scale with radius and not area? Let's look at the concentration
# profile C(r) around a perfect spherical absorber (or pore) of radius 'a'.
# The analytical solution to steady-state diffusion is: C(r) = C0 * (1 - a/r)

a_radius = 1.0
r = np.linspace(a_radius, 15*a_radius, 500) # Distance from the center of the pore
C_r = C0 * (1 - a_radius/r)

plt.figure(figsize=(10, 5))
plt.plot(r, C_r, color='green', linewidth=3, label='Concentration Profile C(r)')
plt.fill_between(r, C_r, alpha=0.2, color='green')

# Mark the depletion zone
plt.axvspan(a_radius, 3*a_radius, color='red', alpha=0.1, label='Local Depletion Zone')
plt.axhline(C0, color='black', linestyle=':', label='Bulk Concentration ($C_0$)')

plt.title("The Physical Reason: The Local Depletion Zone", fontsize=14)
plt.xlabel("Distance from pore center (r)", fontsize=12)
plt.ylabel("Concentration C(r)", fontsize=12)
plt.xlim(0, 15)
plt.ylim(0, 1.2)
plt.legend(fontsize=11, loc='lower right')
plt.tight_layout()
plt.show()

'''
=============================================================================
 WHAT TO LOOK FOR IN THE PLOTS:
=============================================================================
1. THE SCALING PLOT (Top):
   Notice how the blue line (true physics) grows much slower than the red
   dashed line (naive intuition). If you double the radius of a nanopore,
   the flow rate only doubles (2x). It does NOT quadruple (4x) like you
   would expect if it were based on surface area!

2. THE DEPLETION ZONE PLOT (Bottom):
   At the surface of the pore (r = a), the concentration is exactly ZERO
   because the pore is a "perfect absorber" (like a black hole for molecules).
   As you move away, the concentration slowly recovers to the bulk level (C0).
   This massive "funnel" of low concentration acts as the true bottleneck,
   which is why the 3D geometry of the space around the hole (radius) matters
   more than the 2D area of the hole itself.
=============================================================================
'''
