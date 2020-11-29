import os
import math

'''
brief : converts LORD timestamps to PI timestamps
args :
input_stamp_ (string) timestamp in LORD format
correction_ (int) hour offset between WSDA time and computer/server time (can be used to correct timezone issues)
returns : 
returnString (string) timestamp in PI format
'''


def reformatTimestamp(self, input_stamp_, correction_):
    # write and retrieve timestamp data from MSCL point to and from file
    # str() method to access data from Timestamp class is not implemented in python (at all?)
    # without further documentation, the implicit return to the print() function is the only way to access this data
    # this process is slow - would be better if something faster could be implemented
    if os.path.exists("Buffer.txt"):
        os.remove("Buffer.txt")
    buffer = open("Buffer.txt", "x")
    print(input_stamp_, file=buffer)
    buffer.close()
    buffer = open("Buffer.txt", "r")
    stampstring = buffer.read()
    buffer.close()
    os.remove("Buffer.txt")

    # string manipulation to generate PI compatible timestamp
    # Example timestamp format from PIWebAPI "2020-07-07T19:58:01.2800445Z"
    returnstring = stampstring.replace(' ', 'T', 1)
    returnstring = returnstring.replace(' ', '')

    # TODO unhack this by setting the correct system time on the gateway
    hourIndex = returnstring.find('T') + 1
    hour = returnstring[hourIndex] + returnstring[hourIndex + 1]
    hour = int(hour) - correction_
    oldhour = ('T' + returnstring[hourIndex] + returnstring[hourIndex + 1])
    if hour > 9:
        newhour = 'T' + str(hour)
    else:
        newhour = 'T' + '0' + str(hour)
    returnstring = returnstring.replace(oldhour, newhour)

    return returnstring


'''
brief : writes one channel of data to a file
args :
data_list_ (list(namedtuple('dataPoint', ['value', 'timestamp']))) array of tuples with the data values and their timestamps
file_name_ (string) path of file to write to (.txt)
returns : 
None
'''


def writeToFile(data_list_, file_name_):
    cur_path = os.path.dirname(__file__)
    file_path = os.path.relpath(('..\\Data\\' + file_name_), cur_path)

    file = open(file_path, 'x')

    for data_point in data_list_:
        data_string = str(data_point.value) + ' : ' + str(data_point.timestamp)
        file.write(data_string + "\n")

    file.close()

    print('data successfully written to: ', file_path)


'''
brief : breaks one data list object into n smaller lists of length seg_length_
args :
data_list_ (list(namedtuple('dataPoint', ['value', 'timestamp']))) array of tuples with the data values and their timestamps
seg_length_ (int) number of samples in each segment
returns : 
segment_list (list(list(namedtuple('dataPoint', ['value', 'timestamp'])))) 2nd order list of smaller data lists 
'''


def segmentList(data_list_, seg_length_):
    segment_list = []
    segment_index = -1
    num_segments = math.ceil(len(data_list_) / seg_length_)

    for index in range(num_segments):
        segment = []
        segment_list.append(segment)

    for index, data_point in enumerate(data_list_):
        if index % seg_length_ == 0:
            segment_index += 1
        segment_list[segment_index].append(data_point)

    return segment_list


'''
brief : reformats LMS timestamp data to PI server format for upload
args :
input_stamp_ (string) relative timestamp of the data point (in s)
file_start_time_ (string) absolute start time of the collection run
returns : 
output_string (string) absolute time of the data point in PI server format 
'''
# TODO update to add preceding zeros to hour, minute, second fields


def reformatTimeStampLMS(input_stamp_, file_start_time_):
    # Assume data is not collected over midnight
    date = file_start_time_[0]

    # [0] = hour, [1] = minute, [2] = second
    start_time = file_start_time_[1].split(':')

    # [3] = millisecond
    start_time.append(file_start_time_[3])

    start_time[0] = float(start_time[0])
    start_time[1] = float(start_time[1])
    start_time[2] = float(start_time[2])
    start_time[3] = float(start_time[3])
    input_stamp = float(input_stamp_)

    start_time[3] += (input_stamp % 1) * 1000
    start_time[3] = math.floor(start_time[3])
    input_stamp = math.floor(input_stamp)
    if start_time[3] >= 1000:
        start_time[2] += 1
        start_time[3] = start_time[3] % 1000

    start_time[2] += input_stamp
    if start_time[2] >= 60:
        start_time[1] += math.floor(start_time[2] / 60)
        start_time[2] = start_time[2] % 60
    if start_time[1] >= 60:
        start_time[0] += 1
        start_time[1] = start_time[1] % 60

    if start_time[0] < 10:
        start_time[0] = '0' + str(int(start_time[0]))
    else:
        start_time[0] = str(int(start_time[0]))

    if start_time[1] < 10:
        start_time[1] = '0' + str(int(start_time[1]))
    else:
        start_time[1] = str(int(start_time[1]))

    if start_time[2] < 10:
        start_time[2] = '0' + str(int(start_time[2]))
    else:
        start_time[2] = str(int(start_time[2]))

    out_string = str(date) + 'T' + start_time[0] + ':' + start_time[1] + ':' \
                 + start_time[2] + '.' + str(int(start_time[3]))

    return out_string
