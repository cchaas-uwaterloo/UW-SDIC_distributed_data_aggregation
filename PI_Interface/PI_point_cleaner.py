from osisoft.pidevclub.piwebapi.pi_web_api_client import PIWebApiClient
import csv
import urllib3
from PI_Interface.PI_connection import connectToPIServer

'''
brief : removes PI points based one csv file passed, see example files for formatting details 
args : 
file_path_ (string) path to csv file with point information
return : 
void
'''


def removePIPoints(file_path_, client_):
    urllib3.disable_warnings()

    # Read in point data to add from csv file
    reader = csv.DictReader(open(file_path_))
    print('Points to remove:')

    for row in reader:
        print('Point: ', row['name_point'], row['Class'], row['Type'], row['Future'], row['Description'])

        try:
            temp_point = client_.point.get_by_path("\\\\SDICPI\\" + row['name_point'])
            client_.point.delete(temp_point.web_id)
        except:
            print('WARNING: Point [', row['name_point'], '] could not be removed from the database - delete failed')
        else:
            print('Delete Success, the point [' + row['name_point'] + '] has been removed from the database')
