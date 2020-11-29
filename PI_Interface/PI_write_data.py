
from Util.Util import reformatTimestamp
from osisoft.pidevclub.piwebapi.models import PIStreamValues, PITimedValue

'''
Brief : writes list of data points to a specified PI point on the PI server 
args : 
data_list_ (namedtuple('dataPoint', ['value', 'timestamp'])) list of data points to write to the PI point
point_name_ (string) name of the PI point to write to
client (PIWebAPIClient) PIWebApiClient object for read and write operations
return : 
void
'''

# TODO add error checking for write operation
# TODO add reformat timestamp from LMS data?


def writeToPI(data_list_, point_name_, client):

    thisCIPoint = client.point.get_by_path("\\\\SDICPI\\" + point_name_)
    thisStreamValue = PIStreamValues()
    thisStreamValue.web_id = thisCIPoint.web_id

    pi_data_list = []

    for data_point in data_list_:
        thisPoint = PITimedValue()
        thisPoint.value = data_point.value
        thisPoint.timestamp = data_point.timestamp
        # thisPoint.timestamp = reformatTimestamp(reformatTimestamp, data_point.timestamp, 0)
        pi_data_list.append(thisPoint)

    thisStreamValue.items = pi_data_list
    response = client.stream.update_values(thisStreamValue.web_id, thisStreamValue.items)
    print('added to point : ', point_name_)
    print(response)
