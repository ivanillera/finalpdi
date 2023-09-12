import cv2
import numpy as np

def showWait(titulo, imagen):
    cv2.imshow(titulo, imagen)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Cargar la imagen
image = cv2.imread('img/naranjo2.jpg')
showWait('imagen original', image)

# Convertir la imagen a espacio de color HSV
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Definir un rango de colores naranja en HSV
lower_orange = np.array([0, 100, 100])
upper_orange = np.array([20, 255, 255])

# Crear una máscara para el color naranja
mask = cv2.inRange(hsv_image, lower_orange, upper_orange)
cv2.imwrite("Mascara.jpg",mask)
showWait("mascara",mask)

# Hough
img = cv2.imread('Mascara.jpg',cv2.IMREAD_GRAYSCALE)
imgBlur = cv2.medianBlur(img,5)
showWait("img", imgBlur)

cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
circles = cv2.HoughCircles(imgBlur,cv2.HOUGH_GRADIENT,1,20,
 param1=50,param2=8,minRadius=3,maxRadius=20)
circles = np.uint16(np.around(circles))
for i in circles[0,:]:
 # draw the outer circle
 cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
 # draw the center of the circle
 cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
cv2.imshow('detected circles',cimg)
cv2.waitKey(0)
cv2.destroyAllWindows()


# imgBlur = cv2.medianBlur(mask,5)
# cimg = cv2.cvtColor(mask,cv2.COLOR_GRAY2BGR)
# bits = cimg.dtype
# print(bits)

# cimgCentros = cv2.cvtColor(mask,cv2.COLOR_GRAY2BGR)

# circles = cv2.HoughCircles(cimg, cv2.HOUGH_GRADIENT,1,20,
#  param1=50,param2=30,minRadius=0,maxRadius=0)
# circles = np.uint16(np.around(circles))
# for i in circles[0,:]:
#  # draw the outer circle
#  cv2.circle(cimgCentros,(i[0],i[1]),i[2],(0,255,0),2)
#  # draw the center of the circle
#  cv2.circle(cimgCentros,(i[0],i[1]),2,(0,0,255),3)

# showWait("cimg",cimg)
# showWait("cimg2",cimgCentros)

# Encontrar los contornos de las regiones naranjas
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Dibujar los contornos encontrados en la imagen original
imgContornos = cv2.drawContours(image, contours, -1, (0, 255, 0), 1)
cv2.imwrite("Contornos.jpg",imgContornos)
# Calcular centroide de las regiones, los que coinciden son naranjas y los que no son más de una naranja. Si la superficie
# de findcontours es mayor a la hough significa que tendría más de una naranja
# si es menor no sé, basura.

# Mostrar la imagen con los contornos de las naranjas
# Contar la cantidad de naranjas detectadas
num_naranjas = len(contours)

# Mostrar el número de naranjas detectadas
print(f"Número de naranjas detectadas: {num_naranjas}")
showWait("Naranjas detectadas", image)
