from opcua import Server
from datetime import datetime
import asyncio
import logging

# Configure logging to save logs to a file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='./log/opcua_server.log',  # Log file name
    filemode='w'  # Write mode, 'a' for append mode
)
logger = logging.getLogger(__name__)

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
command.set_writable()

# Start the server
server.start()
logger.info(f"Server started at {server.endpoint}")

async def update_variable():
    while True:
        # Update the variable value with the current time in seconds
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        
        # Log the server status and variable value
        logger.info(f"OPC UA Server Running - Current Time: {current_time}")
        logger.info(f"Current Value: {command.get_value()}")

        # Sleep for 1 second
        await asyncio.sleep(1)

async def main():
    try:
        await update_variable()
    except KeyboardInterrupt:
        logger.info("Server stopped manually")
    finally:
        server.stop()
        logger.info("Server stopped")

# Run the asyncio event loop
asyncio.run(main())
