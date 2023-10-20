import cv2
import numpy as np
import statistics


def showWait(titulo, imagen):
    cv2.imshow(titulo, imagen)
    cv2.waitKey(0)
    # cv2.destroyAllWindows()


# Cargar la imagen
image = cv2.imread("img/naranjo.jpg")
# Convertir la imagen a espacio de color HSV
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
# Definir un rango de colores naranja en HSV
lower_orange = np.array([0, 100, 100])
upper_orange = np.array([25, 255, 255])
# Crear una máscara para el color naranja
mask = cv2.inRange(hsv_image, lower_orange, upper_orange)
cv2.imwrite("Mascara.jpg", mask)

iterations = input("Por favor, ingrese la cantidad de iteraciones para la erosión: ")
showWait("Máscara sin erosión", mask)

kernel = np.ones((5, 5), np.uint8)
eroded_mask = cv2.erode(mask, kernel, iterations=int(iterations))
cv2.imwrite("mascara_erosionada.jpg", eroded_mask)
showWait("Máscara erosionada", eroded_mask)

# Encontrar los contornos de las regiones naranjas
contours, _ = cv2.findContours(eroded_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

better_contours = []
areas = []

# Armo un vector areas de los contornos, sacando las nulas.
for cnt in contours:
    area = cv2.contourArea(cnt)
    if area > 0:
        # if area > 90000:
        areas.append(area)

areas.sort()
q0 = np.percentile(areas, 0)
q1 = np.percentile(areas, 25)
q2 = np.percentile(areas, 50)
q3 = np.percentile(areas, 75)
q4 = np.percentile(areas, 100)
print("\nPrimer cuartil (Q1):", q1)
print("\nSegundo cuartil (Q2):", q2)
print("\nTercer cuartil (Q3):", q3)
print("\nCuarto cuartil (Q4):", q4)

# Crear listas con los componentes de cada quartile
quartile1 = [x for x in areas if x <= q1]
quartile2 = [x for x in areas if q1 < x <= q2]
quartile3 = [x for x in areas if q2 < x <= q3]
quartile4 = [x for x in areas if x > q3]

accepted_quartiles = []


def quartile_accepted(quartile):
    if (sum(quartile) / sum(areas)) > 0.1:
        accepted_quartiles.append(quartile)


quartiles = [quartile1, quartile2, quartile3, quartile4]

for quartile in quartiles:
    quartile_accepted(quartile)

print(f"\nAcepté un total de {len(accepted_quartiles)} cuartiles de 4")

accepted_areas = []
for quartile in accepted_quartiles:
    for area in areas:
        if area in quartile:
            accepted_areas.append(area)


area_media_accepted_areas = sum(accepted_areas) / len(accepted_areas)
area_desviacion_estandar_accepted_areas = statistics.stdev(accepted_areas)
max_area_accepted_areas = max(accepted_areas)
min_area_accepted_areas = min(accepted_areas)


min_area_prox = abs(
    int(area_media_accepted_areas - area_desviacion_estandar_accepted_areas)
)
max_area_prox = int(area_media_accepted_areas + area_desviacion_estandar_accepted_areas)
print(f"\nMínima área promedio de naranja: {min_area_prox}")
print(f"Máxima área promedio de naranja: {max_area_prox}")


# accepted_areas = [valor for valor in accepted_areas if valor >= min_area_prox and valor <= max_area_prox]

area_media_accepted_areas = sum(accepted_areas) / len(accepted_areas)
area_desviacion_estandar_accepted_areas = statistics.stdev(accepted_areas)
max_area_accepted_areas = max(accepted_areas)
min_area_accepted_areas = min(accepted_areas)

print(f"\nArea media de las áreas aceptadas como válidas: {area_media_accepted_areas}")
print(
    f"Desviación estándar de las áreas aceptadas como válidas: {area_desviacion_estandar_accepted_areas}"
)
print(f"Máxima área aceptada: {max_area_accepted_areas}")
print(f"Mínima área aceptada {min_area_accepted_areas}")


for cnt in contours:
    area = cv2.contourArea(cnt)
    if area in accepted_areas:
        better_contours.append(cnt)

imgBetterContours = cv2.drawContours(image, better_contours, -1, (255, 255, 0), 3)
cv2.imwrite("imgBetterContours.jpg", imgBetterContours)
num_naranjas = len(better_contours)
print(f"\nNúmero de Naranjas: {num_naranjas}")
showWait("BetterContours", imgBetterContours)

# # Contornos originales - DEPRECATED
# imgContours = cv2.drawContours(image, contours, -1, (255,255,12), 2)
# cv2.imwrite("imgContours.jpg", imgContours)
# num_naranjas = len(contours)
# print(f"Número de Naranjas: {num_naranjas}")
# showWait("Contours",imgContours)
