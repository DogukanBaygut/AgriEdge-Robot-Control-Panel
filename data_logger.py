# -*- coding: utf-8 -*-
##
# ===============================================================================
#  AGRIEDGE - Data Logging & Analysis Module
# ===============================================================================
# @file data_logger.py
# @brief Provides real-time telemetry logging and analysis for AgriEdge robot system.
# @version 1.0
# @date 2025-05-04
# @author Doğukan Avcı, Sinan İlbey
#
# @details
# This module provides a modular, polymorphic logging and analysis system. It includes:
# - Abstract interfaces: AbstractLogger, BaseAnalysis
# - Concrete loggers: TelemetryLogger (pandas), MemoryLogger (list)
# - Analysis strategies: BasicAnalysis, DetailedAnalysis
#
# ## Design Patterns:
# - Strategy Pattern: Enables dynamic switching between analysis behaviors at runtime.
# - Interface Pattern: Enforces consistent logging and analysis behavior through abstraction.
#
# ## Object-Oriented Principles:
# - Inheritance: Concrete classes inherit from abstract bases.
# - Polymorphism: Loggers and analysis strategies are interchangeable via interface.
# - Encapsulation & Data Hiding: Internal data structures (_log, __telemetry_data) are protected/private.
# ===============================================================================

import pandas as pd
import numpy as np
from datetime import datetime
from abc import ABC, abstractmethod

# ===============================================================================
# 1. ANALYSIS STRATEGY BASE CLASS (POLYMORPHIC)
# ===============================================================================

##
# @class BaseAnalysis
# @brief Abstract strategy interface for analyzing sensor data.
#
# @details
# This class defines the contract for all analysis strategies. It is used by loggers to compute
# statistics on telemetry data. Concrete implementations override `analyze()` method.
#
# @note Used in Strategy Pattern by loggers
# @polymorphic Yes
# @abstract Must be subclassed
#
class BaseAnalysis(ABC):
    @abstractmethod
    def analyze(self, df):
        """
        Analyze the input telemetry data.

        Parameters:
            df (pd.DataFrame): A DataFrame with columns: [Zaman, Hiz, Sicaklik, Batarya]

        Returns:
            dict | str: Summary of computed statistics.
        """
        pass

##
# @class BasicAnalysis
# @brief Computes basic statistics (min, max, mean) for speed and temperature.
#
# @inherits BaseAnalysis
# @polymorphic Yes
#
class BasicAnalysis(BaseAnalysis):
    def analyze(self, df):
        if df.empty:
            return "Veri yok."
        hizlar = df["Hiz"].to_numpy()
        sicakliklar = df["Sicaklik"].to_numpy()
        return {
            "Ortalama Hız": round(np.mean(hizlar), 1),
            "Maksimum Hız": np.max(hizlar),
            "Minimum Hız": np.min(hizlar),
            "Maksimum Sıcaklık": np.max(sicakliklar),
            "Minimum Sıcaklık": np.min(sicakliklar)
        }

##
# @class DetailedAnalysis
# @brief Computes extended statistics including standard deviation and battery range.
#
# @inherits BaseAnalysis
# @polymorphic Yes
#
class DetailedAnalysis(BaseAnalysis):
    def analyze(self, df):
        if df.empty:
            return "Veri yok."
        hizlar = df["Hiz"].to_numpy()
        sicakliklar = df["Sicaklik"].to_numpy()
        batarya = df["Batarya"].to_numpy()
        return {
            "Maksimum Hız": np.max(hizlar),
            "Minimum Hız": np.min(hizlar),
            "Ortalama Hız": round(np.mean(hizlar), 2),
            "Hız Std Sapma": round(np.std(hizlar), 2),
            "Maksimum Sıcaklık": np.max(sicakliklar),
            "Minimum Sıcaklık": np.min(sicakliklar),
            "Sıcaklık Ortalaması": round(np.mean(sicakliklar), 2),
            "Batarya Min": np.min(batarya),
            "Batarya Max": np.max(batarya)
        }

