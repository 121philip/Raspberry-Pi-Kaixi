import nidaqmx
from nidaqmx.constants import AcquisitionType, LoggingMode, LoggingOperation, READ_ALL_AVAILABLE
import matplotlib.pyplot as plt
import numpy as np

# Set a higher sampling rate and increase the number of samples
sampling_rate = 10000  # Sampling rate in Hz
samples_per_channel = 200  # Number of samples to capture

with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Dev2/ai0", min_val=-10.0, max_val=10.0)
    task.timing.cfg_samp_clk_timing(rate=sampling_rate, sample_mode=AcquisitionType.CONTINUOUS)
    data = task.read(number_of_samples_per_channel=samples_per_channel)

    print(data)
    # Generate time values for the x-axis
    time = np.linspace(0, len(data) / sampling_rate, len(data))

    # Plot the waveform with time on the x-axis
    plt.plot(time, data)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('Waveform')
    plt.grid(True)
    plt.show()
