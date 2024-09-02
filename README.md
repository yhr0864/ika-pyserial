# IKA Remote Control

This project facilitates the remote control of an IKA hotplate using PySerial and OPC UA, with the BeagleBone Black (BBB) serving as the main controller.

## About The Project

![Remote Control Scheme](./images/remote_control_scheme.png?raw=true)

This project aims to establish communication with an IKA hotplate through an OPC UA server-client setup. The system is powered by a BeagleBone Black (BBB), which is connected to a PC via a USB cable.

### Communication Workflow:
- **Command Transmission:** NAMUR commands are sent from the client on the PC to the server running on the BBB.
- **Command Reception:** The server on the BBB receives the commands, and the client on the BBB reads these commands from the server.
- **Device Control:** The received commands are then forwarded to the IKA hotplate for execution.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started

Follow the instructions below to set up and start the project.


### Installation

To set up the project, perform the following steps:

1. Clone the repo
   ```sh
   git clone https://github.com/yhr0864/ika-pyserial.git
   ```
2. Install required packages
   ```sh
   pip install -r requirement.txt
   ```
3. Run the server first
   ```sh
   python server.py
   ```
4. Run the client
   ```sh
   python client.py
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>




