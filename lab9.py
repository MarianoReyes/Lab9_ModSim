import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# Definir las variables crisp para encontrar la pelota
pos_pelota_x = 5  # Coordenada X de la pelota
pos_pelota_y = 3  # Coordenada Y de la pelota
pos_robot_x = 2   # Coordenada X del robot
pos_robot_y = 1   # Coordenada Y del robot

# Crear variables lingüísticas para encontrar la pelota
distancia_x = ctrl.Antecedent(np.arange(0, 10, 1), 'distancia_x')
distancia_y = ctrl.Antecedent(np.arange(0, 10, 1), 'distancia_y')
encontrar_pelota = ctrl.Consequent(np.arange(0, 11, 1), 'encontrar_pelota')

# Definir funciones de membresía para las variables lingüísticas
distancia_x['cerca'] = fuzz.trimf(distancia_x.universe, [0, 2, 4])
distancia_x['medio'] = fuzz.trimf(distancia_x.universe, [3, 5, 7])
distancia_x['lejos'] = fuzz.trimf(distancia_x.universe, [6, 8, 9])

distancia_y['cerca'] = fuzz.trimf(distancia_y.universe, [0, 2, 4])
distancia_y['medio'] = fuzz.trimf(distancia_y.universe, [3, 5, 7])
distancia_y['lejos'] = fuzz.trimf(distancia_y.universe, [6, 8, 9])

# Definir funciones de pertenencia para la variable de salida
encontrar_pelota['baja'] = fuzz.trimf(encontrar_pelota.universe, [0, 3, 6])
encontrar_pelota['media'] = fuzz.trimf(encontrar_pelota.universe, [4, 6, 8])
encontrar_pelota['alta'] = fuzz.trimf(encontrar_pelota.universe, [7, 10, 10])

# Definir reglas de búsqueda de la pelota (cláusulas de Horn)
regla1 = ctrl.Rule(distancia_x['cerca'] & distancia_y['cerca'],
                   encontrar_pelota['alta'])
regla2 = ctrl.Rule(distancia_x['medio'] & distancia_y['medio'],
                   encontrar_pelota['media'])
regla3 = ctrl.Rule(distancia_x['lejos'] & distancia_y['lejos'],
                   encontrar_pelota['baja'])

# Crear el sistema de control difuso
sistema_ctrl = ctrl.ControlSystem([regla1, regla2, regla3])
encontrar_pelota_ctrl = ctrl.ControlSystemSimulation(sistema_ctrl)

# Entrada de valores crisp
encontrar_pelota_ctrl.input['distancia_x'] = pos_pelota_x - pos_robot_x
encontrar_pelota_ctrl.input['distancia_y'] = pos_pelota_y - pos_robot_y

# Calcula la pertenencia difusa
encontrar_pelota_ctrl.compute()

# Defuzzificación
valor_encontrar_pelota = encontrar_pelota_ctrl.output['encontrar_pelota']

# Graficar funciones de pertenencia
distancia_x.view()
distancia_y.view()
encontrar_pelota.view()
plt.show()

print(f"Valor de encontrar_pelota: {valor_encontrar_pelota:.2f}")
