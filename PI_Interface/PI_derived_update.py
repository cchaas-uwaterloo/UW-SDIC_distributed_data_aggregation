from collections import namedtuple
from PI_Interface import readPIPoint, writeToPI
from Operations import calculateStdev, calculateMean

'''
brief : updates Statistical Process Control values for specified PI data, by default the entire data history is used to 
        update limits
args : 
client_ (PIWebAPIClient) PIWebApiClient object for read and write operations
source_point_ (string) name of PI point to update SPC limits for 
target_point_ (string) name of PI point holding desired SPC limit
value_type_ (string) either: 'mean', 'stdev' type of SPC limit component to calculate and write to 
start_time_ (string) optional, start time for sample to calculate from (by default the last five years)
end_time_ (string) optional, end time for sample to calculate from (be default now)
return : 
True
'''
# TODO carry through error checking for read and write operations


def updateSPCvalue(client_, source_point_, target_point_, value_type_, start_time_='*-5y', end_time_='*'):
    source_values = readPIPoint(client_, source_point_, start_time_, end_time_)

    # these values represent the latest updates so trailing timestamps will be used
    if value_type_ == 'mean':
        update_value = calculateMean(source_values, 'trailing')
    elif value_type_ == 'stdev':
        update_value = calculateStdev(source_values, 'trailing')

    data_list = [update_value]

    writeToPI(data_list, target_point_, client_)

    return True










