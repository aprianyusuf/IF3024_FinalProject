"""
Modul untuk ekstraksi sinyal respirasi.

Ekstraksi sinyal respirasi dari sebuah frame video.
Parameter : Frame video sebagai input.
Return : Nilai sinyal respirasi yang diekstraksi.
"""
import numpy as np
def ekstrak_sinyal_respirasi(frame):
    # Menggunakan intensitas rata-rata piksel
    nilai_sinyal = np.mean(frame)
    return nilai_sinyal