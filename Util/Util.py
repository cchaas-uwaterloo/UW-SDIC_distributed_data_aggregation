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
    hour = returnstring[hourIndex] + returnstring[hourIndex+1]
    hour = int(hour) - correction_
    oldhour = ('T'+returnstring[hourIndex]+returnstring[hourIndex+1])
    if hour > 9:
        newhour = 'T'+str(hour)
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







