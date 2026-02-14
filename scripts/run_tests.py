"""
Comprehensive Test Suite for Motor Vibration Fault Detector
Tests all core functionality and validates fault detection logic
"""
import sys
from pathlib import Path
import numpy as np

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.features import (
    rms, peak_to_peak, kurtosis, crest_factor,
    compute_fft, spectral_energy, peak_frequency_amplitude,
    extract_fault_indicators
)
from src.diagnostics import (
    detect_faults, calculate_health_score, diagnose_vibration,
    FaultType
)
from src.io_utils import load_csv


class TestResults:
    """Track test results"""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []
    
    def add_test(self, name: str, passed: bool, message: str = ""):
        self.tests.append((name, passed, message))
        if passed:
            self.passed += 1
        else:
            self.failed += 1
    
    def print_summary(self):
        print("\n" + "="*70)
        print("TEST SUMMARY")
        print("="*70)
        for name, passed, message in self.tests:
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"{status} - {name}")
            if message and not passed:
                print(f"        {message}")
        
        print("="*70)
        print(f"Total: {self.passed + self.failed} | Passed: {self.passed} | Failed: {self.failed}")
        if self.failed == 0:
            print("✅ ALL TESTS PASSED!")
        else:
            print(f"❌ {self.failed} TEST(S) FAILED")
        print("="*70)


def test_time_domain_features(results: TestResults):
    """Test time-domain feature extraction"""
    print("\n📊 Testing Time-Domain Features...")
    
    # Test data: simple sine wave
    t = np.linspace(0, 1, 1000)
    x = np.sin(2 * np.pi * 10 * t)  # 10 Hz sine
    
    # RMS test
    rms_val = rms(x)
    expected_rms = 1 / np.sqrt(2)  # 0.707 for unit sine
    results.add_test(
        "RMS calculation",
        abs(rms_val - expected_rms) < 0.01,
        f"Expected ~{expected_rms:.3f}, got {rms_val:.3f}"
    )
    
    # Peak-to-peak test
    p2p = peak_to_peak(x)
    results.add_test(
        "Peak-to-Peak calculation",
        abs(p2p - 2.0) < 0.01,
        f"Expected ~2.0, got {p2p:.3f}"
    )
    
    # Kurtosis test (sine wave should have kurtosis ~1.5)
    kurt = kurtosis(x)
    results.add_test(
        "Kurtosis calculation",
        1.0 < kurt < 2.0,
        f"Expected ~1.5, got {kurt:.3f}"
    )
    
    # Test with impulsive signal
    x_impulsive = np.zeros(1000)
    x_impulsive[500] = 10.0  # Single spike
    kurt_impulsive = kurtosis(x_impulsive)
    results.add_test(
        "Kurtosis detects impulsive signal",
        kurt_impulsive > 10,
        f"Expected >10, got {kurt_impulsive:.3f}"
    )


def test_frequency_domain_features(results: TestResults):
    """Test FFT and frequency-domain analysis"""
    print("\n📊 Testing Frequency-Domain Features...")
    
    # Generate test signal: 10 Hz + 20 Hz components
    fs = 1000  # 1 kHz sampling
    t = np.linspace(0, 2, 2*fs)
    x = np.sin(2*np.pi*10*t) + 0.5*np.sin(2*np.pi*20*t)
    
    # Compute FFT
    freqs, mags = compute_fft(x, fs)
    
    # Test FFT output shape
    results.add_test(
        "FFT output shapes match",
        len(freqs) == len(mags),
        f"Freqs: {len(freqs)}, Mags: {len(mags)}"
    )
    
    # Test peak detection at 10 Hz
    peak_10hz = peak_frequency_amplitude(freqs, mags, 10.0, bandwidth=2.0)
    results.add_test(
        "FFT detects 10 Hz component",
        peak_10hz > 0.8,
        f"Expected >0.8, got {peak_10hz:.3f}"
    )
    
    # Test peak detection at 20 Hz
    peak_20hz = peak_frequency_amplitude(freqs, mags, 20.0, bandwidth=2.0)
    results.add_test(
        "FFT detects 20 Hz component",
        peak_20hz > 0.4,
        f"Expected >0.4, got {peak_20hz:.3f}"
    )
    
    # Test spectral energy
    total_energy = spectral_energy(freqs, mags, 0, fs/2)
    results.add_test(
        "Spectral energy is positive",
        total_energy > 0,
        f"Got {total_energy:.3f}"
    )


