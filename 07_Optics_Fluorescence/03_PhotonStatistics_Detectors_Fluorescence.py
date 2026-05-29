'''
=============================================================================
 PARTICLE NATURE, DETECTORS & FLUORESCENCE
=============================================================================
1. PHOTON SHOT NOISE (The Quantum Limit)
   Light arrives in discrete, quantized packets (photons). The arrival of
   photons at a detector follows POISSON STATISTICS.
   - Mean photons = N
   - Variance = N
   - Standard Deviation (Noise) = sqrt(N)
   - Signal-to-Noise Ratio (SNR) = N / sqrt(N) = sqrt(N)
   This means shot noise is FUNDAMENTAL. You cannot engineer it away.
   To double your SNR, you must collect 4x more photons.

2. OPTICAL DETECTORS
   - Photodiodes: Photovoltaic effect, linear, moderate sensitivity.
   - PMTs (Photomultiplier Tubes): Electron multiplication cascade,
     extremely high gain, excellent for low light.
   - APDs (Avalanche Photodiodes): Semiconductor avalanche effect,
     fast, high sensitivity, compact.
   All are ultimately limited by photon shot noise at high flux.

3. FLUORESCENCE MICROSCOPY & THE FILTER CUBE
   Epi-fluorescence microscopes use three critical optical filters:
   - Excitation Filter: Passes ONLY the wavelength that excites the fluorophore.
   - Dichroic Mirror: Reflects excitation light DOWN to the sample, but
     TRANSMITS longer-wavelength emission light UP to the detector.
   - Emission Filter: Blocks any scattered excitation light, passing ONLY
     the fluorescence signal.
   This spectral separation allows us to see glowing molecules against a
   perfectly dark background.
=============================================================================
'''

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sbn
from scipy.stats import poisson

sbn.set_theme(style="whitegrid")

#--------------------------------------------------------------------------------#
# PLOT 1: PHOTON SHOT NOISE & SNR SCALING
#--------------------------------------------------------------------------------#
fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Left: Poisson Distributions for different mean photon counts
means = [10, 100, 1000]
x_vals = np.arange(0, 1200)
colors = ['blue', 'green', 'red']

for mu, c in zip(means, colors):
    # Scale probability for visualization
    probs = poisson.pmf(x_vals, mu)
    ax1.plot(x_vals, probs, color=c, linewidth=2, label=rf'Mean $N$ = {mu}, $\sigma$ = {np.sqrt(mu):.1f}')

ax1.set_title("Photon Shot Noise: Poisson Statistics", fontsize=14)
ax1.set_xlabel("Detected Photon Count")
ax1.set_ylabel("Probability")
ax1.legend(fontsize=11)
ax1.set_xlim(0, 1100)

# Right: SNR vs Mean Photon Count
N_range = np.logspace(0, 4, 500)
SNR = np.sqrt(N_range)

ax2.loglog(N_range, SNR, color='purple', linewidth=3)
ax2.set_title(r"SNR Scaling: $\text{SNR} = \sqrt{N}$", fontsize=14)
ax2.set_xlabel("Mean Photon Count (N) [Log Scale]")
ax2.set_ylabel("Signal-to-Noise Ratio (SNR) [Log Scale]")
ax2.grid(True, which="both", ls="--", alpha=0.5)

# Annotation
ax2.annotate(r'To double SNR, you need 4x photons!',
             xy=(100, 10), xytext=(200, 25),
             arrowprops=dict(arrowstyle='->', color='darkorange', lw=2),
             fontsize=12, fontweight='bold', color='darkorange')

plt.tight_layout()
plt.show()


#--------------------------------------------------------------------------------#
# PLOT 2: FLUORESCENCE FILTER CUBE SPECTRA
#--------------------------------------------------------------------------------#
lam = np.linspace(400, 700, 1000) # Wavelength in nm

# Simulated Gaussian filter profiles
excitation = np.exp(-0.5 * ((lam - 480) / 10)**2)
emission = np.exp(-0.5 * ((lam - 525) / 15)**2)

# Dichroic mirror: Sharp transition (reflects <500nm, transmits >500nm)
dichroic = 1 / (1 + np.exp(-0.5 * (lam - 500)))

fig2, ax3 = plt.subplots(figsize=(10, 6))

ax3.fill_between(lam, excitation, color='blue', alpha=0.4, label='Excitation Filter (Passes ~480 nm)')
ax3.fill_between(lam, emission, color='green', alpha=0.4, label='Emission Filter (Passes ~525 nm)')
ax3.plot(lam, dichroic, color='red', linewidth=3, linestyle='--', label='Dichroic Mirror (Reflects <500, Transmits >500)')

ax3.set_title("Fluorescence Filter Cube: Spectral Separation", fontsize=16)
ax3.set_xlabel("Wavelength (nm)", fontsize=12)
ax3.set_ylabel("Transmission / Reflection Efficiency", fontsize=12)
ax3.legend(fontsize=11, loc='upper right')
ax3.set_ylim(0, 1.1)
ax3.axvline(500, color='gray', linestyle=':', alpha=0.6)
ax3.text(460, 0.9, 'Excitation Path\n(Reflected DOWN)', ha='center', color='blue', fontweight='bold')
ax3.text(540, 0.9, 'Emission Path\n(Transmitted UP)', ha='center', color='green', fontweight='bold')

plt.tight_layout()
plt.show()

'''
WHAT TO LOOK FOR:
1. SHOT NOISE PLOT:
   - The left plot shows that photon arrival is inherently random. At low
     light (N=10), the distribution is wide relative to the mean. At high
     light (N=1000), it becomes tightly Gaussian, but the absolute noise
     (sigma) still grows as sqrt(N).
   - The right plot proves the professor's point: SNR scales with the
     SQUARE ROOT of photons. This is the fundamental limit of all optical
     detectors (PMTs, APDs, cameras).

2. FLUORESCENCE FILTER PLOT:
   - The blue region is the excitation light. The dichroic mirror (red dashed)
     reflects it downward to hit the sample.
   - The sample fluoresces at a longer wavelength (Stokes Shift), shown in green.
   - The dichroic mirror now TRANSMITS this green light upward.
   - The emission filter blocks any stray blue light, ensuring ONLY the
     green fluorescence reaches the detector. This is the exact light path
     described in the lecture for epi-fluorescence microscopy!
'''
