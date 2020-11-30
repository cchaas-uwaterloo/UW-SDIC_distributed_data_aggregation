from PI_Interface import writeToPI, createPIPoints, connectToPIServer
from collections import namedtuple
import os

DataPoint = namedtuple('DataPoint', ['value', 'timestamp'])

# Test data set (timestamp format just a placeholder)
data_point_add_1 = DataPoint(0.6, '2020-11-07 13:31:01.2800')
data_point_add_2 = DataPoint(0.7, '2020-11-07 11:30:02.2800')
data_point_add_3 = DataPoint(0.8, '2020-11-07 13:12:03.2800')
data_point_add_4 = DataPoint(-0.6, '2020-11-07 13:12:04.2800')
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

client, dataServer = connectToPIServer("admin-stan", "BT5mR,!R")

cur_path = os.path.dirname(__file__)
file_path = os.path.relpath(('..\\PI_Interface\\' + 'Point_builder.csv'), cur_path)

createPIPoints(file_path, client, dataServer)

writeToPI(data_list_test, "Unit_test_1", client)

writeToPI(data_list_test, "Gibberish", client)
