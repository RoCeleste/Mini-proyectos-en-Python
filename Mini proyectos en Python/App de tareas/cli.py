from util import leer_registros, editar_registros
from datetime import datetime

hoy = datetime.today()
print(f" --- {hoy.day}/{hoy.month}/{hoy.year} {hoy.hour}:{hoy.minute} --- ")
lista_tareas = leer_registros()

orden = input("Ingresar comando: ").strip().lower()
while True:
	match orden:
		case "agregar":
			tarea = input("Ingresa la nueva tarea: ").strip()
			lista_tareas.append(tarea)

		case "mostrar":
			for i in range(len(lista_tareas)):
				print(f"{i + 1}) {lista_tareas[i]}")

		case "editar":
			try:
				posicion = int(input("Posicion de la tarea que queres editar: ")) - 1
				nueva_tarea = input("Ingresar nueva tarea: ").strip()
				lista_tareas[posicion] = nueva_tarea

			except ValueError:
				print("Error: Tenes que ingresar un numero entero")
				posicion = int(input("Posicion de la tarea que queres editar: ")) - 1
			except IndexError:
				print("Error: No hay tarea con ese numero")
				posicion = int(input("Posicion de la tarea que queres editar: ")) - 1

		case "borrar lista":
			lista_tareas = []

		case "borrar":
			posicion = int(input("Posicion de la tarea que queres borrar: ")) - 1
			lista_tareas.pop(posicion)

		case "terminar":
			editar_registros(lista_tareas)
			break

		case _:
			print("Comando invalido")

	orden = input("Ingresar comando: ").strip().lower()
