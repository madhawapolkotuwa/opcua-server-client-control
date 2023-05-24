# OPC-UA Server and Client Control Application

This is a Python application that includes an OPC-UA server and client control functionality. The server side runs on an Ubuntu OS PC, while the client side runs on a Windows 10 PC. The server periodically updates values at a rate of 0.1 seconds and displays them on the Human-Machine Interface (HMI) developed using PyQt5 (or PySide6). The client side can control the server by sending commands over the OPC-UA protocol.

[![Demo Video](https://img.youtube.com/vi/VIDEO_ID/maxresdefault.jpg)](https://www.youtube.com/watch?v=VIDEO_ID)

**[Watch the Demo Video]([https://www.youtube.com/watch?v=VIDEO_ID](https://youtu.be/_bI4E2RvG0o))**

## Features

- OPC-UA server with data update at 0.1-second intervals
- OPC-UA client control functionality
- Human-Machine Interface (HMI) developed using PyQt5 (or PySide6)

## Prerequisites

- Ubuntu OS PC for server side
- Windows 10 PC for client side
- Python 3.x installed on both systems
- OPC-UA server and client libraries installed:
    - [Python OPC-UA](https://github.com/FreeOpcUa/python-opcua) library for server
    - [Python OPC-UA](https://github.com/FreeOpcUa/python-opcua) library for client

## Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/your-username/opc-ua-server-client-control.git
   ```

2. Install the required Python packages using pip:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Server-side:

   - Run the OPC-UA server on the Ubuntu OS PC:

     ```bash
     python serverMain.py
     ```

2. Client-side:

   - Run the OPC-UA client on the Windows 10 PC:

     ```bash
     python clientMain.py
     ```

3. The HMI developed using PyQt5 (or PySide6) will launch on the client-side, displaying the real-time values from the OPC-UA server.

4. Use the client application to send commands and control the OPC-UA server as needed.

## Demo Video

Check out the [demo video](https://youtu.be/_bI4E2RvG0o) to see the OPC-UA server and client control application in action.

## License

This project is licensed under the [MIT License](LICENSE).

## Contributing

Contributions are welcome! If you have any ideas, improvements, or bug fixes, please open an issue or submit a pull request.

## Contact

For any questions or inquiries, please contact [Madhawa Polkotuwa](mailto:your-madhawapolkotuwa@gmail.com).

---

