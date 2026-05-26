import numpy as np
import matplotlib.pyplot as plt
import seaborn as sbn

sbn.set_theme(style="whitegrid")

'''
=============================================================================
 THE EINSTEIN-STOKES RELATIONSHIP: BRIDGING MACRO AND MICRO
=============================================================================
CONCEPT:
In the previous sections, we treated the Diffusion Coefficient (D) as an
experimentally determined constant. But Albert Einstein and George Stokes
provided a way to ESTIMATE it using fundamental physics.

The relationship connects the random thermal kicks a molecule receives
(microscopic) to the fluid drag it experiences when moving (macroscopic).

1. THE "SKYDIVER" ANALOGY (Macroscopic Drag)
   Imagine a skydiver. Gravity pulls them down, but air resistance (drag)
   pushes back. Eventually, they hit a "terminal velocity" where the forces
   balance. The drag force is proportional to velocity: F_drag = gamma * v.
   Here, 'gamma' is the drag coefficient.

   For a perfectly spherical molecule moving through a viscous fluid,
   Stokes' Law tells us the drag coefficient is:
   gamma = 6 * pi * eta * r

   - eta (η) = dynamic viscosity of the fluid (e.g., water vs. honey)
   - r       = radius of the spherical molecule

2. EINSTEIN'S GENIUS (Microscopic Thermal Energy)
   Einstein realized that the same fluid that causes "drag" on a moving
   particle is also the fluid that randomly "kicks" the particle when it
   is sitting still (Brownian motion).
   He proved that the Diffusion Coefficient (D) is simply the ratio of
   the ambient thermal energy to the drag coefficient:

   D = (k_B * T) / gamma

   Substituting Stokes' Law into Einstein's equation gives the master formula:

   D = (k_B * T) / (6 * pi * eta * r)

3. THE "BIONUMBER" ESTIMATION (Poll 3 Example: GFP in Water)
   - k_B * T (Thermal energy at room temp) ≈ 4.11 x 10^-21 Joules
   - eta (Viscosity of water) ≈ 1 x 10^-3 Pa·s
   - r (Radius of Green Fluorescent Protein) ≈ 3 nm (3 x 10^-9 m)

   Plugging these in gives D ≈ 7.2 x 10^-11 m^2/s.
   If the protein is inside a cell (cytoplasm is ~10x more viscous than
   water), D drops by a factor of 10!
=============================================================================
'''

#--------------------------------------------------------------------------------#
# 1. DEFINE PHYSICAL CONSTANTS AND PARAMETERS
#--------------------------------------------------------------------------------#
k_B = 1.380649e-23      # Boltzmann constant (J/K)
T = 298.15              # Room temperature (Kelvin)
kT = k_B * T            # Thermal energy ≈ 4.11 x 10^-21 J

eta_water = 1.0e-3      # Viscosity of water (Pa·s or kg/(m·s))
eta_cyto  = 10.0e-3     # Viscosity of cell cytoplasm (approx 10x water)

# Radius of GFP (Green Fluorescent Protein)
r_GFP = 3.0e-9          # 3 nanometers in meters

#--------------------------------------------------------------------------------#
# 2. CALCULATE D FOR GFP (The Poll 3 Bionumber Estimation)
#--------------------------------------------------------------------------------#
def calculate_D(kT, eta, r):
    """Einstein-Stokes Equation"""
    return kT / (6 * np.pi * eta * r)

D_GFP_water = calculate_D(kT, eta_water, r_GFP)
D_GFP_cyto  = calculate_D(kT, eta_cyto, r_GFP)

print("--- BIONUMBER ESTIMATION: GFP DIFFUSION ---")
print(f"Thermal Energy (kT): {kT:.2e} J")
print(f"D (GFP in Water):    {D_GFP_water:.2e} m^2/s  (Order of magnitude: ~10^-10)")
print(f"D (GFP in Cytoplasm):{D_GFP_cyto:.2e} m^2/s   (10x slower due to viscosity!)")
print("-------------------------------------------\n")

