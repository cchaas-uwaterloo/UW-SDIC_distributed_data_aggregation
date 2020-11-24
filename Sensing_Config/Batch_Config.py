import mscl
from collections import namedtuple
from Util.Util import reformatTimestamp
import csv
from osisoft.pidevclub.piwebapi.pi_web_api_client import PIWebApiClient
from osisoft.pidevclub.piwebapi.models import PIStreamValues, PITimedValue
import urllib3
import sys
from datetime import datetime

urllib3.disable_warnings()

print(mscl.MSCL_VERSION)

# '''''''''''''''''''''''''''''''''''''''''''''''''''''''' #
# '''''''''''''' Initialize API Connections '''''''''''''' #
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''' #

# Set up LORD basestation
connection = mscl.Connection.TcpIp("192.168.0.100", 5000)
basestation = mscl.BaseStation(connection)

# Set up PI Server connection
client = PIWebApiClient("https://sdicpi/piwebapi", useKerberos=False, username="admin-stan", password="BT5mR,!R",
                        verifySsl=False)
dataServer = client.dataServer.get_by_path("\\\\SDICPI")

# '''''''''''''''''''''''''''''''''''''''''''''''''''''''' #
# '''''''''''' Configure Sensor Connections '''''''''''''' #
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''' #

# Init nodes
nodeList = []

# CONFIG_
SYNC = True
PI_CONNECTION = False
LOGGING = True

# CONFIG_ Node -> Asset config
nodeAssetLookup = {
    '29289': 'EBW01/02',
    '29290': 'Asset_2',
    '29291': 'Asset_3',
    '29292': 'Asset_4',
    '29293': 'Asset_5',
    '4660': 'BeaconEcho',  # time sync beacon for network
}

# CONFIG_ Channel -> Point config
channelPropertyLookup = {
    'ch1': 'accel_x',
    'ch2': 'accel_y',
    'ch3': 'accel_z',
    'ch1_rms': 'accel_x_rms',
    'ch2_rms': 'accel_y_rms',
    'ch3_rms': 'accel_z_rms',
    'diagnostic_internalTemp': 'temp',
    'beaconEcho': 'beaconEcho'  # time sync beacon for network
}

# CONFIG_ Instantiate active nodes
node29289 = mscl.WirelessNode(29289, basestation)
# node29290 = mscl.WirelessNode(29290, basestation)
# node29291 = mscl.WirelessNode(29291, basestation)
# node29292 = mscl.WirelessNode(29292, basestation)
# node29293 = mscl.WirelessNode(29293, basestation)

# CONFIG_ Add active nodes to node list
nodeList.append(node29289)
# nodeList.append(node29290)
# nodeList.append(node29291)
# nodeList.append(node29292)
# nodeList.append(node29293)

