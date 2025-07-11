# =============================================================================
#  AGRIEDGE CONTROL INTERFACE - MAIN MODULE
# =============================================================================
#  Author       : Doğukan AVCI, Sinan ILBEY
#  Description  : 
#      This is the main application file for the AgriEdge Smart Agriculture Robot.
#      It integrates manual and autonomous control modes, sensor telemetry logging,
#      real-time map building, and visual interface enhancements for intuitive usage.
#
#  Modules Used :
#      - PyQt5       : GUI framework
#      - pyttsx3     : Text-to-speech for voice alerts
#      - matplotlib  : Sensor data plotting
#      - platform    : OS version detection for version info
#
#  Features:
#      ✅ Manual and Autonomous Mode Switching
#      ✅ Real-time Sensor Logging (Speed, Temperature, Battery)
#      ✅ Dynamic Warning System with Visual Alerts
#      ✅ GUI-based Map Control and Data Export
#      ✅ Terminal-like Command Input with History
#      ✅ Voice Notifications using TTS
#
#  Last Updated : 2025-05-04
#  License      : MIT License 
# =============================================================================


# System and UI Libraries
import sys  # System-specific functions and parameters
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QWidget, QLabel, QVBoxLayout, QDialog, QLineEdit    # GUI elements
from PyQt5.QtGui import QPixmap  # For handling image display in labels
from PyQt5.QtMultimedia import QSoundEffect  # For playing short sound effects
from PyQt5.QtCore import QUrl, QTimer, Qt, QT_VERSION_STR  # Core Qt functions and constants

# UI and Custom Windows
from OOP2Final import Ui_MainWindow  # Auto-generated main UI from Qt Designer
from Manuel import Ui_Form  # UI class from manual control panel .ui file
from ManuelKod import ManuelModeWindow  # Manual control logic window
from home_page_driver import AgriAssistant  # Calendar and homepage GUI

# Robot and Connection Config
from connection_settings import ConnectionSettingsWindow  # Dialog for connection settings
from robot_parameters import WheeledRobotConfig, RobotParametersWindow  # Robot parameter management

# Data Logging and Analysis
from data_logger import TelemetryLogger, BasicAnalysis, DetailedAnalysis, MemoryLogger  # Logging classes

# Voice and Time Tools
import pyttsx3  # Text-to-speech engine
from datetime import datetime  # Time handling
import random  # Random value generation
import platform  # OS platform info

# Plotting Tools
import matplotlib.pyplot as plt  # General plotting
import os  # OS-level operations
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas  # Embed plots into PyQt5
from matplotlib.figure import Figure  # Matplotlib figure container

from PyQt5.QtGui import QIcon



# -----------------------------------------------------------------------------
# StyleSheet Imports
# These constants define reusable style templates for various UI components
# such as buttons, terminal, labels, and status indicators.
# -----------------------------------------------------------------------------
from style_sheets import (
    GREEN_BUTTON_STYLE,      # Style for start/confirm buttons
    RED_BUTTON_STYLE,        # Style for stop/danger buttons
    CENTRAL_WIDGET_STYLE,    # Main background style for central widget
    GROUPBOX_STYLE,          # Style for grouped sections (QGroupBox)
    MAIN_TITLE_STYLE,        # Style for the main header/title
    TERMINAL_STYLE,          # Style for the terminal-like command window
    WARNING_STYLE,           # Style for danger/alert states
    SAFE_STYLE               # Style for safe/normal operation states
)

# -----------------------------------------------------------------------------
# Text Constants Imports
# These are predefined informational strings used in dialogs or help sections.
# -----------------------------------------------------------------------------
from texts import (
    VERSION_TEXT,            # Version info text displayed in dialogs
    USER_MANUAL_TEXT,        # User guide/help documentation
    CONTACT_TEXT             # Developer contact info for support or feedback
)


##
# @class MainWindow
# @brief Central controller class for the AgriEdge smart agriculture system.
#
# @details
# Acts as the main interface and controller in the application. It integrates:
# - GUI initialization and layout styling
# - Command terminal interpretation
# - Voice alerts via pyttsx3
# - Sensor logging using MemoryLogger or TelemetryLogger
# - Robot mode switching (manual/autonomous)
# - Mapping and cultivation control
#
# @inherits QMainWindow
# @uses Ui_MainWindow (from Qt Designer)
# @uses MemoryLogger, TelemetryLogger
# @uses ConnectionSettingsWindow, RobotParametersWindow
# ### Related Modules:
# - @ref data_logger.py : For logging and analyzing telemetry data.
# - @ref connection_settings.py : For managing connection dialogs.
# - @ref robot_parameters.py : For loading and configuring robot parameters.
# - @ref style_sheets.py : For consistent GUI styling.
# - @ref texts.py : Static UI documentation and version info.

