"""
Fungsi utilitas untuk pemrosesan sinyal.
"""

import numpy as np
from scipy.signal import butter, lfilter, filtfilt

def bandpass_filter(data, lowcut, highcut, fs, order=4):
    """
    Terapkan filter band-pass ke data, dengan penanganan jika data terlalu pendek atau kosong.

    Parameter:
    - data (list atau numpy.ndarray): Sinyal yang akan difilter.
    - lowcut (float): Frekuensi cutoff bawah (Hz).
    - highcut (float): Frekuensi cutoff atas (Hz).
    - fs (float): Frekuensi sampling (Hz).
    - order (int): Orde filter.

    Return:
    - numpy.ndarray: Sinyal yang sudah difilter.
    """
    if len(data) == 0:  # Jika data kosong
        return np.array(data) # Output array([], dtype=float64)

    nyquist = 0.5 * fs  # Frekuensi Nyquist
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')

    # Pastikan panjang data lebih besar dari padlen
    padlen = 3 * max(len(b), len(a)) 
    if len(data) <= padlen: # Jika data terlalu pendek
        return np.array(data)  # Kembalikan data apa adanya
    return filtfilt(b, a, data)

def butterworth_filter(data, cutoff, fs, order=4, filter_type='low'):
    """
    Terapkan filter Butterworth ke data.

    Parameter:
    - data (list atau numpy.ndarray): Sinyal yang akan difilter.
    - cutoff (float): Frekuensi cutoff filter (Hz).
    - fs (float): Frekuensi sampling (Hz).
    - order (int): Orde filter.
    - filter_type (str): Jenis filter ('low', 'high', atau 'band').

    Return:
    - numpy.ndarray: Sinyal yang sudah difilter.
    """
    nyquist = 0.5 * fs  # Frekuensi Nyquist
    normalized_cutoff = cutoff / nyquist  # Normalisasi cutoff
    b, a = butter(order, normalized_cutoff, btype=filter_type, analog=False)
    return lfilter(b, a, data)