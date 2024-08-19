import serial
import serial.tools.list_ports
import time

# List available serial ports (Optional, to see available ports)
ports = serial.tools.list_ports.comports()
for port in ports:
    print(port.device)

# Open the serial port
ser = serial.Serial(port="COM6", baudrate=9600, timeout=2)

# Check if the serial port is open
if ser.is_open:
    print(f"Serial port {ser.name} opened successfully.")

    # Send a message
    msg = b'hello'
    ser.write(msg)
    print(f"Sent: {msg}")

    # Read a response (attempt to read a message)
    time.sleep(0.1)
    response = ser.read(ser.in_waiting or 100)  # Read all available bytes or wait for one byte
    print(f"Received: {response}")

    # Close the serial port
    ser.close()
    print("Serial port closed.")
else:
    print(f"Failed to open serial port {ser.name}.")




