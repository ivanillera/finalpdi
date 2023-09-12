import cv2
import numpy as np

def showWait(titulo, imagen):
    cv2.imshow(titulo, imagen)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Cargar la imagen
image = cv2.imread('img/naranjo.jpg')

# Convertir la imagen a espacio de color HSV
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Definir un rango de colores naranja en HSV
lower_orange = np.array([0, 100, 100])
upper_orange = np.array([20, 255, 255])

# Crear una máscara para el color naranja
mask = cv2.inRange(hsv_image, lower_orange, upper_orange)

# Encontrar los contornos de las regiones naranjas
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Dibujar los contornos encontrados en la imagen original
cv2.drawContours(image, contours, -1, (0, 255, 0), 2)

# Mostrar la imagen con los contornos de las naranjas
# Contar la cantidad de naranjas detectadas
num_naranjas = len(contours)

# Mostrar el número de naranjas detectadas
print(f"Número de naranjas detectadas: {num_naranjas}")
showWait("Naranjas detectadas", image)
