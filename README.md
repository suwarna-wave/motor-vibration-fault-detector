# Motor Vibration Fault Detector
### Predictive Maintenance System (NumPy + FFT)

A production-ready vibration analysis system that detects mechanical faults in rotating machinery using engineering-based signal processing.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![NumPy](https://img.shields.io/badge/NumPy-Powered-orange.svg)
![Tests](https://img.shields.io/badge/Tests-22/22_Passing-green.svg)

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Generate sample data
python3 scripts/generate_sample_data.py

# 3. Run analysis
python3 scripts/analyze_vibration.py

# 4. Generate visualizations
python3 src/visualize.py

# 5. Run tests
python3 scripts/run_tests.py
```

---

## 📊 System Capabilities

✅ **Time-Domain Analysis** - RMS, kurtosis, crest factor, peak-to-peak  
✅ **Frequency-Domain Analysis** - FFT, spectral energy, peak detection  
✅ **Fault Detection** - Imbalance, misalignment, bearing faults  
✅ **Health Scoring** - 0-100 score with status levels  
✅ **Automated Reporting** - Detailed diagnostics with recommendations  
✅ **Visualization** - Time & frequency domain plots  
✅ **Comprehensive Testing** - 22 automated tests  

---

## 🎯 What It Does

Analyzes vibration sensor data to detect mechanical faults:

| Fault Type | Detection Method | Key Indicators |
|------------|------------------|----------------|
| **Imbalance** | Strong 1× frequency | Uneven rotor mass |
| **Misalignment** | Strong 2× harmonic | Shaft alignment issues |
| **Bearing Fault** | High kurtosis + HF energy | Impulsive spikes |

---

## 📁 Project Structure

```
motor-vibration-fault-detector/
├── src/
│   ├── features.py        # Time & frequency domain features
│   ├── diagnostics.py     # Fault detection & health scoring
│   ├── visualize.py       # Plotting capabilities
│   └── io_utils.py        # Data loading
├── scripts/
│   ├── analyze_vibration.py      # Main analysis script
│   ├── generate_sample_data.py   # Generate test data
│   └── run_tests.py              # Test suite
├── sample_data/          # Generated CSV files
└── outputs/              # Analysis plots
```

---

## 🔬 Technical Details

### Feature Extraction

```python
from src.features import extract_fault_indicators

features = extract_fault_indicators(accel, fs=2000, running_freq=30.0)
# Returns: RMS, kurtosis, 1× amplitude, 2× amplitude, HF energy, etc.
```

### Complete Diagnostics

```python
from src.diagnostics import diagnose_vibration

report = diagnose_vibration(accel, fs=2000, running_freq=30.0)
print(f"Health: {report['health_score']}/100")
print(f"Fault: {report['primary_fault']}")
```

---

## 📈 Example Results

```
🚨 HEALTH SCORE: 30/100 (CRITICAL)
🔍 PRIMARY FAULT: BEARING
📈 KEY INDICATORS:
   Kurtosis:        36.85  ← Highly impulsive
   Crest Factor:    12.42  ← Shock impacts
   HF Energy:       0.049  ← Elevated

💡 RECOMMENDATIONS:
   ⚠ Bearing fault indicators present
   🚨 CRITICAL: Schedule immediate maintenance
```

---

## 🧪 Validation

All 22 tests passing:
- ✅ Feature calculation accuracy
- ✅ Fault detection logic
- ✅ Health score correctness
- ✅ Edge case handling

---

## 🎓 Learning Resources

This project demonstrates:
- Signal processing with FFT
- Engineering-based diagnostics
- Test-driven development
- Modular software design

---

**MADE with ❤️ by Suwarna-Wave**
