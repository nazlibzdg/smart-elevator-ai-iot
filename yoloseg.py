import cv2
import numpy as np
from ultralytics import YOLO

ASANSOR_ALAN_M2 = 1.87
PATH_BOS_FOTO = 'zemin.jpeg'        
PATH_BOS_MASKE = 'zemin_maskesi.png' 
PATH_DOLU_FOTO = 'testfoto.jpeg'   
MODEL_PATH = 'yolov8m-seg.pt'

def analiz():
    zemin_mask = cv2.imread(PATH_BOS_MASKE, cv2.IMREAD_GRAYSCALE)
    dolu_foto = cv2.imread(PATH_DOLU_FOTO)
    bos_foto = cv2.imread(PATH_BOS_FOTO) # Boş asansörü de okuyoruz
    
    if zemin_mask is None or dolu_foto is None or bos_foto is None:
        print("HATA: Dosyalar eksik!")
        return

    h, w = dolu_foto.shape[:2]
    zemin_mask = cv2.resize(zemin_mask, (w, h))
    bos_foto = cv2.resize(bos_foto, (w, h))
    _, zemin_mask = cv2.threshold(zemin_mask, 127, 255, cv2.THRESH_BINARY)

    model = YOLO(MODEL_PATH)
    results = model(dolu_foto, conf=0.15, verbose=False) # conf'u biraz düşürdük
    
    yolo_tuvali = np.zeros((h, w), dtype=np.uint8)
    GECERLI_SINIFLAR = [0, 24, 26, 28, 39] 

    if results[0].masks is not None:
        for mask_data, cls in zip(results[0].masks.data, results[0].boxes.cls):
            if int(cls) in GECERLI_SINIFLAR:
                m = cv2.resize(mask_data.cpu().numpy(), (w, h))
                yolo_tuvali[m > 0.5] = 255

    img_diff = cv2.absdiff(cv2.GaussianBlur(bos_foto, (7,7), 0), cv2.GaussianBlur(dolu_foto, (7,7), 0))
    gray_diff = cv2.cvtColor(img_diff, cv2.COLOR_BGR2GRAY)
    _, fark_tuvali = cv2.threshold(gray_diff, 40, 255, cv2.THRESH_BINARY)

    birlesik_nesneler = cv2.bitwise_or(yolo_tuvali, fark_tuvali)

    final_isgal = cv2.bitwise_and(birlesik_nesneler, zemin_mask)
    kernel = np.ones((7,7), np.uint8)
    final_isgal = cv2.morphologyEx(final_isgal, cv2.MORPH_OPEN, kernel)
    final_isgal = cv2.morphologyEx(final_isgal, cv2.MORPH_CLOSE, kernel)
    zemin_px = np.sum(zemin_mask == 255)
    dolu_px = np.sum(final_isgal == 255)
    doluluk = (dolu_px / zemin_px) * 100
    isgal_m2 = (doluluk / 100) * ASANSOR_ALAN_M2

    gosterge = dolu_foto.copy()
    gosterge[final_isgal == 255] = [255, 0, 0] 
    
    display = cv2.resize(gosterge, (int(w * (800/h)), 800))
    cv2.putText(display, f"DOLULUK: %{doluluk:.1f}", (30, 60), 2, 1.2, (0,0,255), 3)

    print(f"Toplam Alan: {isgal_m2:.3f} m2 | Doluluk: %{doluluk:.1f}")
    cv2.imshow("Kirmizi Valiz Dahil Analiz", display)
    cv2.waitKey(0)

if __name__ == "__main__":
    analiz()