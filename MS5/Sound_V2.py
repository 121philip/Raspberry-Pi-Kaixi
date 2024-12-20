import matplotlib.pyplot as plt
import nidaqmx
import numpy as np
from nidaqmx.constants import AcquisitionType
from scipy.signal import butter, filtfilt

# Set a higher sampling rate and increase the number of samples
sampling_rate = 10000  # Sampling rate in Hz
samples_per_channel = 200  # Number of samples to capture

# Define filter parameters
LOWCUT = 400  # Low cutoff frequency (Hz)
HIGHCUT = 600  # High cuttoff frequency (Hz)


# Function to design a Butterworth filter
def butter_bandstop(lowcut, highcut, fs, order=4):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='bandstop')
    return b, a


with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev2/ai0", min_val=-10.0, max_val=10.0)
    task.timing.cfg_samp_clk_timing(rate=sampling_rate, sample_mode=AcquisitionType.CONTINUOUS)
    data = task.read(number_of_samples_per_channel=samples_per_channel)

# Generate time values for the x-axis
time = np.linspace(0, len(data) / sampling_rate, len(data))

# Perform FFT on the signal
fft_data = np.fft.fft(data)
frequencies = np.fft.fftfreq(len(fft_data), d=1 / sampling_rate)

# Define bandstop filter to remove a specific frequency range
b, a = butter_bandstop(LOWCUT, HIGHCUT, sampling_rate)

# Apply the filter to the data
filtered_data = filtfilt(b, a, data)

# Perform FFT on the filtered signal
fft_filtered_data = np.fft.fft(filtered_data)

# Plot the FFT before and after filtering in the same figure
plt.figure()
plt.plot(frequencies[:len(frequencies) // 2], np.abs(fft_data)[:len(frequencies) // 2], label='Original Signal FFT')
plt.plot(frequencies[:len(frequencies) // 2], np.abs(fft_filtered_data)[:len(frequencies) // 2],
         label='Filtered Signal FFT (500 Hz)', linestyle='--')
plt.title('FFT Comparison')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.legend()
plt.grid(True)
plt.show()

# Plot the original and filtered waveforms in the same figure
plt.figure()
plt.plot(time, data, label='Original Signal')  # Subsample the data for performance
plt.plot(time, filtered_data, label='Filtered Signal (500 Hz)', linestyle='--')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.title('Waveform Comparison')
plt.legend()
plt.grid(True)
plt.show()
