import streamlit
import util

def agregar():
	tarea = streamlit.session_state["input"]
	tareas.append(tarea)
	util.editar_registros(tareas)
	streamlit.session_state["input"] = ""

def borrar():
	for tarea in tareas:
		tarea_checkbox = streamlit.session_state[tarea]
		if tarea_checkbox:
			tareas.remove(tarea)
			util.editar_registros(tareas)


def actualizar_pagina():
	for tarea in tareas:
		arg = tarea
		streamlit.checkbox(label=tarea, key=tarea, on_change=borrar)


streamlit.title("App de Tareas")

tareas = util.leer_registros()
actualizar_pagina()
streamlit.text_input(label="Agrega una nueva tarea", key="input", on_change=agregar)
