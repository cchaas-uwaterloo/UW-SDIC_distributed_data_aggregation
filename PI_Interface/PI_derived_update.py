from collections import namedtuple
from PI_Interface import readPIPoint, writeToPI
from Operations import calculateStdev, calculateMean

# TODO carry through error checking for read and write operations


def updateSPCvalue(client_, dataserver_, source_point_, target_point_, value_type_, start_time_='*-5y', end_time_='*'):
    source_values = readPIPoint(client_, source_point_, start_time_, end_time_)

    # these values represent the latest updates so trailing timestamps will be used
    if value_type_ == 'mean':
        update_value = calculateMean(source_values, 'trailing')
    elif value_type_ == 'stdev':
        update_value = calculateStdev(source_values, 'trailing')

    data_list = [update_value]

    writeToPI(data_list, target_point_, client_)

    return True










