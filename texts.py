# -*- coding: utf-8 -*-
##
# ==============================================================================
# @file texts.py
# @brief Text resource definitions used throughout the AGRIEDGE robot interface.
#
# @details
# This module contains structured, preformatted text blocks that serve as UI content
# for various display and dialog areas within the AGRIEDGE GUI. It separates
# hardcoded strings from logic, enabling future internationalization and central
# maintainability of user-visible content.
#
# ## Included Constants:
# - @ref VERSION_TEXT : Dynamic string template for system version information.
# - @ref USER_MANUAL_TEXT : Comprehensive usage instructions.
# - @ref CONTACT_TEXT : Developer and project contact section.
#
# ## Key Benefits:
# - Promotes separation of content and logic
# - Enables future localization (i18n)
# - Easy to update developer info, manuals, version
#
# @authors
# - Doğukan Avcı
# - Sinan İlbey
# @version 1.0
# @date May 4, 2025
# ==============================================================================



##
# @const VERSION_TEXT
# @brief Template text for displaying dynamic system version and build information.
#
# @details
# Filled at runtime using system values such as:
# - OS name, version and architecture
# - Python version
# - Qt version
#
# Appears in the "Hakkında" (About) dialog or when user runs `version` command in the terminal.
#
# @usage
# @code
# print(VERSION_TEXT.format(os_name="Windows", os_version="10", os_arch="x64", python_version="3.11", qt_version="5.15"))
# @endcode
#

VERSION_TEXT = """
📦 Yazılım Sürümü: AGRIEDGE v1.0

🖥️ İşletim Sistemi: {os_name} {os_version} ({os_arch})
🐍 Python Sürümü: {python_version}
🧱 Qt Sürümü: {qt_version}
🧠 UI Framework: PyQt5

Bu yazılım, tarımsal otonom robotlar için geliştirilmiştir.
Tüm hakları saklıdır. © 2025 Doğukan Avcı
"""

##
# @const USER_MANUAL_TEXT
# @brief Embedded user guide for AGRIEDGE interface and functionality.
#
# @details
# This guide outlines all operational procedures including:
# - Connection handling
# - Mode switching
# - Mapping and logging
# - Manual driving and terminal commands
#
# Displayed under "Yardım > Kullanıcı Kılavuzu" or via in-app reference help buttons.
#
# @note Updated with new features in v1.0 including command list, LED warnings, and driving logic.
#

USER_MANUAL_TEXT = """
KULLANICI KILAVUZU - AGRIEDGE TARIM ROBOTU

📌 SİSTEME BAĞLANMA:
- 'Connect' butonuna tıklayarak robot ile bağlantıyı başlatın.
- Bağlantı durumu 'Açık' olarak görünür.

📌 MOD SEÇİMİ:
- Manuel Mod: 'Mode > Manuel' ya da 'mod manuel' komutu ile.
- Otonom Mod: 'Mode > Auto' ya da 'mod otonom' komutu ile.

📌 HARİTALAMA:
- 'Start Mapping' butonu ile haritalamayı başlatın.
- 'Stop Mapping' butonu ile haritalamayı durdurun.
- Haritalama sırasında her 3 saniyede bir sistem verisi (hız, sıcaklık, batarya) kaydedilir.

📌 ÇAPALAMA MODU:
- 'Çapalama Start' butonu ile çapalamaya geçin.
- Bu moddayken haritalama başlatılamaz.

📌 LOG KAYDI:
- 'Log Start' ile sistem verileri CSV dosyasına kaydedilir.
- 'Log Stop' ile veri kaydı durur ve analiz yapılır:
   • Ortalama, max/min hız ve sıcaklık
   • Standart sapma bilgileri

📌 KOMUT SATIRI:
- 'help' → kullanılabilir komutları listeler.
- 'status' → sistem durumu, mod ve batarya bilgisini verir.
- 'set hız [0-100]' → hızı ayarlar (örnek: set hız 50).
- 'delay [sn]' → gecikmeli komut tetikleyici (örnek: delay 5).
- 'map start/stop' → haritalamayı başlatır/durdurur.
- 'temizle' → terminal ekranını temizler.

📌 UYARI SİSTEMİ:
- Sistemin uyarı ışığı tehlike algılanırsa kırmızıya döner.
- Güvenli durumlarda yeşil yanar.

📌 SÜRÜŞ KONTROLÜ:
- Manuel sürüş paneli üzerinden yönlendirme (İleri, Geri, Sol, Sağ, Dur) yapılabilir.

📌 VERSİYON:
- 'version' komutu ile sistem, Python ve Qt sürümü görüntülenebilir.
        """

##
# @const CONTACT_TEXT
# @brief Contact information and contribution notes for AGRIEDGE project.
#
# @details
# Contains names, email addresses, GitHub and LinkedIn links for all contributors.
# Appears in the 'Geliştirici Hakkında' dialog.
#
# Encourages user feedback and community collaboration.
#

CONTACT_TEXT = """
  👨‍💻 GELİŞTİRİCİ BİLGİLERİ

  Ad: Doğukan Avcı
  E-posta: baygutdogukan@gmail.com
  GitHub: https://github.com/dogukanbaygut
  LinkedIn: https://linkedin.com/in/dogukanavci
  
  Ad: Sinan İlbey
  E-posta: snnlby1806@gmail.com
  GitHub: https://github.com/SinanBey06
  LinkedIn: https://www.linkedin.com/in/sn-bey/
  
  Sürüm: AGRIEDGE v1.0


  Her türlü geri bildirim, hata bildirimi veya geliştirme öneriniz için bizimle iletişime geçebilirsiniz.

  Teşekkür ederiz!
  """
  
