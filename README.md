# Single-Mode Fiber (SMF) Coupling Simulation
This repository contains a Python script to simulate the coupling of a free-space wavefront into a single-mode fiber (SMF) and analyze the discrepancies between their profiles by spatially dividing their complex fields.The code models the fiber's modal field using the fundamental mode ($LP_{01}$), approximated by a Gaussian function, and calculates the theoretical coupling efficiency based on the overlap integral between the fields.

## Features
* Complex Field Modeling: Represents incident light and the fiber mode as complex electric fields ($E = A \cdot e^{i\phi}$), allowing the inclusion of phase aberrations (e.g., astigmatism, noise).

* Efficiency Calculation ($\eta$): Computes the coupling efficiency using the overlap integral, returning the value as a percentage (%) and the insertion loss in decibels (dB).

* Profile Division: Performs a complex division of the incident wavefront profile by the fiber profile to expose relative amplitude and phase variations.

* Singularity Handling: Implements tolerance limits (epsilon) to prevent division by zero or numerical noise at the Gaussian edges.

* Data Visualization: Generates a plot matrix containing:
    * Amplitude and Phase of the incident beam.
 
    * Amplitude of the fiber's Gaussian mode.
 
    * Resulting Amplitude and Phase maps from the division.
 
    * Numerical summary of the coupling results.
 
## Prerequisites
To run this script, you will need Python installed along with the following libraries:
```
pip install numpy matplotlib
```
## How to use

1. Clone this repository or download the simulacao_fibra.py file.
2. (Optional) Adjust the global parameters at the beginning of the script to fit your needs:
   * GRID_SIZE: Simulation grid resolution (default: 512).
   * PUPIL_RADIUS: Geometric pupil radius in millimeters.
   * W0_FIBER: Fiber Mode Field Radius ($w_0$).
  
3. Run the script in your terminal or favorite IDE:
```
python simulacao_fibra.py
```
