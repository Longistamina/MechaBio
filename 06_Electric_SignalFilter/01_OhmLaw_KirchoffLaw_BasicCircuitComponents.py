'''
=============================================================================
 PART 1: OHM'S LAW, KIRCHHOFF'S LAWS, & BASIC COMPONENTS
=============================================================================
1. THE FLUIDIC ANALOGY (The Professor's Mental Model)
   - Voltage (V): Potential energy difference between two points. Think of
     it as "Water Pressure" or a height difference (gravity).
   - Current (I): The flow rate of electrical charges. Think of it as the
     "Water Flow Rate" through a pipe.
   - Resistance (R): Opposition to the flow. Think of it as a "narrow pipe"
     or debris blocking the water.

2. OHM'S LAW (V = I * R)
   The voltage drop across a resistor is directly proportional to the current
   flowing through it. It is a strictly linear relationship.

3. KIRCHHOFF'S LAWS (The Conservation Laws)
   - KVL (Voltage Law) = CONSERVATION OF ENERGY:
     The sum of all voltage drops around any closed loop must equal zero.
     (The energy provided by the battery is exactly consumed by the components).
   - KCL (Current Law) = CONSERVATION OF CHARGE (MASS):
     The sum of currents entering a node must equal the sum leaving it.
     (Charges cannot magically accumulate or disappear at an intersection).

4. BASIC CIRCUIT COMPONENTS
   - Resistor (R): Dissipates energy as heat. V = I*R.
   - Capacitor (C): Stores energy in an ELECTRIC field (parallel plates).
     It resists sudden changes in VOLTAGE.
     Equation: I = C * (dV/dt). In DC (steady state), it acts as an OPEN circuit.
   - Inductor (L): Stores energy in a MAGNETIC field (coiled wire).
     It resists sudden changes in CURRENT (Faraday's Inductance).
     Equation: V = L * (dI/dt). In DC (steady state), it acts as a SHORT circuit.

5. IDEAL MEASUREMENT DEVICES
   - Ideal Voltmeter: Must have INFINITE internal resistance so it draws
     zero current and doesn't disturb the circuit it is measuring.
   - Ideal Ammeter: Must have ZERO internal resistance so it drops zero
     voltage and doesn't dampen the flow it is trying to measure.
=============================================================================
'''

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sbn

sbn.set_theme(style="darkgrid")

#--------------------------------------------------------------------------------#
# PLOT 1: OHM'S LAW (The Linear Relationship)
#--------------------------------------------------------------------------------#

I = np.linspace(0, 1, 100) # Current from 0 to 1 Amp
R_values = [10, 50, 100]   # Resistances in Ohms

plt.figure(figsize=(10, 5))
for R in R_values:
    V = I * R
    plt.plot(I, V, linewidth=3, label=f'Resistor R = {R} $\Omega$')

plt.title("Ohm's Law: Voltage vs. Current (Linear Relationship)", fontsize=14)
plt.xlabel("Current (I) [Amperes]", fontsize=12)
plt.ylabel("Voltage Drop (V) [Volts]", fontsize=12)
plt.legend(fontsize=11)
plt.tight_layout()
plt.show()


#--------------------------------------------------------------------------------#
# PLOT 2: DYNAMIC BEHAVIOR OF CAPACITORS AND INDUCTORS
#--------------------------------------------------------------------------------#
# To understand WHY capacitors and inductors create "filters" in AC circuits,
# we must look at their derivative relationships in the time domain.
# The professor emphasized that Capacitors resist dV/dt, and Inductors resist dI/dt.

t = np.linspace(0, 4*np.pi, 1000)
omega = 1.0 # Angular frequency

# Input Signal: A Triangle Wave (Linear ramps)
# Using arcsin(sin(wt)) to generate a perfect mathematical triangle wave
V_in = (2/np.pi) * np.arcsin(np.sin(omega * t))
I_in = (2/np.pi) * np.arcsin(np.sin(omega * t))

# Component Values (Set to 1 for easy visual scaling)
C = 1.0 # 1 Farad
L = 1.0 # 1 Henry

# Calculate the time step for numerical derivative
dt = t[1] - t[0]

# CAPACITOR: I_c = C * (dV/dt)
# The derivative of a linear ramp (triangle wave) is a constant (square wave)!
dV_dt = np.gradient(V_in, dt)
I_c = C * dV_dt

# INDUCTOR: V_l = L * (dI/dt)
# The derivative of a linear ramp (triangle wave) is a constant (square wave)!
dI_dt = np.gradient(I_in, dt)
V_l = L * dI_dt

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10), sharex=True)

# Top Plot: Capacitor
ax1.plot(t, V_in, color='blue', linewidth=3, label='Voltage across Capacitor (Triangle Wave)')
ax1.plot(t, I_c, color='red', linewidth=3, linestyle='--', label='Current through Capacitor (Square Wave)')
ax1.set_title(r"Capacitor: Resists changes in VOLTAGE ($I = C \frac{dV}{dt}$)", fontsize=14)
ax1.set_ylabel("Amplitude (V or I)", fontsize=12)
ax1.legend(loc='upper right', fontsize=11)
ax1.axhline(0, color='black', linewidth=1)

# Bottom Plot: Inductor
ax2.plot(t, I_in, color='green', linewidth=3, label='Current through Inductor (Triangle Wave)')
ax2.plot(t, V_l, color='purple', linewidth=3, linestyle='--', label='Voltage across Inductor (Square Wave)')
ax2.set_title(r"Inductor: Resists changes in CURRENT ($V = L \frac{dI}{dt}$)", fontsize=14)
ax2.set_xlabel("Time (t)", fontsize=12)
ax2.set_ylabel("Amplitude (V or I)", fontsize=12)
ax2.legend(loc='upper right', fontsize=11)
ax2.axhline(0, color='black', linewidth=1)

plt.tight_layout()
plt.show()

'''
=============================================================================
 WHAT TO LOOK FOR IN THE PLOTS (Connecting to the Lecture):
=============================================================================
1. OHM'S LAW PLOT:
   Notice the perfectly straight lines. A resistor doesn't care about time
   or frequency. Whether you apply DC or a 1 MHz AC signal, a 100-ohm
   resistor will always oppose the flow with exactly 100 ohms.

2. CAPACITOR & INDUCTOR PLOTS (The Secret to AC Filters):
   - Look at the CAPACITOR (Top): When the voltage is ramping up linearly,
     the current is a FLAT, HIGH constant. When the voltage is flat (at the
     peaks of the triangle wave, dV/dt = 0), the current drops to ZERO.
     This is why capacitors block DC (steady voltage = zero current)!

   - Look at the INDUCTOR (Bottom): When the current is ramping up linearly,
     the voltage spikes to a FLAT, HIGH constant. If you try to change the
     current instantly (infinite dI/dt), the inductor generates an INFINITE
     voltage spike to fight the change. This is why inductors block high-
     frequency AC but pass DC perfectly!

3. THE BRIDGE TO IMPEDANCE (Z):
   Because C and L rely on DERIVATIVES (rates of change), their "effective
   resistance" depends entirely on HOW FAST the signal is changing (Frequency).
   - Fast changing signal (High Frequency) -> Capacitor passes it easily,
     Inductor blocks it.
   - Slow changing signal (Low Frequency) -> Capacitor blocks it,
     Inductor passes it.
   This mathematical derivative relationship is exactly what we will convert
   into "Impedance" ($Z_C = 1/j\omega C$ and $Z_L = j\omega L$) in the next step!
=============================================================================
'''
