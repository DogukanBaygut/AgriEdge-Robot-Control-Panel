# -*- coding: utf-8 -*-
##
# ==============================================================================
# @file connection_settings.py
# @brief Connection configuration interface supporting multiple communication types.
#
# @details
# This module defines multiple communication types for robot-to-host connectivity, including:
# - Serial (e.g., COM3 at 9600 baud)
# - TCP (IP/Port based)
# - Bluetooth (device/channel)
# - Wi-Fi (host/port)
#
# The system uses an abstract interface (`ConnectionInterface`) to define a contract for all
# connection types, and a PyQt5 GUI (`ConnectionSettingsWindow`) to let users choose, switch,
# and manage connections at runtime.
#
# ## Design Patterns:
# - @b Interface Pattern: All connection types implement `ConnectionInterface`.
# - @b Polymorphism: ConnectionSettingsWindow uses dynamic dispatch via interface pointer.
#
# ## OOP Concepts:
# - @b Abstraction: Common interface for different protocols.
# - @b Inheritance: Concrete classes implement base interface.
# - @b Polymorphism: Swappable connection instances at runtime.
# - @b Encapsulation: Each connection manages its own parameters.
#
# @author Doğukan Avcı
# @date May 4, 2025
# @version 1.0
# ==============================================================================

from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QPushButton, QVBoxLayout, QComboBox
from abc import ABC, abstractmethod
import sys

# ==============================================================================
# ABSTRACT BASE CLASS FOR CONNECTION TYPES
# ==============================================================================

##
# @class ConnectionInterface
# @brief Abstract base class for all connection types.
#
# @details
# This interface ensures that all connection types support the same methods:
# - connect()
# - disconnect()
# - get_settings()
#
# This enables polymorphic usage and UI-driven swapping of connections.
#
# @abstract Yes
# @polymorphic Yes
#
class ConnectionInterface(ABC):
    @abstractmethod
    def connect(self):
        """@brief Initiates the connection session."""
        pass

    @abstractmethod
    def disconnect(self):
        """@brief Terminates the connection session."""
        pass

    @abstractmethod
    def get_settings(self):
        """
        @brief Returns a string summary of connection parameters.
        @return str
        """
        pass

# ==============================================================================
# SERIAL CONNECTION CLASS
# ==============================================================================

##
# @class SerialConnection
# @brief Represents a serial port connection.
#
# @inherits ConnectionInterface
#
class SerialConnection(ConnectionInterface):
    def __init__(self):
        """
        @brief Initializes serial connection with default port and baudrate.
        """
        self.port = "COM3"
        self.baudrate = 9600

    def connect(self):
        """
        @brief Simulates establishing a serial connection.
        """
        print(f"[Serial] Connected to {self.port} at {self.baudrate} baud.")

    def disconnect(self):
        """
        @brief Simulates disconnecting serial.
        """
        print("[Serial] Connection closed.")

    def get_settings(self):
        """
        @brief Returns current serial settings.
        @return str
        """
        return f"Port: {self.port}, Baudrate: {self.baudrate}"

# ==============================================================================
# TCP CONNECTION CLASS
# ==============================================================================

##
# @class TCPConnection
# @brief Represents a TCP/IP connection.
#
# @inherits ConnectionInterface
#
class TCPConnection(ConnectionInterface):
    def __init__(self):
        """
        @brief Initializes TCP connection with default IP and port.
        """
        self.ip = "192.168.1.100"
        self.port = 8080

    def connect(self):
        """
        @brief Simulates TCP connection.
        """
        print(f"[TCP] Connected to {self.ip}:{self.port}")

    def disconnect(self):
        """
        @brief Simulates disconnecting TCP.
        """
        print("[TCP] Connection closed.")

    def get_settings(self):
        """
        @brief Returns current TCP settings.
        @return str
        """
        return f"IP: {self.ip}, Port: {self.port}"

# ==============================================================================
# BLUETOOTH CONNECTION CLASS
# ==============================================================================

