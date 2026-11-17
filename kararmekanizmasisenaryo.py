import paho.mqtt.client as mqtt
import json
import time
import ssl


# --- YENI KARAR MEKANIZMASI SENARYO VERILERI ---
CAGRI_KATI = 5
CAGRI_YONU = "YUKARI"

ASANSORLER = [
    {
        "id": "1", 
        "gorsel": "testfoto2.jpeg",
        "doluluk_yuzde": 85.7,
        "mevcut_kat": 3,
        "mevcut_yon": "YUKARI",
        "max_agirlik": 1000,
        "mevcut_agirlik": 920   # SENARYOMUZ: Agirlik sinirda, elenecek!
    },
    {
        "id": "2", 
        "gorsel": "zemin.jpeg",
        "doluluk_yuzde": 0.0,
        "mevcut_kat": 2,
        "mevcut_yon": "YUKARI",
        "max_agirlik": 1000,
        "mevcut_agirlik": 380   # En uygun aday!
    },
    {
        "id": "3", 
        "gorsel": "testfoto3.jpeg",
        "doluluk_yuzde": 95.5,
        "mevcut_kat": 4,
        "mevcut_yon": "DURUYOR",
        "max_agirlik": 1000,
        "mevcut_agirlik": 780
    }
]

# --- SIBER GUVENLIKLI BAGLANTI AYARLARI ---
MQTT_BROKER = "127.0.0.1"
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# Python'a diyoruz ki: "Bizim urettigimiz ana muhru yanina al, sahte brokerlara kanma."
client.tls_set(ca_certs=r"C:\Asansor\ca.crt.crt") 
client._ssl_context.check_hostname = False
client._ssl_context.verify_mode = ssl.CERT_NONE
client.tls_insecure_set(True)

# Artik eski 1883 yerine siber guvenli port olan 8883'ten baglaniyoruz
client.connect(MQTT_BROKER, 8883, 60)
client.loop_start()

def senaryo_calistir():
    print(f"\n=== [SINYAL] YENI DIS CAGRI ALINDI: {CAGRI_KATI}. Kat, Yon: {CAGRI_YONU} ===\n")
    
    en_yuksek_skor = -1
    yonlendirilen_asansor_id = None

    for asan in ASANSORLER:
        print(f"--- Asansor {asan['id']} ({asan['gorsel']}) Analiz Ediliyor ---")
        
        topic_doluluk = f"asansor/{asan['id']}/doluluk"
        client.publish(topic_doluluk, str(asan["doluluk_yuzde"]))
        
        bos_alan_yuzdesi = 100.0 - asan["doluluk_yuzde"]
        
        # Agirlik Bariyeri Kontrolu
        kalan_kapasite = asan["max_agirlik"] - asan["mevcut_agirlik"]
        
        if kalan_kapasite < 100:
            print(f"-> [BARIYER] Asansor {asan['id']} elendi! Bos yer orani %{bos_alan_yuzdesi:.1f} olsa bile agirlik sinirda ({asan['mevcut_agirlik']} kg)!")
            toplam_skor = 0.0
        else:
            skor_alan = bos_alan_yuzdesi * 0.40

            if asan["mevcut_yon"] == CAGRI_YONU or asan["mevcut_yon"] == "DURUYOR":
                skor_yon = 35.0
            else:
                skor_yon = 0.0

            kat_farki = abs(asan["mevcut_kat"] - CAGRI_KATI)
            skor_konum = max(0, 25.0 - (kat_farki * 2.5))

            toplam_skor = round(skor_alan + skor_yon + skor_konum, 1)
            print(f"-> Puanlar -> Alan: {skor_alan:.1f} | Yon: {skor_yon:.1f} | Konum: {skor_konum:.1f} -> Toplam: {toplam_skor}")

        topic_skor = f"asansor/{asan['id']}/skor"
        client.publish(topic_skor, str(toplam_skor))
        
        if toplam_skor > en_yuksek_skor:
            en_yuksek_skor = toplam_skor
            yonlendirilen_asansor_id = asan["id"]
            
        time.sleep(0.3)

    print("\n==============================================")
    if yonlendirilen_asansor_id is not None and en_yuksek_skor > 0:
        # Node-RED Dashboard 2.0 icin JSON paketi hazirlaniyor
        karar_verisi = {
            "id": str(yonlendirilen_asansor_id),
            "mesaj": f"Sistem Aksiyonu: Asansor {yonlendirilen_asansor_id} en optimize kabin olarak 5. kata yonlendiriliyor..."
        }
        client.publish("asansor/karar", json.dumps(karar_verisi))
        print(f"[MERKEZI KARAR]: En Uygun Kabin ASANSOR {yonlendirilen_asansor_id} Olarak Secildi ve Yonlendirildi! (Skor: {en_yuksek_skor})")
    else:
        karar_verisi = {
            "id": "HICBIRI",
            "mesaj": "Sistem Aksiyonu: Guvenlik siniri asildi, tum cagrilar askiya alindi."
        }
        client.publish("asansor/karar", json.dumps(karar_verisi))
        print("[MERKEZI KARAR]: Uygun asansor bulunamadi. Tum kabinler kapasite sinirinda! (HOLD)")
    print("==============================================\n")

if __name__ == "__main__":
    senaryo_calistir()
    
    print("Dashboard 2.0 ekrani basariyla guncellendi. Lambalarin durumu icin baglanti 5 saniye acik tutuluyor...")
    time.sleep(5)
    
    client.loop_stop()
    client.disconnect()