def leer_registros(archivo="registro.txt"):
	""" Obtiene una lista con las tareas guardadas."""
	registros = []
	with open("registro.txt", "r") as archivo:
		for tarea in archivo:
			if not len(tarea) == 0:
				registros.append(tarea.strip("\n"))
	return registros


def editar_registros(registros, archivo="registro.txt"):
	""" Guarda la lista de registros en el archivo especificado. """
	with open("registro.txt", "w") as archivo:
		for tarea in registros:
			archivo.write(tarea + "\n")
