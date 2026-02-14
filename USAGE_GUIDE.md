# Motor Vibration Fault Detector - Usage Guide

## 🎯 Complete Build and Execution Guide

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

---

## 📦 Installation Steps

### 1. Setup Python Environment

```bash
# Navigate to project directory
cd motor-vibration-fault-detector

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
# OR
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Verify Installation

```bash
python3 -c "import numpy, matplotlib; print('✅ Dependencies installed')"
```

---

## 🚀 Running the System

### Step 1: Generate Sample Data

```bash
python3 scripts/generate_sample_data.py
```

**Output:**
```
Generated sample vibration CSVs in sample_data/
   - normal.csv
   - imbalance.csv
   - misalignment.csv
   - bearing.csv
```

### Step 2: Run Time-Domain Feature Tests

```bash
python3 scripts/test_time_features.py
```

**Output:** RMS, kurtosis, crest factor for all samples

### Step 3: Complete Diagnostic Analysis

```bash
python3 scripts/analyze_vibration.py
```

**Output:** Full diagnostic reports with:
- Health scores (0-100)
- Detected faults
- Confidence levels
- Maintenance recommendations

### Step 4: Generate Visualizations

```bash
python3 src/visualize.py
```

**Output:** Plots saved to `outputs/`:
- Individual analysis plots (time + frequency domain)
- Comparison grid showing all signals

### Step 5: Run Test Suite

```bash
python3 scripts/run_tests.py
```

**Output:** 22 automated tests validating all functionality

---

## 🔧 System Architecture

### Module Overview

#### 1. **src/features.py**
Time-domain and frequency-domain feature extraction

**Functions:**
- `rms(x)` - Root mean square energy
- `kurtosis(x)` - Impulsive behavior measure
- `crest_factor(x)` - Peak-to-RMS ratio
- `compute_fft(x, fs)` - FFT spectrum
- `extract_fault_indicators(x, fs, running_freq)` - Complete feature set

#### 2. **src/diagnostics.py**
Fault detection and health scoring engine

**Classes:**
- `FaultType` - Fault type enumeration

**Functions:**
- `detect_faults(features)` - Identify fault patterns
- `calculate_health_score(features, fault_type)` - 0-100 health score
- `diagnose_vibration(accel, fs)` - Complete diagnostic pipeline

#### 3. **src/visualize.py**
Plotting and visualization

**Functions:**
- `plot_vibration_analysis()` - Single signal plot
- `plot_all_samples()` - Batch plot generation
- `plot_comparison_grid()` - Multi-signal comparison

#### 4. **src/io_utils.py**
Data loading utilities

**Functions:**
- `load_csv(path)` - Load vibration data from CSV

---

## 📊 Understanding the Results

### Health Score Interpretation

| Score | Status | Action Required |
|-------|--------|-----------------|
| 85-100 | ✅ HEALTHY | Continue routine monitoring |
| 70-84 | ✓ ACCEPTABLE | Increased monitoring recommended |
| 50-69 | ⚠️ WARNING | Plan maintenance soon |
| 0-49 | 🚨 CRITICAL | Immediate attention needed |

### Fault Types

**IMBALANCE**
- **Cause:** Uneven mass distribution on rotor
- **Signature:** Strong 1× frequency component
- **Fix:** Balance rotor assembly

**MISALIGNMENT**
- **Cause:** Shaft/coupling alignment issues
- **Signature:** Strong 2× harmonic
- **Fix:** Realign shafts and couplings

**BEARING FAULT**
- **Cause:** Rolling element or raceway damage
- **Signature:** High kurtosis + high-frequency energy + impulsive spikes
- **Fix:** Replace bearing

### Key Indicators Explained

**RMS Energy**
- Overall vibration severity
- Normal: < 0.3
- Warning: 0.3 - 0.6
- Critical: > 0.6

**Kurtosis**
- Measures impulsiveness (spikes/shocks)
- Normal: ~3
- Warning: 5-8
- Critical: >8

**Crest Factor**
- Peak-to-RMS ratio
- Normal: 3-5
- Warning: 6-8
- Critical: >8

**1× Amplitude**
- Energy at running frequency
- High → Imbalance

**2× Amplitude**
- Energy at 2× running frequency
- High → Misalignment

**HF Energy**
- High-frequency content (>100 Hz)
- High → Bearing issues

---

## 🛠️ Customization

### Analyzing Your Own Data

1. **Prepare CSV file:**
```csv
time,accel
0.0000,0.012
0.0005,0.018
0.0010,0.015
...
```

2. **Run analysis:**
```bash
python3 scripts/analyze_vibration.py path/to/your/data.csv 30.0
```
(where 30.0 is your machine running frequency in Hz)

### Adjusting Sensitivity

Edit [src/diagnostics.py](src/diagnostics.py):

```python
# Make imbalance detection more sensitive
if amp_1x > 0.3:  # Default: 0.4
    detected_faults.append(FaultType.IMBALANCE)

