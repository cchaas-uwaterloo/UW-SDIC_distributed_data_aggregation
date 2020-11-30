from osisoft.pidevclub.piwebapi.models import PIPoint
import csv
import urllib3
from PI_Interface.PI_connection import connectToPIServer

'''
brief : creates PI points based one csv file passed, see example files for formatting details 
args : 
file_path_ (string) path to csv file with point information
return : 
void
'''


def createPIPoints(file_path_, client_, dataServer_):
    urllib3.disable_warnings()

    # Read in point data to add from csv file
    reader = csv.DictReader(open(file_path_))

    print('Points to add: ')

    for row in reader:
        print('Point: ', row['name_point'], row['Class'], row['Type'], row['Future'], row['Description'])

        try:
            temp_point = client_.point.get_by_path("\\\\SDICPI\\" + row['name_point'])
        except:
            newPoint = PIPoint()
            newPoint.name = row['name_point']
            newPoint.point_class = row['Class']
            newPoint.point_type = row['Type']
            if row['Future'] == 'True':
                newPoint.future = True
            else:
                newPoint.future = False
            newPoint.descriptor = row['Description']
            res1 = client_.dataServer.create_point_with_http_info(dataServer_.web_id, newPoint)
            print('Add success, the point [' + row['name_point'] + '] has been added to the database')
        else:
            print('WARNING: Point [', row['name_point'], '] already exists in the SDIC PI database - add failed')