class MainWindow(QMainWindow):
    """
    @brief Initializes the main window and sets up the UI and functionality.
    """
    def __init__(self):
        """
        @brief Initializes the main application window and all connected components.
        Sets up UI elements, signal-slot connections, loggers, timers, styles, and TTS engine.
        """
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("AGRIEDGE CONTROL PANEL")
        self.setWindowIcon(QIcon("Assets/Icons/main.png"))
        # =============================================================================
        # @section Menu Action Icons
        # @brief Assign icons to QActions in the application's main menu bar.
        # 
        # This block sets icons for each QAction to improve visual usability
        # and make functionalities easily recognizable by users.
        # =============================================================================
        
        # === Connection & Settings Actions ===
        self.ui.actionConnection_Settings.setIcon(QIcon("C:/Users/doguk/OneDrive/Masaüstü/Bitirme Arayüz/Assets/Icons/settings.png"))
        self.ui.actionRobot_Parameters.setIcon(QIcon("C:/Users/doguk/OneDrive/Masaüstü/Bitirme Arayüz/Assets/Icons/robot.png"))
        
        # === Logging & Monitoring Actions ===
        self.ui.actionView_Logs.setIcon(QIcon("C:/Users/doguk/OneDrive/Masaüstü/Bitirme Arayüz/Assets/Icons/view.png"))
        self.ui.actionExport_Logs.setIcon(QIcon("C:/Users/doguk/OneDrive/Masaüstü/Bitirme Arayüz/Assets/Icons/export.png"))
        self.ui.actionSensor_History.setIcon(QIcon("C:/Users/doguk/OneDrive/Masaüstü/Bitirme Arayüz/Assets/Icons/sensors.png"))
        self.ui.actionSystem_Status.setIcon(QIcon("C:/Users/doguk/OneDrive/Masaüstü/Bitirme Arayüz/Assets/Icons/status.png"))
        
        # === Help & About Actions ===
        self.ui.actionUser_Manual.setIcon(QIcon("C:/Users/doguk/OneDrive/Masaüstü/Bitirme Arayüz/Assets/Icons/manual.png"))
        self.ui.actionContact_Developer.setIcon(QIcon("C:/Users/doguk/OneDrive/Masaüstü/Bitirme Arayüz/Assets/Icons/contact.png"))
        self.ui.actionVersion_Info.setIcon(QIcon("C:/Users/doguk/OneDrive/Masaüstü/Bitirme Arayüz/Assets/Icons/info.png"))
        self.ui.actionCheck_for_Updates.setIcon(QIcon("C:/Users/doguk/OneDrive/Masaüstü/Bitirme Arayüz/Assets/Icons/check.png"))
        
        # === File & Device Access Actions ===
        self.ui.actionOpen.setIcon(QIcon("C:/Users/doguk/OneDrive/Masaüstü/Bitirme Arayüz/Assets/Icons/home.png"))
        self.ui.actionLIDAR.setIcon(QIcon("C:/Users/doguk/OneDrive/Masaüstü/Bitirme Arayüz/Assets/Icons/lidar.png"))
        self.ui.actionKinect_Depth_Cam.setIcon(QIcon("C:/Users/doguk/OneDrive/Masaüstü/Bitirme Arayüz/Assets/Icons/kinect.png"))
        
        # === Mode Switch Actions ===
        self.ui.actionManuel.setIcon(QIcon("C:/Users/doguk/OneDrive/Masaüstü/Bitirme Arayüz/Assets/Icons/manuel.png"))
        self.ui.actionAutomatic.setIcon(QIcon("C:/Users/doguk/OneDrive/Masaüstü/Bitirme Arayüz/Assets/Icons/otonom.png"))
        
        # ------------------------ UI Styling Setup ------------------------
        self.ui.centralwidget.setStyleSheet(CENTRAL_WIDGET_STYLE)
        self.setStyleSheet(GROUPBOX_STYLE)
        self.ui.Main_Title.setStyleSheet(MAIN_TITLE_STYLE)
        
        self.ui.CmdReadOnly.setStyleSheet(TERMINAL_STYLE)
        self.ui.CmdReadOnly.setReadOnly(True)
    
        self.ui.ConnectButon.setStyleSheet(GREEN_BUTTON_STYLE)
        self.ui.StartMapping.setStyleSheet(GREEN_BUTTON_STYLE)
        self.ui.log_start_buton.setStyleSheet(GREEN_BUTTON_STYLE)
        self.ui.CapalamaStart.setStyleSheet(GREEN_BUTTON_STYLE)
    
        self.ui.DisconnectButton.setStyleSheet(RED_BUTTON_STYLE)
        self.ui.StopMapping.setStyleSheet(RED_BUTTON_STYLE)
        self.ui.log_stop_buton.setStyleSheet(RED_BUTTON_STYLE)
        self.ui.CapalamaStop.setStyleSheet(RED_BUTTON_STYLE)
    
        # ------------------------ Robot Configuration ------------------------
        self.robot_config = WheeledRobotConfig("AgriBot", 45.0, 18)
        self.mod = "manuel"
        self.system_connected = False
        self.ui.system_value.setText("Kapalı")
    
        # ------------------------ Logging System ------------------------
        self.logger = MemoryLogger(analyzer=BasicAnalysis())
        self.komut_gecmisi = []
    
        # ------------------------ Terminal Setup ------------------------
        self.terminal_acilis_mesaji()
        self.log_yaz("Terminal başlatıldı. Komutlar için 'help' yazın.", "INFO")
    
        # Replace standard input with custom terminal input widget
        self.custom_cmd_input = KomutGirisi(self)
        self.custom_cmd_input.setObjectName("CmdEnter")
        
        layout = self.ui.CmdEnter.parent().layout()  
        index = layout.indexOf(self.ui.CmdEnter)    
        layout.insertWidget(index, self.custom_cmd_input)  
        self.ui.CmdEnter.deleteLater()                     

        #self.ui.centralwidget.layout().addWidget(self.custom_cmd_input)
    
        # Terminal input events
        self.custom_cmd_input.returnPressed.connect(self.komut_isle)
        self.ui.CmdEnter.returnPressed.connect(self.komut_isle)
    
        # ------------------------ TTS Engine Setup ------------------------
        self.tts_motor = pyttsx3.init()
        for voice in self.tts_motor.getProperty('voices'):
            if "Alexa" in voice.name.lower():
                self.tts_motor.setProperty('voice', voice.id)
                break
        self.tts_motor.setProperty('rate', 150)
        self.sesli_bildirim("Welcome to the Agriedge system. Your assistant is now ready.")
    
        # ------------------------ Timer and Random Warning Simulation ------------------------
        self.warning_timer = QTimer()
        self.warning_timer.timeout.connect(self.randomly_update_warning)
        self.warning_timer.start(2000)
    
        # ------------------------ Sensor & Speed Input ------------------------
        self.ui.Speed_horizontalSlideR.valueChanged.connect(self.hiz_guncelle)
    
        # ------------------------ Mapping System ------------------------
        self.mapping_active = False
        self.mapping_timer = QTimer()
        self.mapping_timer.timeout.connect(self.mapping_surec_logu)
        self.ui.StartMapping.clicked.connect(self.baslat_mapping)
        self.ui.StopMapping.clicked.connect(self.durdur_mapping)
    
        # ------------------------ Cultivation (Çapalama) ------------------------
        self.capalama_active = False
        self.capalama_timer = QTimer()
        self.capalama_timer.timeout.connect(self.capalama_surec_logu)
        self.ui.CapalamaStart.clicked.connect(self.capalama_baslat)
        self.ui.CapalamaStop.clicked.connect(self.capalama_durdur)
    
        # ------------------------ Logging Controls ------------------------
        self.ui.log_start_buton.clicked.connect(self.baslat_loglama)
        self.ui.log_stop_buton.clicked.connect(self.durdur_loglama)
    
        # ------------------------ Command Mode Selection ------------------------
        self.ui.Detail_Check_Box.stateChanged.connect(self.analiz_modu_degistir)
    
        # ------------------------ Camera Simulation ------------------------
        self.set_robot_camera_image()
    
        # ------------------------ Action Menu Connections ------------------------
        self.ui.actionConnection_Settings.triggered.connect(self.open_settings_window)
        self.ui.actionRobot_Parameters.triggered.connect(self.open_robot_parameters)
        self.ui.actionLIDAR.triggered.connect(self.lidar_selected)
        self.ui.actionKinect_Depth_Cam.triggered.connect(self.kinect_selected)
        self.ui.actionManuel.triggered.connect(self.open_manuel_mode)
        self.ui.actionAutomatic.triggered.connect(self.open_otonom_mode)
        self.ui.actionOpen.triggered.connect(self.ac_takvim_penceresi)
    
        self.ui.actionUser_Manual.triggered.connect(self.show_user_manual)
        self.ui.actionVersion_Info.triggered.connect(self.show_version_info)
        self.ui.actionContact_Developer.triggered.connect(self.show_contact_info)
    
        self.ui.actionView_Logs.triggered.connect(self.view_logs)
        self.ui.actionExport_Logs.triggered.connect(self.export_logs)
        self.ui.actionSensor_History.triggered.connect(self.show_sensor_history)
        self.ui.actionSystem_Status.triggered.connect(self.show_system_status)
    
        # ------------------------ System Connect/Disconnect ------------------------
        self.ui.ConnectButon.clicked.connect(self.connect_robot)
        self.ui.DisconnectButton.clicked.connect(self.disconnect_robot)
        
        self.ui.ConnectButon.setIcon(QIcon("Assets/Icons/connect.png"))
        self.ui.DisconnectButton.setIcon(QIcon("Assets/Icons/disconnect.png"))
        
        self.ui.StartMapping.setIcon(QIcon("Assets/Icons/start_mapping.png"))
        self.ui.StopMapping.setIcon(QIcon("Assets/Icons/stop_mapping.png"))
        
        self.ui.CapalamaStart.setIcon(QIcon("Assets/Icons/hoe_start.png"))
        self.ui.CapalamaStop.setIcon(QIcon("Assets/Icons/hoe_stop.png"))
        
        self.ui.log_start_buton.setIcon(QIcon("Assets/Icons/log_start.png"))
        self.ui.log_stop_buton.setIcon(QIcon("Assets/Icons/log_stop.png"))
        
        self.ui.actionConnection_Settings.setIcon(QIcon("Assets/Icons/settings.png"))
        self.ui.actionRobot_Parameters.setIcon(QIcon("Assets/Icons/robot.png"))
        
        self.ui.actionView_Logs.setIcon(QIcon("Assets/Icons/view.png"))
        self.ui.actionExport_Logs.setIcon(QIcon("Assets/Icons/export.png"))
        self.ui.actionSensor_History.setIcon(QIcon("Assets/Icons/sensors.png"))
        self.ui.actionSystem_Status.setIcon(QIcon("Assets/Icons/status.png"))
        
        self.ui.actionUser_Manual.setIcon(QIcon("Assets/Icons/manual.png"))
        self.ui.actionContact_Developer.setIcon(QIcon("Assets/Icons/contact.png"))
        self.ui.actionVersion_Info.setIcon(QIcon("Assets/Icons/info.png"))
        self.ui.actionCheck_for_Updates.setIcon(QIcon("Assets/Icons/check.png"))
        
        self.ui.actionOpen.setIcon(QIcon("Assets/Icons/home.png"))
        
        self.ui.actionManuel.setIcon(QIcon("Assets/Icons/manuel.png"))
        self.ui.actionAutomatic.setIcon(QIcon("Assets/Icons/otonom.png"))
        
        self.ui.actionLIDAR.setIcon(QIcon("Assets/Icons/lidar.png"))
        self.ui.actionKinect_Depth_Cam.setIcon(QIcon("Assets/Icons/kinect.png"))
        self.ui.actionView_Map.setIcon(QIcon("Assets/Icons/viewmap.png"))
        self.ui.actionExport_Map.setIcon(QIcon("Assets/Icons/exportmap.png"))




    def open_settings_window(self):
        """
        @brief Opens the window for connection settings.
        @details Launches a modal dialog where the user can configure 
                 network or serial connection parameters for the robot.
        """
        self.settings_dialog = ConnectionSettingsWindow()
        self.settings_dialog.exec_()  # Open as modal dialog
        self.ui.statusbar.showMessage("🟢 Setting Açıldı!", 3000)
    
    def ac_takvim_penceresi(self):
        """
        @brief Opens the calendar (home page) window.
        @details This function shows the calendar UI screen used for 
                 managing agricultural notes or timeline events.
        """
        self.takvim_penceresi = AgriAssistant()
        self.takvim_penceresi.show()
        self.ui.statusbar.showMessage("🟢 Home Page Açıldı!", 3000)
    
    def terminal_acilis_mesaji(self):
        """
        @brief Displays the initial terminal message with timestamp.
        @details Sends a formatted welcome message to the terminal 
                 display when the application starts.
        """
        saat = datetime.now().strftime("%H:%M:%S")
        self.log_yaz("="*40, "INFO")
        self.log_yaz(f"🧠 AGRIEDGE Sistem Konsolu", "STATUS")
        self.log_yaz(f"⌚ Giriş Zamanı: {saat}", "INFO")
        self.log_yaz(f"👋 Hoş geldiniz! Yardım için 'help' yazın.", "INFO")
        self.log_yaz("="*40, "INFO")
        self.ui.statusbar.showMessage("👋 Hoş geldiniz!", 3000)
    
    def open_robot_parameters(self):
        """
        @brief Opens a dialog for configuring robot parameters.
        @details Shows a new window that allows the user to 
                 adjust robot-specific attributes such as wheel size, 
                 max speed, or sensor range.
        """
        self.robot_param_window = RobotParametersWindow()
        self.robot_param_window.show()
        self.ui.statusbar.showMessage("🟢 Robot Parameters Açıldı!", 3000)


    def log_yaz(self, mesaj, seviye="INFO"):
        """
        @brief Logs messages to the terminal output with timestamps.
        @param mesaj The message string to be displayed in the terminal.
        @param seviye The severity level of the message (e.g., INFO, STATUS, WARNING, ERROR, COMMAND).
        @details Applies color-coding based on the severity level and appends the message
                 to the terminal area (`CmdReadOnly`) with a timestamp.
        """
        zaman = datetime.now().strftime("%H:%M:%S")
    
        renkler = {
            "INFO": "#BBBBBB",        # Light gray
            "STATUS": "#00FF99",      # Bright green
            "WARNING": "#FFA500",     # Orange
            "ERROR": "#FF3333",       # Red
            "COMMAND": "#0099FF"      # Blue
        }
    
        renk = renkler.get(seviye, "#DDDDDD")
        html_mesaj = f'<span style="color:{renk}">[{zaman}] {mesaj}</span>'
        self.ui.CmdReadOnly.append(html_mesaj)

    def show_version_info(self):
        """
        @brief Displays system and application version information.
        @details Shows a popup window containing details like OS name, architecture,
                 Python version, and Qt version using predefined format text.
        """
        version_text = VERSION_TEXT.format(
            os_name=platform.system(),
            os_version=platform.release(),
            os_arch=platform.machine(),
            python_version=platform.python_version(),
            qt_version=QT_VERSION_STR
        )
        QMessageBox.information(self, "Version Info", version_text)
        self.ui.statusbar.showMessage("🟢 Version Info Açıldı!", 3000)
    
    def show_user_manual(self):
        """
        @brief Shows a user manual popup window.
        @details Displays instructions or usage guide using predefined manual text.
        """
        QMessageBox.information(self, "User Manual", USER_MANUAL_TEXT)
        self.ui.statusbar.showMessage("🟢 User Manual Açıldı!", 3000)
    
    def show_contact_info(self):
        """
        @brief Shows developer contact information.
        @details Displays a popup with developer or support contact details.
        """
        QMessageBox.information(self, "Contact Developer", CONTACT_TEXT)
        self.ui.statusbar.showMessage("🟢 Contact Developer Page Açıldı!", 3000)

    def view_logs(self):
        """
        @brief Displays the log data and, if enabled, analysis results.
        @details Retrieves logged telemetry data from the logger instance. If the analyzer is
                 set to DetailedAnalysis, it also appends the statistical analysis results to the display.
        """
    
        data = self.logger.get_data()  # Retrieve the current log DataFrame
    
        # If no data is available, notify the user
        if data is None or data.empty:
            QMessageBox.information(self, "Log Verisi", "Henüz veri kaydı yok.")
            return
    
        try:
            # Check if detailed analysis is active
            if isinstance(self.logger.analyzer, DetailedAnalysis):
                analysis = self.logger.analyze()  # Run analysis (e.g., mean, variance)
                log_text = data.to_string(index=False)  # Convert DataFrame to string (no index column)
    
                # Format additional analysis output
                detay_text = "\n\n📊 DETAYLI ANALİZ:\n"
                if isinstance(analysis, dict):
                    for key, val in analysis.items():
                        detay_text += f"{key}: {val}\n"  # Format each metric line by line
                else:
                    detay_text += str(analysis)  # Fallback for unexpected output types
    
                full_text = log_text + detay_text  # Combine log and analysis outputs
            else:
                # If in basic mode, only display time and speed columns
                full_text = data[["Zaman", "Hiz"]].to_string(index=False)
    
            # Show the final result in a popup window
            QMessageBox.information(self, "Log Verisi", full_text)
    
        except Exception as e:
            # Display an error if any exception occurs during log rendering
            QMessageBox.warning(self, "Hata", f"Log görüntüleme sırasında hata oluştu:\n{str(e)}")


    def export_logs(self):
        """
        @brief Exports the logs to a CSV file and shows confirmation.
        @details This method saves the collected telemetry data to a CSV file using the
                 logger's export function. It notifies the user about whether the export
                 was performed under detailed or basic analysis mode.
        """
    
        filename = self.logger.export_to_csv()  # Export data to CSV and store the filename
    
        # Check the type of analyzer to determine the analysis mode
        if isinstance(self.logger.analyzer, DetailedAnalysis):
            self.log_yaz("📤 Detaylı analiz ile dışa aktarım yapıldı.", "INFO")  # Log detailed export
            self.ui.statusbar.showMessage("📤 Detaylı analiz ile dışa aktarım yapıldı.", 3000)
        else:
            self.log_yaz("📤 Temel analiz ile dışa aktarım yapıldı.", "INFO")  # Log basic export
            self.ui.statusbar.showMessage("📤 Temel analiz ile dışa aktarım yapıldı.!", 3000)
    
        # Notify user with the filename of the exported logs
        QMessageBox.information(self, "Dışa Aktarım", f"Loglar '{filename}' dosyasına kaydedildi.")

    def show_sensor_history(self):
        """
        @brief Opens a dialog that plots past sensor values.
        @details Retrieves historical sensor data from the logger and displays it
                 both in a custom dialog window and as a matplotlib plot.
                 The plot includes speed, temperature, and battery data over time.
        """
    
        df = self.logger.get_data()  # Get logged telemetry data as a DataFrame
    
        # Check if there's any recorded data; notify user if empty
        if df.empty:
            QMessageBox.information(self, "Sensör Geçmişi", "Kayıtlı veri yok.")
            return
    
        # Open a custom dialog window showing sensor history
        self.sensor_window = SensorHistoryWindow(df, self)
        self.sensor_window.show()
    
        # Create a new figure for plotting with a fixed size
        plt.figure(figsize=(10, 5))
    
        # Plot each sensor metric with corresponding label
        plt.plot(df["Zaman"], df["Hiz"], label="Hız")
        plt.plot(df["Zaman"], df["Sicaklik"], label="Sıcaklık")
        plt.plot(df["Zaman"], df["Batarya"], label="Batarya")
    
        # Set axis labels and title
        plt.xlabel("Zaman")
        plt.ylabel("Değer")
        plt.title("Sensör Geçmişi")
    
        # Annotate with current analysis mode
        mode = "Detaylı" if isinstance(self.logger.analyzer, DetailedAnalysis) else "Temel"
        plt.suptitle(f"Analiz Modu: {mode}", fontsize=10, color="gray")
    
        plt.legend()                 # Show legend for all metrics
        plt.xticks(rotation=45)     # Rotate x-axis ticks for readability
        plt.tight_layout()          # Adjust layout to prevent clipping
        plt.show()                  # Display the plot


    def show_system_status(self):
        """
        @brief Displays the system’s current operational status.
        @details Shows a dialog with key metrics such as system connection state, 
                 current mode (manual or autonomous), battery percentage, temperature, 
                 speed, and whether detailed analysis is enabled.
        """
    
        # Determine whether the system is connected
        status = "Açık" if self.system_connected else "Kapalı"
    
        # Fetch current robot mode (manuel / otonom)
        mod = self.mod
    
        # Get current sensor values from UI
        hiz = self.ui.Speed_Value.text()         # Current speed
        batarya = self.ui.Battery_Value.text()   # Battery percentage
        sicaklik = self.ui.Temp_Value.text()     # Temperature in Celsius
    
        # Determine if detailed or basic analysis is active
        analiz_modu = "Detaylı" if isinstance(self.logger.analyzer, DetailedAnalysis) else "Temel"
    
        # Prepare the formatted status message
        status_text = f"""
        🖥️ Sistem Durumu: {status}
        🚦 Mod: {mod}
        📊 Analiz Modu: {analiz_modu}
        🔋 Batarya: {batarya}%
        🌡️ Sıcaklık: {sicaklik}°C
        🚗 Hız: {hiz}
        """
    
        # Show the status in a message box
        QMessageBox.information(self, "Sistem Durumu", status_text)
    
        # Update the status bar with a message
        self.ui.statusbar.showMessage("Sistem Durumu Açıldı", 3000)


    def analiz_modu_degistir(self, state):
        """
        @brief Switches between detailed and basic analysis logging modes.
        @param state Checkbox state (Qt.Checked or Qt.Unchecked).
        @details When the user checks the analysis mode checkbox, this method
                 enables a detailed logging mechanism that stores data into CSV
                 files using pandas. When unchecked, it switches back to basic 
                 in-memory logging mode for lightweight operation.
        """
    
        if state == Qt.Checked:
            # Enable detailed analysis mode with persistent telemetry logging (to CSV)
            self.logger = TelemetryLogger(analyzer=DetailedAnalysis())
    
            # Log the mode switch to terminal
            self.log_yaz("🔍 Detaylı analiz + TelemetryLogger aktif edildi.", "INFO")
    
            # Announce the mode switch via voice assistant
            self.sesli_bildirim("Detailed analysis with telemetry logger activated.")
    
            # Show confirmation in the status bar
            self.ui.statusbar.showMessage("🔍 Detaylı analiz + TelemetryLogger aktif edildi.", 3000)
        else:
            # Switch to basic analysis mode using memory-only logging
            self.logger = MemoryLogger(analyzer=BasicAnalysis())
    
            # Log the mode switch to terminal
            self.log_yaz("📈 Temel analiz + MemoryLogger aktif edildi.", "INFO")
    
            # Announce the mode switch via voice assistant
            self.sesli_bildirim("Basic analysis with memory logger activated.")
    
            # Show confirmation in the status bar
            self.ui.statusbar.showMessage("📈 Temel analiz + MemoryLogger aktif edildi.", 3000)


    def komut_isle(self):
        """
        @brief Handles command parsing and execution from terminal input.
        @details This method reads the input from the custom terminal widget,
                 interprets built-in commands (such as help, status, mod changes),
                 and executes the corresponding system functionality. It also supports
                 command aliases and basic validation.
        """
    
        # Get the command input, remove leading/trailing whitespace, convert to lowercase
        komut = self.custom_cmd_input.text().strip().lower()
        if komut == "":
            return  # Do nothing for empty input
    
        # Define aliases for convenience (e.g., 's' -> 'status')
        alias = {"s": "status", "r": "restart", "h": "help"}
        komut = alias.get(komut, komut)
    
        # Log the typed command
        self.log_yaz(f">> {komut}", "COMMAND")
    
        # Add to history if not already the last one
        if not self.komut_gecmisi or self.komut_gecmisi[-1] != komut:
            self.komut_gecmisi.append(komut)
        self.custom_cmd_input.set_gecmis_kaynak(self.komut_gecmisi)
    
        # Command: Help
        if komut == "help":
            self.log_yaz("Komutlar: help, status, temizle, restart, set hız [0-100], delay [sn]", "INFO")
    
        # Command: Clear terminal
        elif komut == "temizle":
            self.ui.CmdReadOnly.clear()
    
        # Command: Show system status
        elif komut == "status":
            mevcut_hiz = self.ui.Speed_Value.text()
            mevcut_mod = self.mod
            sistem_durumu = "Açık" if self.system_connected else "Kapalı"
            self.log_yaz(f"🟢 Sistem Durumu: {sistem_durumu} | Mod: {mevcut_mod} | Batarya: %85 | Hız: {mevcut_hiz}", "STATUS")
    
        # Command: Start mapping
        elif komut == "map start":
            self.baslat_mapping()
    
        # Command: Stop mapping
        elif komut == "map stop":
            self.durdur_mapping()
    
        # Command: Switch to manual mode
        elif komut == "mod manuel":
            if not self.system_connected:
                self.log_yaz("❌ Önce sisteme bağlanmalısınız!", "ERROR")
                self.sesli_bildirim("Please connect to the system first.")
                return
    
            self.mod = "Manuel"
            self.ui.Mod_Value.setText("Manuel")
            self.log_yaz("🚗 Manuel moda geçildi.", "STATUS")
    
        # Command: Switch to autonomous mode
        elif komut == "mod otonom":
            if not self.system_connected:
                self.log_yaz("❌ Önce sisteme bağlanmalısınız!", "ERROR")
                self.sesli_bildirim("Please connect to the system first.")
                return
    
            self.mod = "Otonom"
            self.ui.Mod_Value.setText("Otonom")
            self.log_yaz("🤖 Otonom moda geçildi.", "STATUS")
    
        # Command: Restart the system (simulate reboot with delay)
        elif komut == "restart":
            self.log_yaz("Sistem yeniden başlatılıyor...", "WARNING")
            QTimer.singleShot(2000, lambda: self.log_yaz("✅ Yeniden başlatma tamamlandı.", "STATUS"))
    
        # Command: Display version information
        elif komut == "version":
            self.log_yaz("📦 AGRIEDGE v1.0", "STATUS")
            self.log_yaz(f"🖥️  System: {platform.system()} {platform.release()} {platform.machine()}", "INFO")
            self.log_yaz(f"🐍  Python: {platform.python_version()}", "INFO")
            self.log_yaz(f"🧱  Qt Version: {QT_VERSION_STR}", "INFO")
            self.log_yaz("🎛️  UI Framework: PyQt5", "INFO")
            self.sesli_bildirim("Agriedge system version 1.0 loaded.")
    
        # Command: Set speed (e.g., "set hız 50")
        elif komut.startswith("set hız"):
            try:
                hiz_deger = int(komut.split()[-1])
                if 0 <= hiz_deger <= 100:
                    self.log_yaz(f"Hız {hiz_deger} olarak ayarlandı.", "STATUS")
                    self.ui.Speed_horizontalSlideR.setValue(hiz_deger)
                    self.sesli_bildirim(f"Speed set to {hiz_deger}.")
                else:
                    self.log_yaz("Hız değeri 0-100 arasında olmalı!", "ERROR")
            except:
                self.log_yaz("Geçersiz hız komutu. Örnek: set hız 40", "ERROR")
    
        # Command: Delay execution (e.g., "delay 5")
        elif komut.startswith("delay "):
            try:
                saniye = int(komut.split()[1])
                self.log_yaz(f"{saniye} saniye sonra komut tetiklenecek...", "INFO")
                QTimer.singleShot(saniye * 1000, lambda: self.log_yaz("⏱️ Gecikmeli komut çalıştı!", "STATUS"))
            except:
                self.log_yaz("Geçersiz delay komutu. Örnek: delay 5", "ERROR")
    
        # Unknown command
        else:
            self.log_yaz("Bilinmeyen komut!", "ERROR")
    
        # Clear the command input after processing
        self.custom_cmd_input.clear()


    def hiz_guncelle(self, value):
        """
        @brief Updates the UI speed display based on slider input.
        @param value Slider value representing speed.
        """
    
        # Update the speed label text with the current slider value
        self.ui.Speed_Value.setText(str(value))


    def sesli_bildirim(self, mesaj):
        """
        @brief Provides audio feedback using text-to-speech.
        @param mesaj The message to be spoken.
        """
    
        # Queue the message to be spoken by the text-to-speech engine
        self.tts_motor.say(mesaj)
    
        # Wait until the speaking is finished
        self.tts_motor.runAndWait()


    def lidar_selected(self):
        """
        @brief Triggered when the LIDAR option is selected from the menu.
        
        This function displays an information dialog and updates the status bar
        to inform the user that mapping with LIDAR is being initiated.
        """
    
        # Show a message box informing the user about LIDAR mapping start
        QMessageBox.information(self, "LIDAR Seçildi", "LIDAR ile haritalama başlatılıyor...")
    
        # Update the status bar to reflect the action
        self.ui.statusbar.showMessage("LIDAR ile haritalama başlatılıyor.", 3000)


    def kinect_selected(self):
        """
        @brief Triggered when the Kinect camera option is selected.
        
        Displays an informational dialog and updates the status bar to notify
        the user that mapping will begin using the Kinect Depth Camera.
        """
    
        # Inform the user with a pop-up dialog
        QMessageBox.information(self, "Kinect Seçildi", "Kinect Depth Camera ile haritalama başlatılıyor...")
    
        # Update the status bar with the same message
        self.ui.statusbar.showMessage("Kinect(Stereo) ile haritalama başlatılıyor.", 3000)

        
    def open_manuel_mode(self):
        """
        @brief Opens the manual control window and switches the system to manual mode.
    
        If the robot system is not connected, it shows a warning message. Otherwise,
        it launches the manual mode window and updates the mode state accordingly.
        """
    
        # Check system connection before proceeding
        if not self.system_connected:
            QMessageBox.warning(self, "Bağlantı Gerekli", "Lütfen önce sisteme bağlanın!")
            return
    
        # Open manual control window
        self.manuel_window = ManuelModeWindow(self)
        self.manuel_window.show()
    
        # Update system mode to manual
        self.mod = "Manuel"
        self.ui.Mod_Value.setText("Manuel")
    
        # Log and notify user
        self.log_yaz("🚗 Menüden manuel moda geçildi.", "STATUS")
        self.ui.statusbar.showMessage("Manuel moda geçildi.", 3000)

    
    def open_otonom_mode(self):
        """
        @brief Switches the system to autonomous mode.
    
        Checks whether the system is connected before switching. 
        If connected, updates the mode to 'Otonom', reflects this on the UI,
        and logs the transition both in the terminal and the status bar.
        """
    
        # Prevent switching if the system is not connected
        if not self.system_connected:
            QMessageBox.warning(self, "Bağlantı Gerekli", "Lütfen önce sisteme bağlanın!")
            return
    
        # Update the mode to autonomous
        self.mod = "Otonom"
        self.ui.Mod_Value.setText("Otonom")
    
        # Log the mode change
        self.log_yaz("🤖 Menüden otonom moda geçildi.", "STATUS")
        self.ui.statusbar.showMessage("Otonom moda geçildi.", 3000)

    
    def set_robot_camera_image(self): 
        """
        @brief Sets a default image in the robot camera view.
    
        This function assigns a placeholder image ("Default.png") to the camera display area 
        in the UI, ensuring it scales properly and is centered within its label.
        """
    
        # Get the camera display label from the UI
        self.image_label = self.ui.label_2
    
        # Set the default placeholder image
        self.image_label.setPixmap(QPixmap("Default.png"))
    
        # Scale the image to fit the label size
        self.image_label.setScaledContents(True)
    
        # Center the image within the label
        self.image_label.setAlignment(Qt.AlignCenter)


    def update_warning_lights(self, detected):
        """
        @brief Changes the warning light color based on detected obstacles.
        @param detected Boolean indicating whether a threat is detected.
    
        This function updates the warning label to reflect the current safety status. If a 
        threat (such as a human or animal) is detected, the label turns red with a warning icon. 
        If the area is safe, the label turns green.
        """
    
        if detected:
            # Display a danger icon and message when something is detected
            self.ui.labelWarning1.setText("🔥 Tehlike")
            self.ui.labelWarning1.setAlignment(Qt.AlignCenter)
            self.ui.labelWarning1.setStyleSheet(WARNING_STYLE)
        else:
            # Display a safe message when no danger is present
            self.ui.labelWarning1.setText("✔ Güvenli")
            self.ui.labelWarning1.setAlignment(Qt.AlignCenter)
            self.ui.labelWarning1.setStyleSheet(SAFE_STYLE)


    def randomly_update_warning(self):
        """
        @brief Simulates hazard detection to test warning system.
    
        This method randomly selects a boolean value (True or False)
        to simulate whether a threat is detected or not. It then calls
        the update_warning_lights method to update the UI accordingly.
        Useful for testing warning indicators without actual sensor input.
        """
    
        # Randomly determine whether a threat is present
        detected = random.choice([True, False])
    
        # Update the warning light based on the simulated result
        self.update_warning_lights(detected)

        
    def connect_robot(self):
        """
        @brief Simulates establishing a connection to the robot system.
    
        This method updates the system's connection status to "connected",
        modifies the UI to reflect the connection state visually,
        logs the event to the terminal, and provides auditory feedback.
        It also shows a confirmation message on the status bar.
        """
    
        # Mark the system as connected
        self.system_connected = True
    
        # Update the UI label to show system is "Açık" (Open/Connected)
        self.ui.system_value.setText("Açık")
        self.ui.system_value.setStyleSheet("color: green; font-weight: bold;")
    
        # Log the connection status in the terminal panel
        self.log_yaz("🔗 Sistem bağlantısı kuruldu.", "STATUS")
    
        # Speak the confirmation using text-to-speech
        self.sesli_bildirim("System connected.")
    
        # Show a temporary status bar message
        self.ui.statusbar.showMessage("✅ Sistem bağlantısı kuruldu.", 3000)

    
    def disconnect_robot(self):
        """
        @brief Simulates disconnecting from the robot system.
    
        This method updates the internal state and GUI to reflect that the robot
        is no longer connected. It also logs the disconnection, provides audio
        feedback, and shows a status bar notification.
        """
    
        # Set system connection status to False
        self.system_connected = False
    
        # Update system status label to "Kapalı" (Closed/Disconnected)
        self.ui.system_value.setText("Kapalı")
        self.ui.system_value.setStyleSheet("color: red; font-weight: bold;")
    
        # Log disconnection in the terminal
        self.log_yaz("🔌 Sistem bağlantısı kesildi.", "WARNING")
    
        # Announce the disconnection via TTS
        self.sesli_bildirim("System disconnected.")
    
        # Notify user through status bar
        self.ui.statusbar.showMessage("❌ 'Bağlantıyı Kes' butonuna tıklandı", 3000)


    def baslat_mapping(self):
        """
        @brief Initiates the mapping process and telemetry logging.
    
        This function starts the automated mapping procedure if the system is 
        connected and no cultivation is running. It activates the telemetry timer
        for logging sensor data periodically and updates the UI accordingly.
        """
    
        # Check if system is connected before starting mapping
        if not self.system_connected:
            QMessageBox.warning(self, "Bağlantı Gerekli", "Lütfen önce sisteme bağlanın!")
            return
    
        # If cultivation is active, block mapping process
        if self.capalama_active:
            QMessageBox.warning(self, "Çapalama Aktif", "Lütfen önce çapalamayı durdurun.")
            return
    
        # Prevent duplicate starts
        if self.mapping_active:
            return
    
        # Activate mapping flag and start the mapping timer (e.g., logging steps)
        self.mapping_active = True
        self.mapping_timer.start(3000)  # Log mapping status every 3 seconds
    
        # Update UI to reflect mapping status
        self.ui.haritalama_value.setText("Haritalama Aktif")
        self.ui.haritalama_value.setStyleSheet("color: green; font-weight: bold;")
    
        # Log action in terminal
        self.log_yaz("🗺️ Haritalama başlatıldı.", "STATUS")
    
        # Start telemetry timer for logging system data
        self.telemetry_timer = QTimer()
        self.telemetry_timer.timeout.connect(self.log_sistem_verisi)
        self.telemetry_timer.start(3000)  # Log every 3 seconds
    
        # Notify via status bar
        self.ui.statusbar.showMessage("🗺️ 'Haritalamayı Başlat' butonuna tıklandı", 3000)


    def durdur_mapping(self):
        """
        @brief Stops the ongoing mapping process.
    
        This function halts the mapping routine and disables telemetry logging.
        It updates the UI status and informs the user through terminal and voice feedback.
        """
    
        # If mapping is already stopped, log the info and exit
        if not self.mapping_active:
            self.log_yaz("⚠️ Haritalama zaten durdurulmuş.", "INFO")
            return
    
        # Deactivate mapping flag
        self.mapping_active = False
    
        # Log the mapping stop event
        self.log_yaz("🛑 Haritalama durduruldu.", "WARNING")
    
        # Provide audio notification
        self.sesli_bildirim("Mapping stopped.")
    
        # Update UI to show mapping is no longer active
        self.ui.haritalama_value.setText("Haritalama Aktif Değil")
        self.ui.haritalama_value.setStyleSheet("color: Red; font-weight: bold;")
    
        # Stop telemetry timer to halt data logging
        self.telemetry_timer.stop()
    
        # Display status message on the status bar
        self.ui.statusbar.showMessage("🛑 'Haritalamayı Durdur' butonuna tıklandı", 3000)


    def mapping_surec_logu(self):
        """
        @brief Logs status messages during the mapping process.
    
        This method is periodically triggered by a QTimer while mapping is active.
        It logs the current status to the terminal, providing feedback to the user.
        """
    
        # Only log if the mapping process is currently active
        if self.mapping_active:
            self.log_yaz("🗺️ Haritalama sürüyor...", "INFO")


    def capalama_baslat(self):
        """
        @brief Starts the tilling (Çapalama) operation.
    
        This function checks if the system is connected and mapping is inactive 
        before enabling the tilling process. It updates UI indicators, starts a timer 
        for periodic status logging, and logs the start event to the terminal.
        """
    
        # Ensure system is connected before starting tilling
        if not self.system_connected:
            QMessageBox.warning(self, "Bağlantı Gerekli", "Lütfen önce sisteme bağlanın!")
            return
    
        # Prevent tilling if mapping is already active
        if self.mapping_active:
            QMessageBox.warning(self, "Haritalama Aktif", "Lütfen önce haritalamayı durdurun.")
            return
    
        # If already active, do nothing
        if self.capalama_active:
            return
    
        # Activate tilling state
        self.capalama_active = True
    
        # Start logging timer: logs status every 3 seconds
        self.capalama_timer.start(3000)
    
        # Update UI label to show active state
        self.ui.capalama_value.setText("Başladı")
        self.ui.capalama_value.setStyleSheet("color: Blue; font-weight: bold;")
    
        # Log to terminal and status bar
        self.log_yaz("🔄 Çapalama başlatıldı.", "STATUS")
        self.ui.statusbar.showMessage("🔄 'Çapalama Başlat' butonuna tıklandı", 3000)

        
    def capalama_durdur(self):
        """
        @brief Ends the tilling (Çapalama) operation.
    
        This function deactivates the tilling process if it is currently running.
        It stops the associated timer, updates the user interface to reflect the change,
        and logs the action both visually and in the terminal.
        """
    
        # If tilling is not active, there's nothing to stop
        if not self.capalama_active:
            return
    
        # Deactivate tilling flag
        self.capalama_active = False
    
        # Stop the logging timer
        self.capalama_timer.stop()
    
        # Update UI to indicate that tilling has stopped
        self.ui.capalama_value.setText("Başlamadı")
        self.ui.capalama_value.setStyleSheet("color: Red; font-weight: bold;")
    
        # Log the event to the terminal
        self.log_yaz("⛔ Çapalama durduruldu.", "WARNING")


    def capalama_surec_logu(self):
        """
        @brief Logs status messages during the tilling process.
    
        This function is periodically triggered by a timer while the tilling
        (Çapalama) operation is active. It logs real-time feedback in the terminal
        and updates the status bar accordingly.
        """
    
        # If tilling is active, log a progress message to the terminal
        if self.capalama_active:
            self.log_yaz("⚙️ Çapalama sürüyor...", "INFO")
    
        # Update the status bar regardless of state (can be customized)
        self.ui.statusbar.showMessage("⛔ 'Çapalama Durdur' butonuna tıklandı", 3000)


    def log_sistem_verisi(self):
        """
        @brief Logs current sensor values for speed, temperature, and battery level.
        @details 
        This function fetches the latest UI-displayed sensor values and 
        logs them using the selected logger (MemoryLogger or TelemetryLogger). 
        It also displays the log entry in the terminal and a confirmation 
        in the status bar.
        """
    
        # Get current sensor values from UI
        hiz = int(self.ui.Speed_Value.text())         # Read speed value from UI
        sicaklik = int(self.ui.Temp_Value.text())     # Read temperature value from UI
        batarya = int(self.ui.Battery_Value.text())   # Read battery level from UI
    
        # Log the data using the logger (selected mode determines format)
        self.logger.log_sensor_data(hiz, sicaklik, batarya)
    
        # Write to terminal
        self.log_yaz(f"📥 Veri kaydedildi | Hız: {hiz}, Sıcaklık: {sicaklik}, Batarya: {batarya}", "INFO")
    
        # Show confirmation in the status bar
        self.ui.statusbar.showMessage("💾 Log kaydedildi", 5000)

        
    def baslat_loglama(self):
        """
        @brief Starts periodic logging of sensor data.
        @details 
        This method initializes a QTimer that logs system data such as speed, 
        temperature, and battery level every 3 seconds. It updates the UI to reflect 
        the logging status and provides feedback via terminal and status bar.
        """
    
        # Check if the system is connected before starting logging
        if not self.system_connected:
            QMessageBox.warning(self, "Bağlantı Yok", "Önce sisteme bağlanmalısınız!")
            return
    
        # Create and configure the telemetry timer
        self.telemetry_timer = QTimer()
        self.telemetry_timer.timeout.connect(self.log_sistem_verisi)
        self.telemetry_timer.start(3000)  # Trigger logging every 3 seconds
    
        # Terminal log message
        self.log_yaz("📊 Loglama başlatıldı. Her 3 saniyede bir veri kaydediliyor.", "INFO")
    
        # Voice feedback
        self.sesli_bildirim("Logging started.")
    
        # Update UI to show active logging status
        self.ui.loglama_value.setText("Aktif")
        self.ui.loglama_value.setStyleSheet("color: green; font-weight: bold;")
    
        # Status bar message
        self.ui.statusbar.showMessage("📊 'Log Başlat' butonuna tıklandı", 3000)


    def durdur_loglama(self):
        """
        @brief Stops sensor data logging and exports results.
        @details 
        Terminates the active telemetry timer if it exists, logs the shutdown event,
        exports the collected sensor data to a CSV file, and performs a final analysis 
        that is printed in the terminal. Also updates the UI to reflect the stopped state.
        """
    
        # If telemetry timer exists, stop it to cease data logging
        if hasattr(self, 'telemetry_timer'):
            self.telemetry_timer.stop()
    
        # Log shutdown message to terminal and TTS
        self.log_yaz("⛔ Loglama durduruldu. Veri kaydı sona erdi.", "WARNING")
        self.sesli_bildirim("Logging stopped.")
    
        # Export logs to CSV and log the filename
        dosya = self.logger.export_to_csv()
        self.log_yaz(f"📁 Log verisi '{dosya}' dosyasına kaydedildi.", "STATUS")
    
        # Update UI to show logging is off
        self.ui.loglama_value.setText("Pasif")
        self.ui.loglama_value.setStyleSheet("color: gray; font-weight: bold;")
        self.ui.statusbar.showMessage("📁 'Log Durdur' butonuna tıklandı", 3000)
    
        # Analyze the logged data and display results
        analiz_sonuclari = self.logger.analyze()
        if isinstance(analiz_sonuclari, str):
            # If it's a plain string (basic summary), log as warning
            self.log_yaz(f"📊 {analiz_sonuclari}", "WARNING")
        else:
            # If it's a dict (detailed results), print each item
            self.log_yaz("📊 Log verisi analizi:", "INFO")
            for baslik, deger in analiz_sonuclari.items():
                self.log_yaz(f"{baslik}: {deger}", "INFO")