# Make bearing detection less sensitive
if kurtosis_val > 6.0:  # Default: 4.0
    bearing_score += 0.4
```

---

## 🧪 Test Coverage

The test suite (`scripts/run_tests.py`) validates:

1. **Data Loading** (3 tests)
   - CSV parsing
   - Sampling frequency inference
   - Data integrity

2. **Time-Domain Features** (4 tests)
   - RMS accuracy
   - Kurtosis calculation
   - Crest factor
   - Impulsive signal detection

3. **Frequency-Domain Features** (4 tests)
   - FFT correctness
   - Peak detection
   - Spectral energy
   - Multi-frequency signals

4. **Fault Detection** (4 tests)
   - Normal signal classification
   - Imbalance detection
   - Misalignment detection
   - Bearing fault detection

5. **Health Scoring** (4 tests)
   - Score accuracy
   - Status levels
   - Fault-based penalties
   - Edge cases

6. **Edge Cases** (3 tests)
   - Zero signals
   - Constant signals
   - Division by zero handling

**Total: 22 tests - All passing ✅**

---

## 📈 Sample Analysis Workflow

### Example: Analyzing a Motor

1. **Collect Data**
   - Install accelerometer on motor bearing housing
   - Sample at 2000+ Hz for 2-5 seconds
   - Save as CSV with time and acceleration

2. **Determine Running Frequency**
   - Motor speed: 1800 RPM
   - Running frequency: 1800/60 = 30 Hz

3. **Run Analysis**
   ```bash
   python3 scripts/analyze_vibration.py motor_data.csv 30.0
   ```

4. **Interpret Results**
   - Health score < 70? → Schedule inspection
   - High kurtosis (>6)? → Check bearings
   - Strong 1× (>0.4)? → Check balance
   - Strong 2× (>0.3)? → Check alignment

5. **Generate Plot**
   ```python
   from src.visualize import plot_vibration_analysis
   from src.io_utils import load_csv
   
   time, accel, fs = load_csv('motor_data.csv')
   plot_vibration_analysis(time, accel, fs, 
                          title="Motor Analysis",
                          running_freq=30.0,
                          save_path="motor_plot.png")
   ```

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'src'"

**Solution:** Ensure scripts are run from project root:
```bash
cd motor-vibration-fault-detector
python3 scripts/analyze_vibration.py
```

### "Command 'python' not found"

**Solution:** Use `python3` instead:
```bash
python3 scripts/analyze_vibration.py
```

### "No files found in sample_data/"

**Solution:** Generate sample data first:
```bash
python3 scripts/generate_sample_data.py
```

### Virtual environment not activated

**Solution:**
```bash
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

---

## 📚 Additional Resources

### Learning Materials
- FFT basics: [DSP Guide](https://www.dspguide.com/)
- Vibration analysis: ISO 10816 standard
- Python signal processing: SciPy documentation

### Extended Features
For more advanced analysis, consider:
- **scipy.signal** - Advanced filtering, windowing
- **pandas** - Time-series data management
- **scikit-learn** - Machine learning classification
- **plotly** - Interactive visualizations

---

## 🎓 Educational Notes

This system demonstrates:

1. **Signal Processing Fundamentals**
   - Time-domain statistics
   - Fourier transform applications
   - Spectral analysis

2. **Engineering Diagnostics**
   - Rule-based fault detection
   - Domain knowledge application
   - Explainable AI principles

3. **Software Engineering**
   - Modular design
   - Test-driven development
   - Documentation best practices
   - Error handling

4. **Predictive Maintenance**
   - Condition monitoring
   - Fault signature recognition
   - Health scoring methodologies

---

## 🔮 Next Steps

After mastering this system, explore:

1. **Real sensor integration**
   - Arduino/Raspberry Pi data acquisition
   - Real-time processing

2. **Machine learning enhancement**
   - SVM for fault classification
   - Neural networks for pattern recognition

3. **Advanced techniques**
   - Envelope analysis
   - Order tracking
   - Wavelet transforms

4. **Production deployment**
   - Database integration
   - Web dashboard
   - Alerting system

---

**Built with ❤️ for learning and industrial applications**
