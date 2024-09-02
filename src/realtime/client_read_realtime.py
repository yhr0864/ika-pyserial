from opcua import Client
from opcua import ua
import time


class SubHandler:
    """
    Subscription Handler. Receives notifications from server for a subscription.
    """

    def datachange_notification(self, node, val, data):
        print(f"Data change detected on node {node} with value: {val}")


# Define the OPC UA server URL
server_url = "opc.tcp://localhost:4842"  # Replace with your server URL

# Create a client instance and connect to the server
client = Client(server_url)
client.connect()

try:
    # Define the node ID you want to monitor
    node_id = "ns=2;i=2"  # Replace with your actual node ID

    # Get the node to monitor
    node = client.get_node(node_id)

    # Create a subscription handler
    handler = SubHandler()
    subscription = client.create_subscription(500, handler)
    monitored_item = subscription.subscribe_data_change(node, queuesize=10)

    print(f"Subscribed to node {node_id}. Waiting for data changes...")

    # Keep the script running to receive notifications
    try:
        while True:
            time.sleep(1)  # Sleep to keep the client alive and processing messages
    except KeyboardInterrupt:
        print("Subscription terminated by user.")

finally:
    # Unsubscribe and disconnect
    subscription.delete()
    client.disconnect()
    print("Disconnected from server")
