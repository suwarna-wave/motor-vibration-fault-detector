"""
Visualization Module for Vibration Analysis
Generate plots for time-domain and frequency-domain analysis
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.features import compute_fft
from src.diagnostics import diagnose_vibration


def plot_vibration_analysis(time: np.ndarray, 
                           accel: np.ndarray,
                           fs: float,
                           title: str = "Vibration Analysis",
                           running_freq: float = 30.0,
                           save_path: str = None):
    """
    Create comprehensive vibration analysis plot
    
    Creates a 2-subplot figure:
    - Top: Time-domain signal
    - Bottom: Frequency spectrum with fault indicators
    
    Args:
        time: time array (seconds)
        accel: acceleration signal
        fs: sampling frequency (Hz)
        title: plot title
        running_freq: machine running frequency (Hz)
        save_path: optional path to save figure
    """
    # Run diagnostics
    report = diagnose_vibration(accel, fs, running_freq)
    
    # Compute FFT
    freqs, mags = compute_fft(accel, fs)
    
    # Create figure with 2 subplots
    fig, axes = plt.subplots(2, 1, figsize=(12, 8))
    fig.suptitle(title, fontsize=14, fontweight='bold')
    
    # ========== TIME DOMAIN PLOT ==========
    ax1 = axes[0]
    ax1.plot(time, accel, 'b-', linewidth=0.8, alpha=0.8)
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Acceleration (g)')
    ax1.set_title('Time Domain Signal')
    ax1.grid(True, alpha=0.3)
    
    # Add RMS reference lines
    rms_val = report['features']['rms']
    ax1.axhline(rms_val, color='r', linestyle='--', alpha=0.5, 
                label=f'RMS = {rms_val:.3f}')
    ax1.axhline(-rms_val, color='r', linestyle='--', alpha=0.5)
    ax1.legend(loc='upper right')
    
    # ========== FREQUENCY DOMAIN PLOT ==========
    ax2 = axes[1]
    ax2.plot(freqs, mags, 'b-', linewidth=1.0)
    ax2.set_xlabel('Frequency (Hz)')
    ax2.set_ylabel('Magnitude')
    ax2.set_title('Frequency Spectrum (FFT)')
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim([0, min(500, fs/2)])  # Show up to 500 Hz
    
    # Mark key frequencies
    # 1× running frequency
    ax2.axvline(running_freq, color='green', linestyle='--', 
                alpha=0.6, label=f'1× ({running_freq} Hz)')
    
    # 2× harmonic
    ax2.axvline(2*running_freq, color='orange', linestyle='--', 
                alpha=0.6, label=f'2× ({2*running_freq} Hz)')
    
    # High-frequency region (bearing faults)
    ax2.axvspan(100, min(500, fs/2), alpha=0.1, color='red', 
                label='HF Region (Bearing)')
    
    ax2.legend(loc='upper right')
    
    # Add diagnostic info as text box
    info_text = f"""Health Score: {report['health_score']}/100
