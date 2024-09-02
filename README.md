# ika-remote-control
remote control of hotplate through pyserial and opc ua based on BBB

## About The Project

![alt text](./images/remote_control_scheme.png?raw=true)

We plan to communicate with ika hotplate through OPC UA server-client with the help of MCU (BeagleBone Black), which is connected to the PC through USB cable.

Here's communication progress:
* We send NAMUR commands from client on PC to the server on BBB
* The server received the command and the client on the BBB read from the server
* The recieved commands are then sent to the device ika hotplate

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started

Here shows how to start with the following instructions.


### Installation

Below is an example of how you can instruct your audience on installing and setting up your app. This template doesn't rely on any external dependencies or services.

1. Clone the repo
   ```sh
   git clone https://github.com/github_username/repo_name.git
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




