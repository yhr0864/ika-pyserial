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

        print(f"Subscribed to node {myvar}. Waiting for data changes...")

        # Keep the script running to receive notifications

        while True:
            await asyncio.sleep(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Subscription terminated by user.")
