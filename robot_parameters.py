# -*- coding: utf-8 -*-
##
# =============================================================================
# @file robot_parameters.py
# @brief Defines abstract and concrete robot configuration classes using OOP principles,
#        and provides a PyQt5-based GUI for editing robot parameters.
#
# @version 1.0
# @date 2025-05-04
# @authors
# - Doğukan Baygut
#
# @details
# This module showcases inheritance, encapsulation, abstraction, and polymorphism
# through the use of robot configuration classes and a GUI editor.
#
# ## Structure:
# - @ref BaseRobotConfig: Abstract base class.
# - @ref WheeledRobotConfig, @ref TrackedRobotConfig: Polymorphic concrete classes.
# - @ref RobotParametersWindow: GUI for editing robot parameters at runtime.
#
# ## Object-Oriented Design:
# - @b Inheritance: Wheeled/Tracked configs inherit from BaseRobotConfig.
# - @b Encapsulation: Robot attributes are encapsulated per object.
# - @b Polymorphism: `get_type()` is resolved at runtime.
# - @b Dynamic Instantiation: Robot type is selected by user at runtime (Factory-style).
#
# =============================================================================

from abc import ABC, abstractmethod
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QComboBox, QPushButton, QVBoxLayout, QMessageBox

# =============================================================================
# 1. ABSTRACT ROBOT CONFIGURATION CLASS
# =============================================================================

##
# @class BaseRobotConfig
# @brief Abstract base class defining the general structure of a robot.
#
# @details
# This class holds shared robot parameters (name, speed, battery).
# Subclasses must override `get_type()` to specify robot type.
#
# @abstract Yes
# @polymorphic Yes
#
class BaseRobotConfig(ABC):
    def __init__(self, name, speed, battery):
        """
        @brief Initializes a new robot configuration.
        @param name (str): Robot name
        @param speed (float): Maximum speed
        @param battery (float): Battery level or capacity
        """
        self.name = name
        self.speed = speed
        self.battery = battery

    @abstractmethod
    def get_type(self):
        """
        @brief Abstract method returning the robot type (to be overridden).
        @return (str): Robot type (e.g., 'Tekerlekli', 'Paletli')
        """
        pass

    def get_info(self):
        """
        @brief Returns a human-readable string of robot's parameters.
        @return (str): Concatenated name, speed, battery values
        """
        return f"Ad: {self.name}, Hız: {self.speed}, Batarya: {self.battery}"

# =============================================================================
# 2. CONCRETE ROBOT TYPES
# =============================================================================

##
# @class WheeledRobotConfig
# @brief Represents a robot that moves using wheels.
#
# @inherits BaseRobotConfig
# @polymorphic Yes
#
class WheeledRobotConfig(BaseRobotConfig):
    def get_type(self):
        """
        @brief Returns the type of robot.
        @return (str): 'Tekerlekli'
        """
        return "Tekerlekli"

##
# @class TrackedRobotConfig
# @brief Represents a robot that moves using tracks (caterpillar-type).
#
# @inherits BaseRobotConfig
# @polymorphic Yes
#
class TrackedRobotConfig(BaseRobotConfig):
    def get_type(self):
        """
        @brief Returns the type of robot.
        @return (str): 'Paletli'
        """
        return "Paletli"

# =============================================================================
# 3. GUI: Robot Parameters Editing Window
# =============================================================================

##
# @class RobotParametersWindow
# @brief GUI window for entering and saving robot configuration.
#
# @details
# This QWidget-based dialog allows users to input a robot's name, speed, battery,
# and choose its type (wheeled or tracked) from a combo box. When 'Save' is clicked,
# an object of the correct type is created and shown in a dialog box.
#
# @inherits QWidget
# @uses WheeledRobotConfig, TrackedRobotConfig
# @polymorphic Yes (via runtime decision)
# @pattern Factory-like instantiation at runtime
#
class RobotParametersWindow(QWidget):
    def __init__(self, parent=None):
        """
        @brief Initializes the GUI components and layout.
        @param parent (QWidget): Optional parent widget.
        """
        super().__init__(parent)
        self.setWindowTitle("Robot Parametreleri")
        self.resize(300, 200)

        # Input fields
        self.name_edit = QLineEdit()
        self.speed_edit = QLineEdit()
        self.battery_edit = QLineEdit()
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Tekerlekli", "Paletli"])
        self.save_button = QPushButton("Kaydet")

        # Layout setup
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Robot Adı:"))
        layout.addWidget(self.name_edit)
        layout.addWidget(QLabel("Hız:"))
        layout.addWidget(self.speed_edit)
        layout.addWidget(QLabel("Batarya:"))
        layout.addWidget(self.battery_edit)
        layout.addWidget(QLabel("Tip:"))
        layout.addWidget(self.type_combo)
        layout.addWidget(self.save_button)
        self.setLayout(layout)

        # Connect logic
        self.save_button.clicked.connect(self.kaydet)

    def kaydet(self):
        """
        @brief Reads user input and creates a robot config instance accordingly.
        @details
        - Chooses between Wheeled and Tracked types.
        - Displays final configuration with `get_info()` and `get_type()`.
        - Handles user errors (invalid float input).
        @exception ValueError: Raised if numeric fields contain invalid text.
        @post Displays QMessageBox with robot summary or error.
        """
        try:
            name = self.name_edit.text()
            speed = float(self.speed_edit.text())
            battery = float(self.battery_edit.text())
            robot_type = self.type_combo.currentText()

            if robot_type == "Tekerlekli":
                self.config = WheeledRobotConfig(name, speed, battery)
            else:
                self.config = TrackedRobotConfig(name, speed, battery)

            QMessageBox.information(self, "Başarılı",
                                    f"Robot: {self.config.get_info()}\nTip: {self.config.get_type()}")
            self.close()

        except ValueError:
            QMessageBox.warning(self, "Hata", "Lütfen geçerli sayılar girin.")
