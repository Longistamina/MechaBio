import numpy as np
import matplotlib.pyplot as plt
import seaborn as sbn

sbn.set_theme(style="whitegrid")

'''
=============================================================================
 FICK'S SECOND LAW OF DIFFUSION: TIME-DEPENDENT SPREADING
=============================================================================
CONCEPT:
Fick's First Law tells us the FLUX (J) at a specific moment. But what happens
when that flux causes molecules to accumulate or deplete in a specific region
over time? Fick's Second Law answers this by combining Fick's First Law with
the Law of Conservation of Mass.

1. THE DERIVATION (Conservation of Mass)
   Imagine a tiny microscopic box of width Δx.
   - Molecules enter from the left at flux J(x).
   - Molecules exit to the right at flux J(x + Δx).
   - The net change in the number of molecules (ΔN) over time (Δt) is:
     ΔN = [J(x) - J(x + Δx)] * Area * Δt

   To find the change in CONCENTRATION (ΔC), we divide by the Volume (Area * Δx):
   ΔC / Δt = - [J(x + Δx) - J(x)] / Δx

   Taking the limit as Δx and Δt approach zero gives the continuity equation:
   ∂C/∂t = -∂J/∂x

   Now, substitute Fick's First Law (J = -D * ∂C/∂x) into this equation:
   ∂C/∂t = -∂/∂x (-D * ∂C/∂x)

   FICK'S SECOND LAW:  ∂C/∂t = D * (∂²C/∂x²)

2. THE SOLUTION (The Gaussian Spread)
   If you drop a single microscopic droplet of dye (a "point source" or Dirac
   delta function) into a tube of water at t=0, the mathematical solution to
   Fick's Second Law is a Gaussian (Normal) Distribution:

   C(x,t) = [M / sqrt(4 * pi * D * t)] * exp(-x² / (4 * D * t))

   - The peak concentration drops over time as the dye spreads.
   - The variance of the Gaussian is σ² = 2Dt.
   - The characteristic diffusion length scale is L = sqrt(2Dt).

3. THE BIOLOGICAL SCALING LAW (The Fourier Number)
   Because L = sqrt(2Dt), the TIME it takes to diffuse a certain distance
   scales with the SQUARE of the distance (t ∝ L²).
   - Diffusing across a cell (10 µm) takes milliseconds.
   - Diffusing across a tissue organ (10 cm) would take YEARS.
   This is why biological systems rely on blood vessels (advection) for long
   distances, and why cells must remain microscopic!
=============================================================================
'''

#--------------------------------------------------------------------------------#
# PLOT 1: THE MACROSCOPIC VIEW (Gaussian Spreading over Time)
#--------------------------------------------------------------------------------#
D = 1.0  # Diffusion coefficient (arbitrary units)
M = 1.0  # Total mass of the point source
x = np.linspace(-15, 15, 1000)

# Time steps to visualize the spreading
times = [0.5, 2.0, 5.0, 10.0]
colors = ['red', 'orange', 'green', 'blue']

fig1, ax1 = plt.subplots(figsize=(10, 6))

for t, color in zip(times, colors):
    # Analytical solution to Fick's Second Law for a point source
    # Note: At t=0, this is a Dirac delta function (infinite height, zero width)
    C_x_t = (M / np.sqrt(4 * np.pi * D * t)) * np.exp(-x**2 / (4 * D * t))

    ax1.plot(x, C_x_t, color=color, linewidth=3, label=f't = {t} s')
    ax1.fill_between(x, C_x_t, color=color, alpha=0.1)

    # Mark the characteristic diffusion length L = sqrt(2Dt)
    L = np.sqrt(2 * D * t)
    ax1.axvline(L, color=color, linestyle='--', alpha=0.6)
    ax1.axvline(-L, color=color, linestyle='--', alpha=0.6)

ax1.set_title("Macroscopic View: Fick's Second Law (Gaussian Spreading)", fontsize=16)
ax1.set_xlabel("Position (x)", fontsize=14)
ax1.set_ylabel("Concentration C(x,t)", fontsize=14)
ax1.legend(fontsize=12, title="Time elapsed")
plt.tight_layout()
plt.show()


#--------------------------------------------------------------------------------#
# PLOT 2: THE MICROSCOPIC VIEW (Random Walk Simulation)
#--------------------------------------------------------------------------------#
# The professor emphasized that diffusion is driven purely by RANDOMNESS.
# Let's simulate 5000 individual molecules doing a 1D random walk and prove
# that their collective chaos perfectly matches Fick's deterministic calculus!

num_particles = 5000
num_steps = 1000
dt = 0.01      # Time step
dx = np.sqrt(2 * D * dt)  # Step size derived from D = dx^2 / (2*dt)

# Generate random steps: +dx or -dx with 50% probability
random_steps = np.random.choice([-dx, dx], size=(num_particles, num_steps))

# Calculate the cumulative position of each particle over time
trajectories = np.cumsum(random_steps, axis=1)
time_array = np.arange(1, num_steps + 1) * dt

fig2, (ax2, ax3) = plt.subplots(2, 1, figsize=(10, 10), gridspec_kw={'height_ratios': [1, 1]})

# Top: Spaghetti plot of a few random walk trajectories
num_to_plot = 50
for i in range(num_to_plot):
    ax2.plot(time_array, trajectories[i, :], color='gray', alpha=0.2, linewidth=1)
ax2.set_title(f"Microscopic View: {num_to_plot} Individual Random Walk Trajectories (out of {num_particles})", fontsize=16)
ax2.set_xlabel("Time (t)", fontsize=14)
ax2.set_ylabel("Position (x)", fontsize=14)

# Bottom: Histogram of final positions vs. Fick's Second Law Prediction
final_positions = trajectories[:, -1]
final_time = time_array[-1]

# Plot the histogram of the simulated particles
ax3.hist(final_positions, bins=50, density=True, color='skyblue', edgecolor='black', alpha=0.7, label='Simulated Random Walk')

# Overlay the exact analytical prediction from Fick's Second Law
x_theory = np.linspace(-10, 10, 500)
C_theory = (M / np.sqrt(4 * np.pi * D * final_time)) * np.exp(-x_theory**2 / (4 * D * final_time))
ax3.plot(x_theory, C_theory, color='red', linewidth=4, label=f"Fick's 2nd Law Prediction (t={final_time}s)")

ax3.set_title("The Bridge: Random Chaos perfectly matches Deterministic Calculus", fontsize=16)
ax3.set_xlabel("Final Position (x)", fontsize=14)
ax3.set_ylabel("Probability Density / Concentration", fontsize=14)
ax3.legend(fontsize=12)

plt.tight_layout()
plt.show()

'''
=============================================================================
 WHAT TO LOOK FOR IN THE PLOTS:
=============================================================================
1. THE GAUSSIAN SPREADING (Plot 1):
   Notice how the peak concentration drops rapidly as time goes on, while the
   "bell curve" widens. The dashed lines mark L = sqrt(2Dt). This visually
   proves the professor's point: the "width" of the spread grows with the
   SQUARE ROOT of time. To diffuse 2x further, it takes 4x longer!

2. THE RANDOM WALK BRIDGE (Plot 2):
   - Top: You can see the pure, unpredictable chaos of individual molecules
     bouncing left and right.
   - Bottom: When you zoom out and look at all 5,000 molecules at the final
     time step, their chaotic distribution (blue bars) forms a perfect bell
     curve that perfectly aligns with the red line predicted by Fick's
     calculus. This is the profound beauty of statistical mechanics!
=============================================================================
'''
