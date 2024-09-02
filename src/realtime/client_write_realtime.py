from opcua import Client
import time


class SubHandler:
    """
    Subscription Handler. To receive events from server for a subscription.
    """

    def datachange_notification(self, node, val, data):
        print(f"Data change detected on node {node} with value: {val}")


# Define the OPC UA server URL
# url = "opc.tcp://localhost:4842"
url = "opc.tcp://192.168.7.2:4841"

# Create and connect the client
client = Client(url)
client.connect()
print("Client connected to OPC UA server")

try:
    # Get the namespace index from the server
    idx = client.get_namespace_index("http://example.org/opcuapy")

    node = client.get_node("ns={};s=Command".format(idx))

    handler = SubHandler()
    subscription = client.create_subscription(500, handler)
    monitored_item = subscription.subscribe_data_change(node, queuesize=10)

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
    subscription.delete()
    client.disconnect()
    print("Client disconnected")
