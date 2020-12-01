from Util import reformatTimestamp
from Util import reformatTimeStampLMS
from collections import namedtuple

DataPoint = namedtuple('DataPoint', ['value', 'timestamp'])
data_point_add_1 = DataPoint(0.6, '2020-11-07 13:31:01.2800')

PI_stamp = reformatTimestamp(reformatTimestamp, data_point_add_1.timestamp, 0)

print(PI_stamp)

abs_LMS_time = ['2020-10-14', '15:59:32', 'ms', '773.595']
rel_LMS_time = '56.3333'

PI_stamp2 = reformatTimeStampLMS(rel_LMS_time, abs_LMS_time)

print(PI_stamp2)
