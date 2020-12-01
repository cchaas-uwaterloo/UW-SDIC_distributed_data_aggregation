from PI_Interface import updateSPCvalue, connectToPIServer, createPIPoints
import os
from collections import namedtuple

client, dataServer = connectToPIServer("admin-stan", "BT5mR,!R")

cur_path = os.path.dirname(__file__)
file_path = os.path.relpath(('..\\PI_Interface\\' + 'Point_builder.csv'), cur_path)

createPIPoints(file_path, client, dataServer)

source_point = 'APM_Gate_120_RMS'
target_point_mean = 'Unit_test_1_mean'
target_point_stdev = 'Unit_test_1_stdev'

update_success_mean = updateSPCvalue(client, source_point, target_point_mean, 'mean')

print(update_success_mean)

update_success_stdev = updateSPCvalue(client, source_point, target_point_stdev, 'stdev')

print(update_success_stdev)