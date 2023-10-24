import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import Canvas
import skfuzzy.control as ctrl
import random
import math
# 1. y 2. Variables crisp y lingüísticas para encontrar la pelota
# Distancia del robot a la pelota de 0 a 100 metros
x_dist = np.arange(0, 201, 1)
# Distancia de la pelota a la porteria
b_dist = np.arange(0, 401, 1)
# Ángulo entre el robot y la pelota de -180 a 180 grados
x_ang = np.arange(-180, 181, 1)

# Funciones de pertenencia para la distancia
dist_muy_cerca = fuzz.trimf(x_dist, [0, 0, 25])
dist_cerca = fuzz.trimf(x_dist, [0, 25, 50])
dist_lejos = fuzz.trimf(x_dist, [50, 75, 100])
dist_muy_lejos = fuzz.trimf(x_dist, [100, 150, 200])

# Funciones de pertenencia para la distancia
bdist_muy_cerca = fuzz.trimf(b_dist, [0, 50, 100])
bdist_cerca = fuzz.trimf(b_dist, [100, 150, 200])
bdist_lejos = fuzz.trimf(b_dist, [200, 250, 300])
bdist_muy_lejos = fuzz.trimf(b_dist, [300, 350, 400])

# Funciones de pertenencia para el ángulo
ang_muy_izq = fuzz.trimf(x_ang, [-180, -180, -90])
ang_izq = fuzz.trimf(x_ang, [-180, -90, 0])
ang_frente = fuzz.trimf(x_ang, [-90, 0, 90])
ang_der = fuzz.trimf(x_ang, [0, 90, 180])
ang_muy_der = fuzz.trimf(x_ang, [90, 180, 180])

# 5. y 6. Variables crisp y lingüísticas para saber
# la fuerza con la que se debe patear la pelota
x_force = np.arange(0, 101, 1)  # Fuerza de la patada de 0 a 100%

# Funciones de pertenencia para la fuerza
force_suave = fuzz.trimf(x_force, [0, 0, 50])
force_medio = fuzz.trimf(x_force, [0, 50, 100])
force_fuerte = fuzz.trimf(x_force, [50, 100, 100])

distancia_corrida = np.arange(0, 101, 1)
distancia_poca = fuzz.trimf(distancia_corrida, [0, 0, 50])
distancia_media = fuzz.trimf(distancia_corrida, [0, 50, 100])
distancia_mucha = fuzz.trimf(distancia_corrida, [50, 100, 100])

# 9. Gráfica de las funciones de pertenencia para encontrar la pelota
plt.figure()
plt.plot(x_dist, dist_muy_cerca, 'b', label='Muy Cerca')
plt.plot(x_dist, dist_cerca, 'g', label='Cerca')
plt.plot(x_dist, dist_lejos, 'r', label='Lejos')
plt.plot(x_dist, dist_muy_lejos, 'y', label='Muy Lejos')
plt.title('Funciones de pertenencia para la distancia al balón')
plt.xlabel('Distancia (m)')
plt.ylabel('Grado de pertenencia')
plt.legend()

plt.figure()
plt.plot(b_dist, bdist_muy_cerca, 'b', label='Muy Cerca')
plt.plot(b_dist, bdist_cerca, 'g', label='Cerca')
plt.plot(b_dist, bdist_lejos, 'r', label='Lejos')
plt.plot(b_dist, bdist_muy_lejos, 'y', label='Muy Lejos')
plt.title('Funciones de pertenencia para la distancia a la porteria')
plt.xlabel('Distancia (m)')
plt.ylabel('Grado de pertenencia')
plt.legend()

plt.figure()
plt.plot(x_ang, ang_muy_izq, 'b', label='Muy a la Izquierda')
plt.plot(x_ang, ang_izq, 'g', label='Izquierda')
plt.plot(x_ang, ang_frente, 'r', label='Frente')
plt.plot(x_ang, ang_der, 'y', label='Derecha')
plt.plot(x_ang, ang_muy_der, 'm', label='Muy a la Derecha')
plt.title('Funciones de pertenencia para el ángulo con el balón')
plt.xlabel('Ángulo (grados)')
plt.ylabel('Grado de pertenencia')
plt.legend()

plt.figure()
plt.plot(distancia_corrida, distancia_poca, 'b', label='Poca')
plt.plot(distancia_corrida, distancia_media, 'g', label='Media')
plt.plot(distancia_corrida, distancia_mucha, 'r', label='Mucha')
plt.title('Funciones de pertenencia para la distancia del robot con la pelota')
plt.xlabel('Distancia corrida (m)')
plt.ylabel('Grado de pertenencia')
plt.legend()


