import cv2
import numpy as np
import statistics

def showWait(titulo, imagen):
    cv2.imshow(titulo, imagen)
    cv2.waitKey(0)
    #cv2.destroyAllWindows()

# Cargar la imagen
image = cv2.imread('img/cosarara.jpg')
#image = cv2.resize(image, dsize=(400,400), interpolation=cv2.INTER_CUBIC)

# Convertir la imagen a espacio de color HSV
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Definir un rango de colores naranja en HSV
#TODO RANGO COMO EL ORANGETE
lower_orange = np.array([20, 100, 80])
upper_orange = np.array([20, 255, 255])

# Crear una máscara para el color naranja
mask = cv2.inRange(hsv_image, lower_orange, upper_orange)
cv2.imwrite("Mascara.jpg",mask)

# Encontrar los contornos de las regiones naranjas
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

better_contours = []
areas = []

# Armo un vector areas de los contornos, sacando las nulas.
for cnt in contours:
   area = cv2.contourArea(cnt)
   if area != 0:
      #if area > 100:
         areas.append(area)
      
areas.sort()
q0 = np.percentile(areas,0)
q1 = np.percentile(areas, 25)
q2 = np.percentile(areas, 50)
q3 = np.percentile(areas, 75)
q4 = np.percentile(areas,100)
print("Primer cuartil (Q1):", q1)
print("Segundo cuartil (Q2):", q2)
print("Tercer cuartil (Q3):", q3)
print("Cuarto cuartil (Q4):", q4)

# Crear listas con los componentes de cada quartile
quartile1 = [x for x in areas if x <= q1]
quartile2 = [x for x in areas if q1 < x <= q2]
quartile3 = [x for x in areas if q2 < x <= q3]
quartile4 = [x for x in areas if x > q3]


accepted_quartiles = []
def quartile_accepted(quartile):
   if ((len(quartile) / len(areas)) > 0.1):
      accepted_quartiles.append(quartile)

quartiles = [quartile1, quartile2, quartile3, quartile4]

for quartile in quartiles:
   quartile_accepted(quartile)

print(f"Acepté un total de {len(accepted_quartiles)} cuartiles de 4")   

accepted_areas = []
for quartile in accepted_quartiles:
   for area in areas:
      if area in quartile:
         accepted_areas.append(area)
         

area_media_accepted_areas = sum(accepted_areas) / len(accepted_areas)
area_desviacion_estandar_accepted_areas = statistics.stdev(accepted_areas)
max_area_accepted_areas = max(accepted_areas)
min_area_accepted_areas = min(accepted_areas)
#print(f"area_media area_accepted_areas: {area_media_accepted_areas}")
#print(f"desviacion estandar_accepted_areas {area_desviacion_estandar_accepted_areas}")
#print(f"max_area {max_area_accepted_areas}")
#print(f"min_area {min_area_accepted_areas}")
      
#area minima de la naranja aproximada
min_area_prox = int(area_media_accepted_areas - area_desviacion_estandar_accepted_areas)
max_area_prox = int(area_media_accepted_areas + area_desviacion_estandar_accepted_areas)
print(min_area_prox, max_area_prox)  

accepted_areas = [valor for valor in accepted_areas if valor >= min_area_prox and valor <= max_area_prox]

area_media_accepted_areas = sum(accepted_areas) / len(accepted_areas)
area_desviacion_estandar_accepted_areas = statistics.stdev(accepted_areas)
max_area_accepted_areas = max(accepted_areas)
min_area_accepted_areas = min(accepted_areas)
print(f"area_media area_accepted_areas: {area_media_accepted_areas}")
print(f"desviacion estandar_accepted_areas {area_desviacion_estandar_accepted_areas}")
print(f"max_area {max_area_accepted_areas}")
print(f"min_area {min_area_accepted_areas}")



for cnt in contours:
   area = cv2.contourArea(cnt)
   if area in accepted_areas:
      better_contours.append(cnt)

imgBetterContours = cv2.drawContours(image, better_contours, -1, (0,0,255), 1)
cv2.imwrite("imgBetterContours.jpg", imgBetterContours)
print("len better contours")
num_naranjas = len(better_contours)
print(num_naranjas)
#print(f"Número de naranjas contornos con area {num_naranjas}")
showWait("BetterContours",imgBetterContours)

showWait("mascara",mask)
# imgContours = cv2.drawContours(image, contours, -1, (0,255,0), 1)
# cv2.imwrite("imgContours.jpg", imgContours)
# print("len contours")
# num_naranjas = len(contours)
# print(num_naranjas)
# #print(f"Número de naranjas contornos con area {num_naranjas}")
# showWait("Contours",imgContours)



