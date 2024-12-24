"""
Program utama untuk memproses video dari webcam dan menampilkan sinyal respirasi serta rPPG.
"""

import cv2
from respiration import ekstrak_sinyal_respirasi
from rppg import ekstrak_sinyal_rppg
from utils import butterworth_filter, bandpass_filter
import matplotlib.pyplot as plt
import sys
import os

# Menambahkan path direktori 'src' ke sys.path
sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "src")))

def main():
    # Membuka webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Tidak dapat mengakses webcam.")
        return

    # Membuat plot untuk visualisasi sinyal
    plt.ion()
    fig, (ax1, ax2) = plt.subplots(2, 1)
    sinyal_respirasi, sinyal_rppg = [], []
    fig.tight_layout(pad=4)

    # Buat kondisi perulangan untuk menjalankan program
    while True:
        # Membaca frame dari webcam
        ret, frame = cap.read()
        if not ret:
            break

        # Mengubah ukuran frame untuk mengurangi beban komputasi
        frame_resized = cv2.resize(frame, (320, 240))

        # Ekstraksi sinyal respirasi dan rPPG
        resp_signal = ekstrak_sinyal_respirasi(frame_resized)
        rppg_signal = ekstrak_sinyal_rppg(frame_resized)
        
        # Simpan sinyal
        sinyal_respirasi.append(resp_signal)
        sinyal_rppg.append(rppg_signal)

        """
        Percobaan menggunakan filter

        # PENERAPAN BUTTERWORTH FILTER
        fs = 30  # Frekuensi sampling (misalnya, 30 Hz untuk webcam)
        cutoff_resp = 0.3  # Cutoff frekuensi untuk respirasi (0.3 Hz, band low-frequency)
        cutoff_rppg = 1.5  # Cutoff frekuensi untuk rPPG (1.5 Hz)
        
        # Terapkan filter butterworth ke sinyal yang diekstraksi
        resp_signal_filtered = butterworth_filter(
            sinyal_respirasi + [resp_signal], cutoff_resp, fs, order=4)
        rppg_signal_filtered = butterworth_filter(
            sinyal_rppg + [rppg_signal], cutoff_rppg, fs, order=4)
        
        # Simpan nilai terakhir setelah filtering
        sinyal_respirasi.append(resp_signal_filtered[-1])
        sinyal_rppg.append(rppg_signal_filtered[-1])


        # PENERAPAN BANDPASS FILTER
        # Terapkan filter jika data cukup panjang
        fs = 30
        if len(sinyal_respirasi) > 30:  # Misalnya, tunggu hingga 30 sampel terkumpul
            resp_filtered = bandpass_filter(sinyal_respirasi, lowcut=0.1, highcut=0.5, fs=fs, order=4)
            rppg_filtered = bandpass_filter(sinyal_rppg, lowcut=0.8, highcut=2, fs=fs, order=4)
        else:
            resp_filtered = sinyal_respirasi
            rppg_filtered = sinyal_rppg

        # Pastikan data yang difilter tidak kosong
        if len(resp_filtered) > 0:
            sinyal_respirasi.append(resp_filtered[-1])
        if len(rppg_filtered) > 0:
            sinyal_rppg.append(rppg_filtered[-1])
        """

        # Menampilkan video dari webcam
        cv2.imshow("Webcam", frame_resized)

        # Memperbarui plot sinyal
        ax1.clear()
        ax1.plot(sinyal_respirasi[-100:], color='blue')
        ax1.set_title("Sinyal Respirasi")
        ax1.set_xlabel("Waktu")
        ax1.set_ylabel("Amplitude")
        ax1.grid(True)

        ax2.clear()
        ax2.plot(sinyal_rppg[-100:], color='green')
        ax2.set_title("Sinyal rPPG")
        ax2.set_xlabel("Waktu")
        ax2.set_ylabel("Amplitude")
        ax2.grid(True)

        # Refresh tampilan matplotlib
        plt.pause(0.01)

        # Keluar dari loop jika tombol 'Esc' ditekan
        if cv2.waitKey(1) & 0xFF == 27:
            break

    # Membersihkan sumber daya
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()