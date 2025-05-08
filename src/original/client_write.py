from opcua import Client
import time


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
        idx = self.client.get_namespace_index(self.namespace_uri)
        self.node = self.client.get_node(f"ns={idx};i={self.node_id}")

    def disconnect(self):
        self.client.disconnect()
        print("Disconnected from OPC UA server")

    def send_commands(self, commands, delay=1):
        for cmd in commands:
            self.node.set_value(cmd)
            print(f"Sent command: {cmd.strip()}")
            time.sleep(delay)


if __name__ == "__main__":
    SERVER_URL = "opc.tcp://localhost:4841"
    NAMESPACE_URI = "http://emap.kit.edu/haoran"

    commands = [
        "IN_NAME\r\n",  # Read device name
        "OUT_SP_1 30\r\n",  # Set temperature to 30
        "OUT_SP_4 150\r\n",  # Set speed to 150
        "START_1\r\n",  # Start heater
        "START_4\r\n",  # Start motor
    ]

    client = HotplateClient(SERVER_URL, NAMESPACE_URI)

    try:
        client.connect()
        client.send_commands(commands)

    except KeyboardInterrupt:
        print("Client stopped manually")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        client.disconnect()
