import cv2
import numpy as np
# Idea. empezar detectando circulos y luego filtrar por color.

# Cargar la imagen
image = cv2.imread('img/naranjo2.jpg')

# Definir el rango de color naranja en RGB
lower_orange = np.array([0, 70, 130], dtype=np.uint8)
upper_orange = np.array([196, 243, 255], dtype=np.uint8)

# Aplicar una máscara para los píxeles naranjas en el rango definido
orange_mask = cv2.inRange(image, lower_orange, upper_orange)

# Aplicar operaciones morfológicas para mejorar la detección de las naranjas
kernel = np.ones((5, 5), np.uint8)
orange_mask = cv2.morphologyEx(orange_mask, cv2.MORPH_CLOSE, kernel)
orange_mask = cv2.morphologyEx(orange_mask, cv2.MORPH_OPEN, kernel)

# Encontrar los contornos de los objetos naranjas
contours, _ = cv2.findContours(orange_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Imprimir el número de naranjas encontradas
print(f"Número de naranjas encontradas: {len(contours)}")

# Dibujar un marco y el centroide de cada contorno
for contour in contours:
    # Dibujar un marco alrededor del contorno
    x, y, w, h = cv2.boundingRect(contour)
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
    
    # Calcular el centroide del contorno
    M = cv2.moments(contour)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        
        # Dibujar el centroide
        cv2.circle(image, (cX, cY), 5, (0, 255, 0), -1)

# Mostrar la imagen con los marcos y centroides dibujados
cv2.imshow('Naranjas detectadas', image)
cv2.waitKey(0)

# Liberar las ventanas abiertas
cv2.destroyAllWindows()
