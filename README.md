# IKA Remote Control

This project facilitates the remote control of an IKA hotplate using PySerial and OPC UA, with the BeagleBone Black (BBB) serving as the main controller.

## About The Project

![Remote Control Scheme](./images/remote_control_scheme.png?raw=true)

This project aims to establish communication with an IKA hotplate through an OPC UA server setup. The system is powered by a BeagleBone Black (BBB), which is connected to a PC via a USB cable.

### Communication Workflow:
- **Command Transmission:** NAMUR commands are sent from the client/UaExpert on the PC to the server running on the BBB.
- **Command Reception:** The server on the BBB receives the commands, and then send these commands to hot plate via usb serial communication.
- **Device Control:** The received commands are then forwarded to the IKA hotplate for execution.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started
Just follow the steps below when you connect your Beagle Bone Black via SSH.

1. Clone the repo on Beagle Bone Black
   ```sh

   git clone https://github.com/yhr0864/ika-pyserial.git

   ```
2. Create virtual environment

   ```sh

   python -m venv my_env

   ```
3. Install required packages

   ```sh

   pip install -r requirement.txt

   ```
4. Activate environment

   ```sh

   source my_env/bin/activate

   ```
5. Run the server first (Note: you may need to reset the COM port and server URL first!)

   ```sh

   python ./src/opcua-asyncio/opcua-asyncio_server.py

   ```
6. Ether run the client code or use UaExpert to send command
   ```sh

   python ./src/original/client_write.py

   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>




