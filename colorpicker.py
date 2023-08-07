import cv2
import numpy as np

# Cargar la imagen
image = cv2.imread('img/naranjo.jpg')

# Mostrar la imagen y seleccionar un píxel naranja
def select_orange_pixel(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        pixel = image[y, x]
        print("Valor del píxel seleccionado (RGB):", pixel)

cv2.namedWindow('Seleccionar píxel naranja')
cv2.setMouseCallback('Seleccionar píxel naranja', select_orange_pixel)

while True:
    cv2.imshow('Seleccionar píxel naranja', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
