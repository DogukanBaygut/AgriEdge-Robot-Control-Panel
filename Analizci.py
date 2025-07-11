# -*- coding: utf-8 -*-
##
# ==============================================================================
# @file analizci.py
# @brief AGRIEDGE Smart Agriculture – Regional RGB Map Analysis Module
# @version 2.0
# @date 2025-05-12
# @authors
#     - Sinan İLBEY
#     - Doğukan AVCI
#
# ==============================================================================
# DESCRIPTION:
# ------------------------------------------------------------------------------
# This module defines the `RGBMapAnalyzer` class, a reusable and object-oriented
# component designed for regional analysis of agricultural field condition maps
# (soil moisture, light intensity, and temperature) encoded in RGB format.
#
# The goal is to help farmers and agronomists extract interpretable insights
# from sensor or drone-captured field maps by:
#   - Segmenting images into four cardinal regions (North, South, East, West)
#   - Calculating average red, green, and blue intensities per region
#   - Interpreting results based on map type and generating visual warnings
#   - Producing an HTML report with tables, color-coded insights, and bar plots
#
# ------------------------------------------------------------------------------
# OBJECT-ORIENTED STRUCTURE:
# ------------------------------------------------------------------------------
# ✅ Encapsulation: Analysis logic is wrapped within the RGBMapAnalyzer class  
# ✅ Reusability: Same class handles all map types (nem, isik, sicaklik)  
# ✅ Abstraction: User calls only `.to_html()` to perform entire analysis  
# ✅ Extensibility: Future support for new metrics or regions possible  
#
# ------------------------------------------------------------------------------
# CLASS OVERVIEW:
# ------------------------------------------------------------------------------
# @class RGBMapAnalyzer
# @brief Main analyzer for regional RGB maps
#
# Attributes:
#   - image_path (str): File path to the map image
#   - map_type (str): "nem", "isik", or "sicaklik"
#
# Methods:
#   - load_image(): Loads and segments image
#   - analyze_regions(): Calculates RGB ratios for each region
#   - generate_chart_html(): Produces bar chart as base64 HTML image
#   - interpret_results(): Generates interpretation text per region
#   - to_html(): Full pipeline output as a styled HTML block
#
# ------------------------------------------------------------------------------
# DEPENDENCIES:
# ------------------------------------------------------------------------------
# - Pillow (PIL) for image handling
# - NumPy for efficient pixel analysis
# - Pandas for tabular output
# - Matplotlib for visualization
# - base64, io for HTML-safe chart rendering
#
# ------------------------------------------------------------------------------
# USAGE EXAMPLE:
# ------------------------------------------------------------------------------
#     from analizci import RGBMapAnalyzer
#     analyzer = RGBMapAnalyzer("nem_haritasi.png", "nem")
#     result_html = analyzer.to_html()
#     text_browser.setHtml(result_html)
#
# ==============================================================================


from PIL import Image
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

class RGBMapAnalyzer:
    """
    Performs directional region-based RGB analysis on an agricultural map image.

    Attributes:
        image_path (str): Path to the RGB image file.
        map_type (str): Type of map ("nem", "isik", or "sicaklik").
    """

    def __init__(self, image_path, map_type):
        """
        Initializes the analyzer with a specific image and analysis type.

        Args:
            image_path (str): Path to the image file.
            map_type (str): Type of map ("nem", "isik", "sicaklik").
        """
        self.image_path = image_path
        self.map_type = map_type
        self.data = None
        self.regions = {}
        self.stats = []

    def load_image(self):
        """Loads the image and prepares regional slices."""
        img = Image.open(self.image_path).convert('RGB')
        self.data = np.array(img)
        h, w, _ = self.data.shape

        self.regions = {
            "Kuzey": self.data[:h//2, :],
            "Güney": self.data[h//2:, :],
            "Batı": self.data[:, :w//2],
            "Doğu": self.data[:, w//2:]
        }

    def _compute_color_ratios(self, region):
        """Computes average red, green, blue intensities for a region."""
        red = np.mean((region[:, :, 0] > 130) & (region[:, :, 1] < 100) & (region[:, :, 2] < 100))
        green = np.mean((region[:, :, 1] > 130) & (region[:, :, 0] < 120) & (region[:, :, 2] < 120))
        blue = np.mean((region[:, :, 2] > 130) & (region[:, :, 0] < 110) & (region[:, :, 1] < 110))
        return red, green, blue

    def analyze_regions(self):
        """Calculates RGB ratios for each directional region."""
        self.stats.clear()
        for name, region in self.regions.items():
            r, g, b = self._compute_color_ratios(region)
            self.stats.append((name, r, g, b))

    def generate_chart_html(self):
        """Creates a bar chart as a base64-encoded HTML <img> tag."""
        df = pd.DataFrame(self.stats, columns=["Bölge", "Kırmızı Oranı", "Yeşil Oranı", "Mavi Oranı"])
        fig, ax = plt.subplots(figsize=(3.2, 1.8))
        df.set_index("Bölge").plot(kind="bar", ax=ax, legend=True)
        ax.set_ylabel("Oran")
        ax.set_title("Renk Yoğunlukları", fontsize=9)
        ax.tick_params(axis='x', labelrotation=0)
        ax.legend(fontsize=6, loc='upper right')
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100)
        buf.seek(0)
        encoded = base64.b64encode(buf.read()).decode("utf-8")
        plt.close(fig)
        return f"<img src='data:image/png;base64,{encoded}'><br>"

    def interpret_results(self):
        """Generates per-region HTML interpretation based on map type."""
        html = ""
        for region, r, g, b in self.stats:
            html += f"<h4>📍 {region} Bölgesi:</h4>"
            if self.map_type == "nem":
                if r > 0.02:
                    html += "🔴 Nem eksikliği tespit edildi.<br>→ Kuruma riski var.<br>"
                if g > 0.03:
                    html += "🟢 Nem seviyesi ideal.<br>→ Bitki gelişimi uygun.<br>"
                if b > 0.02:
                    html += "🔵 Hafif kuraklık olabilir.<br>→ Toprak nemi düşük.<br>"
            elif self.map_type == "isik":
                if r > 0.02:
                    html += "🔴 Aşırı ışık.<br>→ Gölgeleme gerekebilir.<br>"
                if g > 0.03:
                    html += "🟢 Işık seviyesi ideal.<br>→ Fotosentez verimli.<br>"
                if b > 0.02:
                    html += "🔵 Işık yetersiz.<br>→ Gölge budaması önerilir.<br>"
            elif self.map_type == "sicaklik":
                if r > 0.02:
                    html += "🔴 Yüksek sıcaklık.<br>→ Buharlaşma artabilir.<br>"
                if g > 0.03:
                    html += "🟢 Sıcaklık dengeli.<br>→ Üretim koşulları iyi.<br>"
                if b > 0.02:
                    html += "🔵 Düşük sıcaklık.<br>→ Geç ekim önerilir.<br>"
        return html

    def to_html(self):
        """Executes the full analysis pipeline and returns final HTML."""
        try:
            self.load_image()
            self.analyze_regions()

            df = pd.DataFrame(self.stats, columns=["Bölge", "Kırmızı Oranı", "Yeşil Oranı", "Mavi Oranı"])
            html = "<b>📊 Bölgesel Renk Yoğunlukları:</b><br>"
            html += df.to_html(index=False, border=1)
            html += "<br>" + self.generate_chart_html()
            html += self.interpret_results()
            return html.strip()
        except Exception as e:
            return f"<b style='color:red;'>⚠️ Hata oluştu:</b> {e}"
