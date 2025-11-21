import tkinter as tk
from tkinter import Toplevel, messagebox
from tkinter import ttk
import sqlite3  


# conectar base de datos
conn = sqlite3.connect("dbcodearts.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS alumnos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT UNIQUE NOT NULL,
        correo TEXT NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS cursos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT UNIQUE NOT NULL,
        descripcion TEXT NOT NULL
    )
""")


conn.commit()


# lista donde se guardan los alumnos
alumnos = []

# lista donde se guardan los cursos
cursos = []

app = tk.Tk()
app.title("🏫 Gestor de alumnos")
app.geometry("550x550")
style = ttk.Style()
style.theme_use("clam")  


def ventana1():
    # creo la ventana de alumnos
    ventana1 = Toplevel(app)
    ventana1.title("🧑‍🎓 Alumnos")
    ventana1.geometry("550x300")



    # para que las columnas se ajusten solas
    ventana1.grid_columnconfigure(0, weight=1)
    ventana1.grid_columnconfigure(1, weight=1)
    ventana1.grid_columnconfigure(2, weight=2)

    # titulo de la ventana
    titulo = tk.Label(ventana1, text="Gestion de alumnos", font=("Arial", 14, "bold"))
    titulo.grid(row=0, column=0, columnspan=3, pady=10)

    # etiqueta para nombre
    nombre_label = tk.Label(ventana1, text="Nombre:")
    nombre_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    # caja donde escribo el nombre
    entrada_nombre = tk.Entry(ventana1, relief="solid", bd=1)
    entrada_nombre.grid(row=1, column=1, columnspan=2, padx=10, pady=10, sticky="ew")

    # etiqueta para correo
    correo_label = tk.Label(ventana1, text="Correo:")
    correo_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

    # caja donde escribo el correo
    entrada_correo = tk.Entry(ventana1, relief="solid", bd=1)
    entrada_correo.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky="ew")
    

    # tabla donde se muestran los alumnos
    tabla_alumnos = ttk.Treeview(ventana1, columns=("Nombre", "Correo"), show="headings", height=10)
    tabla_alumnos.heading("Nombre", text="Nombre")
    tabla_alumnos.heading("Correo", text="Correo")
    tabla_alumnos.column("Nombre", width=300)
    tabla_alumnos.column("Correo", width=300)
    tabla_alumnos.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="ew")



    # para cargar los alumnos a base de datos
    cursor.execute("SELECT nombre, correo FROM alumnos")
    for fila in cursor.fetchall():
        tabla_alumnos.insert("", "end", values=fila)
 

    def guardar_alumno():
        # recojo los valores escritos
        nombre = entrada_nombre.get()
        correo = entrada_correo.get()

        # Para verificar que los campos no se queden vacios
        if nombre == "" or correo == "":
            messagebox.showwarning("error", "por favor rellena todos los campos")
            return

        # para revisar si ya existe en la lista actual
        for alumno in alumnos:
            if alumno["nombre"].lower() == nombre.lower():
                messagebox.showerror("duplicado", f"el alumno '{nombre}' ya existe")
                return

        # guardar los datos en la base de datos
        try:
            cursor.execute("INSERT INTO alumnos (nombre, correo) VALUES (?, ?)", (nombre, correo))
            conn.commit()
        except sqlite3.IntegrityError:
            messagebox.showerror("duplicado", f"el alumno '{nombre}' ya existe")
            return
      

        # añado el alumno a la lista
        alumnos.append({"nombre": nombre, "correo": correo})

        # lo muestro en la tabla
        tabla_alumnos.insert("", "end", values=(nombre, correo))

        # limpio las cajas
        entrada_nombre.delete(0, tk.END)
        entrada_correo.delete(0, tk.END)

        # aviso de que se ha guardado
        messagebox.showinfo("guardado", f"alumno '{nombre}' guardado")

    def borrar_formulario():
        # borra lo escrito en las cajas
        entrada_nombre.delete(0, tk.END)
        entrada_correo.delete(0, tk.END)

    def borrar_seleccionado():
        # recojo lo seleccionado
        seleccion = tabla_alumnos.selection()

        # aviso si no hay nada seleccionado
        if not seleccion:
            messagebox.showwarning("error", "selecciona un alumno para borrar")
            return

        # borro uno por uno
        for item in seleccion:
            valores = tabla_alumnos.item(item, "values")
            nombre = valores[0]

            # borrar en la base de datos
            cursor.execute("DELETE FROM alumnos WHERE nombre = ?", (nombre,))
            conn.commit()
       

            # lo quito de la lista
            for a in alumnos:
                if a["nombre"] == nombre:
                    alumnos.remove(a)
                    break

            # lo quito de la tabla
            tabla_alumnos.delete(item)

    # boton para guardar alumno
    tk.Button(ventana1, text="✅ Guardar", command=guardar_alumno).grid(row=3, column=0, padx=10, pady=10)

    # boton para borrar alumno seleccionado
    tk.Button(ventana1, text="❌ Borrar seleccionado", command=borrar_seleccionado).grid(row=3, column=1, padx=10, pady=10)

    # boton para limpiar formulario
    tk.Button(ventana1, text="🗑️ Borrar formulario", command=borrar_formulario).grid(row=3, column=2, padx=10, pady=10)


def ventana2():
    # creo la ventana de cursos
    ventana2 = Toplevel(app)
    ventana2.title("📘 Cursos")
    ventana2.geometry("550x300")

    # que las columnas se adapten
    ventana2.grid_columnconfigure(0, weight=1)
    ventana2.grid_columnconfigure(1, weight=1)
    ventana2.grid_columnconfigure(2, weight=2)

    # titulo de la ventana
    titulo = tk.Label(ventana2, text="Gestion de cursos", font=("Arial", 14, "bold"))
    titulo.grid(row=0, column=0, columnspan=3, pady=10)

    # nombre del curso
    nombre_label = tk.Label(ventana2, text="Nombre:")
    nombre_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    # caja para escribir el nombre
    entrada_nombre = tk.Entry(ventana2, relief="solid", bd=1)
    entrada_nombre.grid(row=1, column=1, columnspan=2, padx=10, pady=10, sticky="ew")

    # descripcion del curso
    descr_label = tk.Label(ventana2, text="Descripcion:")
    descr_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

    # caja donde escribo descripcion
    entrada_descr = tk.Entry(ventana2, relief="solid", bd=1)
    entrada_descr.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky="ew")

    # tabla donde se ven los cursos y descripcion
    tabla_cursos = ttk.Treeview(ventana2, columns=("Nombre", "Descripcion"), show="headings", height=10)
    tabla_cursos.heading("Nombre", text="Nombre")
    tabla_cursos.heading("Descripcion", text="Descripcion")
    tabla_cursos.column("Nombre", width=300)
    tabla_cursos.column("Descripcion", width=300)
    tabla_cursos.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

    # cargar datos desde la base

    cursor.execute("SELECT nombre, descripcion FROM cursos")
    for fila in cursor.fetchall():
        tabla_cursos.insert("", "end", values=fila)


    def guardar_curso():
        # coger lo escrito
        nombre = entrada_nombre.get()
        descripcion = entrada_descr.get()

        # si falta algo aviso
        if nombre == "" or descripcion == "":
            messagebox.showwarning("error", "por favor rellena todos los campos")
            return

        # reviso duplicados
        for curso in cursos:
            if curso["nombre"].lower() == nombre.lower():
                messagebox.showerror("duplicado", f"el curso '{nombre}' ya existe")
                return

        # guardar en la basee de datos
        try:
            cursor.execute("INSERT INTO cursos (nombre, descripcion) VALUES (?, ?)", (nombre, descripcion))
            conn.commit()
        except sqlite3.IntegrityError:
            messagebox.showerror("duplicado", f"el curso '{nombre}' ya existe")
            return


        # añado a la lista
        cursos.append({"nombre": nombre, "descripcion": descripcion})

        # lo muestro en la tabla
        tabla_cursos.insert("", "end", values=(nombre, descripcion))

        # borro lo escrito
        entrada_nombre.delete(0, tk.END)
        entrada_descr.delete(0, tk.END)

        # aviso 
        messagebox.showinfo("guardado", f"curso '{nombre}' guardado")

    def borrar_formulario_curso():
        # limpiar lo escrito
        entrada_nombre.delete(0, tk.END)
        entrada_descr.delete(0, tk.END)

    def borrar_seleccionado_curso():
        # recojo la seleccion
        seleccion = tabla_cursos.selection()

        # aviso si no hay nada sleeccioando
        if not seleccion:
            messagebox.showwarning("error", "selecciona un curso para borrar")
            return

        # borro uno por uno
        for item in seleccion:
            valores = tabla_cursos.item(item, "values")
            nombre = valores[0]

            # borrar rn la base detaos
            cursor.execute("DELETE FROM cursos WHERE nombre = ?", (nombre,))
            conn.commit()
            # -------------------------------------------------

            # para quitar de la lista
            for c in cursos:
                if c["nombre"] == nombre:
                    cursos.remove(c)
                    break

            # quitar de la tabla
            tabla_cursos.delete(item)

    # boton para guardar curso
    tk.Button(ventana2, text="✅ Guardar", command=guardar_curso).grid(row=3, column=0, padx=10, pady=10)

    # boton para borrar seleccionado
    tk.Button(ventana2, text="❌ Borrar seleccionado", command=borrar_seleccionado_curso).grid(row=3, column=1, padx=10, pady=10)

    # boton para borrar formulario
    tk.Button(ventana2, text="🗑️ Borrar formulario", command=borrar_formulario_curso).grid(row=3, column=2, padx=10, pady=10)


# configuracion de la ventana principa
app.grid_columnconfigure(0, weight=1)

# titulo grande
label_inicio = tk.Label(app, text="Bienvenido al programa de gestion de alumnos/cursos",
                       font=("Arial", 16, "bold"))
label_inicio.grid(row=0, column=0, pady=10)

# botones principales
tk.Button(app, text="🧑‍🎓 Alumnos", command=ventana1, bd=4, relief="solid").grid(row=1, column=0, pady=10)
tk.Button(app, text="📘 Cursos", command=ventana2, bd=4, relief="solid").grid(row=2, column=0, pady=10)
tk.Button(app, text="❌ Salir", command=app.destroy, bd=4, relief="solid").grid(row=3, column=0, pady=10)

# inicio del programa
app.mainloop()
