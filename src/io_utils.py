import numpy as np

def load_csv(path: str):
    """
    Loads CSV with either:
      - time, accel
      - accel only

    Returns:
      time (np.ndarray or None),
      accel (np.ndarray),
      fs (float or None)   # inferred from time if available
    """
    data = np.genfromtxt(path, delimiter=",", names=True)
    cols = data.dtype.names

    if cols is None:
        raise ValueError("CSV must have a header row (e.g., time,accel).")

    # accel column
    if "accel" in cols:
        accel = np.asarray(data["accel"], dtype=float)
    else:
        # fallback: last column
        accel = np.asarray(data[cols[-1]], dtype=float)

    # time column (optional)
    if "time" in cols:
        time = np.asarray(data["time"], dtype=float)
        if len(time) >= 2:
            dt = float(np.median(np.diff(time)))
            fs = (1.0 / dt) if dt > 0 else None
        else:
            fs = None
    else:
        time = None
        fs = None

    return time, accel, fs
