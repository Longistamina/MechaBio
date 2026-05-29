'''
=============================================================================
 FOURIER OPTICS & SPATIAL FILTERING
=============================================================================
1. THE LENS AS A FOURIER TRANSFORMER
   The professor stated: "Images from the optical system can be viewed as a
   Fourier transform." In Fourier optics, a lens naturally computes the 2D
   spatial Fourier Transform of the light field at its front focal plane.
   The back focal plane becomes the "Frequency Domain" of the image.

2. APERTURE -> POINT SPREAD FUNCTION (PSF)
   When light passes through an aperture, the diffraction pattern formed
   is mathematically the Fourier Transform of the aperture shape.
   - Square Aperture -> FT -> 2D Sinc Function
   - Circular Aperture -> FT -> Airy Disk (J1/x pattern)
   This diffraction pattern IS the Point Spread Function (PSF) of the system.

3. SPATIAL FREQUENCY & LOW-PASS FILTERING
   Sharp edges and fine details in an image correspond to HIGH spatial
   frequencies. The finite size of a lens aperture acts as a natural
   LOW-PASS FILTER, blocking high spatial frequencies. This is why all
   optical systems have a fundamental resolution limit (diffraction limit).
   Blocking high frequencies = blurring the image = sinc-shaped PSF.
=============================================================================
'''

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sbn

sbn.set_theme(style="whitegrid")


#--------------------------------------------------------------------------------#
# 1. CREATE APERTURES (Spatial Domain)
#--------------------------------------------------------------------------------#
N = 256
x = np.linspace(-1, 1, N)
X, Y = np.meshgrid(x, x)

# Square Aperture
square_aperture = np.zeros((N, N))
square_aperture[(np.abs(X) < 0.2) & (np.abs(Y) < 0.2)] = 1.0

# Circular Aperture
r = np.sqrt(X**2 + Y**2)
circular_aperture = (r < 0.2).astype(float)

#--------------------------------------------------------------------------------#
# 2. COMPUTE FOURIER TRANSFORMS (Frequency / Focal Plane Domain)
#--------------------------------------------------------------------------------#
# 2D FFT -> Shift zero frequency to center -> Take magnitude -> Log scale for visibility
def compute_psf(aperture):
    ft = np.fft.fft2(aperture)
    ft_shifted = np.fft.fftshift(ft)
    psf = np.abs(ft_shifted)**2
    return np.log1p(psf) # log(1+x) to compress dynamic range

psf_square = compute_psf(square_aperture)
psf_circular = compute_psf(circular_aperture)

#--------------------------------------------------------------------------------#
# 3. PLOT RESULTS
#--------------------------------------------------------------------------------#
fig, axes = plt.subplots(2, 3, figsize=(15, 10))

# Row 1: Square Aperture
axes[0, 0].imshow(square_aperture, cmap='gray', extent=[-1,1,-1,1])
axes[0, 0].set_title("Square Aperture\n(Spatial Domain)", fontsize=12)
axes[0, 0].axis('off')

axes[0, 1].imshow(psf_square, cmap='inferno', extent=[-1,1,-1,1])
axes[0, 1].set_title(r"FT of Square $\rightarrow$ 2D Sinc PSF", fontsize=12)
axes[0, 1].axis('off')

# Cross-section of the Sinc PSF
center_line = psf_square[N//2, :]
axes[0, 2].plot(np.linspace(-1, 1, N), center_line, color='red', linewidth=2)
axes[0, 2].set_title("Cross-Section: Sinc² Profile", fontsize=12)
axes[0, 2].set_xlabel("Spatial Frequency")
axes[0, 2].set_ylabel("Intensity")

# Row 2: Circular Aperture
axes[1, 0].imshow(circular_aperture, cmap='gray', extent=[-1,1,-1,1])
axes[1, 0].set_title("Circular Aperture\n(Spatial Domain)", fontsize=12)
axes[1, 0].axis('off')

axes[1, 1].imshow(psf_circular, cmap='inferno', extent=[-1,1,-1,1])
axes[1, 1].set_title(r"FT of Circle $\rightarrow$ Airy Disk PSF", fontsize=12)
axes[1, 1].axis('off')

center_line_circ = psf_circular[N//2, :]
axes[1, 2].plot(np.linspace(-1, 1, N), center_line_circ, color='blue', linewidth=2)
axes[1, 2].set_title("Cross-Section: Airy Pattern", fontsize=12)
axes[1, 2].set_xlabel("Spatial Frequency")
axes[1, 2].set_ylabel("Intensity")

plt.suptitle("Fourier Optics: Aperture Shape Dictates the PSF via Fourier Transform", fontsize=16, y=1.02)
plt.tight_layout()
plt.show()

'''
WHAT TO LOOK FOR:
- The professor explicitly linked the square aperture to the sinc function:
  "Fourier transform of this will become a sinc function." The top row
  proves this mathematically. The 2D FFT of a square box is a 2D sinc.
- The bottom row shows the circular aperture, which creates the famous
  "Airy Disk" pattern. This is the fundamental PSF of almost all microscope
  objectives.
- The finite width of the central peak in the PSF represents the
  DIFFRACTION LIMIT. You cannot resolve two points closer than the width
  of this central lobe. This is the physical origin of optical resolution limits!
'''