# ===============================================================================
# 2. ABSTRACT LOGGER INTERFACE (INTERFACE PATTERN)
# ===============================================================================

##
# @class AbstractLogger
# @brief Abstract base interface for logging and analyzing telemetry data.
#
# @details
# This interface enforces method contracts for all logger types. Both concrete loggers implement:
# - Data logging
# - Strategy switching
# - Export to CSV
# - Get/set telemetry buffer
#
# @polymorphic Yes
# @abstract Must be subclassed
#
class AbstractLogger(ABC):
    @abstractmethod
    def log_sensor_data(self, hiz, sicaklik, batarya):
        """Logs a new sensor data entry."""
        pass

    @abstractmethod
    def analyze(self):
        """Analyzes current data using selected strategy."""
        pass

    @abstractmethod
    def export_to_csv(self, filename):
        """Exports current telemetry data to CSV."""
        pass

    @abstractmethod
    def get_data(self):
        """Returns current telemetry data as pandas DataFrame."""
        pass

    @abstractmethod
    def set_analyzer(self, analyzer: BaseAnalysis):
        """Sets the active analysis strategy object."""
        pass

# ===============================================================================
# 3. TELEMETRY LOGGER (PANDAS BACKEND)
# ===============================================================================

##
# @class TelemetryLogger
# @brief Concrete logger using Pandas DataFrame as backend.
#
# @inherits AbstractLogger
# @encapsulation Uses __telemetry_data for data hiding
# @strategy Uses BaseAnalysis as pluggable strategy object
#
class TelemetryLogger(AbstractLogger):
    """
    @class TelemetryLogger
    @brief Concrete logger using Pandas DataFrame as backend.
    @inherits AbstractLogger
    @strategy Uses BaseAnalysis strategy interface.
    @encapsulation Uses __telemetry_data as private data buffer.
    """

    def __init__(self, analyzer: BaseAnalysis = None):
        """
        @brief Constructor.
        @param analyzer (BaseAnalysis) Optional analysis strategy. Defaults to BasicAnalysis.
        """
        self.__telemetry_data = pd.DataFrame(columns=["Zaman", "Hiz", "Sicaklik", "Batarya"])
        self._analyzer = analyzer if analyzer else BasicAnalysis()

    def log_sensor_data(self, hiz, sicaklik, batarya):
        """
        @brief Logs new sensor data entry.
        @param hiz (float): Robot speed value
        @param sicaklik (float): Temperature value
        @param batarya (float): Battery percentage
        @override Implements AbstractLogger
        """
        zaman = datetime.now().strftime("%H:%M:%S")
        yeni_veri = {
            "Zaman": zaman,
            "Hiz": hiz,
            "Sicaklik": sicaklik,
            "Batarya": batarya
        }
        self.__telemetry_data = pd.concat([self.__telemetry_data, pd.DataFrame([yeni_veri])], ignore_index=True)

    def analyze(self):
        """
        @brief Performs statistical analysis using current strategy.
        @return (dict or str): Result of analysis.
        @override
        """
        return self._analyzer.analyze(self.__telemetry_data)

    def export_to_csv(self, filename="data_log.csv"):
        """
        @brief Saves the current data to a CSV file.
        @param filename (str): Path to export file.
        @return (str): The filename used.
        @override
        """
        self.__telemetry_data.to_csv(filename, index=False)
        return filename

    def get_data(self):
        """
        @brief Returns the full telemetry data.
        @return (pd.DataFrame): Internal pandas DataFrame
        @override
        """
        return self.__telemetry_data

    def set_data(self, new_data):
        """
        @brief Replaces existing data.
        @param new_data (pd.DataFrame): New dataset.
        @raises TypeError: If input is not a DataFrame
        """
        if isinstance(new_data, pd.DataFrame):
            self.__telemetry_data = new_data
        else:
            raise TypeError("Yeni veri bir pandas.DataFrame olmalıdır.")

    def set_analyzer(self, analyzer: BaseAnalysis):
        """
        @brief Sets new analysis strategy object.
        @param analyzer (BaseAnalysis): A strategy object (BasicAnalysis or DetailedAnalysis)
        @override
        """
        self._analyzer = analyzer

    @property
    def analyzer(self):
        """
        @brief Getter for current strategy object.
        @return (BaseAnalysis): Currently assigned strategy
        """
        print("[DEBUG] analyzer property çağrıldı")
        return self._analyzer


