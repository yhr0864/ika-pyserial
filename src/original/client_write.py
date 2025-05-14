from opcua import Client
import time

nodes = {
    "GET_NAME": "ns=2;i=2",
    "READ_TEMP": "ns=2;i=5",
    "SET_TEMP": "ns=2;i=3",
    "START_HEATER": "ns=2;i=4",
}


class HotplateClient:
    def __init__(self, server_url, namespace_uri, node_id=2):
        self.server_url = server_url
        self.namespace_uri = namespace_uri
        self.node_id = node_id
        self.client = Client(self.server_url)
        self.node = None

    def connect(self):
        self.client.connect()
        print(f"Connected to OPC UA server at {self.server_url}")
        self.node_objects = {
            key: self.client.get_node(value) for key, value in nodes.items()
        }

    def disconnect(self):
        self.client.disconnect()
        print("Disconnected from OPC UA server")

    def execute(self, node: str, command):
        self.node_objects[node].set_value(command)


if __name__ == "__main__":
    SERVER_URL = "opc.tcp://localhost:4841"
    NAMESPACE_URI = "http://emap.kit.edu/haoran"

    client = HotplateClient(SERVER_URL, NAMESPACE_URI)

    try:
        client.connect()
        while True:
            node, cmd = input(
                "Give the input for Node and Command (space-separated): "
            ).split(" ")
            client.execute(node, cmd)
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Client stopped manually")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        client.disconnect()
