from PI_Interface import readPIPoint, connectToPIServer

client, dataServer = connectToPIServer("admin-stan", "BT5mR,!R")

read_data = readPIPoint(client, 'Escalator_1230_RMS', '*-1y', '*')

print(read_data)

read_data = readPIPoint(client, 'gibberish', '*-1y', '*')

print(read_data)