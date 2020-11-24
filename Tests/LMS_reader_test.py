from Downloaders import readLMSData
import os

target_file_path = os.path.dirname(__file__)
dir_index = target_file_path.rfind('/')
target_file_path = target_file_path[:dir_index]
target_file_path = target_file_path + '/Data/APM_OCT14_2020_GATE120_SPEED2.txt'
print(target_file_path)

data_list = readLMSData(target_file_path, 'Input2')


