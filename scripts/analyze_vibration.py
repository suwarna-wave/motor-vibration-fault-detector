"""
Motor Vibration Analysis Script
Complete diagnostic analysis of vibration data files
"""
import sys
import glob
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.io_utils import load_csv
from src.diagnostics import diagnose_vibration


def print_separator(char="=", length=70):
    """Print a visual separator"""
    print(char * length)


def print_report(filename: str, report: dict):
    """Pretty-print diagnostic report"""
    print(f"\n📁 File: {filename}")
    print_separator("-")
    
    # Health status with color indicators (text-based)
    status_emoji = {
        "HEALTHY": "✅",
        "ACCEPTABLE": "✓",
        "WARNING": "⚠️",
        "CRITICAL": "🚨"
    }
    
    status = report['status']
    emoji = status_emoji.get(status, "•")
    
    print(f"\n{emoji} HEALTH SCORE: {report['health_score']}/100 ({status})")
    print(f"🔍 PRIMARY FAULT: {report['primary_fault']}")
    
    if report['detected_faults']:
        print(f"📊 DETECTED FAULTS: {', '.join(report['detected_faults'])}")
        print(f"🎯 CONFIDENCE: {report['confidence']*100:.1f}%")
    else:
        print("📊 DETECTED FAULTS: None")
    
    # Feature summary (key indicators)
    print("\n📈 KEY INDICATORS:")
    features = report['features']
    print(f"   RMS Energy:      {features['rms']:.4f}")
    print(f"   Kurtosis:        {features['kurtosis']:.4f}")
    print(f"   Crest Factor:    {features['crest_factor']:.4f}")
    print(f"   1× Amplitude:    {features['1x_amplitude']:.4f}")
    print(f"   2× Amplitude:    {features['2x_amplitude']:.4f}")
    print(f"   HF Energy:       {features['hf_energy']:.4f}")
    
    # Recommendations
    print("\n💡 RECOMMENDATIONS:")
    for rec in report['recommendations']:
        print(f"   {rec}")
    
    print_separator("-")


def analyze_all_files(pattern: str = "sample_data/*.csv", 
                     running_freq: float = 30.0):
    """
    Analyze all vibration data files matching the pattern
    
    Args:
        pattern: glob pattern for CSV files
        running_freq: machine running frequency in Hz
    """
    files = sorted(glob.glob(pattern))
    
    if not files:
        print(f"❌ No files found matching: {pattern}")
        print("\n💡 Run 'python scripts/generate_sample_data.py' first")
        return
    
    print_separator()
    print("🔧 MOTOR VIBRATION FAULT DETECTOR")
    print("   Predictive Maintenance Analysis System")
    print_separator()
    print(f"\nAnalyzing {len(files)} file(s) with running frequency = {running_freq} Hz\n")
    
    # Analyze each file
    results = []
    
    for filepath in files:
        try:
            # Load data
            time, accel, fs = load_csv(filepath)
            
            if fs is None:
                print(f"⚠️  Warning: Could not infer sampling frequency from {filepath}")
                continue
            
            # Run diagnostics
            report = diagnose_vibration(accel, fs, running_freq)
            report['filename'] = Path(filepath).name
            report['sampling_freq'] = fs
            
            results.append(report)
            
            # Print individual report
            print_report(Path(filepath).name, report)
            
        except Exception as e:
            print(f"❌ Error processing {filepath}: {e}")
            continue
    
    # Summary comparison
    if len(results) > 1:
        print_summary_comparison(results)
    
    return results


def print_summary_comparison(results: list):
    """Print comparison table of all analyzed files"""
    print("\n")
    print_separator()
    print("📊 SUMMARY COMPARISON")
    print_separator()
    
    # Table header
    print(f"\n{'Filename':<20} {'Health':<8} {'Status':<12} {'Primary Fault':<15}")
    print("-" * 70)
    
    # Table rows
    for r in results:
        filename = r['filename'][:18]  # Truncate long names
        health = f"{r['health_score']}/100"
        status = r['status']
        fault = r['primary_fault']
        
        print(f"{filename:<20} {health:<8} {status:<12} {fault:<15}")
    
    print_separator()


def main():
    """Main entry point"""
    # Default settings
    pattern = "sample_data/*.csv"
    running_freq = 30.0  # Hz - machine running frequency
    
    # Parse command line arguments (simple)
    if len(sys.argv) > 1:
        pattern = sys.argv[1]
    if len(sys.argv) > 2:
        running_freq = float(sys.argv[2])
    
    # Run analysis
    analyze_all_files(pattern, running_freq)


if __name__ == "__main__":
    main()
