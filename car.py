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

    # Define the size based on the longest possible traffic light state (green, yellow, red)
    data_size = 6  # "yellow" is the longest state with 6 characters

    try:
        while True:
            time.sleep(1)

            # Read the byte data from shared memory
            data_bytes = bytes(existing_shm.buf[:data_size])

            # Convert the bytes back into a string and remove null bytes
            data = data_bytes.decode("utf-8").rstrip("\x00")
            print(f"Now is {data}")

            # Transition based on the traffic light state
            if data == "red" and car.state == "moving":
                car.light_turns_red()
                print("Car stops")
            elif data == "green" and car.state == "stop":
                car.light_turns_green()
                print("Car moves")
            else:
                # Add any specific behavior for "yellow" or any other state
                print("Waiting...")

    except KeyboardInterrupt:
        pass
    finally:
        # Clean up shared memory
        existing_shm.close()
