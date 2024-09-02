import serial
import time
from opcua import Client

class SubHandler:
    """
    Subscription Handler. Receives notifications from server for a subscription.
    """

    def datachange_notification(self, node, val, data):
        print(f"Data change detected on node {node} with value: {val}")
        send_command(val)

# Open the virtual COM port
ser = serial.Serial(
    port="/dev/ttyACM0",  # This might be /dev/ttyUSB0 depending on your setup
    baudrate=9600,  # Set this according to your device's specification
    timeout=1,
    parity=serial.PARITY_EVEN,
)

# Function to send a command and read the response
def send_command(command):
    print(f"Sending command: {command.strip()}")
    ser.write(command.encode("utf-8"))  # Send the command
    time.sleep(0.5)  # Wait a moment for the device to process the command
    if ser.in_waiting > 0:  # Check if there's a response
        response = ser.read(ser.in_waiting).decode("utf-8")  # Read response
        print(f"Response: {response.strip()}")
    else:
        print("No response received.")

# Define the OPC UA server URL and Node ID
url = "opc.tcp://192.168.7.2:4841"

# Create and configure the OPC UA client
client = Client(url=url)

try:
    client.connect()
    print("Client connected to OPC UA server")

    # Get the namespace index from the server
    idx = client.get_namespace_index("http://example.org/opcuapy")
    node = client.get_node("ns={};i=2".format(idx))

    # Create a subscription handler
    handler = SubHandler()
    subscription = client.create_subscription(500, handler)
    monitored_item = subscription.subscribe_data_change(node, queuesize=10)

    # Keep the script running to receive notifications
    try:
        while True:
            time.sleep(1)  # Sleep to keep the client alive and processing messages
    except KeyboardInterrupt:
        print("Subscription terminated by user.")

finally:
    # Disconnect the client when done
    subscription.delete()
    client.disconnect()
    print("Client disconnected")
    ser.close()

