import mscl
from collections import namedtuple
import sys


'''
brief : reads data from one channel of a connected node beginning at the specified start time for the duration specified
args :
node_number_ (int) five digit node identifier
channel_ (string) channel name
start_time_ (mscl::Timestamp) start time for data to read
start_time_ (litteral string "start") configures to read from start of node's logged data
duration_ (int) duration of interval to read in ms
returns : 
data_list (list(namedtuple('dataPoint', ['value', 'timestamp']))) array of tuples with the data values and their timestamps
'''


def readNodeData(self, node_number_, channel_, start_time_, duration_) :

    print(mscl.MSCL_VERSION)

    # Set up LORD basestation
    connection = mscl.Connection.TcpIp("192.168.0.100", 5000)
    basestation = mscl.BaseStation(connection)

    # Init downloaders
    nodeDownloader = namedtuple('nodeDownloader', ['downloader', 'nodeName'])

    # CONFIG_ Instantiate node
    node = mscl.WirelessNode(node_number_, basestation)

    # Set all nodes to idle and check connection

    try:
        idleStatus = node.setToIdle()

        while not idleStatus.complete():
            print(".")

        result = idleStatus.result()
        if result == mscl.SetToIdleStatus.setToIdleResult_success:
            print("Node", node.nodeAddress(), "is now in idle mode.")
            response = node.ping()
            if response.success():
                response.baseRssi()  # the BaseStation RSSI
                response.nodeRssi()  # the Node RSSI
                print("Node", node.nodeAddress(), "connected.")
                print("Number of Datalog sessions stored on node: " + str(node.getNumDatalogSessions()))
            else:
                print('failed to communicate with node: ' + str(node.nodeAddress()) + ' Aborting...')
                sys.exit(0)

    except EOFError:
        print("EOFError: failed to connect to Node", node.nodeAddress())

    # CONFIG_ Create downloader objects for each active node

    node_data_downloader = nodeDownloader(mscl.DatalogDownloader(node), str(node_number_))


    # Sample from logs

    DataPoint = namedtuple('DataPoint', ['value', 'timestamp'])
    data_list = []

    end_reached = False

    if start_time_ != "start":
        start_time = start_time_
        end_time = mscl.TimeSpan.MilliSeconds(duration_)
    else:
        start_time = 0
        end_time = 0

    while not end_reached:

        if nodeDownloader.downloader.complete():
            end_reached = True
            break

        sweep = node_data_downloader.downloader.getNextData()
        data = sweep.data()
        timestamp = sweep.timestamp()

        if start_time == 0: 
            start_time = sweep.timestamp()
            
        delta_time = timestamp - start_time
        
        if delta_time > end_time:
            end_reached = True
            break

        if sweep.timestamp >= start_time:
            for point in data:
                if point.channelName == channel_:
                    print(point.as_string())
                    print(sweep.timestamp())
                    data_point_add = DataPoint(float(point.as_string()), timestamp)
                    data_list.append(data_point_add)

    print("Data downloaded successful.")

    return data_list


