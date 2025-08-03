# 🩺 Health Data Monitoring System

Welcome to the **Health Data Monitoring System**, a Python-based application designed to generate, analyze, and store realistic health data. This system leverages the **DeepSeek API** for medical evaluations and a **MySQL database** for data storage. A sleek **Flask-based web interface** allows users to visualize patient data, while an automation script simplifies running all components. 🚀

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Logging](#logging)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

---

## 🌟 Overview

The Health Data Monitoring System is built to simulate and analyze vital signs such as pulse rate, oxygen saturation, respiration rate, temperature, and ECG rhythm. It consists of three core scripts:

- **🔍 `health_monitor.py`**: Generates realistic health data, sends it to the DeepSeek API for medical analysis, and stores results in a MySQL database.
- **🌐 `health_data_webui.py`**: Provides a Flask-based web interface to view patient data and manage the database.
- **⚙️ `run_all.py`**: Automates the startup of the Ollama server, `health_monitor.py`, and `health_data_webui.py`.

> **Note**: All operations and errors are logged to rotating files and the console for easy monitoring.

---

## ✨ Features

- **📊 Data Generation**: Simulates realistic vital signs:
  - Pulse rate: 60–100 bpm
  - Oxygen saturation: 95–100%
  - Respiration rate: 12–20 bpm
  - Temperature: 36–37.5°C
  - ECG rhythm: Various types (e.g., Normal Sinus Rhythm, Atrial Fibrillation)
- **🧠 DeepSeek API Integration**: Sends vital signs for medical analysis.
- **💾 MySQL Storage**: Stores patient data and analysis results securely.
- **🖥️ Web Interface**: Displays data in a user-friendly table and allows table deletion.
- **🤖 Automation**: Simplifies execution with `run_all.py`.
- **📜 Logging**: Tracks operations and errors with rotating log files.
- **🛡️ Error Handling**: Robust handling for API, database, and web requests.

---

## 📦 Requirements

To run the system, ensure you have:

- **Python 3.6+**
- **MySQL database**
- **DeepSeek API** running locally at `http://localhost:11434/v1/chat/completions`
- **Python Libraries**:
  - `requests`
  - `mysql-connector-python`
  - `flask`
- **Configuration File**: A `config.py` file with the following structure:

  ```python
  DB_HOST = "your_host"       # e.g., "localhost"
  DB_USER = "your_user"       # e.g., "root"
  DB_PASSWORD = "your_password"
  DB_NAME = "health_data"
  DEBUG = True                # Set to False for production
  HOST = "0.0.0.0"            # Flask host
  PORT = 5000                 # Flask port
  ```

---

## 🛠️ Setup

Follow these steps to set up the system:

1. **Install Python Dependencies** 📥

   Install the required libraries using pip:

   ```bash
   pip install requests mysql-connector-python flask
   ```

2. **Set Up the MySQL Database** 🗄️

   - Connect to your MySQL server using a client (e.g., MySQL Workbench, phpMyAdmin, or command line).
   - Create the `health_data` database and `patient_data` table with the following SQL commands:

     ```sql
     CREATE DATABASE IF NOT EXISTS health_data;
     USE health_data;
     CREATE TABLE IF NOT EXISTS patient_data (
         id INT AUTO_INCREMENT PRIMARY KEY,
         patient_id VARCHAR(10),
         time DATETIME,
         pulse_rate INT,
         oxygen_saturation FLOAT,
         respiration_rate INT,
         temperature FLOAT,
         ecg_rhythm VARCHAR(50),
         health_status TEXT,
         a0_value INT,
         current_bpm INT
     );
     ```

   - Grant permissions to the MySQL user specified in `config.py`:

     ```sql
     GRANT ALL PRIVILEGES ON health_data.* TO 'your_user'@'localhost' IDENTIFIED BY 'your_password';
     FLUSH PRIVILEGES;
     ```

     Replace `'your_user'` and `'your_password'` with the values from `config.py`.

   - Update `config.py` with your MySQL credentials and Flask settings, ensuring `DB_NAME` is set to `"health_data"`.

3. **Install Ollama** 🖥️

   - Download and install Ollama from [Ollama's official website](https://ollama.com/download).
   - **Windows**: Run the installer and follow the prompts.
   - **macOS**: Use Homebrew (`brew install ollama`) or download the installer.
   - **Linux**: Run the installation script:

     ```bash
     curl -fsSL https://ollama.com/install.sh | sh
     ```

   - Verify installation:

     ```bash
     ollama --version
     ```

4. **Set Up DeepSeek R1** 🤖

   - Ollama supports DeepSeek R1 models ranging from 1.5B to 671B parameters. The 671B model is the original, while smaller models are distilled versions based on Qwen and Llama architectures.
   - Pull a model suitable for your hardware (replace `X` with `1.5b`, `7b`, `8b`, `14b`, `32b`, `70b`, or `671b`):

     ```bash
     ollama pull deepseek-r1:Xb
     ```

     Example for the 7B model:

     ```bash
     ollama pull deepseek-r1:7b
     ```

   - Start the Ollama server:

     ```bash
     ollama serve
     ```

     This runs the server at `http://localhost:11434` for API requests.

---

## 🚀 Usage

### 1. **Run the Entire System**

Use `run_all.py` to start all components at once:

```bash
python run_all.py
```

This script:
- Launches the Ollama server (`http://localhost:11434`).
- Runs `health_monitor.py` to generate and process health data.
- Starts `health_data_webui.py` for the web interface.
- Stops all processes when complete (press `Ctrl+C`).

### 2. **Access the Web Interface** 🌐

- Open your browser and navigate to `http://localhost:5000` (or the configured host/port).
- Features:
  - View patient data in a table.
  - Delete the `patient_data` table (redirects to the main page after deletion).

### 3. **Manual Execution (Optional)**

Run components individually:

- Start the Ollama server:

  ```bash
  ollama serve
  ```

- Run the data generation script:

  ```bash
  python health_monitor.py
  ```

- Run the web interface:

  ```bash
  python health_data_webui.py
  ```

- Stop each process with `Ctrl+C`.

---

## 📂 File Structure

- **`health_monitor.py`**: Generates health data, performs API analysis, and stores results.
- **`health_data_webui.py`**: Flask-based web interface for data visualization and database management.
- **`run_all.py`**: Automates execution of all components.
- **`config.py`**: Stores database and Flask configurations.
- **`health_data.log`**: Logs for `health_monitor.py` (1MB max, 5 backups).
- **`app.log`**: Logs for `health_data_webui.py` (1MB max, 5 backups).
- **`templates/`**: Contains HTML templates (`index.html`, `error.html`) for the Flask interface.

---

## 📜 Logging

- **For `health_monitor.py`**:
  - Logs are saved to `health_data.log` with a 1MB limit and 5 backup files.
- **For `health_data_webui.py`**:
  - Logs are saved to `app.log` with a 1MB limit and 5 backup files.
- Logs are also displayed on the console for real-time monitoring.
- Log format: `%(asctime)s - %(name)s - %(levelname)s - %(message)s`.

---

## 🛠️ Troubleshooting

> **Tip**: Check log files (`health_data.log` and `app.log`) for detailed error messages.

- **Database Errors**:
  - Verify `config.py` credentials.
  - Ensure the MySQL server is running and the `health_data` database and `patient_data` table exist.
  - Common MySQL errors:
    - `1045`: Incorrect username or password.
    - `1049`: Database does not exist (run `CREATE DATABASE`).
    - `1146`: Table does not exist (run `CREATE TABLE`).
- **API Errors**:
  - Confirm the Ollama server is running at `http://localhost:11434`.
  - Check if the DeepSeek R1 model is downloaded (`ollama list`).
- **Web Interface Errors**:
  - Ensure the Flask server is running (`run_all.py` or `python health_data_webui.py`).
  - Verify `config.py` host/port settings and firewall permissions.
  - Check for `index.html` and `error.html` in the `templates/` directory.
- **Ollama Server Errors**:
  - Check if port `11434` is in use:

    ```bash
    netstat -an | grep 11434
    ```

  - Verify Ollama installation (`ollama --version`) and model availability.

---

## 🤝 Contributing

We welcome contributions! To contribute:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m "Add feature"`).
4. Push to the branch (`git push origin feature-name`).
5. Open a pull request.

---

# 🩺 Sağlık Verileri İzleme Sistemi

**Sağlık Verileri İzleme Sistemi**, gerçekçi sağlık verileri üreten, **DeepSeek API** ile analiz eden ve sonuçları **MySQL veritabanında** saklayan Python tabanlı bir uygulamadır. Nabız, oksijen doygunluğu, solunum hızı, sıcaklık ve EKG ritmi gibi hayati bulguları izlemek için tasarlanmıştır. **Flask tabanlı web arayüzü**, verileri görselleştirir ve veritabanını yönetir; bir yardımcı betik ise tüm bileşenleri otomatikleştirir. 🚀

---

## 📋 İçindekiler

- [Genel Bakış](#genel-bakış)
- [Özellikler](#özellikler)
- [Gereksinimler](#gereksinimler)
- [Kurulum](#kurulum)
- [Kullanım](#kullanım)
- [Dosya Yapısı](#dosya-yapısı)
- [Günlük Kaydı](#günlük-kaydı)
- [Sorun Giderme](#sorun-giderme)
- [Katkıda Bulunma](#katkıda-bulunma)

---

## 🌟 Genel Bakış

Bu sistem, aşağıdaki üç ana betikten oluşur:

- **🔍 `health_monitor.py`**: Gerçekçi sağlık verileri üretir, DeepSeek API ile analiz eder ve sonuçları MySQL veritabanına kaydeder.
- **🌐 `health_data_webui.py`**: Hasta verilerini görüntülemek ve veritabanını yönetmek için Flask tabanlı bir web arayüzü sağlar.
- **⚙️ `run_all.py`**: Ollama sunucusu, `health_monitor.py` ve `health_data_webui.py` betiklerini tek komutla çalıştırır.

> **Not**: Tüm işlemler ve hatalar, kolay izleme için hem dosyaya hem de konsola kaydedilir.

---

## ✨ Özellikler

- **📊 Veri Üretimi**: Gerçekçi hayati bulgular üretir:
  - Nabız: 60–100 bpm
  - Oksijen doygunluğu: 95–100%
  - Solunum hızı: 12–20 bpm
  - Sıcaklık: 36–37.5°C
  - EKG ritmi: Çeşitli türler (örn. Normal Sinüs Ritmi, Atriyal Fibrilasyon)
- **🧠 DeepSeek API Entegrasyonu**: Hayati bulguları tıbbi analiz için gönderir.
- **💾 MySQL Depolama**: Verileri ve analiz sonuçlarını güvenli bir şekilde saklar.
- **🖥️ Web Arayüzü**: Verileri kullanıcı dostu bir tabloda gösterir ve tablo silme işlevi sunar.
- **🤖 Otomasyon**: `run_all.py` ile tüm bileşenleri kolayca başlatır.
- **📜 Günlük Kaydı**: İşlemleri ve hataları rotasyonlu dosyalara kaydeder.
- **🛡️ Hata Yönetimi**: API, veritabanı ve web istekleri için sağlam hata yönetimi.

---

## 📦 Gereksinimler

Sistemi çalıştırmak için:

- **Python 3.6+**
- **MySQL veritabanı**
- **DeepSeek API**, yerel olarak `http://localhost:11434/v1/chat/completions` adresinde çalışmalı
- **Python Kütüphaneleri**:
  - `requests`
  - `mysql-connector-python`
  - `flask`
- **Yapılandırma Dosyası**: Aşağıdaki yapıya sahip bir `config.py` dosyası:

  ```python
  DB_HOST = "your_host"       # örn. "localhost"
  DB_USER = "your_user"       # örn. "root"
  DB_PASSWORD = "your_password"
  DB_NAME = "health_data"
  DEBUG = True                # Üretim için False
  HOST = "0.0.0.0"            # Flask host
  PORT = 5000                 # Flask port
  ```

---

## 🛠️ Kurulum

Sistemi kurmak için şu adımları izleyin:

1. **Python Bağımlılıklarını Yükleyin** 📥

   Gerekli kütüphaneleri pip ile yükleyin:

   ```bash
   pip install requests mysql-connector-python flask
   ```

2. **MySQL Veritabanını Kurun** 🗄️

   - MySQL sunucusuna bir istemciyle bağlanın (örn. MySQL Workbench, phpMyAdmin veya komut satırı).
   - `health_data` veritabanını ve `patient_data` tablosunu oluşturmak için şu SQL komutlarını çalıştırın:

     ```sql
     CREATE DATABASE IF NOT EXISTS health_data;
     USE health_data;
     CREATE TABLE IF NOT EXISTS patient_data (
         id INT AUTO_INCREMENT PRIMARY KEY,
         patient_id VARCHAR(10),
         time DATETIME,
         pulse_rate INT,
         oxygen_saturation FLOAT,
         respiration_rate INT,
         temperature FLOAT,
         ecg_rhythm VARCHAR(50),
         health_status TEXT,
         a0_value INT,
         current_bpm INT
     );
     ```

   - `config.py` dosyasındaki kullanıcı için izinleri ayarlayın:

     ```sql
     GRANT ALL PRIVILEGES ON health_data.* TO 'your_user'@'localhost' IDENTIFIED BY 'your_password';
     FLUSH PRIVILEGES;
     ```

     `your_user` ve `your_password` değerlerini `config.py` dosyanızdaki değerlerle değiştirin.

   - `config.py` dosyasını veritabanı kimlik bilgileri ve Flask ayarlarıyla güncelleyin, `DB_NAME` değerinin `"health_data"` olduğundan emin olun.

3. **Ollama'yı Yükleyin** 🖥️

   - Ollama'yı [resmi web sitesinden](https://ollama.com/download) indirip yükleyin.
   - **Windows**: Yükleyiciyi çalıştırın ve talimatları izleyin.
   - **macOS**: Homebrew ile yükleyin (`brew install ollama`) veya yükleyiciyi indirin.
   - **Linux**: Yükleme betiğini çalıştırın:

     ```bash
     curl -fsSL https://ollama.com/install.sh | sh
     ```

   - Kurulumu doğrulayın:

     ```bash
     ollama --version
     ```

4. **DeepSeek R1'i Kurun** 🤖

   - Ollama, 1.5B'den 671B parametreye kadar DeepSeek R1 modellerini destekler. Donanımınıza uygun bir modeli çekin (`X` yerine `1.5b`, `7b`, `8b`, `14b`, `32b`, `70b` veya `671b` yazın):

     ```bash
     ollama pull deepseek-r1:Xb
     ```

     Örnek (7B modeli için):

     ```bash
     ollama pull deepseek-r1:7b
     ```

   - Ollama sunucusunu başlatın:

     ```bash
     ollama serve
     ```

     Bu, sunucuyu `http://localhost:11434` adresinde çalıştırır.

---

## 🚀 Kullanım

### 1. **Tüm Sistemi Çalıştırın**

Tüm bileşenleri tek komutla başlatmak için:

```bash
python run_all.py
```

Bu betik:
- Ollama sunucusunu başlatır (`http://localhost:11434`).
- `health_monitor.py` ile sağlık verileri üretir ve işler.
- `health_data_webui.py` ile web arayüzünü sunar.
- Tüm işlemleri durdurmak için `Ctrl+C` basın.

### 2. **Web Arayüzüne Erişim** 🌐

- Tarayıcınızda `http://localhost:5000` adresine gidin (veya yapılandırılmış host/port).
- Özellikler:
  - Hasta verilerini bir tabloda görüntüleme.
  - `patient_data` tablosunu silme (ana sayfaya yönlendirir).

### 3. **Manuel Çalıştırma (İsteğe Bağlı)**

Bileşenleri ayrı ayrı çalıştırın:

- Ollama sunucusunu başlatın:

  ```bash
  ollama serve
  ```

- Veri üretme betiğini çalıştırın:

  ```bash
  python health_monitor.py
  ```

- Web arayüzünü çalıştırın:

  ```bash
  python health_data_webui.py
  ```

- Her işlemi `Ctrl+C` ile durdurun.

---

## 📂 Dosya Yapısı

- **`health_monitor.py`**: Sağlık verileri üretir, API analizi yapar ve sonuçları kaydeder.
- **`health_data_webui.py`**: Verileri görüntülemek ve veritabanını yönetmek için web arayüzü.
- **`run_all.py`**: Tüm bileşenleri otomatikleştirir.
- **`config.py`**: Veritabanı ve Flask ayarları.
- **`health_data.log`**: `health_monitor.py` için günlükler (1MB, 5 yedek).
- **`app.log`**: `health_data_webui.py` için günlükler (1MB, 5 yedek).
- **`templates/`**: Flask için HTML şablonları (`index.html`, `error.html`).

---

## 📜 Günlük Kaydı

- **`health_monitor.py` için**:
  - Günlükler `health_data.log` dosyasına kaydedilir (1MB, 5 yedek).
- **`health_data_webui.py` için**:
  - Günlükler `app.log` dosyasına kaydedilir (1MB, 5 yedek).
- Günlükler konsolda da gerçek zamanlı gösterilir.
- Format: `%(asctime)s - %(name)s - %(levelname)s - %(message)s`.

---

## 🛠️ Sorun Giderme

> **İpucu**: Hata detayları için `health_data.log` ve `app.log` dosyalarını kontrol edin.

- **Veritabanı Hataları**:
  - `config.py` kimlik bilgilerini doğrulayın.
  - MySQL sunucusunun çalıştığından ve `health_data` veritabanı ile `patient_data` tablosunun mevcut olduğundan emin olun.
  - Yaygın hatalar:
    - `1045`: Yanlış kullanıcı adı/şifre.
    - `1049`: Veritabanı mevcut değil (`CREATE DATABASE` çalıştırın).
    - `1146`: Tablo mevcut değil (`CREATE TABLE` çalıştırın).
- **API Hataları**:
  - Ollama sunucusunun `http://localhost:11434` adresinde çalıştığını kontrol edin.
  - DeepSeek R1 modelinin indirildiğini doğrulayın (`ollama list`).
- **Web Arayüzü Hataları**:
  - Flask sunucusunun çalıştığını kontrol edin (`run_all.py` veya `python health_data_webui.py`).
  - `config.py` host/port ayarlarını ve güvenlik duvarını kontrol edin.
  - `templates/` dizininde `index.html` ve `error.html` dosyalarını doğrulayın.
- **Ollama Sunucu Hataları**:
  - 11434 portunun kullanımda olup olmadığını kontrol edin:

    ```bash
    netstat -an | grep 11434
    ```

  - Ollama kurulumunu (`ollama --version`) ve model varlığını doğrulayın.

---

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Katkıda bulunmak için:

1. Depoyu çatallayın (fork).
2. Özellik dalı oluşturun (`git checkout -b feature-name`).
3. Değişikliklerinizi kaydedin (`git