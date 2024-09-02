from opcua import Client
import time

# Define the OPC UA server URL
# url = "opc.tcp://129.13.79.172"
url = "opc.tcp://192.168.7.2:4841"

# Create and connect the client
client = Client(url)

try:
    client.connect()
    print("Client connected to OPC UA server")

    # Get the namespace index from the server
    idx = client.get_namespace_index("http://example.org/opcuapy")
    node = client.get_node("ns={};i=2".format(idx))

    # Write a new value to the variable
    commands = [
        "IN_NAME\r\n",  # read the device name
        "OUT_SP_1 30\r\n",  # set temperature value 30
        "OUT_SP_4 150\r\n",  # set speed value 150
        "START_1\r\n",  # start the heater
        "START_4\r\n",  # start the motor
    ]

    for command in commands:
        node.set_value(command)
        print(f"Written command: {command}")

        time.sleep(1)

except KeyboardInterrupt:
    print("Client stopped manually")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    client.disconnect()
    print("Client disconnected")
