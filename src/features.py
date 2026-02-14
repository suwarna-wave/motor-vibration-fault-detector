import numpy as np
from typing import Tuple, Dict

# ==================== TIME-DOMAIN FEATURES ====================

def rms(x: np.ndarray) -> float:
    """
    Root Mean Square - Overall vibration energy
    Higher RMS => more vibration severity
    """
    x = np.asarray(x, dtype=float)
    return float(np.sqrt(np.mean(x**2)))

def peak_to_peak(x: np.ndarray) -> float:
    """
    Peak-to-Peak amplitude - Range of vibration
    """
    x = np.asarray(x, dtype=float)
    return float(np.max(x) - np.min(x))

def kurtosis(x: np.ndarray) -> float:
    """
    Kurtosis: E[((x-mu)/sigma)^4]
    Normal-ish signal ~ around 3.
    Higher => more impulsive shocks (bearing faults)
    """
    x = np.asarray(x, dtype=float)
    mu = np.mean(x)
    sigma = np.std(x)
    if sigma == 0:
        return 0.0
    z = (x - mu) / sigma
    return float(np.mean(z**4))

def crest_factor(x: np.ndarray) -> float:
    """
    Crest Factor = Peak / RMS
    Higher => more impulsive/shock behavior
    Typical: 3-5 for normal, >6 for faults
    """
    x = np.asarray(x, dtype=float)
    r = rms(x)
    if r == 0:
        return 0.0
    return float(np.max(np.abs(x)) / r)

# ==================== FREQUENCY-DOMAIN FEATURES ====================

def compute_fft(x: np.ndarray, fs: float) -> Tuple[np.ndarray, np.ndarray]:
    """
    Compute FFT spectrum (one-sided, positive frequencies only)
    
    Returns:
        freqs: frequency bins (Hz)
        mags: magnitude spectrum
    """
    x = np.asarray(x, dtype=float)
    N = len(x)
    
    # FFT with normalization
    fft_vals = np.fft.rfft(x)
    freqs = np.fft.rfftfreq(N, d=1/fs)
    
    # Magnitude spectrum (normalized)
    mags = np.abs(fft_vals) * (2.0 / N)
    
    return freqs, mags

def spectral_energy(freqs: np.ndarray, mags: np.ndarray, 
                   f_low: float, f_high: float) -> float:
    """
    Total spectral energy in a frequency band [f_low, f_high]
    """
    mask = (freqs >= f_low) & (freqs <= f_high)
    return float(np.sum(mags[mask]**2))

def peak_frequency_amplitude(freqs: np.ndarray, mags: np.ndarray,
                             f_center: float, bandwidth: float = 2.0) -> float:
    """
    Find peak amplitude around a target frequency
    Used to detect specific fault frequencies (1×, 2×, etc.)
    
    Args:
        f_center: center frequency to search around
        bandwidth: ±Hz range to search
    """
    f_low = f_center - bandwidth
    f_high = f_center + bandwidth
    mask = (freqs >= f_low) & (freqs <= f_high)
    
    if np.any(mask):
        return float(np.max(mags[mask]))
    return 0.0

def spectral_centroid(freqs: np.ndarray, mags: np.ndarray) -> float:
    """
    Center of mass of spectrum - where is energy concentrated?
    Higher centroid => more high-frequency content
    """
    total_energy = np.sum(mags)
    if total_energy == 0:
        return 0.0
    return float(np.sum(freqs * mags) / total_energy)

# ==================== FAULT DETECTION FEATURES ====================

def extract_fault_indicators(x: np.ndarray, fs: float, 
                             running_freq: float = 30.0) -> Dict[str, float]:
    """
    Extract comprehensive fault indicators from vibration signal
    
    Args:
        x: acceleration signal
        fs: sampling frequency (Hz)
        running_freq: machine running frequency (1× speed, Hz)
    
    Returns:
        Dictionary of fault indicators
    """
    # Time-domain features
    features = {
        'rms': rms(x),
        'peak_to_peak': peak_to_peak(x),
        'kurtosis': kurtosis(x),
        'crest_factor': crest_factor(x),
    }
    
    # Frequency-domain analysis
    freqs, mags = compute_fft(x, fs)
    
    # Imbalance indicator (strong 1× component)
    features['1x_amplitude'] = peak_frequency_amplitude(freqs, mags, running_freq)
    
    # Misalignment indicator (strong 2× component)
    features['2x_amplitude'] = peak_frequency_amplitude(freqs, mags, 2 * running_freq)
    
    # Bearing indicators
    # High-frequency energy (above 100 Hz)
    features['hf_energy'] = spectral_energy(freqs, mags, 100.0, fs/2)
    
    # Low-frequency energy (0-50 Hz)
    features['lf_energy'] = spectral_energy(freqs, mags, 0.0, 50.0)
    
    # Spectral characteristics
    features['spectral_centroid'] = spectral_centroid(freqs, mags)
    
    # Total spectral energy
    features['total_energy'] = spectral_energy(freqs, mags, 0.0, fs/2)
    
    return features
