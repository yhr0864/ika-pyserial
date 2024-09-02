import asyncio
from asyncua import Client


class SubHandler:
    """
    Subscription Handler. To receive events from server for a subscription.
    """

    def datachange_notification(self, node, val, data):
        if val != "Waiting for commands":
            print(f"Data change detected on node {node} with value: {val}")

    def event_notification(self, event):
        print(f"New event: {event}")


async def main():
    url = "opc.tcp://localhost:4842"
    async with Client(url=url) as client:
        namespace = "http://example.org/opcuapy"
        idx = await client.get_namespace_index(namespace)
        myvar = client.get_node(f"ns={idx};s=Command")

        # subscribing to a variable node
        handler = SubHandler()
        sub = await client.create_subscription(500, handler)
        handle = await sub.subscribe_data_change(myvar)

        # Write a new value to the variable
        commands = [
            "IN_NAME\r\n",  # read the device name
            "OUT_SP_1 30\r\n",  # set temperature value 30
            "OUT_SP_4 150\r\n",  # set speed value 150
            "START_1\r\n",  # start the heater
            "START_4\r\n",  # start the motor
        ]

        for command in commands:
            await myvar.write_value(command)
            print(f"Written command: {command}")
            await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
