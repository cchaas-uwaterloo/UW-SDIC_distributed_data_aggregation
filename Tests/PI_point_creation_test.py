from osisoft.pidevclub.piwebapi.pi_web_api_client import PIWebApiClient
from osisoft.pidevclub.piwebapi.models import PIAnalysis, PIItemsStreamValues, PIStreamValues, PITimedValue, PIRequest, PIResponse, PIPoint


client = PIWebApiClient("https://sdicpi/piwebapi", useKerberos=False, username="admin-stan", password="BT5mR,!R", verifySsl=False)

# Pull data server WebID for point creation
dataServer = client.dataServer.get_by_path("\\\\SDICPI")

# Create new PIPoints for each test sensor datastream

# Sensor 1
# Vibration
# Principle component 1
newTestPoint1 = PIPoint()

newTestPoint1.name = "Microstrain_vibration_1"

newTestPoint1.point_class = "classic"
newTestPoint1.point_type = "float32"
newTestPoint1.future = False

newTestPoint1.descriptor = "Microstrain 1 vibration test feed"

res1 = client.dataServer.create_point_with_http_info(dataServer.web_id, newTestPoint1)
