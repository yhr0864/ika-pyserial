import serial
from opcua import Server
from datetime import datetime
import time


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
        self.idx = self.server.register_namespace(self.namespace)
        self._setup_opcua_nodes()

        self.prev_set_temp = 0
        self.prev_start_heater = False

    def _setup_opcua_nodes(self):
        # Setup all the opcua nodes
        node = self.server.nodes.objects
        device = node.add_object(self.idx, "IKA_hotplate")

        self.get_name = device.add_variable(self.idx, "GET_NAME", False)
        self.set_temp = device.add_variable(self.idx, "SET_TEMP", 0)
        self.start_heater = device.add_variable(self.idx, "START_HEATER", False)
        self.read_temp = device.add_variable(self.idx, "READ_TEMP", 0)

        self.get_name.set_writable()
        self.set_temp.set_writable()
        self.start_heater.set_writable()

    def start_server(self):
        self.server.start()
        print("Server started at {}".format(self.server.endpoint))

    def stop_server(self):
        self.server.stop()
        print("Server stopped")

    def send_command(self, command, timeout=1):
        # Send commands and wait for feedback
        clean_command = command.strip() + "\r\n"
        self.ser.write(clean_command.encode("utf-8"))
        time.sleep(0.5)
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.ser.in_waiting > 0:
                response = self.ser.readline().decode("utf-8")
                # Do not print out if we send command for current temp.
                if clean_command != "IN_PV_2\r\n":
                    print(f"Response: {response.strip()}")
                return response.strip()
        print("No response")
        return None

    def get_temperature(self, timeout=1):
        return self.send_command("IN_PV_2", timeout)

    def run(self):
        try:
            while True:
                now = datetime.now().strftime("%H:%M:%S")
                current_temp = self.get_temperature().split()[0]
                if current_temp:
                    self.read_temp.set_value(float(current_temp))
                    print(f"OPC UA Running {now} | Current Temp: {current_temp} C")

                if self.get_name.get_value():
                    self.send_command("IN_NAME")
                    self.get_name.set_value(False)

                if self.set_temp.get_value() != self.prev_set_temp:
                    self.send_command(f"OUT_SP_1 {self.set_temp.get_value()}")
                    self.prev_set_temp = self.set_temp.get_value()

                if self.start_heater.get_value() != self.prev_start_heater:
                    cmd = "START_1" if self.start_heater.get_value() else "STOP_1"
                    self.send_command(cmd)
                    self.prev_start_heater = self.start_heater.get_value()

                time.sleep(0.5)

        except KeyboardInterrupt:
            print("Stopped manually")
        finally:
            self.stop_server()


if __name__ == "__main__":
    # Change the port and server_url based on your practical use
    controller = HotplateController(
        port="COM16",
        baudrate=9600,
        server_url="opc.tcp://localhost:4841",
    )
    controller.start_server()
    controller.run()
