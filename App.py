import cv2
import numpy as np
from pyzbar.pyzbar import decode
from PIL import Image
import mss
import time

def capturar_todas_as_telas():
    imagens = []
    with mss.mss() as sct:
        monitores = sct.monitors[1:]  # Ignora monitor[0], que é toda a área virtual

        for monitor in monitores:
            screenshot = sct.grab(monitor)
            img = Image.frombytes("RGB", (screenshot.width, screenshot.height), screenshot.rgb)
            imagens.append(np.array(img))

    return imagens

def escutar_qrcodes(pausar=0.5):
    print("🔁 Escutando QR Codes em todas as telas...\n(Pressione Ctrl+C para sair)")
    detectados = set()

    try:
        while True:
            telas = capturar_todas_as_telas()

            for idx, img in enumerate(telas):
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                qrcodes = decode(gray)

                for qrcode in qrcodes:
                    dados = qrcode.data.decode('utf-8')
                    if dados not in detectados:
                        print(f"\n✅ QR Code detectado na tela {idx+1}: {dados}")
                        detectados.add(dados)

            time.sleep(pausar)

    except KeyboardInterrupt:
        print("\n🛑 Encerrado pelo usuário.")

if __name__ == "__main__":
    escutar_qrcodes()
