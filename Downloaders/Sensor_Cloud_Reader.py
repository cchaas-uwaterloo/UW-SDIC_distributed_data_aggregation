import http.client
import xdrlib
from collections import namedtuple


'''
brief : reads data from sensor cloud for one channel of one node beginning and ending at the times specified
args :
device_id_ (string) WSDA device ID (GTAA WSDA: W020000000106730)
key_ (string) open API key for WSDA (GTAA WSDA: f96393da481b1a3de9dda8a2ddf6473d3d5c019380f70be3c84cc2576d800356)
node_name_ (int) 5 digit node identifier
channel_name_ (string) name of channel to read data from
start_time_ (mscl::Timestamp) start time for data to read
end_time_ (mscl::Timestamp) end time for data to read
return : 
data_list (list(namedtuple('DataPoint', ['value', 'timestamp']))) array of tuples with the data values and timestamps
'''

# TODO update to take duration rather than end time to sync with other readers


def readSCData(device_id_, key_, node_name_, channel_name_, start_time_, end_time_):

    # authenticate API key and get token for rest of read operations
    server, auth_token = authenticate_key(device_id_, key_)

    conn = http.client.HTTPSConnection(server)

    url = "/SensorCloud/devices/%s/sensors/%s/channels/%s/streams/timeseries/data/?version=1&auth_token=%s&starttime=%s&endtime=%s" % (
    device_id_, node_name_, channel_name_, auth_token, start_time_, end_time_)
    headers = {"Accept": "application/xdr"}
    print("Downloading data...")
    conn.request("GET", url=url, headers=headers)
    response = conn.getresponse()
    DataPoint = namedtuple('DataPoint', ['value', 'timestamp'])
    data_list = []
    if response.status is http.client.OK:
        print("Data retrieved")
        unpacker = xdrlib.Unpacker(response.read())
        while True:
            try:
                timestamp = unpacker.unpack_uhyper()
                value = unpacker.unpack_float()
                data_point = DataPoint(value, timestamp)
                data_list.append(data_point)
            except Exception as error:
                print(error)
                break
        return data_list
    else:
        print("Status: %s" % response.status)
        print("Reason: %s" % response.reason)
        return data_list


def authenticate_key(device_id, key):
    """
    authenticate with sensorcloud and get the server and auth_key for all subsequent api requests
    """
    auth_server = "sensorcloud.microstrain.com"

    conn = http.client.HTTPSConnection(auth_server)

    headers = {"Accept": "application/xdr"}
    url = "/SensorCloud/devices/%s/authenticate/?version=1&key=%s" % (device_id, key)

    print("authenticating...")
    conn.request('GET', url=url, headers=headers)
    response = conn.getresponse()
    print(response.status, response.reason)

    # if response is 200 ok then we can parse the response to get the auth token and server
    if response.status is http.client.OK:
        print("Credential are correct")

        # read the body of the response
        data = response.read()

        # response will be in xdr format. Create an XDR unpacker and extract the token and server as strings
        unpacker = xdrlib.Unpacker(data)
        auth_token = unpacker.unpack_string()
        server = unpacker.unpack_string()

        print("unpacked xdr.  server:%s  token:%s" % (server, auth_token))

        return server, auth_token
