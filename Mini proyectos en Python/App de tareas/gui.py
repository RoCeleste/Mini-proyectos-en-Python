import util
import PySimpleGUI

PySimpleGUI.theme("LightBrown")
reloj_label = PySimpleGUI.Text("", key="reloj")
label = PySimpleGUI.Text("Ingresar una tarea: ")
agregar_text_box = PySimpleGUI.InputText(tooltip="Tarea", key="tarea")
agregar_boton = PySimpleGUI.Button("Agregar", mouseover_colors="LightBlue2")

editar_listbox = PySimpleGUI.Listbox(values=util.leer_registros(), key="tareas", enable_events=True, size=[45, 10])
editar_boton = PySimpleGUI.Button("Editar", mouseover_colors="LightBlue2")

borrar_boton = PySimpleGUI.Button("Borrar", mouseover_colors="LightBlue2")

terminar_boton = PySimpleGUI.Button("Terminar", mouseover_colors="LightBlue2")

pantalla = PySimpleGUI.Window("App De Tareas",
							  layout=[[label], [agregar_text_box, agregar_boton], [editar_listbox, editar_boton], [borrar_boton], [terminar_boton]],
							  font=("Nunito", 18),
							  )
tareas = util.leer_registros()
while True:
	evento, info = pantalla.read()
	match evento:
		case "Agregar":
			nueva_tarea = info["tarea"]
			tareas.append(nueva_tarea)
			util.editar_registros(tareas)
			pantalla["tareas"].update(values=tareas)

		case "Editar":
			try:
				tarea_a_editar = info["tareas"][0]
				nueva_tarea = info["tarea"]

				indice = tareas.index(tarea_a_editar)
				tareas[indice] = nueva_tarea
				util.editar_registros(tareas)
				pantalla["tareas"].update(values=tareas)
			except IndexError:
				PySimpleGUI.popup("Selecciona un elemento primero", font=("Nunito", 18))

		case "Borrar":
			try:
				tarea_a_borrar = info["tareas"][0]
				tareas.remove(tarea_a_borrar)
				util.editar_registros(tareas)
				pantalla["tareas"].update(values=tareas)
				pantalla["tarea"].update(value="")
			except IndexError:
				PySimpleGUI.popup("Selecciona un elemento primero", font=("Nunito", 18))

		case "Terminar":
			break
		case "tareas":
			pantalla["tarea"].update(value=info["tareas"][0].strip("\n"))

		case PySimpleGUI.WIN_CLOSED:
			break
pantalla.close()