# ===============================================================================
# 4. LIGHTWEIGHT LOGGER (NO EXTERNAL DEPENDENCIES)
# ===============================================================================

##
# @class MemoryLogger
# @brief Lightweight in-memory logger using Python lists.
#
# @inherits AbstractLogger
# @note Recommended for embedded or testing use
#
class MemoryLogger(AbstractLogger):

    def __init__(self, analyzer: BaseAnalysis = None):
        """
        @brief Constructor for MemoryLogger.
        @param analyzer (BaseAnalysis): Optional strategy object. Defaults to BasicAnalysis.
        @post _log list is initialized empty; _analyzer is set.
        """
        self._log = []  #: @private Internal list buffer for telemetry tuples (zaman, hiz, sicaklik, batarya)
        self._analyzer = analyzer if analyzer else BasicAnalysis()

    def log_sensor_data(self, hiz, sicaklik, batarya):
        """
        @brief Appends a new sensor reading to internal memory log.
        @param hiz (float): Speed value of robot.
        @param sicaklik (float): Temperature value.
        @param batarya (float): Battery level.
        @override Implements AbstractLogger
        @post New tuple is added to `_log`.
        """
        zaman = datetime.now().strftime("%H:%M:%S")
        self._log.append((zaman, hiz, sicaklik, batarya))

    def analyze(self):
        """
        @brief Analyzes all logged data using current strategy.
        @return (dict | str): Dictionary of statistics or message string if empty.
        @override Implements AbstractLogger
        @note Converts internal list to DataFrame for strategy use.
        """
        if not self._log:
            return "Veri yok."
        df = pd.DataFrame(self._log, columns=["Zaman", "Hiz", "Sicaklik", "Batarya"])
        return self._analyzer.analyze(df)

    def export_to_csv(self, filename="memory_log.csv"):
        """
        @brief Exports memory log to a CSV file.
        @param filename (str): Path to output file.
        @return (str): File name or 'Veri yok.' if no data exists.
        @override Implements AbstractLogger
        @exception ValueError: Raised if log is empty (handled internally).
        """
        if not self._log:
            return "Veri yok."
        df = pd.DataFrame(self._log, columns=["Zaman", "Hiz", "Sicaklik", "Batarya"])
        df.to_csv(filename, index=False)
        return filename

    def get_data(self):
        """
        @brief Retrieves current telemetry data as a pandas DataFrame.
        @return (pd.DataFrame): All stored data with proper column headers.
        @override Implements AbstractLogger
        @note Returns empty DataFrame if no entries exist.
        """
        if not self._log:
            return pd.DataFrame(columns=["Zaman", "Hiz", "Sicaklik", "Batarya"])
        return pd.DataFrame(self._log, columns=["Zaman", "Hiz", "Sicaklik", "Batarya"])

    def set_analyzer(self, analyzer: BaseAnalysis):
        """
        @brief Assigns a new analysis strategy at runtime.
        @param analyzer (BaseAnalysis): Concrete analysis object.
        @override Implements AbstractLogger
        @post Updates `_analyzer` strategy reference.
        """
        self._analyzer = analyzer

    @property
    def analyzer(self):
        """
        @brief Property getter for current analyzer strategy object.
        @return (BaseAnalysis): The strategy in use (e.g., BasicAnalysis)
        @note This is primarily for debugging purposes.
        """
        print("[DEBUG] analyzer property çağrıldı")
        return self._analyzer
