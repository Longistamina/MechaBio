import numpy as np
import matplotlib.pyplot as plt
import seaborn as sbn

sbn.set_theme(style="whitegrid")

'''
=============================================================================
 THE COMPLETE CHAIN OF DIFFUSION
=============================================================================
Step 1: Einstein-Stokes -> Gets D
Step 2: Fick's 1st Law  -> Gets J (Flux)
Step 3: Conservation    -> Gets dC/dt (Fick's 2nd Law)
=============================================================================
'''

#--------------------------------------------------------------------------------#
# STEP 1: EINSTEIN-STOKES RELATIONSHIP (Finding D)
#--------------------------------------------------------------------------------#
# Let's estimate D for a Green Fluorescent Protein (GFP) in water at room temp.
k_B = 1.38e-23      # Boltzmann constant (J/K)
T = 300             # Temperature (Kelvin)
eta = 1.0e-3        # Viscosity of water (Pa*s)
r = 3.0e-9          # Radius of GFP (~3 nm)

# Formula: D = kT / (6 * pi * eta * r)
D = (k_B * T) / (6 * np.pi * eta * r)
print(f"Estimated Diffusion Coefficient (D) for GFP: {D:.2e} m^2/s")
# (Note: The professor noted this is roughly ~10^-10 m^2/s, which matches perfectly!)

#--------------------------------------------------------------------------------#
# STEP 2 & 3: FICK'S LAWS & TIME EVOLUTION
#--------------------------------------------------------------------------------#
# Let's create a 1D space (e.g., a microfluidic channel or tissue scaffold)
L = 100e-6          # 100 micrometers long
N_points = 500
x = np.linspace(0, L, N_points)
dx = x[1] - x[0]

# Initial Condition: A sharp drop of GFP in the middle of the channel
# (Mathematically close to a delta function at t=0)
C = np.zeros_like(x)
center = N_points // 2
C[center-5 : center+5] = 1.0  # High concentration block in the middle

# We will simulate the spreading over a few time steps
dt = 0.001          # Time step (seconds)
steps_to_plot = [0, 50, 200, 800]

fig, axes = plt.subplots(3, 1, figsize=(10, 12), sharex=True)

for step in range(max(steps_to_plot) + 1):

    # Calculate spatial gradient (dC/dx) using numpy's gradient function
    dC_dx = np.gradient(C, dx)

    # STEP 2: FICK'S FIRST LAW (Calculate Flux J)
    # J = -D * (dC/dx)
    J = -D * dC_dx

    # STEP 3: CONSERVATION OF MASS (Calculate dC/dt)
    # dC/dt = - (dJ/dx)  --> Which mathematically becomes D * (d^2C/dx^2)
    dJ_dx = np.gradient(J, dx)
    dC_dt = -dJ_dx

    # If we are at a step we want to visualize, plot the current state
    if step in steps_to_plot:
        idx = steps_to_plot.index(step)

        # Plot Concentration C(x)
        axes[0].plot(x * 1e6, C, label=f't = {step*dt*1000:.1f} ms')

        # Plot Flux J(x)
        axes[1].plot(x * 1e6, J * 1e12, label=f't = {step*dt*1000:.1f} ms')

        # Plot Rate of Change dC/dt
        axes[2].plot(x * 1e6, dC_dt * 1e6, label=f't = {step*dt*1000:.1f} ms')

    # Update Concentration for the next time step (Euler method)
    # C_new = C_old + (dC/dt) * dt
    C = C + dC_dt * dt

#--------------------------------------------------------------------------------#
# FORMATTING THE PLOTS
#--------------------------------------------------------------------------------#
axes[0].set_title("1. Concentration Profile C(x) [Fick's 2nd Law Result]", fontsize=14)
axes[0].set_ylabel("Concentration (C)")
axes[0].legend(title="Time", loc='upper right')
axes[0].set_ylim(-0.1, 1.2)

axes[1].set_title("2. Diffusion Flux J(x) [Fick's 1st Law]", fontsize=14)
axes[1].set_ylabel(r"Flux ($J \times 10^{12}$)")
axes[1].axhline(0, color='black', linewidth=1, linestyle='--')

axes[2].set_title(r"3. Rate of Change $\frac{\partial C}{\partial t}$ (Conservation of Mass)", fontsize=14)
axes[2].set_ylabel(r"dC/dt ($\times 10^6$)")
axes[2].set_xlabel("Position (micrometers)")
axes[2].axhline(0, color='black', linewidth=1, linestyle='--')

plt.tight_layout()
plt.show()
