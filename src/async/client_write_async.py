import asyncio
import logging
from opcua import Client, ua

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="./log/opcua_client_write.log",  # Log file name
    filemode="w",  # Write mode, 'a' for append mode
)
logger = logging.getLogger(__name__)

# Define the OPC UA server URL
url = "opc.tcp://192.168.7.2:4841"


async def acknowledgment_callback(sequence_number, ack_event):
    # Simulate waiting for acknowledgment from the server
    await asyncio.sleep(1)  # Simulate network delay, adjust as needed
    ack_event.set()  # Signal that acknowledgment is received
    logger.info(f"Acknowledgment received for command {sequence_number}")


async def send_command_with_ack(client, node, command, sequence_number, ack_event):
    retries = 0
    max_retries = 5

    while retries < max_retries:
        try:
            # Send the command to the server
            node.set_value(ua.Variant(command, ua.VariantType.String))
            logger.info(f"Written command {sequence_number}: {command.strip()}")

            # Wait for acknowledgment
            await acknowledgment_callback(sequence_number, ack_event)

            # Wait until acknowledgment is received
            await ack_event.wait()

            # If acknowledgment is received, exit the loop
            logger.info(f"Command {sequence_number} acknowledged.")
            break

        except Exception as e:
            logger.error(f"Error sending command {sequence_number}: {e}")
            retries += 1
            logger.warning(
                f"Retrying command {sequence_number}... ({retries}/{max_retries})"
            )
            await asyncio.sleep(1)  # Adjust delay as needed

    if retries == max_retries:
        logger.error(
            f"Failed to receive acknowledgment after {max_retries} retries for command {sequence_number}."
        )


async def main():
    client = Client(url)
    try:
        client.connect()
        logger.info("Client connected to OPC UA server")

        # Get the namespace index from the server
        idx = client.get_namespace_index("http://example.org/opcuapy")
        node = client.get_node(f"ns={idx};i=2")

        # List of commands to send
        commands = [
            "IN_NAME\r\n",  # read the device name
            "OUT_SP_1 30\r\n",  # set temperature value 30
            "OUT_SP_4 150\r\n",  # set speed value 150
            "START_1\r\n",  # start the heater
            "START_4\r\n",  # start the motor
        ]

        tasks = []
        for sequence_number, command in enumerate(commands, start=1):
            ack_event = asyncio.Event()
            task = asyncio.create_task(
                send_command_with_ack(client, node, command, sequence_number, ack_event)
            )
            tasks.append(task)
            await asyncio.sleep(3)  # Delay between sending commands

        await asyncio.gather(*tasks)

    except KeyboardInterrupt:
        logger.info("Client stopped manually")

    except Exception as e:
        logger.error(f"An error occurred: {e}")

    finally:
        client.disconnect()
        logger.info("Client disconnected")


# Run the asyncio event loop
asyncio.run(main())
