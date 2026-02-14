#!/usr/bin/env python3
"""
Complete Demo Script - Motor Vibration Fault Detector
Runs all components of the system in sequence
"""
import sys
from pathlib import Path
import time

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")

def print_step(step_num, text):
    """Print step indicator"""
    print(f"\n{'─'*70}")
    print(f"📍 STEP {step_num}: {text}")
    print(f"{'─'*70}\n")
    time.sleep(0.5)

def main():
    """Run complete demo"""
    import subprocess
    import os
    
    # Change to project root
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    # Get Python executable
    python_exe = sys.executable
    
    print_header("🔧 MOTOR VIBRATION FAULT DETECTOR - COMPLETE DEMO")
    
    print("This demo will run the complete vibration analysis system:")
    print("  1. Generate synthetic vibration data")
    print("  2. Extract time-domain features")
    print("  3. Run complete diagnostic analysis")
    print("  4. Generate visualizations")
    print("  5. Run test suite")
    print("\nPress Enter to continue...")
    input()
    
    # Step 1: Generate data
    print_step(1, "Generating Sample Vibration Data")
    subprocess.run([python_exe, "scripts/generate_sample_data.py"], check=True)
    
    # Step 2: Time features
    print_step(2, "Extracting Time-Domain Features")
    subprocess.run([python_exe, "scripts/test_time_features.py"], check=True)
    
    # Step 3: Complete analysis
    print_step(3, "Running Complete Diagnostic Analysis")
    subprocess.run([python_exe, "scripts/analyze_vibration.py"], check=True)
    
    # Step 4: Visualizations
    print_step(4, "Generating Visualizations")
    subprocess.run([python_exe, "src/visualize.py"], check=True)
    
    # Step 5: Tests
    print_step(5, "Running Test Suite")
    result = subprocess.run([python_exe, "scripts/run_tests.py"], check=True)
    
    # Summary
    print_header("✅ DEMO COMPLETE - SYSTEM FULLY OPERATIONAL")
    
    print("📊 Generated Files:")
    print(f"   • 4 sample vibration signals in sample_data/")
    print(f"   • 5 analysis plots in outputs/")
    print(f"   • All 22 tests passed ✅")
    
    print("\n🚀 Next Steps:")
    print("   • Review plots in outputs/ directory")
    print("   • Examine diagnostic reports above")
    print("   • Read USAGE_GUIDE.md for detailed documentation")
    print("   • Try analyzing your own vibration data")
    
    print("\n📖 Key Files:")
    print("   • README.md - Project overview")
    print("   • USAGE_GUIDE.md - Detailed usage instructions")
    print("   • src/features.py - Feature extraction")
    print("   • src/diagnostics.py - Fault detection engine")
    
    print_header("Thank you for exploring the Motor Vibration Fault Detector!")
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error during demo: {e}")
        sys.exit(1)
