from collections import namedtuple
import sys
import typing

'''
brief : reads data from text file exported from LMS, reads data from a single channel
args :
file_name_ (string) absolute path to the text file, note that directory delimiters must be '/'
channel_ (string) PhysicalChannelID (shown in header of the text file) eg. 'Input1', 'Input2'
returns : 
data_list (list(namedtuple('dataPoint', ['value', 'timestamp']))) array of tuples with the data values and their timestamps
*Note timestamps from LMS are stored relative to the start of the run 
'''
# TODO: Add conversion from relative to absolute time and further to PI date/time format

DataPoint = namedtuple('DataPoint', ['value', 'timestamp'])


def readLMSData(file_name_, channel_):

    data_list = []
    at_data = False
    num_lines_indicator = 'Number of lines'
    num_lines = 1
    current_line = 0
    preamble_delimiter = "Y axis unit	g"
    abs_time_line = 2
    line_index = 0
    abs_time = []

    print("Download progress:")

    with open(file_name_, 'r') as file:

        # reading each line
        for line in file:
            timestamp = 0
            data = 0

            if line_index == abs_time_line:
                time_line_words = line.split()
                abs_time = time_line_words[2:6]

            # reading each word
            for pos, word in enumerate(line.split()):

                if word == channel_:
                    channel_pos = pos

                if at_data:

                    if pos == 0:
                        timestamp = float(word)

                    if pos == channel_pos:
                        data = float(word)

            if at_data:
                current_line += 1
                data_point_add = DataPoint(float(data), float(timestamp))
                data_list.append(data_point_add)
                progress = int(current_line/int(num_lines)*100)
                sys.stdout.flush()
                sys.stdout.write("%d%%   \r" % progress)

            if preamble_delimiter in line:
                at_data = True
            if num_lines_indicator in line:
                num_lines = line.split()[3]

            line_index += 1

    print('Complete')
    return data_list, abs_time

