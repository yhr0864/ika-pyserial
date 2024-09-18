import time
from transitions import Machine
from multiprocessing import shared_memory
import struct


class Vehicle(object):

    states = ["stop", "moving"]

    def __init__(self):
        # Initialize the state machine
        self.machine = Machine(model=self, states=Vehicle.states, initial="stop")

        self.machine.add_transition(
            trigger="light_turns_green", source="stop", dest="moving"
        )
        self.machine.add_transition("light_turns_red", "moving", "stop")


if __name__ == "__main__":
    car = Vehicle()
    # Connect to the existing shared memory block using the known name
    shm_name = "my_custom_shm"
    existing_shm = shared_memory.SharedMemory(name=shm_name)

    # Define the format and size for unpacking the integers (must match the original format)
    data_size = 1

    while True:
        time.sleep(1)
        # Read the byte data from shared memory
        data_bytes = bytes(existing_shm.buf[:data_size])

        # Convert the bytes back into a string
        data = data_bytes.decode(
            "utf-8"
        ).rstrip()  # Use .rstrip() to remove trailing whitespace
        print(f"Now is {data}")
        if data == "red":
            car.light_turns_red()
            print("car stops")
        elif data == "green":
            car.light_turns_green()
            print("car moves")
        else:
            pass
