import cv2
import numpy as np
import statistics

def showWait(titulo, imagen):
    cv2.imshow(titulo, imagen)
    cv2.waitKey(0)
    #cv2.destroyAllWindows()

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
# Hough
img = cv2.imread('Mascara.jpg',cv2.IMREAD_GRAYSCALE)
imgBlur = cv2.medianBlur(img,5)
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
num_centros = circles.shape[1]
print(f"Cantidad de centros encontrados con Hough: {num_centros}")
cv2.waitKey(0)
#cv2.destroyAllWindows()

# Encontrar los contornos de las regiones naranjas
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contornosConArea = []
areas = []
for cnt in contours:
   area = cv2.contourArea(cnt)
   if area != 0:
      areas.append(area)
      contornosConArea.append(cnt)
print(contornosConArea)
minimo = min(areas)
maximo = max(areas)
print(f"minimo {minimo} y maximo {maximo}")
media = sum(areas) / len(areas)
desviacion_estandar = statistics.stdev(areas)
print(f"media aresas: {media}")
print(f"desviacion estandar {desviacion_estandar}")

tamaño_cuartil = (maximo - minimo) / 4
cuartil1 = []
cuartil2 = []
cuartil3 = []
cuartil4 = []
for area in areas:
   if area < tamaño_cuartil:
      cuartil1.append(area)
   elif (area < (2*tamaño_cuartil)) & (area > tamaño_cuartil):
      cuartil2.append(area)
   elif (area < (3*tamaño_cuartil)) & (area > 2*tamaño_cuartil):
      cuartil3.append(area)
   elif (area > 3*tamaño_cuartil):
      cuartil4.append(area)
print(f"cuartil1 {len(cuartil1)} cuartil2 {len(cuartil2)} cuartil3 {len(cuartil3)} cuartil4 {len(cuartil4)}")
# nos damos cuenta que hay que descartar los cuartiles 3 y 4 porque son 8 y 2 respectivamente...

areasAceptadas = []
for area in areas:
   if (area < 2*tamaño_cuartil) & (area >5):
      areasAceptadas.append(area)


media_ca = sum(areasAceptadas) / len(areasAceptadas)
desviacion_estandar_ca = statistics.stdev(areasAceptadas)
maximo_ca = max(areasAceptadas)
minimo_ca = min(areasAceptadas)
print(f"media area_ca: {media_ca}")
print(f"desviacion estandar_ca {desviacion_estandar_ca}")
print(f"maximo {maximo_ca}")
print(f"minimo {minimo_ca}")
      
# Dibujar los contornos encontrados en la imagen original
imgContornos = cv2.drawContours(image, contours, -1, (0, 255, 0), 1)
cv2.imwrite("Contornos.jpg",imgContornos)
num_naranjas = len(contours)
print(f"Número de naranjas detectadas con contorno: {num_naranjas}")
showWait("Naranjas detectadas", image)

imgContornosConArea = cv2.drawContours(image, contornosConArea, -1, (0,255,0), 1)
cv2.imwrite("ContornosConArea.jpg", imgContornosConArea)
num_naranjas = len(contornosConArea)
print(f"Número de naranjas contornos con area {num_naranjas}")
showWait("asaddas",image)
