# Motor Vibration Fault Detector (FFT + Health Score)

A lightweight, engineering-focused **predictive maintenance mini-lab** built using **NumPy**.  
The project analyzes vibration time-series data from rotating machinery and produces an **interpretable health score (0–100)** along with **fault-type indicators** using time-domain statistics and FFT-based frequency analysis.

---

## 🚀 Why this project?

Vibration-based condition monitoring is widely used in:
- Manufacturing plants
- Robotics and automation
- Water pumps and HVAC systems
- Vehicle engines and rotating equipment

This project demonstrates how **signal processing fundamentals** can be used to detect early fault patterns **without heavy machine learning**.

---

## 🔍 What does it do?

Given vibration data (CSV):

- Computes time-domain features (RMS, peak-to-peak, kurtosis, crest factor)
- Performs FFT to extract dominant frequencies
- Estimates rotating speed (1× frequency)
- Detects fault-like patterns:
  - **Imbalance**
  - **Misalignment**
  - **Bearing-like faults**
- Generates:
  - Health score (0–100)
  - Fault flags
  - Frequency report
  - FFT plots

---

## 📁 Project Structure

motor-vibration-fault-detector/
├── README.md
├── requirements.txt
├── src/ # Core feature extraction & logic
├── notebooks/ # Analysis & reporting notebook
├── sample_data/ # Example vibration CSV files
├── scripts/ # Data generation utilities
└── outputs/ # Generated reports & plots (ignored in git)


