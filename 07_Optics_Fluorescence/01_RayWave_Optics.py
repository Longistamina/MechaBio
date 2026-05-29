'''
=============================================================================
 PART I: RAY OPTICS & WAVE OPTICS
=============================================================================
1. RAY TRACING BASICS (The 4 Golden Rules)
   The professor emphasized that instead of deriving complex formulas, we
   use 4 conceptual ray-tracing rules to design microscopes:
   Rule 1: Rays originating from the focal point emerge PARALLEL to the axis.
   Rule 2: Parallel incoming rays CONVERGE at the focal point.
   Rule 3: Rays from the focal plane emerge COLLIMATED (parallel to each other).
   Rule 4: Collimated rays passing through the focal plane focus to a single point.

2. SIMPLEST MICROSCOPY (2-Lens System)
   Distance between lenses = f1 + f2.
   The first lens collimates light from the sample; the second lens focuses
   it to form a magnified image. Magnification M = -f2 / f1.

3. WAVE OPTICS: INTERFERENCE & DIFFRACTION
   Light behaves as a wave. When it passes through slits, it spreads out
   (Huygens-Fresnel Principle) and interferes with itself.
   - Double-Slit Interference: Creates alternating bright/dark fringes.
     I(θ) = I0 * cos²(π*d*sinθ / λ)
   - Single-Slit Diffraction: Creates a broad central peak with fading side lobes.
     I(θ) = I0 * sinc²(π*a*sinθ / λ)
   - Real Pattern: The double-slit fringes are "enveloped" by the single-slit
     diffraction pattern.
=============================================================================
'''

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sbn

sbn.set_theme(style="whitegrid")


#--------------------------------------------------------------------------------#
# PLOT 1: RAY TRACING & SIMPLE 2-LENS MICROSCOPE (Conceptual Schematic)
#--------------------------------------------------------------------------------#
fig1, ax1 = plt.subplots(figsize=(12, 6))

# Optical Axis
ax1.axhline(0, color='black', linewidth=1.5, linestyle='-')

# Lens 1 (Objective)
ax1.plot([0, 0], [-2, 2], color='blue', linewidth=4)
ax1.text(0, 2.3, 'Lens 1 (f1)', ha='center', color='blue', fontweight='bold')
# Focal points for Lens 1
ax1.plot([-2, -2], [-0.2, 0.2], 'ro')
ax1.text(-2, -0.5, 'F1', ha='center', color='red')
ax1.plot([2, 2], [-0.2, 0.2], 'ro')
ax1.text(2, -0.5, "F1'", ha='center', color='red')

# Lens 2 (Eyepiece/Tube Lens)
ax1.plot([5, 5], [-2, 2], color='green', linewidth=4)
ax1.text(5, 2.3, 'Lens 2 (f2)', ha='center', color='green', fontweight='bold')
# Focal points for Lens 2
ax1.plot([3, 3], [-0.2, 0.2], 'mo')
ax1.text(3, -0.5, 'F2', ha='center', color='purple')
ax1.plot([7, 7], [-0.2, 0.2], 'mo')
ax1.text(7, -0.5, "F2'", ha='center', color='purple')

# Ray Tracing (Rule 1 & 2 combined for microscopy)
# Ray from sample at F1 -> emerges parallel -> hits Lens 2 -> focuses at F2'
ax1.plot([-2, 0], [1, 0], color='orange', linewidth=2) # To lens 1
ax1.plot([0, 5], [0, 0], color='orange', linewidth=2, linestyle='--') # Collimated
ax1.plot([5, 7], [0, -1], color='orange', linewidth=2) # Focuses at F2'

# Second ray (bottom of sample)
ax1.plot([-2, 0], [-1, 0], color='cyan', linewidth=2)
ax1.plot([0, 5], [0, 0], color='cyan', linewidth=2, linestyle='--')
ax1.plot([5, 7], [0, 1], color='cyan', linewidth=2)

ax1.set_xlim(-3, 8)
ax1.set_ylim(-2.5, 2.5)
ax1.axis('off')
ax1.set_title("Ray Optics: Simple 2-Lens Microscope (Distance = f1 + f2)", fontsize=16, pad=15)
plt.tight_layout()
plt.show()


#--------------------------------------------------------------------------------#
# PLOT 2: WAVE OPTICS - INTERFERENCE & DIFFRACTION INTENSITY
#--------------------------------------------------------------------------------#
theta = np.linspace(-0.05, 0.05, 1000) # Small angle approximation
lam = 500e-9  # 500 nm (green light)
d = 50e-6     # Slit separation (double slit)
a = 10e-6     # Slit width (single slit)

# Phase terms
alpha = np.pi * d * np.sin(theta) / lam  # Interference term
beta = np.pi * a * np.sin(theta) / lam   # Diffraction term

# Intensities
I_interference = np.cos(alpha)**2
I_diffraction = np.sinc(beta / np.pi)**2 # numpy sinc is sin(pi*x)/(pi*x)
I_combined = I_interference * I_diffraction

fig2, axes = plt.subplots(3, 1, figsize=(10, 10), sharex=True)

axes[0].plot(theta*1e3, I_interference, color='blue', linewidth=2)
axes[0].set_title(r"Double-Slit Interference: $I \propto \cos^2(\frac{\pi d \sin\theta}{\lambda})$", fontsize=14)
axes[0].set_ylabel("Normalized Intensity")
axes[0].set_ylim(0, 1.1)

axes[1].plot(theta*1e3, I_diffraction, color='red', linewidth=2)
axes[1].set_title(r"Single-Slit Diffraction Envelope: $I \propto \text{sinc}^2(\frac{\pi a \sin\theta}{\lambda})$", fontsize=14)
axes[1].set_ylabel("Normalized Intensity")
axes[1].set_ylim(0, 1.1)

axes[2].plot(theta*1e3, I_combined, color='purple', linewidth=2.5)
axes[2].set_title(r"Real Pattern: Interference × Diffraction Envelope", fontsize=14)
axes[2].set_xlabel(r"Angle $\theta$ (milliradians)")
axes[2].set_ylabel("Normalized Intensity")
axes[2].set_ylim(0, 1.1)

plt.tight_layout()
plt.show()

'''
WHAT TO LOOK FOR:
- Top Plot: Pure interference creates equally spaced, equal-height fringes.
- Middle Plot: Diffraction creates a broad central peak that rapidly fades.
- Bottom Plot: The real physical pattern! The interference fringes are
  "chopped" by the diffraction envelope. This matches the professor's
  explanation of how slit geometry dictates the final light distribution.
'''
