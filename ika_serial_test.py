import serial
import time

# Open the virtual COM port
ser = serial.Serial(
    port="/dev/ttyACM0",  # This might be /dev/ttyUSB0 depending on your setup
    baudrate=9600,  # Set this according to your device's specification
    timeout=1,
    parity=serial.PARITY_EVEN,
)


# Function to send a command and read the response
def send_command(command):
    print(f"Sending command: {command.strip()}")
    ser.write(command.encode("utf-8"))  # Send the command
    time.sleep(0.5)  # Wait a moment for the device to process the command
    if ser.in_waiting > 0:  # Check if there's a response
        response = ser.read(ser.in_waiting).decode("utf-8")  # Read response
        print(f"Response: {response.strip()}")
    else:
        print("No response received.")


# List of commands to send
commands = [
    "IN_NAME\r\n",  # read the device name
    "OUT_SP_1 30\r\n",  # set temperature value 30
    "OUT_SP_4 150\r\n",  # set speed value 150
    "START_1\r\n",  # start the heater
    "START_4\r\n",  # start the motor
]

commands2 = ["STOP_1\r\n", "STOP_4\r\n"]

# Send each command in the list
for command in commands:
    send_command(command)

# Close the serial connection when done
ser.close()