#--------------------------------------------------------------------------------#
# 3. PLOT 1: HOW MOLECULE SIZE AFFECTS DIFFUSION
#--------------------------------------------------------------------------------#
# Let's look at molecules ranging from 1 nm (small metabolite) to 10 nm (large protein complex)
r_array = np.linspace(1e-9, 10e-9, 100)

D_water = calculate_D(kT, eta_water, r_array)
D_cyto  = calculate_D(kT, eta_cyto, r_array)

fig1, ax1 = plt.subplots(figsize=(10, 6))
ax1.plot(r_array * 1e9, D_water, color='blue', linewidth=3, label='In Water ($\eta = 1$ mPa·s)')
ax1.plot(r_array * 1e9, D_cyto, color='red', linewidth=3, label='In Cytoplasm ($\eta = 10$ mPa·s)')

# Mark GFP
ax1.scatter([3], [D_GFP_water], color='darkblue', s=100, zorder=5, edgecolor='black')
ax1.annotate('GFP (Water)', xy=(3, D_GFP_water), xytext=(4, D_GFP_water + 2e-11),
             arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8))

ax1.set_title("Einstein-Stokes: Effect of Molecular Size on Diffusion", fontsize=16)
ax1.set_xlabel("Molecule Radius (nm)", fontsize=14)
ax1.set_ylabel("Diffusion Coefficient D ($m^2/s$)", fontsize=14)
ax1.legend(fontsize=12)
plt.tight_layout()
plt.show()

#--------------------------------------------------------------------------------#
# 4. PLOT 2: HOW FLUID VISCOSITY AFFECTS DIFFUSION
#--------------------------------------------------------------------------------#
# Let's keep the molecule size fixed (GFP, 3nm) and change the fluid environment
# Viscosity ranges from water (1) to glycerol-like environments (100)
eta_array = np.linspace(1e-3, 100e-3, 100)
D_varying_visc = calculate_D(kT, eta_array, r_GFP)

fig2, ax2 = plt.subplots(figsize=(10, 6))
ax2.plot(eta_array * 1e3, D_varying_visc, color='purple', linewidth=3)
ax2.fill_between(eta_array * 1e3, D_varying_visc, color='purple', alpha=0.1)

ax2.set_title("Einstein-Stokes: Effect of Fluid Viscosity on GFP Diffusion", fontsize=16)
ax2.set_xlabel("Fluid Viscosity $\eta$ (mPa·s)", fontsize=14)
ax2.set_ylabel("Diffusion Coefficient D ($m^2/s$)", fontsize=14)

# Add text annotations for biological contexts
ax2.axvline(1, color='blue', linestyle='--', alpha=0.7)
ax2.text(1.5, 6e-11, 'Water / Blood Plasma', color='blue', fontsize=12)

ax2.axvline(10, color='red', linestyle='--', alpha=0.7)
ax2.text(12, 6e-11, 'Cell Cytoplasm', color='red', fontsize=12)

ax2.axvline(80, color='green', linestyle='--', alpha=0.7)
ax2.text(50, 2e-11, 'Mucus / Dense Matrix', color='green', fontsize=12)

plt.tight_layout()
plt.show()

'''
=============================================================================
 WHAT TO LOOK FOR IN THE PLOTS:
=============================================================================
1. THE INVERSE RELATIONSHIPS:
   - D is inversely proportional to radius (1/r). If a protein complex is
     twice as large, it diffuses half as fast.
   - D is inversely proportional to viscosity (1/eta). The cytoplasm is
     incredibly crowded with proteins and organelles, making it effectively
     10x more viscous than pure water. This acts as a massive "speed bump"
     for molecular transport inside cells.

2. THE LIMITS OF DIFFUSION:
   Because D is so small (10^-11 m^2/s), and diffusion time scales with
   L^2 / 2D, a protein relying purely on diffusion would take hours to
   travel across a large cell (like a neuron). This mathematically proves
   why cells require active transport (motor proteins walking on microtubules)
   and why large organisms require circulatory systems (advection)!
=============================================================================
'''