##
# @class KomutGirisi
# @brief Custom line edit widget that supports command history and navigation.
#
# @details
# `KomutGirisi` is a subclass of `QLineEdit` designed specifically for terminal-style input
# within the AgriEdge robot interface. It enhances the basic input field by allowing the user
# to navigate through previous commands using the arrow keys, simulating a terminal environment.
#
# This widget works in tandem with the `MainWindow`'s command parsing logic.
# It is often embedded inside a terminal console GUI.
#
# ### Features:
# - Navigate command history with ↑ and ↓ keys.
# - Shared command memory with external list.
# - Intuitive integration into PyQt5-based layouts.
#
# @inherits QLineEdit
#
# @see MainWindow::komut_isle()
# @see MainWindow::terminal_acilis_mesaji()


class KomutGirisi(QLineEdit):
    """
    @class KomutGirisi
    @brief Custom QLineEdit to support command history with arrow key navigation.
    """

    def __init__(self, parent=None):
        """
        @brief Constructor for the custom command input widget.
        @param parent The parent widget.
        """
        super().__init__(parent)
        self.komut_gecmisi = []  # Stores list of previously entered commands
        self.komut_index = -1    # Keeps track of the current position in history

    def set_gecmis_kaynak(self, kaynak):
        """
        @brief Assigns external command history list.
        @param kaynak A list of past command strings to be navigated.
        """
        self.komut_gecmisi = kaynak              # Link to the external history list
        self.komut_index = len(kaynak)           # Reset index to the end of list (no command selected)

    def keyPressEvent(self, event):
        """
        @brief Handles arrow key events to navigate through command history.
        @param event Key press event triggered by user input.
        """

        if event.key() == Qt.Key_Up:
            # User pressed ↑: move up in history if not at the beginning
            if self.komut_index > 0:
                self.komut_index -= 1
                self.setText(self.komut_gecmisi[self.komut_index])  # Set previous command

        elif event.key() == Qt.Key_Down:
            # User pressed ↓: move down in history if not at the latest
            if self.komut_index < len(self.komut_gecmisi) - 1:
                self.komut_index += 1
                self.setText(self.komut_gecmisi[self.komut_index])
            else:
                self.komut_index = len(self.komut_gecmisi)  # Reset to new input
                self.clear()  # Clear text field for fresh command

        else:
            # For all other keys, proceed with default behavior
            super().keyPressEvent(event)


