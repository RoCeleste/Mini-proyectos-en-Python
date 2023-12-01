from PyQt6.QtWidgets import QMainWindow, QGridLayout, QLabel, QLineEdit, QPushButton, QApplication, QTableWidget, QTableWidgetItem, QDialog, QVBoxLayout, QComboBox, QToolBar, QStatusBar
from PyQt6.QtGui import QAction, QIcon
import sys
import sqlite3

BASE_DE_DATOS = "data.db"

class Home(QMainWindow):

    def __init__(self):
        """ Muestra la ventana principal """

        super().__init__()
        self.setWindowTitle("Home")
        self.setMinimumSize(800, 600)

        menu_archivo = self.menuBar().addMenu("&Archivo")
        menu_ayuda = self.menuBar().addMenu("&Ayuda")

        agregar_estudiante = QAction(QIcon("iconos/agregar.png"), "Agregar Estudiante", self)
        agregar_estudiante.triggered.connect(self.agregar_registro)
        menu_archivo.addAction(agregar_estudiante)

        info = QAction("Info", self)
        menu_ayuda.addAction(info)
        info.triggered.connect(self.sobre)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(4)
        self.tabla.setHorizontalHeaderLabels(("ID", "Nombre", "Curso", "Contacto"))
        self.setCentralWidget(self.tabla)
        self.cargar_registros()

        barra_herramientas = QToolBar()
        self.addToolBar(barra_herramientas)
        barra_herramientas.addAction(agregar_estudiante)

        self.editar = None
        self.borrar = None
        self.barra_estado = QStatusBar()
        self.setStatusBar(self.barra_estado)
        self.tabla.cellClicked.connect(self.barra_estado_celda_seleccionada)


    def barra_estado_celda_seleccionada(self):
        """ Muestra la barra de estado al seleccionar una celda """

        if self.editar and self.borrar:
            self.barra_estado.removeWidget(self.editar)
            self.barra_estado.removeWidget(self.borrar)
        self.editar = QPushButton("Editar registro")
        self.borrar = QPushButton("Borrar registro")
        self.editar.clicked.connect(self.editar_registro)
        self.borrar.clicked.connect(self.borrar_registro)
        self.barra_estado.addWidget(self.editar)
        self.barra_estado.addWidget(self.borrar)


    def cargar_registros(self):
        """ Carga la BASE_DE_DATOS y muestra los registros en la tabla """
        # O(m.n), m=nro_filas, n=nro_columnas

        conexion = sqlite3.connect(BASE_DE_DATOS)
        cursor = conexion.execute("SELECT * FROM students")
        datos = cursor.fetchall()
        self.tabla.setRowCount(0)
        for i in range(len(datos)):
            self.tabla.insertRow(i)
            for j in range(len(datos[0])):
                self.tabla.setItem(i, j, QTableWidgetItem(str(datos[i][j])))
        conexion.close()

    def agregar_registro(self):
        popup = InsertarPopup()
        popup.exec()

    def editar_registro(self):
        popup = InsertarPopup()
        popup.exec()

    def borrar_registro(self):
        popup = BorrarPopup()
        popup.exec()

    def sobre(self):
        popup = SobrePopup()
        popup.exec()

class InsertarPopup(QDialog):

    def __init__(self):
        """ Muestra la ventana de insercion y edicion de estudiante """

        super().__init__()
        self.setWindowTitle("Agregar Estudiante")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        nombre_label = QLabel("Nombre")
        self.nombre_texto = QLineEdit()

        curso_label = QLabel("Curso")
        self.curso_combo = QComboBox()
        self.curso_combo.addItems(["Quimica", "Matematica", "Computacion", "Fisica"])

        contacto_label = QLabel("Contacto")
        self.contacto_texto = QLineEdit()

        boton_agregar = QPushButton("Agregar Estudiante")
        boton_agregar.clicked.connect(self.agregar_estudiante)

        boton_editar = QPushButton("Editar Estudiante")
        boton_editar.clicked.connect(self.editar_estudiante)

        layout.addWidget(nombre_label)
        layout.addWidget(self.nombre_texto)
        layout.addWidget(curso_label)
        layout.addWidget(self.curso_combo)
        layout.addWidget(contacto_label)
        layout.addWidget(self.contacto_texto)
        layout.addWidget(boton_agregar)
        layout.addWidget(boton_editar)

        self.setLayout(layout)

    def agregar_estudiante(self):
        # O(1)

        conexion = sqlite3.connect(BASE_DE_DATOS)
        cursor = conexion.cursor()

        nombre = self.nombre_texto.text()
        curso = self.curso_combo.itemText(self.curso_combo.currentIndex())
        contacto = self.contacto_texto.text()

        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)", (nombre, curso, contacto))

        conexion.commit()
        cursor.close()
        conexion.close()
        home.cargar_registros()

    def editar_estudiante(self):
        # O(1) o O(n), depende la implementacion de busqueda de miembro en base de datos

        fila = home.tabla.currentRow()
        conexion = sqlite3.connect(BASE_DE_DATOS)
        cursor = conexion.cursor()

        nombre = self.nombre_texto.text()
        curso = self.curso_combo.itemText(self.curso_combo.currentIndex())
        contacto = self.contacto_texto.text()

        cursor.execute("UPDATE students SET name=?, course=?, mobile=? WHERE id=?", (nombre, curso, contacto, home.tabla.item(fila, 0).text()))

        conexion.commit()
        cursor.close()
        conexion.close()
        home.cargar_registros()


class BorrarPopup(QDialog):

    def __init__(self):
        """ Muestra la ventana de confirmacion de borrar estudiante """

        super().__init__()
        self.setWindowTitle("Borrar Estudiante")

        layout = QGridLayout()
        confirmacion = QLabel("Desea borrar estx estudiante?")
        si = QPushButton("Si")
        si.clicked.connect(self.borrar_estudiante)
        no = QPushButton("No")
        no.clicked.connect(self.cancelar_borrado)
        layout.addWidget(confirmacion, 0, 0, 1, 2)
        layout.addWidget(si, 1, 0)
        layout.addWidget(no, 1, 1)
        self.setLayout(layout)

    def borrar_estudiante(self):
        # O(1) o O(n), depende la implementacion de busqueda de miembro en base de datos

        fila = home.tabla.currentRow()
        conexion = sqlite3.connect(BASE_DE_DATOS)
        cursor = conexion.cursor()

        cursor.execute("DELETE from students WHERE id=?", [home.tabla.item(fila, 0).text()])

        conexion.commit()
        cursor.close()
        conexion.close()
        self.close()
        home.cargar_registros()

    def cancelar_borrado(self):
        self.close()


class SobrePopup(QDialog):

    def __init__(self):
        """ Muestra la ventana de info """

        super().__init__()
        layout = QGridLayout()
        texto = QLabel("Esta app es un modelado de registro de estudiantes en una institucion educativa.\nEsta permitida la modificacion y el uso de la misma.")
        boton = QPushButton("OK")
        boton.clicked.connect(self.cerrar)
        layout.addWidget(texto, 0, 0, 1, 3)
        layout.addWidget(boton, 1, 1, 1, 1)
        self.setLayout(layout)

    def cerrar(self):
        self.close()

app = QApplication(sys.argv)
home = Home()
home.show()
sys.exit(app.exec())
