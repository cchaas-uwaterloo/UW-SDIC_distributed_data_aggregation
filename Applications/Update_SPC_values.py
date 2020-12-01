from PI_Interface import connectToPIServer, updateSPCvalue, createPIPoints
import os
import csv

client, dataServer = connectToPIServer("admin-stan", "BT5mR,!R")

# Create any missing PI points
cur_path = os.path.dirname(__file__)
builder_file_path = os.path.relpath(('..\\PI_Interface\\' + 'Point_builder.csv'), cur_path)
link_file_path = os.path.relpath(('..\\Config\\' + 'SPC_links.csv'), cur_path)

createPIPoints(builder_file_path, client, dataServer)

# Read in SPC point linking data from config file
reader = csv.DictReader(open(link_file_path))

print('Updating the following SPC points: ')

for row in reader:
    print('Link: ', row['base_point'], row['mean_point'], row['stdev_point'])

    source_point = row['base_point']
    target_point_mean = row['mean_point']
    target_point_stdev = row['stdev_point']

    # Update the mean point
    update_success = updateSPCvalue(client, source_point, target_point_mean, 'mean')

    # Update the standard devation point
    update_success = updateSPCvalue(client, source_point, target_point_stdev, 'stdev')

    print('--> Update successful')
