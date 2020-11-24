from osisoft.pidevclub.piwebapi.pi_web_api_client import PIWebApiClient
import urllib3

'''
Brief : gets data server connection with PI server, required for any read/write operations 
args : 
username_ (string) Cam: admin-cchaas, Stan: admin-stan
password_ (string) Cam: Flowerstation1981*, Stan: BT5mR,!R
returns : 
client (PIWebAPIClient) PIWebApiClient object for read and write operations
data_server (PIDataArchiveWebId) PIDataArchiveWebId object for point creation and deletion 
'''

# TODO add error checking to connection


def connectToPIServer (username_, password_):
    urllib3.disable_warnings()

    client = PIWebApiClient("https://sdicpi/piwebapi", useKerberos=False, username=username_, password=password_,
                            verifySsl=False)
    data_server = client.dataServer.get_by_path("\\\\SDICPI")

    return client, data_server
