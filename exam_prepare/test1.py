'''
======================================================================
 MECHANICAL AND BIOLOGICAL INSTRUMENTATION: COMPREHENSIVE MOCK EXAM
======================================================================
Time Limit: 90 Minutes | Total Points: 100
Coverage: Basic Measurements, Statistics, Signal Analysis, Diffusion,
Mechanical Sensors, Electronics, Optics, and Single-Cell Analysis.

======================================================================
 PART I: MULTIPLE CHOICE & CONCEPTUAL "TRICK" QUESTIONS (3 Pts Each)
======================================================================

1. Experimental Design: Replication vs. Repetition
You are measuring the stiffness of HeLa cells.
- Experiment A: You measure the exact same cell 10 times in a row.
- Experiment B: You measure 10 different cells from the same flask once each.
Which correctly identifies these actions and the type of noise they break up?
A) A is Replication (breaks sample noise); B is Repetition (breaks measurement noise)
B) A is Repetition (breaks measurement noise); B is Replication (breaks sample noise)
C) Both are Replications (breaks extraneous variable trends)
D) Both are Repetitions (breaks systematic errors)

2. Statistics: The Central Limit Theorem
You are estimating the mean diameter of a population of microbeads. If you
increase your sample size (N) by a factor of 4, what happens to the Standard
Error of the Mean (the standard deviation of the sample means)?
A) It decreases by a factor of 4.
B) It decreases by a factor of 2.
C) It remains unchanged, but the population variance decreases.
D) It increases by a factor of 2.

3. Signal Analysis: Aliasing
A true biological signal (e.g., a beating heart cell) oscillates at 8 Hz.
Your data acquisition board is incorrectly set to sample at 11 Hz. According
to the Nyquist theorem and aliasing mathematics, what "fake" frequency will
your FFT incorrectly report?
A) 19 Hz
B) 8 Hz
C) 3 Hz
D) 0.5 Hz

4. Signal Analysis: DFT Limitations
You perform an FFT on a 5.5 Hz sine wave sampled for exactly 1 second. You
notice the energy is smeared across multiple frequency bins instead of forming
a single sharp peak. What is this phenomenon called, and what computational
technique can visually smooth the spectrum *without* adding new physical info?
A) Aliasing; Anti-aliasing filter
B) Spectral Leakage; Zero Padding
C) Spectral Leakage; Windowing
D) Impulse Train; Convolution

5. Diffusion & Dimensional Analysis
Using dimensional analysis, the net flow rate of molecules through a tiny
membrane pore scales with the pore's radius (a^1) rather than its area (a^2).
What physical phenomenon causes this counter-intuitive scaling?
A) The Einstein-Stokes drag coefficient
B) The Peclet Number advection limit
C) The formation of a local concentration depletion zone around the pore
D) The Gaussian variance of Fick's Second Law

6. Mechanical Sensors: Euler-Bernoulli Scaling
You are designing a rectangular cantilever beam for an AFM. If you double the
WIDTH (depth) of the cantilever while keeping the thickness (height) and
length the same, what happens to its fundamental resonant frequency?
A) It doubles.
B) It quadruples.
C) It decreases by half.
D) It remains completely unchanged.

7. Mechanical Sensors: The SMR Innovation
Traditional cantilevers submerged in liquid suffer from a massive drop in
their Q-factor (by ~65 times), destroying their mass sensitivity. How does
the Suspended Microchannel Resonator (SMR) solve this problem to achieve
femtogram resolution?
A) It uses magnetic tweezers to artificially increase the spring constant k.
B) It flows the fluid *inside* a hollow cantilever while the outside vibrates in a vacuum.
C) It cools the liquid to near absolute zero to eliminate Johnson noise.
D) It operates in static mode rather than dynamic mode.

8. Basic Electronics: The Hall Effect "Trick"
In a Hall effect sensor, conventional current flows to the right (+x), and
the magnetic field points out of the page (+z). In which direction are the
PHYSICAL ELECTRONS pushed by the Lorentz force?
A) Upwards (+y)
B) Downwards (-y)
C) Into the page (-z)
D) To the left (-x)

9. Electronics: Active vs. Passive Filters
Why are Active Filters (using Op-Amps, like the Sallen-Key topology) generally
preferred over higher-order Passive Filters for miniaturized biosensor boards?
A) Active filters do not require an external power supply.
B) Passive filters cannot block 60 Hz power-line noise.
C) Active filters avoid the need for bulky inductors and can simultaneously amplify the passband signal.
D) Passive filters inherently introduce aliasing.

10. Optics: Fourier Optics & Resolution
In Fourier optics, the finite circular aperture of a microscope objective acts
as what type of filter on the spatial frequencies of an image, ultimately
resulting in the Airy Disk (Point Spread Function)?
A) High-pass filter
B) Band-stop filter
C) Low-pass filter
D) Notch filter

11. Optics: Fluorescence Filter Cubes
In an epi-fluorescence microscope, what is the specific function of the
DICHROIC MIRROR?
A) It blocks all light except the exact emission wavelength of the fluorophore.
B) It reflects the shorter-wavelength excitation light down to the sample, but transmits the longer-wavelength emission light up to the detector.
C) It polarizes the light to increase the contrast of the cell membrane.
D) It acts as a lens to focus the laser onto a single molecule.

12. Photonics: Shot Noise & SNR
Due to the Poisson statistics of photon arrival (Shot Noise), if you want to
DOUBLE your Signal-to-Noise Ratio (SNR), by what factor must you increase the
number of collected photons (or the measurement integration time)?
A) Factor of sqrt(2) (1.41x)
B) Factor of 2
C) Factor of 4
D) Factor of 8


======================================================================
 PART II: SHORT ANSWER & CONCEPTUAL PROOFS (10 Points Each)
======================================================================

13. Control Systems:
A Proportional (P) controller is used to maintain a microfluidic incubator
at 37°C. However, the system consistently stabilizes at 36.2°C. What is this
error called, and what specific type of controller must be added to the
feedback loop to eliminate it completely?

14. Electronics (Op-Amps):
State the TWO "Golden Rules" of an ideal Operational Amplifier (Op-Amp) when
it is placed in a negative feedback configuration.

15. Biosensors & Transducers:
Briefly contrast the physical mechanism of a Photomultiplier Tube (PMT) with
a standard Photodiode. Which effect (Photoelectric or Photovoltaic) governs
each?

16. Single-Cell Analysis:
Single-cell RNA sequencing (scRNA-seq) is incredibly powerful for
transcriptomics. However, the professor highlighted distinct advantages to
measuring single-cell BIOPHYSICAL properties (like mass via SMR or stiffness
via AFM). List two major advantages of biophysical phenotyping over scRNA-seq.

17. Bionumber Estimation (Back-of-the-Envelope):
A typical mammalian cell has a mass of roughly 1 nanogram. DNA accounts for
approximately 0.6% of the total cell mass.
Question: Without looking it up, estimate the mass of the DNA inside a single
cell in picograms (pg). Based on this, if a single base pair has a mass of
~10^-21 grams, what is the rough order of magnitude for the number of base
pairs in the genome?


======================================================================
 (STOP SCROLLING HERE IF YOU ARE TAKING THE TEST!)
 ANSWER KEY & EXPLANATIONS BELOW
======================================================================


======================================================================
 ANSWER KEY & EXPLANATIONS
======================================================================

1. B
Explanation: Repetition is measuring the *same* sample multiple times (breaks
measurement/instrument noise). Replication is measuring *different* biological
samples (breaks sample-to-sample biological noise).

2. B
Explanation: The Standard Error of the Mean is defined as σ / sqrt(N). If N
increases by a factor of 4, the denominator becomes sqrt(4N) = 2*sqrt(N).
Therefore, the standard error decreases by a factor of 2.

3. C
Explanation: Aliasing occurs when fs < 2*fmax. The aliased frequency folds
back and is calculated as |f_true - f_s| (or integer multiples).
|8 Hz - 11 Hz| = |-3| = 3 Hz.

4. B
Explanation: Because 5.5 cycles do not fit perfectly into the 1-second window,
the DFT's assumption of infinite periodicity creates a discontinuity at the
edges, causing Spectral Leakage. Zero Padding adds zeros to the end of the
time signal, which interpolates the frequency bins, making the leakage curve
look smooth and continuous, though it does not increase true physical resolution.

5. C
Explanation: The professor's dimensional analysis poll proved flow scales with
a^1. The physical reason is the local depletion zone. Molecules are absorbed
so fast at the pore that the concentration right at the hole drops to zero,
creating a 3D "funnel" bottleneck that limits uptake based on the radius of
the depletion sphere, not the 2D area of the hole.

6. D
Explanation: According to Euler-Bernoulli beam theory, the resonant frequency
ωn is proportional to the thickness/height (h), but is completely independent
of the width/depth (d). Adding width adds stiffness (I ∝ d), but it adds an
exactly proportional amount of mass (A ∝ d), so the two effects cancel out.

7. B
Explanation: Fluid drag destroys the Q-factor. The SMR bypasses this by making
the cantilever hollow. The cells flow *inside* the microchannel, while the
exterior of the cantilever vibrates in a strict vacuum, preserving a Q-factor
of ~1000+ and enabling femtogram mass sensing.

8. B
Explanation: The professor's classic trick question! Conventional current flows
Right (+x), meaning physical electrons (negative charge) move Left (-x).
Velocity v is -x. Magnetic field B is +z. The cross product v x B is
(-x) x (+z) = +y (Up). However, because the electron charge q is negative,
the Lorentz force F = q(v x B) flips direction to -y (Downwards).

9. C
Explanation: Passive higher-order filters require Inductors (L), which are
bulky copper coils that cannot be miniaturized onto silicon chips. Active
filters use Op-Amps, Resistors, and Capacitors to achieve sharp roll-offs
(e.g., -40 dB/decade) while simultaneously providing gain (amplification).

10. C
Explanation: In Fourier optics, a finite aperture blocks the highest angle
light rays (which correspond to high spatial frequencies/fine details).
Therefore, the aperture acts as a Low-Pass Filter, resulting in the blurring
of a perfect point source into an Airy Disk.

11. B
Explanation: The dichroic mirror is angled at 45 degrees. It is designed to
reflect short wavelengths (excitation light) down toward the objective/sample,
but transmit longer wavelengths (Stokes-shifted emission light) straight up
into the detector.

12. C
Explanation: Photon shot noise follows Poisson statistics, where Noise = sqrt(N)
and Signal = N. Therefore, SNR = N / sqrt(N) = sqrt(N). To double the SNR
(2 * sqrt(N)), you must increase the number of photons N by a factor of 4
(since sqrt(4N) = 2*sqrt(N)).

13. Steady-State Error; Integral (I) Control
Explanation: A Proportional controller requires an error to generate a driving
force, leading to a permanent offset called steady-state error. Adding an
Integral controller accumulates the error over time and continuously drives
the actuator until the error is exactly zero.

14. The Two Golden Rules:
1. Infinite Input Impedance: No current flows *into* the input pins (I+ = I- = 0).
2. Virtual Short (Negative Feedback): The Op-Amp adjusts its output to force
the voltage difference between the two inputs to be exactly zero (V+ = V-).

15. Photoelectric vs. Photovoltaic:
- PMT: Uses the Photoelectric effect. Photons physically eject electrons out
of a metal cathode into a vacuum, which are then multiplied via a dynode
cascade (high internal gain, great for single-photon/low-light).
- Photodiode: Uses the Photovoltaic effect. Photons excite electron-hole pairs
*inside* a semiconductor material, generating a current within the solid state
(no internal gain, used for brighter signals).

16. Biophysical Phenotyping Advantages:
1. Label-free & Non-invasive: Does not require fluorescent tags, antibodies,
or lysing the cell (keeps the cell alive).
2. Real-time Dynamics: Can track rapid, asynchronous, and continuous changes
(like cell growth or mass accumulation) over time, whereas scRNA-seq is
typically an endpoint "snapshot" that destroys the cell.

17. Bionumber Estimation:
- DNA Mass: 1 ng = 1000 pg. 0.6% of 1000 pg is roughly 6 picograms.
- Base Pairs: 6 pg = 6 x 10^-12 grams. Divide by mass per base pair (10^-21 g/bp):
(6 x 10^-12) / (10^-21) = 6 x 10^9.
The genome size is on the order of billions (10^9) of base pairs. (This
matches the professor's exact back-of-the-envelope calculation from Lecture 04!)

======================================================================
 GOOD LUCK ON YOUR EXAM!
======================================================================
'''
