Health Data Monitoring System
This Python-based system generates realistic health data, analyzes it using the DeepSeek API, and stores the results in a MySQL database. It is designed for monitoring vital signs such as pulse rate, oxygen saturation, respiration rate, temperature, and ECG rhythm, providing medical evaluations based on the data. A Flask-based web interface allows users to view the collected data and manage the database, and a utility script automates the execution of the system components.
Table of Contents

Overview
Features
Requirements
Setup
Usage
File Structure
Logging
Troubleshooting
Contributing

Overview
The system consists of three main scripts:

health_monitor.py: Generates realistic health data (e.g., pulse rate, oxygen saturation, respiration rate, temperature, and ECG rhythm), sends it to the DeepSeek API for medical analysis, and stores the results in a MySQL database.
health_data_webui.py: Provides a Flask-based web interface to display stored patient data and allows users to drop the database table.
run_all.py: Automates the execution of the Ollama server, health_monitor.py, and health_data_webui.py, ensuring all components start and stop together.

Logging is implemented to track operations and errors, with logs saved to rotating files and displayed on the console.
Features

Data Generation: Generates realistic health data for pulse rate (60-100 bpm), oxygen saturation (95-100%), respiration rate (12-20 bpm), temperature (36-37.5°C), and ECG rhythm.
DeepSeek API Integration: Sends vital signs to the DeepSeek API for medical analysis.
MySQL Storage: Saves patient data and analysis results to a MySQL database.
Web Interface: Displays patient data in a web browser and allows table deletion via a Flask-based UI.
Automation: Uses run_all.py to start the Ollama server and both Python scripts in one command.
Logging: Logs operations and errors to both files and console with rotation to manage log size.
Error Handling: Robust error handling for API requests, database operations, and web requests.

Requirements

Python 3.6+

MySQL database

DeepSeek API running locally at http://localhost:11434/v1/chat/completions

Required Python libraries:

requests
mysql-connector-python
flask


A config.py file with database and Flask configurations:
DB_HOST = "your_host"
DB_USER = "your_user"
DB_PASSWORD = "your_password"
DB_NAME = "health_data"
DEBUG = True  # or False for production
HOST = "0.0.0.0"
PORT = 5000



Setup

Install Dependencies:
pip install requests mysql-connector-python flask


Set Up the MySQL Database:

Connect to your MySQL server using a client like MySQL Workbench, phpMyAdmin, or the MySQL command-line tool.

Create the health_data database and patient_data table by running the following SQL commands:
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


Grant permissions to the MySQL user specified in config.py:
GRANT ALL PRIVILEGES ON health_data.* TO 'your_user'@'localhost' IDENTIFIED BY 'your_password';
FLUSH PRIVILEGES;

Replace 'your_user' and 'your_password' with the values from config.py.

Update config.py with your database credentials and Flask settings, ensuring DB_NAME is set to "health_data".



Install Ollama:

Download and install Ollama for your operating system from Ollama's official website.

Windows: Run the installer and follow the prompts.

macOS: Use Homebrew (brew install ollama) or download the installer.

Linux: Run the installation script:
curl -fsSL https://ollama.com/install.sh | sh


Verify installation:
ollama --version




Set Up DeepSeek R1:

Ollama supports a range of DeepSeek R1 models, from 1.5B to 671B parameters. The 671B model is the original DeepSeek R1, while smaller models are distilled versions based on Qwen and Llama architectures.

If your hardware cannot support the 671B model, select a smaller model by replacing X with the desired parameter size (e.g., 1.5b, 7b, 8b, 14b, 32b, 70b, 671b):
ollama pull deepseek-r1:Xb


For example, to use the 7B model:
ollama pull deepseek-r1:7b


Start the Ollama server to make DeepSeek R1 available:
ollama serve


This runs the server at http://localhost:11434, which the script uses for API requests.




Usage

Run the Entire System:

Use the run_all.py script to start the Ollama server, health_monitor.py, and health_data_webui.py simultaneously:
python run_all.py


The script will:

