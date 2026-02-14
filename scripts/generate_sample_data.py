import os
import numpy as np

def save_csv(path: str, t: np.ndarray, x: np.ndarray):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data = np.column_stack([t, x])
    np.savetxt(path, data, delimiter=",", header="time,accel", comments="")

def gen_signal(
    fs=2000,
    seconds=3.0,
    base_f=30.0,
    noise=0.05,
    imbalance=False,
    misalignment=False,
    bearing=False,
    seed=42,
):
    """
    Generates synthetic vibration signals:
    - Normal: mostly clean 1× sine + small noise
    - Imbalance: stronger 1× component
    - Misalignment: stronger 2× component
    - Bearing-like: high-frequency resonance + impulsive spikes
    """
    rng = np.random.default_rng(seed)
    t = np.arange(0, seconds, 1 / fs)

    # Base 1× rotation vibration
    x = 0.2 * np.sin(2 * np.pi * base_f * t)

    # Imbalance => strong 1× energy
    if imbalance:
        x += 0.6 * np.sin(2 * np.pi * base_f * t)

    # Misalignment => strong 2× harmonic energy
    if misalignment:
        x += 0.45 * np.sin(2 * np.pi * (2 * base_f) * t)

    # Bearing-like => high-frequency resonance + spikes (impulsive)
    if bearing:
        hf = 350.0
        x += 0.12 * np.sin(2 * np.pi * hf * t)

        spikes = np.zeros_like(t)
        n_spikes = max(8, len(t) // 250)
        idx = rng.choice(len(t), size=n_spikes, replace=False)
        spikes[idx] = rng.uniform(1.5, 2.5, size=n_spikes) * rng.choice([-1, 1], size=n_spikes)
        x += spikes

    # Add noise
    x += noise * rng.standard_normal(len(t))
    return t, x

def main():
    # Settings
    fs = 2000       # samples per second
    secs = 3.0      # duration
    base_f = 30.0   # "running frequency" (1×) ~ 30 Hz

    # Generate 4 conditions
    t, x = gen_signal(fs, secs, base_f, seed=1)
    save_csv("sample_data/normal.csv", t, x)

    t, x = gen_signal(fs, secs, base_f, imbalance=True, seed=2)
    save_csv("sample_data/imbalance.csv", t, x)

    t, x = gen_signal(fs, secs, base_f, misalignment=True, seed=3)
    save_csv("sample_data/misalignment.csv", t, x)

    t, x = gen_signal(fs, secs, base_f, bearing=True, seed=4)
    save_csv("sample_data/bearing.csv", t, x)

    print("Generated sample vibration CSVs in sample_data/")
    print("   - normal.csv")
    print("   - imbalance.csv")
    print("   - misalignment.csv")
    print("   - bearing.csv")

if __name__ == "__main__":
    main()
