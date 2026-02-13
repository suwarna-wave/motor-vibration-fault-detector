# Motor Vibration Fault Detector
### Predictive Maintenance Mini-Lab (NumPy + FFT)

A lightweight, engineering-focused vibration analysis system that detects early fault patterns in rotating machinery using time-domain statistics and frequency-domain FFT analysis.

---

## 📌 Project Purpose

Rotating machines such as motors, pumps, fans, and industrial equipment naturally produce vibration during operation.

When faults begin to develop — such as imbalance, misalignment, or bearing damage — vibration patterns change in measurable ways.

This project simulates a simplified industrial vibration monitoring system that:

- Analyzes vibration time-series data
- Extracts meaningful signal features
- Detects fault-like patterns
- Produces an interpretable health score (0–100)

No machine learning is used. The system is fully explainable and engineering-driven.

---

## 🎯 Problem Statement

Given vibration sensor data:

Can we determine:
- Whether the machine is healthy?
- If abnormal vibration patterns exist?
- What type of mechanical issue might be developing?

---

## ⚙️ How the System Works

The system analyzes vibration signals in two domains:

### 1️⃣ Time Domain Analysis
Measures overall vibration behavior:
- RMS Energy
- Peak-to-Peak Amplitude
- Kurtosis (impulsive behavior detection)
- Crest Factor

These indicate vibration severity and shock-like behavior.

---

### 2️⃣ Frequency Domain Analysis (FFT)
The Fast Fourier Transform converts the signal into frequency components.

This allows detection of:
- 1× running frequency (imbalance indicator)
- 2× harmonic (misalignment indicator)
- High-frequency energy (bearing-related patterns)

---

## 🧠 Fault Logic (Engineering-Based)

| Fault Type | Typical Indicator |
|------------|-------------------|
| Imbalance | Strong 1× frequency component |
| Misalignment | Strong 2× harmonic component |
| Bearing-like Fault | High kurtosis + high-frequency energy |

---

## ❤️ Health Score (0–100)

The system assigns a deterministic health score:

- Starts at 100
- Deducts points based on:
  - Excessive vibration energy
  - High impulsiveness
  - Abnormal frequency energy distribution
  - Fault pattern detection

Higher score → healthier machine.

---

## 📊 Input Data Format

CSV file containing:

### Preferred Format
```csv
time,accel
0.0000,0.012
0.0005,0.015



MADE with ❤️ by Suwarna-Wave.
