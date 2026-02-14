import glob
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.io_utils import load_csv
from src.features import rms, peak_to_peak, kurtosis, crest_factor

def main():
    files = sorted(glob.glob("sample_data/*.csv"))
    if not files:
        print("No files found in sample_data/. Run generate_sample_data.py first.")
        return

    print("=== Time-Domain Feature Report ===")
    for f in files:
        _, accel, fs = load_csv(f)
        print(f"\nFile: {f}")
        print(f"fs (inferred): {fs:.2f} Hz" if fs else "fs: (not available)")
        print(f"RMS:         {rms(accel):.4f}")
        print(f"Peak-to-Peak:{peak_to_peak(accel):.4f}")
        print(f"Kurtosis:    {kurtosis(accel):.4f}")
        print(f"CrestFactor: {crest_factor(accel):.4f}")

if __name__ == "__main__":
    main()
