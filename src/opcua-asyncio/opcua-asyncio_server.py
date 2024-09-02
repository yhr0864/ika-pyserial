import asyncio
from datetime import datetime
from asyncua import Server


class SubHandler:
    """
    Subscription Handler. To receive events from server for a subscription
    """

    def datachange_notification(self, node, val, data):
        print(f"Data change detected on node {node} with value: {val}")

    def event_notification(self, event):
        print(f"New event: {event}")


async def main():
    server = Server()
    await server.init()

    server.set_endpoint("opc.tcp://localhost:4842")
    server.set_server_name("My OPC UA Server")

    # setup our own namespace
    namespace = "http://example.org/opcuapy"
    idx = await server.register_namespace(namespace)

    # create directly some objects and variables
    myobj = await server.nodes.objects.add_object(idx, "IKA_hotplate")
    myvar = await myobj.add_variable(
        f"ns={idx};s=Command", "NAMUR", "Waiting for commands"
    )

    await myvar.set_writable()  # Set MyVariable to be writable by clients

    # starting!

    async with server:
        print(f"Server started at {server.endpoint}")
        # enable following if you want to subscribe to nodes on server side

        handler = SubHandler()
        sub = await server.create_subscription(500, handler)
        handle = await sub.subscribe_data_change(myvar)

        while True:
            # Update the variable value with the current time in seconds
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")

            # Log the server status and variable value
            print("OPC UA Server Running", current_time)
            print("Current Value: ", await myvar.get_value())

            await myvar.write_value("Waiting for commands")

            await asyncio.sleep(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server stopped manually")
