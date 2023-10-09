import cv2
import numpy as np
import statistics

def showWait(titulo, imagen):
    cv2.imshow(titulo, imagen)
    cv2.waitKey(0)
    #cv2.destroyAllWindows()

# Cargar la imagen
image = cv2.imread('img/naranjo2.jpg')
#showWait('imagen original', image)

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
#cv2.imshow('detected circles',cimg)
num_centros = circles.shape[1]
#print(f"Cantidad de centros encontrados con Hough: {num_centros}")
#cv2.waitKey(0)
#cv2.destroyAllWindows()

# Encontrar los contornos de las regiones naranjas
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
better_contours = []
areas = []

for cnt in contours:
   area = cv2.contourArea(cnt)
   if area != 0:
      areas.append(area)
      #better_contours.append(cnt) #better_contours no tiene mas area cero, falta que esté en los cuartiles aceptados

print(areas)
#print(contours_with_area)
min_area = min(areas)
max_area = max(areas)
#print(f"min_area {min_area} y max_area {max_area}")
area_media = sum(areas) / len(areas)
area_desviacion_estandar = statistics.stdev(areas)
#print(f"area_media aresas: {area_media}")
#print(f"desviacion estandar {area_desviacion_estandar}")

distribution_size = max_area - min_area
quartile_size = distribution_size / 4

def alfa(quartile):
   alfa = len(quartile) / distribution_size
   #print(alfa)
   #print("alfa")
   

quartile1 = []
quartile2 = []
quartile3 = []
quartile4 = []

for area in areas:
   if area < quartile_size: # PRIMER CUARTIL
      quartile1.append(area)
   elif (area < (2*quartile_size)) & (area > quartile_size): #SEGUNDO CUARTIl
      quartile2.append(area)
   elif (area < (3*quartile_size)) & (area > 2*quartile_size): #TERCER CUARTIL
      quartile3.append(area)
   elif (area > 3*quartile_size): #CUARTO CUARTIL
      quartile4.append(area)

min_quartile1 = min(quartile1)
max_quartile4 = max(quartile4)
new_distribution_size = len(quartile1)+len(quartile2)+len(quartile3)+len(quartile4)


# alfa_quartile1 = len(quartile1) / new_distribution_size
# alfa_quartile2 = len(quartile2) / new_distribution_size
# alfa_quartile3 = len(quartile3) / new_distribution_size
# alfa_quartile4 = len(quartile4) / new_distribution_size

#print(alfa_quartile1, alfa_quartile2, alfa_quartile3, alfa_quartile4)

# accepted_areas = []
accepted_quartiles = []




def quartile_accepted(quartile):
   if ((len(quartile) / new_distribution_size) > 0.1):
      accepted_quartiles.append(quartile)

quartiles = [quartile1, quartile2, quartile3, quartile4]

for quartile in quartiles:
   quartile_accepted(quartile)

print(accepted_quartiles)
print(f"Acepté un total de {len(accepted_quartiles)} cuartiles")   

accepted_areas = []

for quartil in accepted_quartiles:
   for area in areas:
      if area in quartil:
         accepted_areas.append(area)
         

area_media_accepted_areas = sum(accepted_areas) / len(accepted_areas)
area_desviacion_estandar_accepted_areas = statistics.stdev(accepted_areas)
max_area_accepted_areas = max(accepted_areas)
min_area_accepted_areas = min(accepted_areas)
print(f"area_media area_accepted_areas: {area_media_accepted_areas}")
print(f"desviacion estandar_accepted_areas {area_desviacion_estandar_accepted_areas}")
print(f"max_area {max_area_accepted_areas}")
print(f"min_area {min_area_accepted_areas}")
      
#area minima de la naranja aproximada
min_area_prox = int(area_media_accepted_areas - area_desviacion_estandar_accepted_areas)
max_area_prox = int(area_media_accepted_areas + area_desviacion_estandar_accepted_areas)
print(min_area_prox, max_area_prox)  

accepted_areas = [valor for valor in accepted_areas if valor >= min_area_prox and valor <= max_area_prox]

print(f"Accepted_areas: {accepted_areas}")
# # Dibujar los contornos encontrados en la imagen original
# imgContornos = cv2.drawContours(image, contours, -1, (0, 255, 0), 1)
# cv2.imwrite("Contornos.jpg",imgContornos)
# num_naranjas = len(contours)
# #print(f"Número de naranjas detectadas con contorno: {num_naranjas}")
# showWait("Naranjas detectadas", image)


#TODO Usar better_contours en vez de contours
for cnt in contours:
   area = cv2.contourArea(cnt)
   if area in accepted_areas:
      better_contours.append(cnt)
print("len better contours")
print(len(better_contours))

imgContours = cv2.drawContours(image, contours, -1, (0,255,0), 1)
cv2.imwrite("contours_with_area.jpg", imgContours)
print("len contours")
num_naranjas = len(contours)
print(num_naranjas)
#print(f"Número de naranjas contornos con area {num_naranjas}")
showWait("Contours",imgContours)

imgBetterContours = cv2.drawContours(image, contours, -1, (0,255,0), 1)
cv2.imwrite("contours_with_area.jpg", imgBetterContours)
print("len contours")
num_naranjas = len(better_contours)
print(num_naranjas)
#print(f"Número de naranjas contornos con area {num_naranjas}")
showWait("BetterContours",imgBetterContours)
