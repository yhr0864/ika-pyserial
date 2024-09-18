import time
from transitions import Machine
from multiprocessing import shared_memory
import struct


class TrafficLight(object):

    states = ["green", "yellow", "red"]

    def __init__(self):
        # Initialize the state machine
        self.machine = Machine(model=self, states=TrafficLight.states, initial="green")

        self.machine.add_transition(trigger="timeup", source="green", dest="red")
        self.machine.add_transition("timeup", "red", "yellow")
        self.machine.add_transition("timeup", "yellow", "green")


if __name__ == "__main__":
    traffic_light = TrafficLight()
    # Example data (a list of integers)
    data = " "
    data_bytes = data.encode("utf-8")

    data_size = len(data_bytes)

    # Create shared memory with a custom name
    shm = shared_memory.SharedMemory(name="my_custom_shm", create=True, size=data_size)

    while True:
        time.sleep(2)
        traffic_light.timeup()
        data = traffic_light.state

        print(data)
        # Pack and write the data to shared memory
        shm.buf[:data_size] = data_bytes
