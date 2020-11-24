from collections import namedtuple
from Util import writeToFile

DataPoint = namedtuple('DataPoint', ['value', 'timestamp'])

# Test data set (timestamp format just a placeholder)
data_point_add_1 = DataPoint(0.6, '2020-11-06 19:58:01.2800')
data_point_add_2 = DataPoint(0.7, '2020-11-06 19:58:02.2800')
data_point_add_3 = DataPoint(0.8, '2020-11-06 19:58:03.2800')
data_point_add_4 = DataPoint(-0.6, '2020-11-06 19:58:04.2800')
data_point_add_5 = DataPoint(-0.7, '2020-11-06 19:58:05.2800')
data_point_add_6 = DataPoint(-0.8, '2020-11-06 19:58:06.2800')
data_point_add_7 = DataPoint(1, '2020-11-06 19:58:07.2800')
data_point_add_8 = DataPoint(0, '2020-11-06 19:58:08.2800')

data_list_test = [data_point_add_1,
                  data_point_add_2,
                  data_point_add_3,
                  data_point_add_4,
                  data_point_add_5,
                  data_point_add_6,
                  data_point_add_7,
                  data_point_add_8]

test_file_name = 'wtf_test.txt'

writeToFile(data_list_test, test_file_name)