Status: {report['status']}
Fault: {report['primary_fault']}
Kurtosis: {report['features']['kurtosis']:.2f}
Crest Factor: {report['features']['crest_factor']:.2f}"""
    
    ax2.text(0.98, 0.97, info_text,
             transform=ax2.transAxes,
             verticalalignment='top',
             horizontalalignment='right',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
             fontsize=9,
             family='monospace')
    
    plt.tight_layout()
    
    # Save if requested
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"📊 Plot saved: {save_path}")
    
    return fig, report


def plot_all_samples(data_pattern: str = "sample_data/*.csv",
                    output_dir: str = "outputs",
                    running_freq: float = 30.0):
    """
    Generate plots for all sample data files
    
    Args:
        data_pattern: glob pattern for data files
        output_dir: directory to save plots
        running_freq: machine running frequency (Hz)
    """
    import glob
    from src.io_utils import load_csv
    
    files = sorted(glob.glob(data_pattern))
    if not files:
        print(f"No files found matching: {data_pattern}")
        return
    
    # Create output directory
    Path(output_dir).mkdir(exist_ok=True)
    
    print(f"Generating plots for {len(files)} file(s)...")
    
    for filepath in files:
        try:
            # Load data
            time, accel, fs = load_csv(filepath)
            
            if fs is None:
                print(f"⚠️  Skipping {filepath} - no sampling frequency")
                continue
            
            # Generate plot
            filename = Path(filepath).stem
            title = f"Vibration Analysis: {filename.upper()}"
            save_path = Path(output_dir) / f"{filename}_analysis.png"
            
            plot_vibration_analysis(time, accel, fs, title, 
                                  running_freq, str(save_path))
            
            plt.close()  # Close to avoid memory issues
            
        except Exception as e:
            print(f"❌ Error plotting {filepath}: {e}")
    
    print(f"\n✅ All plots saved to: {output_dir}/")


def plot_comparison_grid(data_pattern: str = "sample_data/*.csv",
                        running_freq: float = 30.0,
                        save_path: str = "outputs/comparison_grid.png"):
    """
    Create a comparison grid showing all samples
    
    Args:
        data_pattern: glob pattern for data files
        running_freq: machine running frequency (Hz)
        save_path: path to save comparison figure
    """
    import glob
    from src.io_utils import load_csv
    
    files = sorted(glob.glob(data_pattern))
    if not files:
        print(f"No files found matching: {data_pattern}")
        return
    
    n_files = len(files)
    fig, axes = plt.subplots(n_files, 2, figsize=(14, 3*n_files))
    
    if n_files == 1:
        axes = axes.reshape(1, -1)
    
    fig.suptitle('Vibration Analysis Comparison', fontsize=16, fontweight='bold')
    
    for idx, filepath in enumerate(files):
        try:
            # Load data
            time, accel, fs = load_csv(filepath)
            
            if fs is None:
                continue
            
            # Compute FFT
            freqs, mags = compute_fft(accel, fs)
            
            # Run diagnostics
            report = diagnose_vibration(accel, fs, running_freq)
            
            filename = Path(filepath).stem.upper()
            
            # Time domain
            ax_time = axes[idx, 0]
            ax_time.plot(time, accel, 'b-', linewidth=0.6, alpha=0.8)
            ax_time.set_ylabel('Accel (g)')
            ax_time.set_title(f'{filename} - Time Domain')
            ax_time.grid(True, alpha=0.3)
            
            if idx == n_files - 1:
                ax_time.set_xlabel('Time (s)')
            
            # Frequency domain
            ax_freq = axes[idx, 1]
            ax_freq.plot(freqs, mags, 'b-', linewidth=0.8)
            ax_freq.set_ylabel('Magnitude')
            ax_freq.set_title(f'{filename} - FFT (Health: {report["health_score"]}/100)')
            ax_freq.set_xlim([0, 200])
            ax_freq.grid(True, alpha=0.3)
            
            # Mark fault frequencies
            ax_freq.axvline(running_freq, color='green', linestyle='--', alpha=0.5)
            ax_freq.axvline(2*running_freq, color='orange', linestyle='--', alpha=0.5)
            
            if idx == n_files - 1:
                ax_freq.set_xlabel('Frequency (Hz)')
            
        except Exception as e:
            print(f"Error plotting {filepath}: {e}")
    
    plt.tight_layout()
    
    # Save
    Path(save_path).parent.mkdir(exist_ok=True)
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"\n📊 Comparison grid saved: {save_path}")
    
    return fig


if __name__ == "__main__":
    """Generate all visualizations when run directly"""
    print("🎨 Generating vibration analysis visualizations...\n")
    
    # Individual plots
    plot_all_samples()
    
    # Comparison grid
    plot_comparison_grid()
    
    print("\n✅ All visualizations complete!")
