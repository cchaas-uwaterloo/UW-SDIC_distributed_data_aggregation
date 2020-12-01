from Downloaders import readLMSData
from Operations import calculateRMS
from Util import segmentList, reformatTimeStampLMS
from collections import namedtuple
from PI_Interface import connectToPIServer, writeToPI, createPIPoints

import os

# Get data file path

# Local data files
'''
target_file_path = os.path.dirname(__file__)
dir_index = target_file_path.rfind('/')
target_file_path = target_file_path[:dir_index]
# Config_
target_file_path = target_file_path + '/Data/APM_OCT14_2020escalator1.txt'
'''

# Other data files
target_file_path = 'C:/Users/camer/Desktop/Fall 2020 URI/oct_7_site/Data/APM_OCT14_2020escalator1.txt'

target_write_point = 'Escalator_1230_RMS_Speed2'

print(target_file_path)

# Config_
INPUT_TO_WRITE = 'Input1'

if INPUT_TO_WRITE == 'Input1':
    print("Reading Input1 data")
    raw_data_list, abs_file_time = readLMSData(target_file_path, 'Input1')
elif INPUT_TO_WRITE == 'Input2':
    print("Reading Input2 data")
    raw_data_list, abs_file_time = readLMSData(target_file_path, 'Input2')

# Get the RMS value for the entire run
run_rms = calculateRMS(raw_data_list)

# segment the run into 10 second intervals and get rms values for each interval
sample_rate_Hz = 40960
segment_length = 5
print("segmenting data:")
segments_Input = segmentList(raw_data_list, (sample_rate_Hz*segment_length))

segments_Input_rms = []

DataPoint = namedtuple('DataPoint', ['value', 'timestamp'])

for segment in segments_Input:
    segment_rms = calculateRMS(segment)
    segment_rms_PI = DataPoint(segment_rms.value, reformatTimeStampLMS(segment_rms.timestamp, abs_file_time))
    segments_Input_rms.append(segment_rms_PI)

# write to console
print('-------------------------------------------')
print('SUMMARY')
print('Absolute run time: ', abs_file_time)
print('Overall run indicators:')
print('RMS: ', run_rms.value)
print(' ')
print('Segmented run indicators:')
print('RMS:')
for value in segments_Input_rms:
    print(value.value, ' : ', value.timestamp)

# Write to PI

client, dataServer = connectToPIServer("admin-stan", "BT5mR,!R")

cur_path = os.path.dirname(__file__)
file_path = os.path.relpath(('..\\PI_Interface\\' + 'Point_builder.csv'), cur_path)

createPIPoints(file_path, client, dataServer)

writeToPI(segments_Input_rms, target_write_point, client)



