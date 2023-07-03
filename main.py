import cv2
import numpy as np

# Cargar la imagen
image = cv2.imread('img/naranjo.jpg')

# Convertir la imagen de BGR a HSV
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Definir el rango de color naranja en HSV
lower_orange = np.array([0, 50, 50])
upper_orange = np.array([30, 255, 255])

# Crear una máscara para los píxeles naranjas en el rango definido
orange_mask = cv2.inRange(hsv_image, lower_orange, upper_orange)

# Aplicar operaciones morfológicas para mejorar la detección de las naranjas
kernel = np.ones((5, 5), np.uint8)
orange_mask = cv2.morphologyEx(orange_mask, cv2.MORPH_CLOSE, kernel)
orange_mask = cv2.morphologyEx(orange_mask, cv2.MORPH_OPEN, kernel)

# Encontrar los contornos de los objetos naranjas
contours, _ = cv2.findContours(orange_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Encontrar el centroide y dibujar un marco alrededor de cada contorno
for contour in contours:
    # Calcular el centroide del contorno
    M = cv2.moments(contour)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        # Dibujar el centroide
        cv2.circle(image, (cX, cY), 5, (0, 255, 0), -1)

        # Dibujar un marco alrededor del contorno
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

# Mostrar la imagen con los centroides y marcos dibujados
cv2.imshow('Naranjas detectadas', image)
cv2.waitKey(0)

# Liberar las ventanas abiertas
cv2.destroyAllWindows()
