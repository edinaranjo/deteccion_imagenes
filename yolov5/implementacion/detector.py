
#Importamos librerias

import torch
import cv2
import numpy as np
import pandas as pd

# Leemos el modelo

# path es la ruta hacia el archivo de pytorch generado por el modelo

model = torch.hub.load('ultralytics/yolov5', 'custom',
                       path='./archivo.pt')


# Realizamos la videocaptura


cap = cv2.VideoCapture(0)


while True:
    
    ret, frame = cap.read()
    
    # Detecciones
    
    detect = model(frame)
    
    
    info = detect.pandas().xyxy[0]
    print(info)
    
    
    # Mostrar FPS
    
    cv2.imshow('Detector de Flores', np.squeeze(detect.render()))
    
    
    # Leer el teclado
    
    t = cv2.waitKey(5)
    
    if t == 27:
        break

cap.release()
cv2.destroyAllWindows()


