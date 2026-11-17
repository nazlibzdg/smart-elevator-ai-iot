import cv2
import numpy as np

# --- AYARLAR ---
FOTO_YOLU = "zemin.jpeg" 
noktalar = []

def nokta_sec(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # Tıklanan noktayı orijinal boyutlara geri oranla
        orig_x = int(x / oran)
        orig_y = int(y / oran)
        noktalar.append((orig_x, orig_y))
        
        # Ekranda (küçültülmüş hali üzerinde) göster
        cv2.circle(display_img, (x, y), 5, (0, 255, 0), -1)
        if len(noktalar) > 1:
            # Önceki noktayı da küçültülmüş koordinata çevirip çizgi çek
            prev_x = int(noktalar[-2][0] * oran)
            prev_y = int(noktalar[-2][1] * oran)
            cv2.line(display_img, (prev_x, prev_y), (x, y), (0, 255, 0), 2)
        cv2.imshow("Zemin Secimi", display_img)

# 1. Fotoğrafı Yükle
orig_img = cv2.imread(FOTO_YOLU)
if orig_img is None:
    print("HATA: Fotoğraf bulunamadı!")
    exit()

# 2. Ekrana sığdırmak için boyutlandır
screen_res = 800  # Pencere yüksekliği 800 piksel olsun
h, w = orig_img.shape[:2]
oran = screen_res / h
display_img = cv2.resize(orig_img, (int(w * oran), screen_res))

cv2.namedWindow("Zemin Secimi")
cv2.setMouseCallback("Zemin Secimi", nokta_sec)

print("Talimatlar: 4 köşeye tıkla, 's' ile kaydet, 'r' ile sıfırla.")

while True:
    cv2.imshow("Zemin Secimi", display_img)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("r"):
        display_img = cv2.resize(orig_img, (int(w * oran), screen_res))
        noktalar = []
    
    elif key == ord("s"):
        if len(noktalar) >= 3:
            # Orijinal boyutta maske oluştur
            mask = np.zeros(orig_img.shape[:2], dtype=np.uint8)
            roi_corners = np.array([noktalar], dtype=np.int32)
            cv2.fillPoly(mask, roi_corners, 255)
            
            cv2.imwrite("zemin_maskesi.png", mask)
            print(f"BAŞARILI: Orijinal boyutta ({w}x{h}) maske kaydedildi!")
            break
    elif key == ord("q"):
        break

cv2.destroyAllWindows()