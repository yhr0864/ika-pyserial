import time
import serial
import asyncio
from asyncua import Server
from datetime import datetime


class HotplateController:
    def __init__(
        self,
        port,
        baudrate,
        server_url,
        server_name="IKA Hotplate Server",
        name_space="http://emap.kit.edu/haoran",
    ):
        self.ser = serial.Serial(port=port, baudrate=baudrate, timeout=1)
        self.server = Server()
        self.server.set_endpoint(server_url)
        self.server.set_server_name(server_name)

        self.namespace = name_space
        self.idx = None
        self.get_name = None
        self.set_temp = None
        self.start_heater = None
        self.read_temp = None

        self.prev_set_temp = 0
        self.prev_start_heater = False

    async def setup(self):
        await self.server.init()
        self.idx = await self.server.register_namespace(self.namespace)
        node = self.server.nodes.objects
        device = await node.add_object(self.idx, "IKA_hotplate")

        self.get_name = await device.add_variable(self.idx, "GET_NAME", False)
        self.set_temp = await device.add_variable(self.idx, "SET_TEMP", 0.0)
        self.start_heater = await device.add_variable(self.idx, "START_HEATER", False)
        self.read_temp = await device.add_variable(self.idx, "READ_TEMP", 0.0)

        await self.get_name.set_writable()
        await self.set_temp.set_writable()
        await self.start_heater.set_writable()

    async def send_command(self, command, timeout=1):
        clean_command = command.strip() + "\r\n"
        self.ser.write(clean_command.encode("utf-8"))
        await asyncio.sleep(0.5)
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.ser.in_waiting > 0:
                response = self.ser.readline().decode("utf-8").strip()
                if clean_command != "IN_PV_2\r\n":
                    print(f"Response: {response}")
                return response
        print("No response")
        return None

    async def get_temperature(self, timeout=1):
        return await self.send_command("IN_PV_2", timeout)

    async def run(self):
        await self.setup()
        try:
            async with self.server:
                print("Server started at {}".format(self.server.endpoint))
                while True:
                    now = datetime.now().strftime("%H:%M:%S")
                    current_temp = await self.get_temperature()
                    current_temp = float(current_temp.split()[0])
                    if current_temp:
                        await self.read_temp.write_value(current_temp)
                        print(f"OPC UA Running {now} | Current Temp: {current_temp} C")

                    if await self.get_name.read_value():
                        await self.send_command("IN_NAME")
                        await self.get_name.write_value(False)

                    if await self.set_temp.read_value() != self.prev_set_temp:
                        await self.send_command(
                            f"OUT_SP_1 {await self.set_temp.read_value()}"
                        )
                        self.prev_set_temp = await self.set_temp.read_value()

                    if await self.start_heater.read_value() != self.prev_start_heater:
                        cmd = (
                            "START_1"
                            if await self.start_heater.read_value()
                            else "STOP_1"
                        )
                        await self.send_command(cmd)
                        self.prev_start_heater = await self.start_heater.read_value()

                    await asyncio.sleep(0.5)

        except asyncio.CancelledError:
            print("Task cancelled, shutting down...")
        except KeyboardInterrupt:
            print("Stopped manually")
        finally:
            print("Stopping server...")
            await self.server.stop()


if __name__ == "__main__":
    controller = HotplateController(
        port="COM16",
        baudrate=9600,
        server_url="opc.tcp://localhost:4841",
    )
    asyncio.run(controller.run())