def test_fault_detection(results: TestResults):
    """Test fault detection logic on sample data"""
    print("\n📊 Testing Fault Detection...")
    
    # Test on normal signal
    time, accel, fs = load_csv("sample_data/normal.csv")
    features = extract_fault_indicators(accel, fs, running_freq=30.0)
    fault, fault_list, conf = detect_faults(features, running_freq=30.0)
    
    results.add_test(
        "Normal signal detected as NORMAL",
        fault == FaultType.NORMAL,
        f"Detected as {fault}"
    )
    
    # Test on imbalance signal
    time, accel, fs = load_csv("sample_data/imbalance.csv")
    features = extract_fault_indicators(accel, fs, running_freq=30.0)
    fault, fault_list, conf = detect_faults(features, running_freq=30.0)
    
    results.add_test(
        "Imbalance signal detected",
        FaultType.IMBALANCE in fault_list,
        f"Detected: {fault_list}"
    )
    
    # Test on misalignment signal
    time, accel, fs = load_csv("sample_data/misalignment.csv")
    features = extract_fault_indicators(accel, fs, running_freq=30.0)
    fault, fault_list, conf = detect_faults(features, running_freq=30.0)
    
    results.add_test(
        "Misalignment signal detected",
        FaultType.MISALIGNMENT in fault_list,
        f"Detected: {fault_list}"
    )
    
    # Test on bearing fault signal
    time, accel, fs = load_csv("sample_data/bearing.csv")
    features = extract_fault_indicators(accel, fs, running_freq=30.0)
    fault, fault_list, conf = detect_faults(features, running_freq=30.0)
    
    results.add_test(
        "Bearing fault detected",
        FaultType.BEARING in fault_list,
        f"Detected: {fault_list}"
    )


def test_health_scoring(results: TestResults):
    """Test health score calculation"""
    print("\n📊 Testing Health Scoring...")
    
    # Normal signal should have high health score
    time, accel, fs = load_csv("sample_data/normal.csv")
    report = diagnose_vibration(accel, fs, running_freq=30.0)
    
    results.add_test(
        "Normal signal has high health score",
        report['health_score'] >= 85,
        f"Score: {report['health_score']}"
    )
    
    results.add_test(
        "Normal signal status is HEALTHY",
        report['status'] == "HEALTHY",
        f"Status: {report['status']}"
    )
    
    # Bearing fault should have low health score
    time, accel, fs = load_csv("sample_data/bearing.csv")
    report = diagnose_vibration(accel, fs, running_freq=30.0)
    
    results.add_test(
        "Bearing fault has low health score",
        report['health_score'] < 50,
        f"Score: {report['health_score']}"
    )
    
    results.add_test(
        "Bearing fault status is WARNING or CRITICAL",
        report['status'] in ["WARNING", "CRITICAL"],
        f"Status: {report['status']}"
    )


def test_data_loading(results: TestResults):
    """Test CSV data loading functionality"""
    print("\n📊 Testing Data Loading...")
    
    # Test loading sample data
    try:
        time, accel, fs = load_csv("sample_data/normal.csv")
        
        results.add_test(
            "CSV loads successfully",
            time is not None and accel is not None,
            ""
        )
        
        results.add_test(
            "Sampling frequency inferred correctly",
            fs is not None and fs > 0,
            f"fs = {fs}"
        )
        
        results.add_test(
            "Data arrays have correct shape",
            len(time) == len(accel) and len(time) > 0,
            f"time: {len(time)}, accel: {len(accel)}"
        )
        
    except Exception as e:
        results.add_test(
            "CSV loads successfully",
            False,
            str(e)
        )


def test_edge_cases(results: TestResults):
    """Test edge cases and error handling"""
    print("\n📊 Testing Edge Cases...")
    
    # Zero signal
    x_zero = np.zeros(100)
    results.add_test(
        "RMS of zero signal is zero",
        rms(x_zero) == 0.0,
        ""
    )
    
    results.add_test(
        "Crest factor of zero signal is zero",
        crest_factor(x_zero) == 0.0,
        ""
    )
    
    # Constant signal
    x_const = np.ones(100) * 5.0
    kurt_const = kurtosis(x_const)
    results.add_test(
        "Kurtosis of constant signal is zero",
        kurt_const == 0.0,
        f"Got {kurt_const}"
    )


def run_all_tests():
    """Run complete test suite"""
    print("="*70)
    print("🧪 MOTOR VIBRATION FAULT DETECTOR - TEST SUITE")
    print("="*70)
    
    results = TestResults()
    
    # Run all test groups
    test_data_loading(results)
    test_time_domain_features(results)
    test_frequency_domain_features(results)
    test_fault_detection(results)
    test_health_scoring(results)
    test_edge_cases(results)
    
    # Print summary
    results.print_summary()
    
    return results.failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
