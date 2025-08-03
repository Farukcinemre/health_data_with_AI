from flask import Flask, render_template, redirect, url_for
import mysql.connector
from mysql.connector import Error
import logging
from logging.handlers import RotatingFileHandler
import config

app = Flask(__name__)

# Loglama ayarları
def setup_logging():
    logger = logging.getLogger('HealthApp')
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler('app.log', maxBytes=1000000, backupCount=5)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

logger = setup_logging()

# Veritabanı bağlantısı için context manager
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=config.DB_HOST,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            database=config.DB_NAME,
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci'
        )
        logger.info("Veritabanı bağlantısı başarıyla kuruldu")
        return conn
    except Error as err:
        logger.error(f"Veritabanı bağlantı hatası: {err}")
        raise

# Veritabanı sorgu fonksiyonu
def fetch_patient_data():
    with get_db_connection() as conn:
        with conn.cursor(dictionary=True) as cursor:
            query = """
                SELECT id, patient_id, time, pulse_rate, 
                       oxygen_saturation, respiration_rate, 
                       temperature, ecg_rhythm, health_status 
                FROM patient_data 
                ORDER BY time DESC
            """
            cursor.execute(query)
            return cursor.fetchall()

# Tablo silme fonksiyonu
def drop_patient_table():
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS patient_data")
            conn.commit()
            logger.info("patient_data tablosu başarıyla silindi")

# Ana sayfa route'u
@app.route('/')
def index():
    try:
        data = fetch_patient_data()
        return render_template('index.html', data=data)
    except Error as err:
        logger.error(f"Veritabanı hatası: {err}")
        return render_template('error.html', message="Veriler çekilirken bir hata oluştu"), 500

# Tablo silme route'u
@app.route('/drop_table')
def drop_table():
    try:
        drop_patient_table()
        return redirect(url_for('index'))
    except Error as err:
        logger.error(f"Tablo silme hatası: {err}")
        return render_template('error.html', message="Tablo silinirken bir hata oluştu"), 500

# Hata işleme için custom error handler
@app.errorhandler(404)
def page_not_found(e):
    logger.warning(f"404 hatası: {str(e)}")
    return render_template('error.html', message="Sayfa bulunamadı"), 404

@app.errorhandler(500)
def internal_server_error(e):
    logger.error(f"500 hatası: {str(e)}")
    return render_template('error.html', message="Sunucu hatası oluştu"), 500

if __name__ == '__main__':
    app.run(
        debug=config.DEBUG,
        host=config.HOST,
        port=config.PORT
    )