##
# @class SensorHistoryWindow
# @brief Dialog window that visualizes historical sensor data using matplotlib.
#
# @details
# The `SensorHistoryWindow` class provides a visualization utility for sensor logs
# such as speed, temperature, and battery over time. It uses `QDialog` as its base
# and embeds a `matplotlib` canvas to render time-series line charts.
#
# This window is triggered from the main AgriEdge interface under "Sensor History"
# and automatically plots all available telemetry data from the logger.
#
# ### Features:
# - Embedded matplotlib canvas for real-time plotting
# - Clean layout using QVBoxLayout
# - Supports DataFrame inputs from `MemoryLogger` or `TelemetryLogger`
#
# @inherits QDialog
#
# @param df pandas.DataFrame containing columns: Zaman, Hiz, Sicaklik, Batarya
# @see MainWindow::show_sensor_history()

 
class SensorHistoryWindow(QDialog):
    """
    @class SensorHistoryWindow
    @brief Displays a dialog containing a matplotlib plot of historical sensor data.
    """

    def __init__(self, df, parent=None):
        """
        @brief Initializes the sensor history plot dialog window.
        @param df pandas DataFrame containing sensor logs (time, speed, temperature, battery).
        @param parent Parent widget (default is None).
        """
        super().__init__(parent)
        self.setWindowTitle("Sensör Geçmişi Grafiği")  # Dialog title
        self.resize(800, 400)                          # Initial size of the window

        # Create and set the layout for the dialog
        layout = QVBoxLayout(self)

        # Create a Matplotlib canvas object and add it to the layout
        self.canvas = FigureCanvas(Figure(figsize=(8, 4)))
        layout.addWidget(self.canvas)

        # Call the plot function to draw the graph
        self.plot(df)

    def plot(self, df):
        """
        @brief Draws a line graph of speed, temperature, and battery from logged data.
        @param df DataFrame that must contain columns: 'Zaman', 'Hiz', 'Sicaklik', 'Batarya'.
        """
        # Add subplot to the canvas and clear any previous plots
        ax = self.canvas.figure.add_subplot(111)
        ax.clear()

        # Plot sensor values over time
        ax.plot(df["Zaman"], df["Hiz"], label="Hız")             # Speed
        ax.plot(df["Zaman"], df["Sicaklik"], label="Sıcaklık")   # Temperature
        ax.plot(df["Zaman"], df["Batarya"], label="Batarya")     # Battery level

        # Label axes and chart
        ax.set_xlabel("Zaman")           # Time
        ax.set_ylabel("Değer")           # Value
        ax.set_title("Sensör Verileri")  # Title of the graph

        # Add legend and rotate x-axis labels for readability
        ax.legend()
        ax.tick_params(axis='x', rotation=45)

        # Redraw the canvas with updated plot
        self.canvas.draw()


if __name__ == "__main__":
    """
    @brief Entry point for launching the PyQt5 application.
    """

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