# 10. Gráfica de las funciones de pertenencia para saber
# la fuerza con la que se debe patear la pelota
plt.figure()
plt.plot(x_force, force_suave, 'b', label='Suave')
plt.plot(x_force, force_medio, 'g', label='Medio')
plt.plot(x_force, force_fuerte, 'r', label='Fuerte')
plt.title('Funciones de pertenencia para la fuerza de la patada')
plt.xlabel('Fuerza (%)')
plt.ylabel('Grado de pertenencia')
plt.legend()

plt.show()

# 3. Definición de las cláusulas de Horn
distancia_x = ctrl.Antecedent(x_dist, 'distancia_x')
distancia_b = ctrl.Antecedent(b_dist, 'distancia_b')
angulo = ctrl.Antecedent(x_ang, 'angulo')
fuerza = ctrl.Consequent(x_force, 'fuerza')
distancia_ball = ctrl.Consequent(distancia_corrida, 'distancia_ball')

# Define las funciones de pertenencia usando las anteriores definiciones
distancia_x.automf(names=['Muy Cerca', 'Cerca', 'Lejos', 'Muy Lejos'])
distancia_b.automf(names=['Muy Cerca', 'Cerca', 'Lejos', 'Muy Lejos'])
angulo.automf(names=['Muy a la Izquierda', 'Izquierda', 'Frente', 'Derecha',
                     'Muy a la Derecha'])
fuerza.automf(names=['Suave', 'Medio', 'Fuerte'])
distancia_ball.automf(names=['Poca', 'Media', 'Mucha'])

regla1 = ctrl.Rule(distancia_b['Muy Cerca'] & angulo['Frente'],
                   fuerza['Suave'])
regla2 = ctrl.Rule(distancia_b['Muy Cerca'] & angulo['Derecha'],
                   fuerza['Suave'])
regla3 = ctrl.Rule(distancia_b['Muy Cerca'] & angulo['Muy a la Derecha'],
                   fuerza['Medio'])
regla4 = ctrl.Rule(distancia_b['Muy Cerca'] & angulo['Muy a la Izquierda'],
                   fuerza['Medio'])
regla5 = ctrl.Rule(distancia_b['Muy Cerca'] & angulo['Izquierda'],
                   fuerza['Suave'])

regla6 = ctrl.Rule(distancia_b['Cerca'] & angulo['Frente'],
                   fuerza['Medio'])
regla7 = ctrl.Rule(distancia_b['Cerca'] & angulo['Derecha'],
                   fuerza['Medio'])
regla8 = ctrl.Rule(distancia_b['Cerca'] & angulo['Muy a la Derecha'],
                   fuerza['Fuerte'])
regla9 = ctrl.Rule(distancia_b['Cerca'] & angulo['Muy a la Izquierda'],
                   fuerza['Fuerte'])
regla10 = ctrl.Rule(distancia_b['Cerca'] & angulo['Izquierda'],
                    fuerza['Medio'])

regla11 = ctrl.Rule(distancia_b['Lejos'],
                    fuerza['Fuerte'])
regla12 = ctrl.Rule(distancia_b['Muy Lejos'],
                    fuerza['Fuerte'])


# Sistema de control disparo porteria
sistema_ctrl = ctrl.ControlSystem([regla1, regla2, regla3, regla4, regla5,
                                   regla6, regla7, regla8, regla9, regla10,
                                   regla11, regla12])
disparar_porteria_ctrl = ctrl.ControlSystemSimulation(sistema_ctrl)

reglab1 = ctrl.Rule(distancia_x['Muy Cerca'] & angulo['Frente'],
                    distancia_ball['Poca'])
reglab2 = ctrl.Rule(distancia_x['Muy Cerca'] & angulo['Derecha'],
                    distancia_ball['Poca'])
reglab3 = ctrl.Rule(distancia_x['Muy Cerca'] & angulo['Muy a la Derecha'],
                    distancia_ball['Media'])
reglab4 = ctrl.Rule(distancia_x['Muy Cerca'] & angulo['Muy a la Izquierda'],
                    distancia_ball['Media'])
reglab5 = ctrl.Rule(distancia_x['Muy Cerca'] & angulo['Izquierda'],
                    distancia_ball['Poca'])

reglab6 = ctrl.Rule(distancia_x['Cerca'] & angulo['Frente'],
                    distancia_ball['Media'])
reglab7 = ctrl.Rule(distancia_x['Cerca'] & angulo['Derecha'],
                    distancia_ball['Media'])
