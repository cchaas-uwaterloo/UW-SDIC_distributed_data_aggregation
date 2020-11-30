from collections import namedtuple

'''
Brief : reads list of data points from a specified PI point on the PI server
args : 
client_ (PIWebAPIClient) PIWebApiClient object for read and write operations
point_name_ (string) name of the PI point to read from
start_time_ (string) beginning of query window in PI time formatting (can use *-<n>y to effectively select all data)
end_time_ (string) end of query window in PI time formatting (wildcard operator * used to specify now)
return : 
void
'''


def readPIPoint(client_, point_name_, start_time_, end_time_):

    point_path = "pi:\\\\SDICPI\\" + point_name_
    DataPoint = namedtuple('DataPoint', ['value', 'timestamp'])
    data_list = []

    try:
        df1 = client_.data.get_recorded_values(point_path, start_time=start_time_, end_time=end_time_)
    except:
        print('ERROR: Failed to read data for Point [', point_name_,
              '] this point does not exist in the SDIC PI database')
    else:
        print('Point [', point_name_, '] read successfully')

        data_values = df1['Value']
        data_timestamps = df1['Timestamp']

        for index in range(data_values.size):
            this_point = DataPoint(data_values[index], data_timestamps[index])
            data_list.append(this_point)

        return data_list

    return None


