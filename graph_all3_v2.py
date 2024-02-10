# Script to produce a frequency/amplitude graph and a spectrogram from Grape2 data.
# Michael J. Hauan, AC0G
# 2024-02-10


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import spectrogram
import argparse
import re

def save_frequency_and_amplitude(signal, sampling_rate, datetime_str, station):
    """
    Saves the frequency and amplitude plot of a signal to a PNG file.
    """
    fft_result = np.fft.fft(signal)
    amplitude_spectrum = np.abs(fft_result) / len(fft_result)
    freqs = np.fft.fftfreq(len(fft_result), d=1/sampling_rate)

    plt.figure(figsize=(14, 7))
    plt.plot(freqs[:len(freqs)//2], amplitude_spectrum[:len(freqs)//2])
    plt.title(f'Frequency and Amplitude - {station.upper()}')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.grid()
    
    datetime_hour = datetime_str[:13].replace('-', '').replace('T', '')
    filename = f"{datetime_hour}_{station}_frequency.png"
    plt.savefig(filename)
    plt.close()

def save_spectrogram(signal, sampling_rate, datetime_str, station):
    """
    Saves a spectrogram of a signal to a PNG file.
    """
    f, t, Sxx = spectrogram(signal, sampling_rate)
    plt.figure(figsize=(14, 7))
    plt.pcolormesh(t, f, 10 * np.log10(Sxx), shading='gouraud')
    plt.ylabel('Frequency (Hz)')
    plt.xlabel('Time (sec)')
    plt.title(f'Spectrogram - {station.upper()}')
    plt.colorbar(label='Intensity [dB]')
    
    datetime_hour = datetime_str[:13].replace('-', '').replace('T', '')
    filename = f"{datetime_hour}_{station}_spectrogram.png"
    plt.savefig(filename)
    plt.close()

def process_file(filename):
    """
    Process a CSV file to plot frequency, amplitude, and spectrogram for each receiver.
    """
    df = pd.read_csv(filename)
    sampling_rate = 8000  # Hz

    # Extract datetime and station identifier from filename for labeling
    datetime_str = re.search(r'(\d{4}-\d{2}-\d{2}T\d{2})', filename).group(1)

    for column, station in zip(df.columns[1:], ['wwv5', 'wwv10', 'wwv15']):
        signal = pd.to_numeric(df[column], errors='coerce').fillna(0).values

        # Save frequency and amplitude plot
        save_frequency_and_amplitude(signal, sampling_rate, datetime_str, station)

        # Save spectrogram
        save_spectrogram(signal, sampling_rate, datetime_str, station)

def main():
    """
    Main entry point of the script. Parses command line arguments and processes the file.
    """
    parser = argparse.ArgumentParser(description="Analyze and save plots for radio signals.")
    parser.add_argument("filename", help="The path to the CSV file containing the observation data.")
    args = parser.parse_args()
    
    process_file(args.filename)

if __name__ == "__main__":
    main()

