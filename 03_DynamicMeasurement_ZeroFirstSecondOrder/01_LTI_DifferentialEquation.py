'''
=============================================================================
 PART 1: WHY DIFFERENTIAL EQUATIONS? (Modeling Physical "Memory")
=============================================================================
In a perfect mathematical world, if you put a thermometer in boiling water,
it would instantly jump from 20°C to 100°C. But in the real world, physical
systems have "storage elements" (thermal mass, electrical capacitance,
mechanical inertia) that resist sudden changes.

- A thermometer takes time to absorb heat.
- A spring takes time to compress.
- A capacitor takes time to charge.

Differential equations are the mathematical language of "rates of change."
They perfectly capture this physical "memory" or "lag."

1. Zero-Order (No memory):
   y(t) = K * f(t)
   (e.g., a ruler measuring length. Instant response).

2. First-Order (One storage element):
   tau * (dy/dt) + y = K * f(t)
   (e.g., a thermometer. The derivative dy/dt represents the rate of heat absorption).

3. Second-Order (Two storage elements):
   (d^2y/dt^2) + ...
   (e.g., a mass on a spring. It has both inertia and elasticity, leading to oscillations).


=============================================================================
 PART 2: WHY LINEAR MODELS? (The "Logical Bridge" & Superposition)
=============================================================================
Why do we force our models to be Linear and Time-Invariant (LTI)?
Because it unlocks the most powerful shortcut in all of engineering: SUPERPOSITION.

- Linearity: If Input A produces Output A, and Input B produces Output B,
  then Input (A+B) will perfectly produce Output (A+B).

- Time-Invariance: The system's rules don't change over time. If you delay
  the input by 5 seconds, the output is simply delayed by 5 seconds.

--- THE LOGICAL BRIDGE (Connecting Fourier to Systems) ---
Sine waves are "eigenfunctions" of LTI systems.
This is a fancy mathematical way of saying: If you put a sine wave into an LTI system,
a sine wave of the EXACT SAME FREQUENCY comes out.

The system cannot create new frequencies; it can only change the sine wave's:
1. Amplitude (make it bigger/smaller)
2. Phase (shift it left/right in time)

Because Fourier taught us that ANY crazy, complex real-world signal is just a
bunch of sine waves added together, Linearity allows us to do this:

Step 1: Break a complex input signal into simple sine waves (using FFT).
Step 2: Pass each simple sine wave through the system (using the system's Transfer Function).
Step 3: Add the resulting output sine waves back together.

BOOM. You have perfectly predicted how the sensor will react to a highly complex,
messy real-world signal, without having to solve a massive, nightmare-level
differential equation!
'''
