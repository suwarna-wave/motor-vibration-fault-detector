"""
Vibration Diagnostics Module
Fault detection and health scoring based on engineering principles
"""
import numpy as np
from typing import Dict, List, Tuple
from src.features import extract_fault_indicators


class FaultType:
    """Enumeration of detectable fault types"""
    NORMAL = "NORMAL"
    IMBALANCE = "IMBALANCE"
    MISALIGNMENT = "MISALIGNMENT"
    BEARING = "BEARING"
    MULTIPLE = "MULTIPLE"


def detect_faults(features: Dict[str, float], 
                 running_freq: float = 30.0) -> Tuple[str, List[str], float]:
    """
    Engineering-based fault detection logic
    
    Args:
        features: dictionary of extracted features
        running_freq: machine running frequency (Hz)
    
    Returns:
        primary_fault: main fault type detected
        fault_list: list of all detected faults
        confidence: detection confidence (0-1)
    """
    detected_faults = []
    fault_scores = {}
    
    # Extract key features
    rms_val = features.get('rms', 0)
    kurtosis_val = features.get('kurtosis', 3.0)
    crest_factor_val = features.get('crest_factor', 0)
    
    amp_1x = features.get('1x_amplitude', 0)
    amp_2x = features.get('2x_amplitude', 0)
    hf_energy = features.get('hf_energy', 0)
    lf_energy = features.get('lf_energy', 0)
    
    # ========== IMBALANCE DETECTION ==========
    # Strong 1× frequency component relative to baseline
    # Typical imbalance shows dominant running frequency
    if amp_1x > 0.4:  # Threshold based on signal generation
        detected_faults.append(FaultType.IMBALANCE)
        fault_scores[FaultType.IMBALANCE] = min(1.0, amp_1x / 0.8)
    
    # ========== MISALIGNMENT DETECTION ==========
    # Strong 2× harmonic component
    # Misalignment generates strong 2× running frequency
    if amp_2x > 0.3:
        detected_faults.append(FaultType.MISALIGNMENT)
        fault_scores[FaultType.MISALIGNMENT] = min(1.0, amp_2x / 0.6)
    
    # ========== BEARING FAULT DETECTION ==========
    # High kurtosis (impulsive behavior) + high-frequency energy
    bearing_score = 0.0
    
    if kurtosis_val > 4.0:  # Normal ~ 3, bearing faults >> 3
        bearing_score += 0.4
    
    if crest_factor_val > 6.0:  # Impulsive peaks
        bearing_score += 0.3
    
    if hf_energy > 0.02:  # Elevated high-frequency content
        bearing_score += 0.3
    
    if bearing_score > 0.5:
        detected_faults.append(FaultType.BEARING)
        fault_scores[FaultType.BEARING] = min(1.0, bearing_score)
    
    # ========== DETERMINE PRIMARY FAULT ==========
    if len(detected_faults) == 0:
        primary_fault = FaultType.NORMAL
        confidence = 0.9
    elif len(detected_faults) == 1:
        primary_fault = detected_faults[0]
        confidence = fault_scores[primary_fault]
    else:
        # Multiple faults detected
        primary_fault = FaultType.MULTIPLE
        confidence = max(fault_scores.values())
    
    return primary_fault, detected_faults, confidence