##
# @class BluetoothConnection
# @brief Represents a Bluetooth device connection.
#
# @inherits ConnectionInterface
#
class BluetoothConnection(ConnectionInterface):
    def __init__(self):
        """
        @brief Initializes Bluetooth device name and channel.
        """
        self.device_name = "HC-05"
        self.channel = 1

    def connect(self):
        """
        @brief Simulates Bluetooth pairing.
        """
        print(f"[Bluetooth] Connected to {self.device_name} (Channel {self.channel})")

    def disconnect(self):
        """
        @brief Simulates disconnecting Bluetooth.
        """
        print("[Bluetooth] Connection closed.")

    def get_settings(self):
        """
        @brief Returns Bluetooth configuration.
        @return str
        """
        return f"Device: {self.device_name}, Channel: {self.channel}"

# ==============================================================================
# WIFI CONNECTION CLASS
# ==============================================================================

##
# @class WiFiConnection
# @brief Represents a Wi-Fi based connection.
#
# @inherits ConnectionInterface
#
class WiFiConnection(ConnectionInterface):
    def __init__(self):
        """
        @brief Initializes Wi-Fi hostname and port.
        """
        self.hostname = "192.168.0.10"
        self.port = 5050

    def connect(self):
        """
        @brief Simulates Wi-Fi connection.
        """
        print(f"[Wi-Fi] Connected to {self.hostname}:{self.port}")

    def disconnect(self):
        """
        @brief Simulates disconnecting Wi-Fi.
        """
        print("[Wi-Fi] Connection closed.")

    def get_settings(self):
        """
        @brief Returns Wi-Fi settings string.
        @return str
        """
        return f"Hostname: {self.hostname}, Port: {self.port}"

# ==============================================================================
# GUI CLASS TO CONTROL CONNECTION SETTINGS
# ==============================================================================

##
# @class ConnectionSettingsWindow
# @brief PyQt5 GUI window for selecting and controlling connection types.
#
# @details
# Provides a simple interface to:
# - Choose between 4 communication types
# - Connect or disconnect
# - View current settings
#
# @inherits QDialog
# @polymorphic Yes (uses ConnectionInterface as interchangeable backend)
#
class ConnectionSettingsWindow(QDialog):
    def __init__(self):
        """
        @brief Sets up UI elements and default connection (Serial).
        """
        super().__init__()
        self.setWindowTitle("Connection Settings")
        self.resize(300, 200)

        self.label = QLabel("Connection Info:")
        self.combo = QComboBox()
        self.combo.addItems(["Serial", "TCP", "Bluetooth", "Wi-Fi"])

        self.connect_button = QPushButton("Connect")
        self.disconnect_button = QPushButton("Disconnect")

        layout = QVBoxLayout()
        layout.addWidget(self.combo)
        layout.addWidget(self.connect_button)
        layout.addWidget(self.disconnect_button)
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.connection: ConnectionInterface = SerialConnection()

        self.combo.currentTextChanged.connect(self.change_connection)
        self.connect_button.clicked.connect(self.connect)
        self.disconnect_button.clicked.connect(self.disconnect)

        self.label.setText("Selected: " + self.connection.get_settings())

    def change_connection(self, selection):
        """
        @brief Switches the backend connection type dynamically based on dropdown selection.
        @param selection (str): Dropdown item (Serial, TCP, Bluetooth, Wi-Fi)
        """
        connection_map = {
            "Serial": SerialConnection,
            "TCP": TCPConnection,
            "Bluetooth": BluetoothConnection,
            "Wi-Fi": WiFiConnection
        }
        self.connection = connection_map.get(selection, SerialConnection)()
        self.label.setText("Selected: " + self.connection.get_settings())

    def connect(self):
        """
        @brief Calls the connect() method of the current connection object.
        """
        self.connection.connect()
        self.label.setText("Connected: " + self.connection.get_settings())

    def disconnect(self):
        """
        @brief Calls the disconnect() method of the current connection object.
        """
        self.connection.disconnect()
        self.label.setText("Connection closed.")

# ==============================================================================
# MAIN BLOCK FOR STANDALONE TESTING
# ==============================================================================

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ConnectionSettingsWindow()
    window.show()
    sys.exit(app.exec_())
