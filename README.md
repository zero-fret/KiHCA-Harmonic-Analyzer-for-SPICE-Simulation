# Harmonic Analyzer for SPICE Simulation

A professional harmonic analysis tool designed specifically for analyzing SPICE simulation export data. Based on the least squares method, this tool performs accurate harmonic decomposition of periodic signals and calculates key metrics including harmonic amplitudes, phases, and Total Harmonic Distortion (THD).

## Overview

This software provides a user-friendly graphical interface for engineers and researchers working with SPICE simulations. It automatically identifies time-domain signals from CSV files, performs harmonic analysis at a specified fundamental frequency, and presents results in both tabular and graphical formats.

## Key Features

- CSV Data Import - Supports semicolon-delimited files exported from SPICE simulations
- Precise Harmonic Analysis - Multi-harmonic fitting using least squares algorithm
- Visual Spectrum Display - dB-scale harmonic spectrum with numerical labels on data points
- Comprehensive Metrics - THD, total RMS, relative dB values for each harmonic order
- Large Font Interface - Default 20pt fonts optimized for high-resolution displays
- Real-time Analysis - Immediate recalculation and redrawing when parameters change

## System Requirements

- Python 3.7 or higher
- Operating System: Windows / Linux / macOS
- Dependencies: numpy, matplotlib, tkinter (included with Python)

## Data Format Requirements

The CSV file must follow this format:

- Delimiter: Semicolon (;)
- First row: Column names (must include a time column named "Time" or "time")
- Following rows: Data values (supporting scientific notation)
- Encoding: UTF-8

Example format:
Time;V(out);I(L1)
0.000000e+00;1.234567e-01;2.345678e-03
1.000000e-06;1.234589e-01;2.345701e-03


## How to Use

### Step 1: Load Data
- Click the "Browse" button to select your CSV file
- Click "Load Data" to import the data into the software
- The software will automatically identify the time column and all signal columns

### Step 2: Set Analysis Parameters
- Fundamental Frequency (Hz): Enter the expected fundamental frequency of your signal (e.g., 50, 60, 1000)
- Max Harmonic Order: Set the maximum harmonic order to analyze (default is 20)

### Step 3: Select Signal and Analyze
- Choose the signal to analyze from the dropdown menu
- Click "Analyze & Plot" to perform the harmonic analysis

### Step 4: Review Results
- Text Results Area: Displays detailed numerical results including amplitudes, phases, and THD
- Harmonic Spectrum Area: Shows the dB-scale frequency spectrum with labeled data points

## Understanding the Results

### Output Table
The analysis results include for each harmonic order:
- Order number
- Peak amplitude
- Relative amplitude in dB (referenced to fundamental)
- Phase in radians

### Key Metrics
- Total Harmonic Distortion (THD): Expressed as both percentage and linear value
- Total RMS: Complete RMS value including DC component
- DC Component: Direct current offset of the signal

### dB Scale Convention
- 0 dB corresponds to the fundamental frequency amplitude
- Negative dB values indicate harmonics below the fundamental
- The spectrum plot includes value labels for easy reading

## Application Scenarios

This tool is ideal for analyzing:
- Switch-mode power supply outputs
- Inverter waveforms
- Oscillator circuits
- Audio amplifier distortions
- Any periodic signal from SPICE simulations

## Customization Options

### Adjusting Font Sizes
The software uses large fonts by default for better visibility. The font settings can be modified in the source code:
- GUI_FONT_SIZE: Controls interface text size
- CHART_FONT_SIZE: Controls plot labels and titles

### Visual Appearance
The harmonic spectrum plot can be customized including:
- Color schemes for harmonic markers and lines
- Grid line styles and opacity
- Legend position and appearance
- Marker sizes and edge colors

## Tips for Best Results

- Ensure your simulation data covers at least 2-3 complete cycles of the fundamental frequency
- Use a sampling rate at least 10 times higher than the fundamental frequency
- Verify that the fundamental frequency you enter matches your actual signal frequency
- Remove any DC offset from your signal if you want purely AC analysis
- For best numerical stability, avoid extremely large or small amplitude values

## Troubleshooting

### "Singular matrix in least squares" Error
This typically occurs when:
- The data contains insufficient points for the selected harmonic order
- The fundamental frequency does not match the actual signal
- The time vector is not uniformly sampled

Solutions: Increase simulation time, verify frequency, or reduce the maximum harmonic order.

### "Fundamental amplitude too small" Error
This occurs when the fundamental component amplitude is near zero. Check that:
- Your signal actually contains the specified fundamental frequency
- The signal is not purely DC
- The fundamental frequency value is correct

### CSV Loading Fails
Verify that:
- The file uses semicolon (;) as delimiter (not comma)
- Column names contain no empty strings
- The file encoding is UTF-8
- All rows have consistent column counts

### Poor Harmonic Fitting Results
If the harmonic amplitudes seem inaccurate:
- Ensure your simulation reached steady state
- Increase the number of cycles in your data
- Check for numerical noise in the simulation output
- Verify the fundamental frequency with high precision

## Advanced Topics

### Algorithm Background
The software constructs a linear system where each harmonic contributes both cosine and sine components. The least squares method solves for all coefficients simultaneously, providing optimal fitting even with noisy data.

### Interpretation of Phase Values
Phase angles are calculated relative to the cosine reference. For harmonic k, the signal component is:
A_k * cos(2πkf₀t + φ_k)

Where φ_k is the reported phase in radians.

### Relationship Between Peak and RMS
For sinusoidal components:
- RMS = Peak / √2
- Total RMS combines DC, fundamental, and harmonic RMS values quadratically

## Support and Contributions

For bug reports, feature requests, or questions, please use the GitHub Issues section. Contributions to improve the software are welcome.

## License

This software is released under the GPL License. You are free to use, modify, and distribute it according to the license terms.

---

**Designed for electrical engineers, power electronics specialists, and signal processing researchers who demand precise harmonic analysis from SPICE simulations.**
