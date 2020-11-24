from Downloaders import readLMSData
from Operations import calculateRMS
from Util import segmentList
import os

# Get data file path
target_file_path = os.path.dirname(__file__)
dir_index = target_file_path.rfind('/')
target_file_path = target_file_path[:dir_index]
# Config_
target_file_path = target_file_path + '/Data/APM_OCT14_2020escalator1.txt'
print(target_file_path)

# Config_
print("Reading Input1 data")
raw_data_list_Input1 = readLMSData(target_file_path, 'Input1')

print("Reading Input2 data")
raw_data_list_Input2 = readLMSData(target_file_path, 'Input2')

# Get the RMS value for the entire run
run_rms_Input1 = calculateRMS(raw_data_list_Input1)
run_rms_Input2 = calculateRMS(raw_data_list_Input2)

# segment the run into 10 second intervals and get rms values for each interval
sample_rate_Hz = 40960
segment_length = 10
print("segmenting Input1 data:")
segments_Input1 = segmentList(raw_data_list_Input1, (sample_rate_Hz*segment_length))
print("segmenting Input2 data:")
segments_Input2 = segmentList(raw_data_list_Input2, (sample_rate_Hz*segment_length))

segments_Input1_rms = []
segments_Input2_rms = []

for segment in segments_Input1:
    segment_rms = calculateRMS(segment)
    segments_Input1_rms.append(segment_rms)

for segment in segments_Input2:
    segment_rms = calculateRMS(segment)
    segments_Input2_rms.append(segment_rms)

# write to console
print('-------------------------------------------')
print('SUMMARY')
print('Overall run indicators:')
print('Input1:')
print('RMS: ', run_rms_Input1.value)
print('Input2:')
print('RMS:', run_rms_Input2.value)
print(' ')
print('Segmented run indicators:')
print('Input1:')
print('RMS:')
for value in segments_Input1_rms:
    print(value.value)
print('Input2:')
print('RMS:')
for value in segments_Input2_rms:
    print(value.value)

# write to file
# Config_
file_name_ = 'OCT14_2020escalator1_analysis.txt'
cur_path = os.path.dirname(__file__)
file_path = os.path.relpath(('..\\Data\\' + file_name_), cur_path)

file = open(file_path, 'x')

file.write('-------------------------------------------\n')
file.write('SUMMARY\n')
file.write('Overall run indicators:\n')
file.write('Input1:\n')
file.write('RMS: ' + str(run_rms_Input1.value) + '\n')
file.write('Input2:\n')
file.write('RMS:' + str(run_rms_Input2.value) + '\n')
file.write('\n')
file.write('Segmented run indicators: (' + str(segment_length) + 's) \n')
file.write('Input1:\n')
file.write('RMS:\n')
for value in segments_Input1_rms:
    file.write(str(value.value) + '\n')
file.write('Input2:\n')
file.write('RMS:\n')
for value in segments_Input2_rms:
    file.write(str(value.value) + '\n')

file.close()
