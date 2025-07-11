# -*- coding: utf-8 -*-
##
# @file manuel_kod.py
# @brief Manual driving GUI control for the AgriEdge robot system.
# @author Doğukan AVCI, Sinan ILBEY
# @version 1.0
# @date 2025-05-04
#
# @details
# This module defines the `ManuelModeWindow` class, which provides a dedicated QWidget-based
# control panel for manual directional commands for the AgriBot robot. It is designed for
# integration into the AGRIEDGE system.
#
# Features include:
# - Forward, backward, left, right, and stop controls
# - A button for switching robot modes
# - Icon-based buttons with unified styling
# - Real-time logging of user actions into the main terminal
#
# This class follows OOP principles: encapsulation, modularity, and signal-slot separation.
# It communicates with the main window through dependency injection.
##

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QIcon
from Manuel import Ui_Form  # UI designed with Qt Designer
from style_sheets import BUTON_STIL

##
# @class ManuelModeWindow
# @brief Manual GUI panel to control AgriBot’s movement using directional buttons.
#
# @inherits QWidget
# @details
# - Integrates with the main AGRIEDGE GUI for real-time terminal logging.
# - Uses Qt's signal-slot mechanism to handle button actions.
# - Demonstrates modularity by separating UI, logic, styling, and icon configuration.
##
class ManuelModeWindow(QWidget):
    ##
    # @brief Constructor for the manual control panel.
    # @param main_window Reference to the main window object to send logs (optional).
    #
    # @details
    # Initializes UI components, applies styles, sets icons, and connects each button to its logic handler.
    ##
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window  #: Pointer to main GUI for cross-window logging
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.setWindowTitle("Manuel Sürüş Paneli 🚗")
        self.setStyleSheet("background-color: #f5f5f5;")

        self.stil_ver()
        self.iconlari_ayarla()

        # Button signal-slot connections for movement control
        self.ui.Ileri_button.clicked.connect(lambda: self.log_bildir("İleri komutu gönderildi"))
        self.ui.Geri_Button.clicked.connect(lambda: self.log_bildir("Geri komutu gönderildi"))
        self.ui.Sol_Button.clicked.connect(lambda: self.log_bildir("Sola dön komutu gönderildi"))
        self.ui.Sag_Button.clicked.connect(lambda: self.log_bildir("Sağa dön komutu gönderildi"))
        self.ui.Dur_button.clicked.connect(lambda: self.log_bildir("Dur komutu gönderildi"))
        self.ui.Change_Mode.clicked.connect(self.mode_clicked)

    ##
    # @brief Applies the common stylesheet to all GUI buttons for consistent appearance.
    # @details
    # Style is imported from `style_sheets.py` and provides visual coherence for UI elements.
    ##
    def stil_ver(self):
        self.ui.Ileri_button.setStyleSheet(BUTON_STIL)
        self.ui.Geri_Button.setStyleSheet(BUTON_STIL)
        self.ui.Sol_Button.setStyleSheet(BUTON_STIL)
        self.ui.Sag_Button.setStyleSheet(BUTON_STIL)
        self.ui.Dur_button.setStyleSheet(BUTON_STIL)
        self.ui.Change_Mode.setStyleSheet(BUTON_STIL)

    ##
    # @brief Sets button icons for directional and mode buttons.
    # @details
    # Icons are loaded from the `Assets/Icons/` directory and assigned to each QPushButton.
    ##
    def iconlari_ayarla(self):
        self.ui.Ileri_button.setIcon(QIcon("Assets/Icons/up.png"))
        self.ui.Geri_Button.setIcon(QIcon("Assets/Icons/down.png"))
        self.ui.Sol_Button.setIcon(QIcon("Assets/Icons/left.png"))
        self.ui.Sag_Button.setIcon(QIcon("Assets/Icons/right.png"))
        self.ui.Dur_button.setIcon(QIcon("Assets/Icons/stop.png"))
        self.ui.Change_Mode.setIcon(QIcon("Assets/Icons/change.png"))

    ##
    # @brief Slot that is triggered when the "Change Mode" button is clicked.
    # @details
    # Logs the action both in the terminal and visually in the status bar of the parent window.
    ##
    def mode_clicked(self):
        self.log_bildir("Mod değiştirildi.")
        if self.main_window:
            self.main_window.ui.statusbar.showMessage("Mod değiştirildi", 3000)

    ##
    # @brief Sends a log message to the main window’s terminal.
    # @param mesaj The string to be logged with an emoji prefix.
    # @details
    # Enables this child widget to communicate with the parent for centralized logging.
    ##
    def log_bildir(self, mesaj):
        if self.main_window:
            self.main_window.log_yaz(f"🕹️ Manuel: {mesaj}", "INFO")
