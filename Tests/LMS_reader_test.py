from Downloaders import readLMSData
import os

# for local data files
'''
target_file_path = os.path.dirname(__file__)
dir_index = target_file_path.rfind('/')
target_file_path = target_file_path[:dir_index]
target_file_path = target_file_path + '/Data/APM_OCT14_2020_GATE120_SPEED2.txt'
'''

# for other data files
target_file_path = 'C:/Users/camer/Desktop/Fall 2020 URI/oct_7_site/Data/APM_OCT14_2020_GATE120_SPEED2.txt'

print(target_file_path)

data_list, abs_time = readLMSData(target_file_path, 'Input2')

print(abs_time)


