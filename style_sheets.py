# -*- coding: utf-8 -*-
##
# @file style_sheets.py
# @brief Centralized stylesheet module for AGRIEDGE GUI components.
# @author Doğukan AVCI, Sinan ILBEY
# @version 1.0
# @date 2025-05-04
#
# @details
# This module defines global CSS-like style constants as Python strings for use across
# PyQt5 widgets. By externalizing UI styles into a dedicated module:
#   - Visual consistency across the application is ensured,
#   - Code reusability and maintenance are improved,
#   - UI logic is separated cleanly from GUI styling (separation of concerns).
#
# These styles cover buttons, backgrounds, terminal areas, status lights, and group boxes.
# Each constant is intended to be imported and applied using `.setStyleSheet(...)` in GUI classes.
##

# =============================================================================
## @const GREEN_BUTTON_STYLE
#  @brief Style for "start", "connect", or "confirm" QPushButtons.
#  @details Applies a green background with white bold text and rounded edges.
#  Used in: Connect, Start Mapping, Log Start, Cultivation Start buttons.
# =============================================================================
GREEN_BUTTON_STYLE = """
QPushButton {
    background-color: #60B677;
    color: white;
    font-weight: bold;
    font-size: 12pt;
    border: none;
    border-radius: 10px;
    padding: 8px 20px;
}
QPushButton:hover {
    background-color: #45a049;
}
"""

# =============================================================================
## @const RED_BUTTON_STYLE
#  @brief Style for "stop", "disconnect", or danger QPushButtons.
#  @details Applies a red theme for critical actions with hover feedback.
# =============================================================================
RED_BUTTON_STYLE = """
QPushButton {
    background-color: #f44336;
    color: white;
    font-weight: bold;
    font-size: 12pt;
    border: none;
    border-radius: 10px;
    padding: 8px 20px;
}
QPushButton:hover {
    background-color: #e53935;
}
"""

# =============================================================================
## @const CENTRAL_WIDGET_STYLE
#  @brief Global background color for the main window or central widget.
#  @details Light gray background used in most root windows for visual neutrality.
# =============================================================================
CENTRAL_WIDGET_STYLE = """
QWidget {
    background-color: #d3d3d3;
}
"""

# =============================================================================
## @const GROUPBOX_STYLE
#  @brief Styling for QGroupBox containers (title, background, borders).
#  @details Used for logical UI sections like Telemetry, Connection, and Logs.
# =============================================================================
GROUPBOX_STYLE = """
QGroupBox {
    background-color: #f2f2f2;
    border: 2px solid #cccccc;
    border-radius: 10px;
    margin-top: 10px;
    font-weight: bold;
    font-size: 10.5pt;
    padding: 8px;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top center;
    padding: 0 10px;
}
"""

# =============================================================================
## @const MAIN_TITLE_STYLE
#  @brief Large header label styling for application title.
#  @details Includes gradient background, centered text, and large bold font.
# =============================================================================
MAIN_TITLE_STYLE = """
QLabel {
    font-size: 28pt;
    font-weight: bold;
    qproperty-alignment: AlignCenter;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 #66bb6a, stop:1 #43a047);
    color: white;
    padding: 8px;
    border-radius: 12px;
}
"""

# =============================================================================
## @const TERMINAL_STYLE
#  @brief Style for QTextEdit acting as a terminal output log.
#  @details Mimics a console with dark theme and monospaced font.
#  Used in: Terminal panel (`CmdReadOnly`) in the main UI.
# =============================================================================
TERMINAL_STYLE = """
background-color: #1e1e1e;
color: #DDDDDD;
font-family: Consolas;
font-size: 10pt;
border-radius: 6px;
padding: 6px;
"""

# =============================================================================
## @const WARNING_STYLE
#  @brief Visual style for danger or alert status indicators.
#  @details Applied to QLabel warnings when a threat (e.g., obstacle) is detected.
# =============================================================================
WARNING_STYLE = """
background-color: red;
color: white;
font-weight: bold;
border-radius: 6px;
padding: 4px;
"""

# =============================================================================
## @const SAFE_STYLE
#  @brief Visual style for indicating system safety or stable condition.
#  @details Typically used when no threats are detected by sensors.
# =============================================================================
SAFE_STYLE = """
background-color: #4CAF50;
color: white;
font-weight: bold;
border-radius: 6px;
padding: 4px;
"""

# =============================================================================
## @const BUTON_STIL
#  @brief Generic button style used in legacy or custom subpanels.
#  @details Green rounded buttons with hover state for reusability.
#  Used in: Manual driving panel (`manuel_kod.py`).
# =============================================================================
BUTON_STIL = """
QPushButton {
    background-color: #4CAF50;
    color: white;
    font-weight: bold;
    border-radius: 8px;
    padding: 6px;
    font-size: 11pt;
}
QPushButton:hover {
    background-color: #45a049;
}
"""

# =============================================================================
## @const CENTRALWIDGET_STYLE
#  @brief Background style specific to widgets named `centralwidget`.
#  @details Soft blue background used in homepage/calendar window (`TakvimPencere`).
# =============================================================================
CENTRALWIDGET_STYLE = """
QWidget#centralwidget {
    background-color: #82abe8;
}
"""

# =============================================================================
## @const CALENDAR_WIDGET_STYLE
#  @brief Custom background style for calendar container widget (`widget_calendar`).
#  @details Rounded corners and green background for a modern visual.
# =============================================================================
CALENDAR_WIDGET_STYLE = """
QWidget#widget_calendar {
    background-color: #60B677;
    border-radius: 10px;
}
"""
