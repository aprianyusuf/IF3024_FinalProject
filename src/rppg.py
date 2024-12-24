"""
Modul untuk ekstraksi sinyal respirasi.

Ekstraksi sinyal rPPG dari sebuah frame video.
Parameter : Frame video sebagai input.
Return : Nilai sinyal rPPG yang diekstraksi.
"""
import numpy as np
def ekstrak_sinyal_rppg(frame):
    # Menggunakan deviasi standar intensitas piksel
    nilai_sinyal = np.std(frame)
    return nilai_sinyal