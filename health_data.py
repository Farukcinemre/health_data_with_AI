import requests
import mysql.connector
from mysql.connector import Error
from time import sleep
import random
import re
from datetime import datetime
import config
import logging
from logging.handlers import RotatingFileHandler
import serial

# Loglama ayarları
def setup_logging():
    logger = logging.getLogger('HealthData')
    logger.setLevel(logging.INFO)
    
    file_handler = RotatingFileHandler('health_data.log', maxBytes=1000000, backupCount=5)
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(file_formatter)
    logger.addHandler(console_handler)
    
    return logger

logger = setup_logging()

# Serial port ayarları
serial_port = 'COM9'  # Arduino'nun bağlı olduğu portu güncelleyin
baud_rate = 115200
ser = serial.Serial(serial_port, baud_rate, timeout=1)

# DeepSeek API ile analiz yap
def analyze_with_deepseek(data):
    api_url = "http://localhost:11434/v1/chat/completions"
    headers = {"Content-Type": "application/json"}

    prompt = (
        f"Hasta verileri: Nabız {data['pulse_rate']} bpm, "
        f"Oksijen doygunluğu {data['oxygen_saturation']}%, "
        f"Solunum hızı {data['respiration_rate']} bpm, "
        f"Sıcaklık {data['temperature']}°C, "
        f"EKG ritmi {data['ecg_rhythm']}. "
        "Bu vital bulgulara ve EKG verilerine göre tıbbi değerlendirme yap."
    )

    payload = {
        "model": "deepseek-r1:7b",
        "messages": [
            {"role": "system", "content": "Sen deneyimli bir acil servis doktorusun. Lütfen düşünme süreçlerinizi <think> tag’leriyle değil doğrudan cevap formatında verin."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "stream": False
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        response_data = response.json()
        content = response_data['choices'][0]['message']['content']
        content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()
        logger.info("DeepSeek API'den yanıt alındı")
        return content
    except requests.exceptions.RequestException as e:
        logger.error(f"API isteği başarısız oldu: {e}")
        return None
    except (KeyError, ValueError) as e:
        logger.error(f"Yanıt işlenirken hata oluştu: {e}")
        return None

# Veriyi veritabanına kaydet
def save_to_database(data, recommendation, a0_value, current_bpm):
    try:
        conn = mysql.connector.connect(
            host=config.DB_HOST,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            database=config.DB_NAME,
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci'
        )
        cursor = conn.cursor()
        sql = """
        INSERT INTO patient_data (
            patient_id, time, pulse_rate, oxygen_saturation, 
            respiration_rate, temperature, ecg_rhythm, health_status, 
            a0_value, current_bpm
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            data["patient_id"],
            data["time"],
            data["pulse_rate"],
            data["oxygen_saturation"],
            data["respiration_rate"],
            data["temperature"],
            data["ecg_rhythm"],
            recommendation,
            a0_value,
            current_bpm
        )
        cursor.execute(sql, values)
        conn.commit()
        logger.info(f"Veri başarıyla kaydedildi: {data['patient_id']}")
    except Error as err:
        logger.error(f"Veritabanı hatası: {err}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
            logger.info("Veritabanı bağlantısı kapatıldı")

# EKG ritim türleri
ECG_RHYTHMS = [
    "Normal Sinus Rhythm",
    "Atrial Fibrillation",
    "Ventricular Tachycardia",
    "Bradycardia",
    "Supraventricular Tachycardia"
]

# Ana döngü
while True:
    try:
        # Serial porttan veri oku
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8', errors='replace').strip()
            if line:
                if line == "Leads off detected!":
                    logger.info("Sensör bağlantısı kesildi (Leads off detected)")
                    continue
                try:
                    if "," in line:
                        a0_value, current_bpm = map(int, line.split(','))
                        logger.info(f"Alınan Serial Veri: A0={a0_value}, BPM={current_bpm}")
                    else:
                        logger.warning(f"Geçersiz veri formatı: {line.encode('ascii', 'ignore').decode('ascii')}")
                        continue
                except ValueError:
                    logger.warning(f"Geçersiz veri formatı: {line.encode('ascii', 'ignore').decode('ascii')}")
                    continue
            else:
                continue
        else:
            sleep(1)
            continue

        # Hasta verileri (pulse_rate için Arduino'dan gelen veriyi kullan)
        data = {
            "patient_id": f"PT-{random.randint(1000, 9999)}",
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "pulse_rate": current_bpm,  # Arduino'dan gelen gerçek nabız verisi
            "oxygen_saturation": round(random.uniform(90.0, 100.0), 1),
            "respiration_rate": random.randint(12, 30),
            "temperature": round(random.uniform(36.0, 40.0), 1),
            "ecg_rhythm": random.choice(ECG_RHYTHMS)
        }
        logger.info(f"Alınan Veri: {data}")
        
        recommendation = analyze_with_deepseek(data)
        
        if recommendation:
            logger.info(f"Öneri: {recommendation}")
            save_to_database(data, recommendation, a0_value, current_bpm)
        else:
            logger.warning("DeepSeek API'den yanıt alınamadı")
        
        sleep(60)
    except Exception as e:
        logger.error(f"Beklenmedik hata: {e}")
        sleep(60)