reglab8 = ctrl.Rule(distancia_x['Cerca'] & angulo['Muy a la Derecha'],
                    distancia_ball['Mucha'])
reglab9 = ctrl.Rule(distancia_x['Cerca'] & angulo['Muy a la Izquierda'],
                    distancia_ball['Mucha'])
reglab10 = ctrl.Rule(distancia_x['Cerca'] & angulo['Izquierda'],
                     distancia_ball['Media'])

reglab11 = ctrl.Rule(distancia_x['Lejos'],
                     distancia_ball['Mucha'])
reglab12 = ctrl.Rule(distancia_x['Muy Lejos'],
                     distancia_ball['Mucha'])

sistema_ctrl_ball = ctrl.ControlSystem([reglab1, reglab2, reglab3, reglab4,
                                        reglab5, reglab6, reglab7, reglab8,
                                        reglab9, reglab10, reglab11, reglab12])
encontrar_pelota_ctrl = ctrl.ControlSystemSimulation(sistema_ctrl_ball)


# 11. Interfaz Gráfica
root = tk.Tk()
canvas = Canvas(root, width=400, height=400)
canvas.pack()


def simulacion():
    for _ in range(10):
        # Posiciones aleatorias para el robot y la pelota
        pos_robot_x, pos_robot_y = random.randint(0, 200),random.randint(0, 200)
        pos_pelota_x, pos_pelota_y = random.randint(0, 200),random.randint(0, 200)

        posicion_porteria_x, posicion_porteria_y = 380, 200

        # Dibuja las posiciones
        canvas.delete("all")
        pelota = canvas.create_oval(pos_pelota_x - 10,
                                    pos_pelota_y - 10,
                                    pos_pelota_x + 10,
                                    pos_pelota_y + 10,
                                    fill='green')
        robot = canvas.create_rectangle(pos_robot_x - 15,
                                        pos_robot_y - 15,
                                        pos_robot_x + 15,
                                        pos_robot_y + 15,
                                        fill='blue')
        # Dibujar portería (representado por un rectángulo)
        goal = canvas.create_rectangle(380, 150, 400, 250, fill="yellow")

        dx = pos_pelota_x - pos_robot_x
        dy = pos_pelota_y - pos_robot_y

        # Calcula la distancia y el ángulo real
        dist = math.sqrt(dx**2 + dy**2)
        angle = math.degrees(math.atan2(dy, dx))
        print(f'Robot-Balon: Distancia: {dist:.2f} Angulo: {angle:.2f}')

        encontrar_pelota_ctrl.input['distancia_x'] = dist
        encontrar_pelota_ctrl.input['angulo'] = angle
        encontrar_pelota_ctrl.compute()

        valor_encontrar_pelota = encontrar_pelota_ctrl.output['distancia_ball']
        print(f'La distancia que corre el robot: {valor_encontrar_pelota:.2f}')

        dx = pos_pelota_x - posicion_porteria_x
        dy = pos_pelota_y - posicion_porteria_y

        dist = math.sqrt(dx**2 + dy**2)
        angle = math.degrees(math.atan2(dy, dx))
        print(f'Balon-Puerta: Distancia: {dist:.2f} Angulo: {angle:.2f}')

        disparar_porteria_ctrl.input['distancia_b'] = dist
        disparar_porteria_ctrl.input['angulo'] = angle
        disparar_porteria_ctrl.compute()

        valor_disparar_porteria = disparar_porteria_ctrl.output['fuerza']
        print(f'La fuerza con la que pega: {valor_disparar_porteria:.2f}\n')

        # Mover el robot hacia la pelota
        # (Este es un acercamiento simple, se puede hacer más sofisticado)
        # AQUI FALTA ANIMAR EL ROBOT
        if pos_robot_x < pos_pelota_x:
            pos_robot_x += 10
        else:
            pos_robot_x -= 10

        if pos_robot_y < pos_pelota_y:
            pos_robot_y += 10
        else:
            pos_robot_y -= 10
        # Dibuja la nueva posición del robot
        canvas.delete(robot)
        robot = canvas.create_rectangle(pos_robot_x - 15, pos_robot_y - 15,
                                        pos_robot_x + 15, pos_robot_y + 15,
                                        fill='blue')

        # SIGUIENTE SIMULACION:
        root.update()
        root.after(1000)  # Pausa de 1 segundo entre movimientos


btn = tk.Button(root, text="Iniciar Simulación", command=simulacion)
btn.pack()

root.mainloop()