Start the Ollama server (at http://localhost:11434).
Launch health_monitor.py to generate and process health data.
Launch health_data_webui.py to serve the web interface.
Wait for both Python scripts to complete, then terminate the Ollama server.


Press Ctrl+C to stop all processes.



Access the Web Interface:

Open a web browser and navigate to http://localhost:5000 (or the configured host/port) to view the patient data.
The web interface allows you to:
View all stored patient data in a table.
Drop the patient_data table via a button (redirects to the main page after deletion).




Manual Execution (Optional):

If you prefer to run the scripts individually:
Start the Ollama server:
ollama serve


Run the data generation script:
python health_monitor.py


Run the web interface:
python health_data_webui.py


Press Ctrl+C to stop each process individually.






File Structure

health_monitor.py: Main script for generating realistic health data, API analysis, and database storage.
health_data_webui.py: Flask-based web interface for viewing patient data and managing the database.
run_all.py: Utility script to automate the execution of the Ollama server, health_monitor.py, and health_data_webui.py.
config.py: Configuration file for database credentials and Flask settings.
health_data.log: Log file for tracking operations and errors from health_monitor.py (with rotation).
app.log: Log file for tracking operations and errors from health_data_webui.py (with rotation).
templates/: Directory containing HTML templates (index.html, error.html) for the Flask web interface.

Logging

For health_monitor.py:
Logs are saved to health_data.log with a maximum size of 1MB and up to 5 backup files.


For health_data_webui.py:
Logs are saved to app.log with a maximum size of 1MB and up to 5 backup files.


Logs for both scripts are printed to the console for real-time monitoring.
Log format: %(asctime)s - %(name)s - %(levelname)s - %(message)s.

Troubleshooting

Database Errors:
Verify database credentials in config.py.
Ensure the MySQL server is running and the health_data database and patient_data table exist.
Check for common MySQL errors:
1045: Incorrect username or password.
1049: Database does not exist (run the CREATE DATABASE command).
1146: Table does not exist (run the CREATE TABLE command).




API Errors:
Confirm the Ollama server is running (via run_all.py or ollama serve) and accessible at http://localhost:11434.
Check network connectivity and ensure the DeepSeek R1 model is downloaded (ollama list).


Web Interface Errors:
Ensure the Flask server is running (via run_all.py or python health_data_webui.py).
Check the host/port settings in config.py and ensure they are not blocked by a firewall.
Verify that the templates/ directory contains index.html and error.html.


Ollama Server Errors:
If the Ollama server fails to start, check if port 11434 is in use:
netstat -an | grep 11434


Ensure Ollama is installed correctly (ollama --version) and the DeepSeek R1 model is downloaded.




Contributing
Contributions are welcome! Please:

Fork the repository.
Create a feature branch (git checkout -b feature-name).
Commit your changes (git commit -m "Add feature").
Push to the branch (git push origin feature-name).
Open a pull request.


Sağlık Verileri İzleme Sistemi
Bu Python tabanlı sistem, gerçekçi sağlık verileri üretir, DeepSeek API'sini kullanarak analiz eder ve sonuçları bir MySQL veritabanına kaydeder. Nabız, oksijen doygunluğu, solunum hızı, sıcaklık ve EKG ritmi gibi hayati bulguları izlemek ve bu verilere dayalı tıbbi değerlendirmeler sağlamak için tasarlanmıştır. Flask tabanlı bir web arayüzü, kullanıcıların toplanan verileri görüntülemesini ve veritabanını yönetmesini sağlar; bir yardımcı betik ise sistem bileşenlerinin çalıştırılmasını otomatikleştirir.
İçindekiler

Genel Bakış
Özellikler
Gereksinimler
Kurulum
Kullanım
Dosya Yapısı
Günlük Kaydı
Sorun Giderme
Katkıda Bulunma

Genel Bakış
Sistem üç ana betikten oluşur:

health_monitor.py: Gerçekçi sağlık verileri (örneğin, nabız, oksijen doygunluğu, solunum hızı, sıcaklık ve EKG ritmi) üretir, tıbbi analiz için DeepSeek API'sine gönderir ve sonuçları bir MySQL veritabanına kaydeder.
health_data_webui.py: Kaydedilen hasta verilerini görüntülemek ve veritabanı tablosunu silmek için Flask tabanlı bir web arayüzü sağlar.
run_all.py: Ollama sunucusu, health_monitor.py ve health_data_webui.py betiklerinin çalıştırılmasını otomatikleştirir.

İşlemleri ve hataları izlemek için günlük kaydı uygulanmış olup, günlükler hem bir dosyaya hem de konsola kaydedilir ve dosya boyutunu yönetmek için rotasyon kullanılır.
Özellikler

Veri Üretimi: Nabız (60-100 bpm), oksijen doygunluğu (95-100%), solunum hızı (12-20 bpm), sıcaklık (36-37.5°C) ve EKG ritmi için gerçekçi sağlık verileri üretir.
DeepSeek API Entegrasyonu: Hayati bulguları tıbbi analiz için DeepSeek API'sine gönderir.
MySQL Depolama: Hasta verilerini ve analiz sonuçlarını MySQL veritabanına kaydeder.
Web Arayüzü: Hasta verilerini bir web tarayıcısında görüntüler ve tablo silme işlevini sağlar.
Otomasyon: run_all.py ile Ollama sunucusu ve Python betiklerini tek bir komutla başlatır.
Günlük Kaydı: İşlemleri ve hataları hem dosyaya hem de konsola kaydeder; dosya boyutu yönetimi için rotasyon kullanılır.
Hata Yönetimi: API istekleri, veritabanı işlemleri ve web istekleri için sağlam hata yönetimi.

Gereksinimler

Python 3.6+

MySQL veritabanı

DeepSeek API'sinin yerel olarak http://localhost:11434/v1/chat/completions adresinde çalışması

Gerekli Python kütüphaneleri:

requests
mysql-connector-python
flask


Veritabanı ve Flask ayarları için bir config.py dosyası:
DB_HOST = "your_host"
DB_USER = "your_user"
DB_PASSWORD = "your_password"
DB_NAME = "health_data"
DEBUG = True  # veya üretim için False
HOST = "0.0.0.0"
PORT = 5000



Kurulum

Bağımlılıkları Yükleyin:
pip install requests mysql-connector-python flask


MySQL Veritabanını Kurun:

MySQL sunucusuna MySQL Workbench, phpMyAdmin veya MySQL komut satırı gibi bir istemciyle bağlanın.

health_data veritabanını ve patient_data tablosunu oluşturmak için aşağıdaki SQL komutlarını çalıştırın:
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


config.py dosyasındaki kullanıcı için izinleri ayarlayın:
GRANT ALL PRIVILEGES ON health_data.* TO 'your_user'@'localhost' IDENTIFIED BY 'your_password';
FLUSH PRIVILEGES;

your_user ve your_password değerlerini config.py dosyanızdaki değerlerle değiştirin.

config.py dosyasını veritabanı kimlik bilgileri ve Flask ayarlarıyla güncelleyin, DB_NAME değerinin "health_data" olduğundan emin olun.



Ollama Kurulumu:

İşletim sisteminize uygun Ollama'yı Ollama'nın resmi web sitesinden indirip yükleyin.

Windows: Yükleyiciyi çalıştırın ve talimatları izleyin.

macOS: Homebrew ile yükleyin (brew install ollama) veya yükleyiciyi indirin.

Linux: Yükleme betiğini çalıştırın:
curl -fsSL https://ollama.com/install.sh | sh


Kurulumu doğrulayın:
ollama --version




DeepSeek R1 Kurulumu:

Ollama, 1.5B'den 671B parametreye kadar çeşitli DeepSeek R1 modellerini destekler. 671B modeli orijinal DeepSeek R1'dir; daha küçük modeller, Qwen ve Llama mimarilerine dayalı damıtılmış sürümlerdir.

Donanımınız 671B modelini desteklemiyorsa, istediğiniz parametre boyutunu (1.5b, 7b, 8b, 14b, 32b, 70b, 671b) seçerek daha küçük bir modeli çalıştırabilirsiniz:
ollama pull deepseek-r1:Xb


Örneğin, 7B modeli için:
ollama pull deepseek-r1:7b


DeepSeek R1'i sunmak için Ollama sunucusunu başlatın:
ollama serve


Bu, sunucuyu http://localhost:11434 adresinde çalıştırır ve betiğinizin API istekleri için kullandığı adrestir.




Kullanım

Tüm Sistemi Çalıştırın:

run_all.py betiğini kullanarak Ollama sunucusunu, health_monitor.py ve health_data_webui.py betiklerini aynı anda başlatın:
python run_all.py


Betik şunları yapacaktır:

Ollama sunucusunu başlatır (http://localhost:11434 adresinde).
health_monitor.py betiğini çalıştırarak gerçekçi sağlık verileri üretir ve işler.
health_data_webui.py betiğini çalıştırarak web arayüzünü sunar.
Her iki Python betiğinin tamamlanmasını bekler ve ardından Ollama sunucusunu sonlandırır.


Tüm işlemleri durdurmak için Ctrl+C tuşlarına basın.



Web Arayüzüne Erişim:

Bir web tarayıcısında http://localhost:5000 adresine (veya yapılandırılmış host/port adresine) gidin.
Web arayüzü şunları sağlar:
Tüm kaydedilen hasta verilerini bir tabloda görüntüleme.
patient_data tablosunu bir düğme aracılığıyla silme (silme işleminden sonra ana sayfaya yönlendirir).




Manuel Çalıştırma (İsteğe Bağlı):

Betikleri ayrı ayrı çalıştırmak isterseniz:
Ollama sunucusunu başlatın:
ollama serve


Veri üretme betiğini çalıştırın:
python health_monitor.py


Web arayüzünü çalıştırın:
python health_data_webui.py


Her bir işlemi ayrı ayrı durdurmak için Ctrl+C tuşlarına basın.






Dosya Yapısı

health_monitor.py: Gerçekçi sağlık verileri üretme, API analizi ve veritabanı depolama için ana betik.
health_data_webui.py: Hasta verilerini görüntülemek ve veritabanını yönetmek için Flask tabanlı web arayüzü.
run_all.py: Ollama sunucusu, health_monitor.py ve health_data_webui.py betiklerinin çalıştırılmasını otomatikleştiren yardımcı betik.
config.py: Veritabanı kimlik bilgileri ve Flask ayarları için yapılandırma dosyası.
health_data.log: health_monitor.py işlemlerini ve hatalarını izlemek için günlük dosyası (rotasyon ile).
app.log: health_data_webui.py işlemlerini ve hatalarını izlemek için günlük dosyası (rotasyon ile).
templates/: Flask web arayüzü için HTML şablonlarını (index.html, error.html) içeren dizin.

Günlük Kaydı

health_monitor.py için:
Günlükler, maksimum 1MB boyutunda ve en fazla 5 yedek dosyayla health_data.log dosyasına kaydedilir.


health_data_webui.py için:
Günlükler, maksimum 1MB boyutunda ve en fazla 5 yedek dosyayla app.log dosyasına kaydedilir.


Her iki betik için günlükler, gerçek zamanlı izleme için konsola da yazdırılır.
Günlük formatı: %(asctime)s - %(name)s - %(levelname)s - %(message)s.

Sorun Giderme

Veritabanı Hataları:
config.py dosyasındaki veritabanı kimlik bilgilerini doğrulayın.
MySQL sunucusunun çalıştığından ve health_data veritabanı ile patient_data tablosunun mevcut olduğundan emin olun.
Yaygın MySQL hataları:
1045: Yanlış kullanıcı adı veya şifre.
1049: Veritabanı mevcut değil (CREATE DATABASE komutunu çalıştırın).
1146: Tablo mevcut değil (CREATE TABLE komutunu çalıştırın).




API Hataları:
Ollama sunucusunun (run_all.py veya ollama serve ile) çalıştığını ve http://localhost:11434 adresinde erişilebilir olduğunu doğrulayın.
Ağ bağlantısını kontrol edin ve DeepSeek R1 modelinin indirildiğini kontrol edin (ollama list).


Web Arayüzü Hataları:
Flask sunucusunun çalıştığından emin olun (run_all.py veya python health_data_webui.py ile).
config.py dosyasındaki host/port ayarlarını kontrol edin ve güvenlik duvarı tarafından engellenmediğinden emin olun.
templates/ dizininde index.html ve error.html dosyalarının mevcut olduğunu doğrulayın.


Ollama Sunucu Hataları:
Ollama sunucusunun başlatılamaması durumunda, 11434 portunun başka bir uygulama tarafından kullanılıp kullanılmadığını kontrol edin:
netstat -an | grep 11434


Ollama'nın doğru yüklendiğini doğrulayın (ollama --version) ve DeepSeek R1 modelinin indirildiğini kontrol edin (ollama list).




Katkıda Bulunma
Katkılar memnuniyetle karşılanır! Lütfen:

Depoyu çatallayın (fork).
Bir özellik dalı oluşturun (git checkout -b feature-name).
Değişikliklerinizi kaydedin (git commit -m "Add feature").
Dalı itin (git push origin feature-name).
Bir çekme isteği (pull request) açın.
