from opcua import Server
from datetime import datetime
import time

# Create and configure the server
server = Server()
server_url = "opc.tcp://192.168.7.2:4841"
server.set_endpoint(server_url)

# Set server name
server.set_server_name("My OPC UA Server")

# Setup server namespace
namespace = "http://example.org/opcuapy"
idx = server.register_namespace(namespace)

# Add a new object to the address space
node = server.nodes.objects
device = node.add_object(idx, "IKA_hotplate")

# Add a variable to the object
command = device.add_variable(idx, "NAMUR", "Waiting for commands")
# print(f"Node ID: {var.nodeid}")
# breakpoint()
command.set_writable()

# Start the server
server.start()
print("Server started at {}".format(server.endpoint))

try:
    while True:
        # Update the variable value with the current time in seconds
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        # var.set_value(current_time)

        print("OPC UA Server Running", current_time)
        print("Current Value: ", command.get_value())

        time.sleep(1)

except KeyboardInterrupt:
    print("Server stopped manually")

finally:
    # Ensure the server is stopped properly
    server.stop()
    print("Server stopped")
