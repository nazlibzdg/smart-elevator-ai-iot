# Smart Elevator Occupancy Detection & Dynamic Routing System (AI & IoT)

*(English description below )*

---

**TÜBİTAK 2209-A Üniversite Öğrencileri Araştırma Projeleri Destekleme Programı** kapsamında geliştirilen bu proje; çoklu asansör sistemlerinde bekleme sürelerini, gereksiz duraklamaları ve enerji tüketimini optimize etmek amacıyla tasarlanmış gerçek zamanlı bir **Görüntü İşleme, Yapay Zeka ve IoT Tabanlı Merkezi Karar Mekanizması** sistemidir.

### Proje Amacı ve Çalışma Mantığı
Geleneksel asansör sistemleri kabin içi doluluk oranını veya katlardaki yoğunluğu dikkate almadan yalnızca çağrı sırasına göre hareket eder. Bu sistemde:
1. **Görüntü İşleme & Segmentasyon:** Kamera görüntüleri üzerinden **YOLOv8 Segmentation** ve **OpenCV** kullanılarak kabin içi ve kat bekleme alanlarındaki kişi sayısı ve doluluk oranı gerçek zamanlı analiz edilir.
2. **Güvenli Veri İletişimi:** Elde edilen yoğunluk verileri **MQTT (Mosquitto)** haberleşme protokolü üzerinden düşük gecikmeli olarak merkezi sisteme iletilir.
3. **Merkezi Karar Mekanizması:** **Node-RED Dashboard 2.0** üzerinde çalışan dinamik yönlendirme algoritması, gelen verileri işleyerek en uygun asansör kabinini ilgili kata yönlendirir ve anlık izleme imkanı sunar.
4. **Donanım Kontrolü:** Karar mekanizmasından çıkan komutlar **Arduino Mega 2560** donanım prototipine aktarılarak fiziksel asansör simülasyonu kontrol edilir.

### Kullanılan Teknolojiler
* **Yapay Zeka & Görüntü İşleme:** Python, OpenCV, YOLOv8 (Instance Segmentation)
* **IoT & Haberleşme:** MQTT (Mosquitto Broker), Node-RED Dashboard 2.0
* **Gömülü Sistem & Donanım:** Arduino Mega 2560 (C/C++)

### Proje Dosya Yapısı
* `yoloseg.py` — YOLOv8 segmentasyon modeli ile gerçek zamanlı kişi ve doluluk tespiti.
* `maskeleme.py` — Bölge bazlı ilgi alanı (ROI) ve zemin maskeleme işlemleri.
* `kararmekanizmasisenaryo.py` — Çoklu asansör yönlendirme ve yoğunluk senaryosu algoritması.
* `kararmekanizmasıtest.py` — Karar algoritması simülasyon ve doğrulama testleri.
* `mosquitto.conf` — MQTT broker yapılandırma ayarları.

---

## English Description

Developed under the **TÜBİTAK 2209-A University Students Research Projects Support Program**, this project is a real-time **Computer Vision, AI, and IoT-based Central Decision Mechanism** designed to optimize waiting times, unnecessary stops, and energy consumption in multi-elevator systems.

### Project Objective & System Workflow
Conventional elevator systems operate solely based on call order without considering cabin occupancy or floor crowd density. In this system:
1. **Computer Vision & Segmentation:** Using **YOLOv8 Segmentation** and **OpenCV**, passenger counts and occupancy rates inside cabins and floor waiting areas are analyzed in real time via camera feeds.
2. **Low-Latency Data Transmission:** Extracted density metrics are transmitted securely to the central system via the **MQTT (Mosquitto)** communication protocol.
3. **Central Decision Mechanism:** A dynamic routing algorithm running on **Node-RED Dashboard 2.0** processes incoming data, dispatches the optimal elevator cabin to the target floor, and provides a real-time monitoring interface.
4. **Hardware Control:** Routing commands are sent to an **Arduino Mega 2560** hardware prototype to actuate and control the physical multi-elevator simulation.

### Tech Stack
* **AI & Computer Vision:** Python, OpenCV, YOLOv8 (Instance Segmentation)
* **IoT & Messaging:** MQTT (Mosquitto Broker), Node-RED Dashboard 2.0
* **Embedded Systems & Hardware:** Arduino Mega 2560 (C/C++)

### Repository Structure
* `yoloseg.py` — Real-time person and occupancy detection using the YOLOv8 segmentation model.
* `maskeleme.py` — Region of Interest (ROI) and floor masking operations.
* `kararmekanizmasisenaryo.py` — Multi-elevator dynamic routing and crowd scenario algorithm.
* `kararmekanizmasıtest.py` — Simulation and validation tests for the decision mechanism.
* `mosquitto.conf` — MQTT broker configuration settings.

---

## Developer / Geliştirici
* **Nazlıcan Bozdağ** — Software Engineer / Yazılım Mühendisi  
  *Istanbul Gelisim University / İstanbul Gelişim Üniversitesi*
