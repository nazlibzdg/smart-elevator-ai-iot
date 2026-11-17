import cv2
import numpy as np
import paho.mqtt.client as mqtt
import time
from ultralytics import YOLO

MQTT_BROKER = "127.0.0.1" 
MODEL_PATH = 'yolov8m-seg.pt'

FOTO_TEST_SETI = [
    {"id": "1", "dosya": "testfoto2.jpeg"},
    {"id": "2", "dosya": "zemin.jpeg"},
    {"id": "3", "dosya": "testfoto3.jpeg"}
]

print("YOLO Modeli yükleniyor...")
model = YOLO(MODEL_PATH)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
try:
    client.connect(MQTT_BROKER, 1883, 60)
    client.loop_start() 
    mqtt_connected = True
except Exception as e:
    print(f"MQTT Bağlantı Atlandı (Görselleştirme devam ediyor): {e}")
    mqtt_connected = False

# Yan yana dizilecek fotoğrafları bu listede toplayacağız
islenmis_fotograflar = []

# Fotoğrafların ekranda çok büyük olmaması için SABİT NİZAMİ BOYUT (Genişlik, Yükseklik)
HEDEF_GENISLIK = 400
HEDEF_YUKSEKLIK = 700

for madde in FOTO_TEST_SETI:
    asansor_id = madde["id"]
    foto_yolu = madde["dosya"]
    
    img = cv2.imread(foto_yolu)
    mask = cv2.imread('zemin_maskesi.png', cv2.IMREAD_GRAYSCALE)
    
    if img is None or mask is None:
        print(f"Hata: {foto_yolu} veya zemin_maskesi.png eksik!")
        continue

    h, w = img.shape[:2]
    mask = cv2.resize(mask, (w, h))
    
    # Model Tahmini
    results = model(img, conf=0.15, verbose=False)
    nesne_maskesi = np.zeros((h, w), dtype=np.uint8)
    
    if results[0].masks is not None:
        for m_data in results[0].masks.data:
            m_np = m_data.cpu().numpy()
            m_resized = cv2.resize(m_np, (w, h))
            nesne_maskesi[m_resized > 0.5] = 255

    final_isgal = cv2.bitwise_and(nesne_maskesi, mask)
    zemin_piksel = np.sum(mask == 255)
    doluluk_yuzde = round((np.sum(final_isgal == 255) / zemin_piksel) * 100, 1) if zemin_piksel > 0 else 0.0

    # Mavi Maskeyi Uygulama
    output_img = img.copy()
    output_img[final_isgal == 255] = [255, 0, 0] # Saf Mavi
    
    # Orijinal boyutundayken yazıyı ekle
    yazi = f"DOLULUK: %{doluluk_yuzde}"
    cv2.putText(output_img, yazi, (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0, 0, 255), 3, cv2.LINE_AA)
    
    # --- NİZAMİ BOYUTLANDIRMA ---
    # Fotoğrafı ekrana sığacak ve yan yana dizilebilecek standart boyuta getiriyoruz
    nizami_img = cv2.resize(output_img, (HEDEF_GENISLIK, HEDEF_YUKSEKLIK))
    
    # Listeye ekle
    islenmis_fotograflar.append(nizami_img)
    
    # MQTT Gönderimi
    if mqtt_connected:
        topic = f"asansor/{asansor_id}/doluluk"
        client.publish(topic, str(doluluk_yuzde))

# Eğer en az bir fotoğraf başarıyla işlendiyse yan yana birleştir ve göster
if len(islenmis_fotograflar) > 0:
    # np.hstack fonksiyonu resimleri YATAY (Horizontal) olarak tek bir matriste birleştirir
    yan_yana_pencere = np.hstack(islenmis_fotograflar)
    
    # Sonucu göster
    cv2.imshow("Asansor Doluluk Analiz Seti ", yan_yana_pencere)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if mqtt_connected:
    time.sleep(1)
    client.loop_stop()
    client.disconnect()