def calculate_health_score(features: Dict[str, float],
                          fault_type: str,
                          fault_list: List[str],
                          confidence: float) -> int:
    """
    Calculate overall machine health score (0-100)
    100 = Perfect health
    0 = Critical condition
    
    Deducts points based on:
    - Vibration severity (RMS)
    - Impulsiveness (kurtosis, crest factor)
    - Detected faults
    - Spectral anomalies
    """
    score = 100.0
    
    # Extract features
    rms_val = features.get('rms', 0)
    kurtosis_val = features.get('kurtosis', 3.0)
    crest_factor_val = features.get('crest_factor', 0)
    total_energy = features.get('total_energy', 0)
    
    # ========== SEVERITY PENALTIES ==========
    
    # RMS penalty (vibration severity)
    # Normal: < 0.3, Warning: 0.3-0.6, Critical: > 0.6
    if rms_val > 0.6:
        score -= 30
    elif rms_val > 0.3:
        score -= 15
    
    # Kurtosis penalty (impulsiveness)
    # Normal: ~3, High: >5, Critical: >8
    if kurtosis_val > 8:
        score -= 20
    elif kurtosis_val > 5:
        score -= 10
    
    # Crest factor penalty (peak impacts)
    # Normal: 3-5, Warning: 5-8, Critical: >8
    if crest_factor_val > 8:
        score -= 15
    elif crest_factor_val > 6:
        score -= 8
    
    # ========== FAULT-BASED PENALTIES ==========
    
    if fault_type == FaultType.NORMAL:
        pass  # No penalty
    
    elif fault_type == FaultType.IMBALANCE:
        # Imbalance is typically less severe
        score -= 15 * confidence
    
    elif fault_type == FaultType.MISALIGNMENT:
        # Misalignment is moderately severe
        score -= 20 * confidence
    
    elif fault_type == FaultType.BEARING:
        # Bearing faults are critical
        score -= 35 * confidence
    
    elif fault_type == FaultType.MULTIPLE:
        # Multiple faults are very serious
        score -= 40
    
    # ========== ENERGY-BASED PENALTY ==========
    # Overall excessive energy indicates problems
    if total_energy > 0.5:
        score -= 10
    
    # Ensure score stays in valid range
    score = max(0.0, min(100.0, score))
    
    return int(round(score))


def diagnose_vibration(accel: np.ndarray, fs: float, 
                      running_freq: float = 30.0) -> Dict:
    """
    Complete vibration diagnostics pipeline
    
    Args:
        accel: acceleration time-series data
        fs: sampling frequency (Hz)
        running_freq: machine running frequency (Hz)
    
    Returns:
        Comprehensive diagnostic report dictionary
    """
    # Extract all features
    features = extract_fault_indicators(accel, fs, running_freq)
    
    # Detect faults
    primary_fault, fault_list, confidence = detect_faults(features, running_freq)
    
    # Calculate health score
    health_score = calculate_health_score(features, primary_fault, 
                                         fault_list, confidence)
    
    # Compile diagnostic report
    report = {
        'health_score': health_score,
        'status': _health_status(health_score),
        'primary_fault': primary_fault,
        'detected_faults': fault_list,
        'confidence': round(confidence, 3),
        'features': {k: round(v, 4) for k, v in features.items()},
        'recommendations': _generate_recommendations(primary_fault, 
                                                    health_score, 
                                                    fault_list)
    }
    
    return report


def _health_status(score: int) -> str:
    """Convert numeric health score to status label"""
    if score >= 85:
        return "HEALTHY"
    elif score >= 70:
        return "ACCEPTABLE"
    elif score >= 50:
        return "WARNING"
    else:
        return "CRITICAL"


def _generate_recommendations(fault_type: str, 
                             health_score: int,
                             fault_list: List[str]) -> List[str]:
    """Generate actionable maintenance recommendations"""
    recommendations = []
    
    if fault_type == FaultType.NORMAL:
        recommendations.append("✓ Machine operating normally")
        recommendations.append("Continue routine monitoring")
    
    if FaultType.IMBALANCE in fault_list:
        recommendations.append("⚠ Imbalance detected - Check rotor balance")
        recommendations.append("Inspect for uneven mass distribution")
    
    if FaultType.MISALIGNMENT in fault_list:
        recommendations.append("⚠ Misalignment detected - Check shaft alignment")
        recommendations.append("Verify coupling and bearing alignment")
    
    if FaultType.BEARING in fault_list:
        recommendations.append("⚠ Bearing fault indicators present")
        recommendations.append("Inspect bearings for wear/damage")
        recommendations.append("Consider bearing replacement soon")
    
    if len(fault_list) > 1:
        recommendations.append("⚠⚠ Multiple fault indicators - Priority inspection needed")
    
    if health_score < 50:
        recommendations.append("🚨 CRITICAL: Schedule immediate maintenance")
    elif health_score < 70:
        recommendations.append("⚠ Plan maintenance within next scheduled window")
    
    return recommendations