# '''''''''''''''''''''''''''''''''''''''''''''''''''''''' #
# '''''''''''' Configure PI Point Connections '''''''''''' #
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''' #

# CONFIG_ Generate lists to store data for each point to write to (from point builder .csv)
nodesDataList = []

PointWrapper = namedtuple('PointWrapper', ['name_point', 'asset', 'property', 'dataList', 'streamValue'])

reader = csv.DictReader(open('Point_builder.csv'))
for row in reader:
    thisPointDataList = []
    thisCIPoint = client.point.get_by_path("\\\\SDICPI\\" + row['name_point'])
    thisStreamValue = PIStreamValues()
    thisStreamValue.web_id = thisCIPoint.web_id
    if row['Asset'] != 'NA' and row['Property'] != 'NA':
        thisPointWrapper = PointWrapper(row['name_point'], row['Asset'], row['Property'], thisPointDataList,
                                        thisStreamValue)
        nodesDataList.append(thisPointWrapper)

# Set all nodes to idle and check connection
for node in nodeList:
    try:
        idleStatus = node.setToIdle()

        while not idleStatus.complete():
            print(".")

        result = idleStatus.result()
        if result == mscl.SetToIdleStatus.setToIdleResult_success:
            print("Node", node.nodeAddress(), "is now in idle mode.")
            response = node.ping()
            if response.success():
                response.baseRssi()
                response.nodeRssi()
                print("Node", node.nodeAddress(), "connected.")
                print("Number of Datalog sessions stored on node: " + str(node.getNumDatalogSessions()))
            else:
                print('failed to communicate with node: ' + str(node.nodeAddress()) + ' Aborting...')
                sys.exit(0)

    except EOFError:
        print("EOFError: failed to connect to Node", node.nodeAddress())

# create a WirelessNodeConfig which is used to set all node configuration options
config = mscl.WirelessNodeConfig()

config.inactivityTimeout(7200)
config.sampleRate(mscl.WirelessTypes.sampleRate_32Hz)
config.derivedDataRate(mscl.WirelessTypes.sampleRate_1Hz)
config.unlimitedDuration(True)

# CONFIG_ enable desired sampling channels:
# TODO Automate this based on the channel dictionary

baseChannelMask = mscl.ChannelMask()
baseChannelMask.enable(1, True)         # x_accel
# baseChannelMask.enable(2, True)       # y_accel
# baseChannelMask.enable(3, True)       # z_accel
# baseChannelMask.enable(143, True)     # x_rms
# baseChannelMask.enable(144, True)     # y_rms
# baseChannelMask.enable(145, True)     # z_rms

config.activeChannels(baseChannelMask)

# TODO Check raw and derived mode enabled vs actual enabled channels

# config.dataMode(mscl.WirelessTypes.dataMode_raw)          # use if only raw channels enabled
config.dataMode(mscl.WirelessTypes.dataMode_derived)        # use if only derived channels enabled
config.dataMode(mscl.WirelessTypes.dataMode_raw_derived)    # use if both raw and derived channels enabled

# set event triggered sampling
triggerConfig = mscl.EventTriggerOptions()
xAccelTrigger = mscl.Trigger(1, mscl.WirelessTypes.eventTrigger_ceiling, 1.000)
yAccelTrigger = mscl.Trigger(2, mscl.WirelessTypes.eventTrigger_ceiling, 1.000)
zAccelTrigger = mscl.Trigger(3, mscl.WirelessTypes.eventTrigger_ceiling, 1.000)

triggerConfig.trigger(0, xAccelTrigger)
triggerConfig.trigger(1, yAccelTrigger)
triggerConfig.trigger(2, zAccelTrigger)

triggerConfig.enableTrigger(0, True)
triggerConfig.enableTrigger(1, True)
triggerConfig.enableTrigger(2, True)

triggerConfig.postDuration(15000)   # in ms, time to collect samples after trigger fires
triggerConfig.preDuration(30000)    # in ms, minimum time between triggers firing

config.eventTriggerOptions(triggerConfig)

if SYNC:
    config.samplingMode(mscl.WirelessTypes.samplingMode_sync)
else:
    config.samplingMode(mscl.WirelessTypes.samplingMode_nonSync)

# set the nodes to log and transmit or only to transmit their data
if LOGGING:
    config.dataCollectionMethod(mscl.WirelessTypes.collectionMethod_logAndTransmit)
else:
    config.dataCollectionMethod(mscl.WirelessTypes.collectionMethod_transmitOnly)

print('Data collection method set to: ' + str(config.dataCollectionMethod()))

# apply the configuration to the Nodes
for node in nodeList:
    node.applyConfig(config)
    print("node configuration applied")

# '''''''''''''''''''''''''''''''''''''''''''''''''''''''' #
# ''''''''''''''''''' Start Sensing  ''''''''''''''''''''' #
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''' #

# create sampling network (or start each node sampling individually if sampling asynchronously)
if SYNC:
    network = mscl.SyncSamplingNetwork(basestation)

    # add nodes to the network
    for node in nodeList:
        network.addNode(node)

    network.ok()  # check if the network status is ok
    network.lossless(True)  # enable Lossless for the network
    network.percentBandwidth()  # get the total percent of bandwidth of the network

    # apply the network configuration to every node in the network
    network.applyConfiguration()

    # start all the nodes in the network sampling.
    network.startSampling()
    print("Synchronous sampling started")

else:
    for node in nodeList:
        node.startNonSyncSampling()
    print("Asynchronous sampling started")

# '''''''''''''''''''''''''''''''''''''''''''''''''''''''' #
# '''''' (Optional) Write Data Directly PI Server '''''''' #
# '''''''''''''''''''''''''''''''''''''''''''''''''''''''' #

# TODO determine write time to PI server (highest sampling rate in real time possible)

# TEST_
dataPointCount = 0

start = datetime.now()

while True:

    # get all the data sweeps that have been collected, with a timeout of 500 milliseconds
    sweeps = basestation.getData(500)

    for sweep in sweeps:

        # get the vector of data in the sweep (one sweep for each connected node)
        data = sweep.data()

        print(sweep.nodeAddress(), end=": ")
        print(reformatTimestamp(reformatTimestamp, sweep.timestamp(),0))

        # TEST_
        timeElapsed = datetime.now() - start
        print(timeElapsed)

        # iterate over each point in the sweep (one point per channel of the node in the current sweep)
        for dataPoint in data:
            dataPointCount += 1
            print(dataPointCount)
            print(dataPoint.channelName(), end=': ')
            print(dataPoint.as_string())
            print(sweep.nodeAddress())
            print(nodeAssetLookup[str(sweep.nodeAddress())])
            if 'diagnostic' not in dataPoint.channelName():
                print(channelPropertyLookup[str(dataPoint.channelName())])

            if 'diagnostic' not in dataPoint.channelName() or dataPoint.channelName() == 'diagnostic_internalTemp':
                for point_ in nodesDataList:
                    if nodeAssetLookup[str(sweep.nodeAddress())] == point_.asset and channelPropertyLookup[str(dataPoint.channelName())] == point_.property:
                        if PI_CONNECTION:
                            print('Added to point: ' + point_.name_point)
                            startWrite = datetime.now()
                            thisPoint = PITimedValue()
                            thisPoint.value = dataPoint.as_string()
                            thisPoint.timestamp = reformatTimestamp(reformatTimestamp, sweep.timestamp(),0)
                            point_.dataList.append(thisPoint)
                            point_.streamValue.items = point_.dataList
                            response = client.stream.update_values(point_.streamValue.web_id, point_.streamValue.items)
                            endWrite = datetime.now()
                            writeTime = endWrite-startWrite
                            print(response)
                            print("write time: ", writeTime)
                        if point_.dataList:
                            point_.dataList.pop(0)

