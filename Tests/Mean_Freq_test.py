from Operations import getFrequencySpectrum
from Downloaders import readLMSData
import matplotlib.pyplot as plt
from Util import segmentList, reformatTimeStampLMS
from collections import namedtuple
from PI_Interface import connectToPIServer, writeToPI, createPIPoints

import os

# Use LMS recorded data
target_file_path = 'C:/Users/camer/Desktop/Fall 2020 URI/oct_7_site/Data/APM_OCT14_2020_GATE120_SPEED1.txt'

print(target_file_path)

# Config_
INPUT_TO_WRITE = 'Input1'

if INPUT_TO_WRITE == 'Input1':
    print("Reading Input1 data")
    raw_data_list, abs_file_time = readLMSData(target_file_path, 'Input1')
elif INPUT_TO_WRITE == 'Input2':
    print("Reading Input2 data")
    raw_data_list, abs_file_time = readLMSData(target_file_path, 'Input2')


# segment the run into 10 second intervals and get rms values for each interval
sample_rate_Hz = 40960
segment_length = 5
print("segmenting data:")
segments_Input = segmentList(raw_data_list, (sample_rate_Hz*segment_length))

DataPoint = namedtuple('DataPoint', ['value', 'timestamp'])

# get frequency spectrum for window in middle of run

freq_spectrum,frequencies = getFrequencySpectrum(segments_Input[10], 40960)

print(freq_spectrum)


plt.plot(frequencies, freq_spectrum.real)
plt.show()


