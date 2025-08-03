import subprocess
import time

# Ollama server'ı başlat
ollama_process = subprocess.Popen(["ollama", "serve"])
print("Ollama server başlatıldı...")
time.sleep(5)  # Ollama'nın tam açılması için 5 sn bekle

# Sadece ana çalıştırılacak scriptler
scripts = ["health_data4.py", "akilli_bileklik_webui.py"]

# Python scriptlerini başlat
processes = [subprocess.Popen(["python", script]) for script in scripts]

# Hepsinin bitmesini bekle
for p in processes:
    p.wait()

# Ollama'yı kapat
ollama_process.terminate()
print("Tüm scriptler ve Ollama server kapatıldı.")
