import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

# Funciones para operar en la base de datos
def conectar_db():
    conn = sqlite3.connect('biblioteca.db')
    cursor = conn.cursor()
    return conn, cursor

def desconectar_db(conn):
    conn.commit()
    conn.close()

def ejecutar_consulta(query, parameters=()):
    conn, cursor = conectar_db()
    cursor.execute(query, parameters)
    conn.commit()
    desconectar_db(conn)
    return cursor

def obtener_registros(tabla):
    conn, cursor = conectar_db()
    query = f'SELECT * FROM {tabla}'
    cursor.execute(query)
    registros = cursor.fetchall()
    desconectar_db(conn)
    return registros

def agregar_registro(tabla, campos, valores):
    if all(valores):
        query = f'INSERT INTO {tabla} ({", ".join(campos)}) VALUES ({", ".join("?" * len(valores))})'
        ejecutar_consulta(query, valores)
        messagebox.showinfo("Información", f"Registro agregado en {tabla}")
    else:
        messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")

def eliminar_registro(tabla, idcampo, idvalor):
    query = f'DELETE FROM {tabla} WHERE {idcampo} = ?'
    ejecutar_consulta(query, (idvalor,))
    messagebox.showinfo("Información", f"Registro eliminado en {tabla}")

# Función para actualizar el treeview
def actualizar_treeview(tree, tabla):
    for item in tree.get_children():
        tree.delete(item)
    registros = obtener_registros(tabla)
    for registro in registros:
        tree.insert("", "end", values=registro)

# Crear la ventana principal de la aplicación
root = tk.Tk()
root.title("Gestión de Biblioteca")
root.geometry("800x600")

# Crear un Notebook para las pestañas
notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True, fill="both")

# Función para crear un frame con la estructura básica para CRUD
def crear_tabla(tabla, campos, idcampo):
    frame = ttk.Frame(notebook)
    notebook.add(frame, text=tabla)
    
    canvas = tk.Canvas(frame)
    v_scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    h_scrollbar = ttk.Scrollbar(frame, orient="horizontal", command=canvas.xview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    v_scrollbar.pack(side="right", fill="y")
    h_scrollbar.pack(side="bottom", fill="x")

    # Treeview para mostrar los registros
    tree = ttk.Treeview(scrollable_frame, columns=campos, show="headings")
    tree.pack(pady=20, expand=True, fill="both")
    
    for campo in campos:
        tree.heading(campo, text=campo)
        tree.column(campo, anchor="w")
    
    # Actualizar Treeview
    actualizar_treeview(tree, tabla)

    # Campos de entrada para agregar un nuevo registro
    entries = {}
    for campo in campos:
        if campo != idcampo:
            label = tk.Label(scrollable_frame, text=campo)
            label.pack(pady=2)
            entry = tk.Entry(scrollable_frame)
            entry.pack(pady=2)
            entries[campo] = entry

    def agregar():
        valores = [entries[campo].get() for campo in campos if campo != idcampo]
        agregar_registro(tabla, [campo for campo in campos if campo != idcampo], valores)
        actualizar_treeview(tree, tabla)

    def eliminar():
        selected_item = tree.selection()[0]
        idvalor = tree.item(selected_item)['values'][0]
        eliminar_registro(tabla, idcampo, idvalor)
        actualizar_treeview(tree, tabla)

    btn_agregar = tk.Button(scrollable_frame, text="Agregar", command=agregar, bg="lightgreen", fg="black", font=("Arial", 12, "bold"))
    btn_agregar.pack(pady=5)

    btn_eliminar = tk.Button(scrollable_frame, text="Eliminar", command=eliminar, bg="red", fg="white", font=("Arial", 12, "bold"))
    btn_eliminar.pack(pady=5)

# Crear una pestaña para cada tabla
crear_tabla("USUARIO", ["idusuario", "dni", "nombre", "apellido", "contraseña", "direccion", "celular", "roles", "autores_idautor", "libros_autores_libros_idlibros", "libros_autores_autores_idautor"], "idusuario")
crear_tabla("LIBRO", ["idlibro", "titulo", "autores", "edicion", "descripcion", "año", "numero_paginas", "categoria_idcategoria", "categorias_idcategorias", "autores_idautor"], "idlibro")
crear_tabla("PRESTAMOS", ["idprestamo", "fecha_prestamo", "fecha_entrega", "libros_idlibros", "usuario_idusuario", "USUARIOS_idusuario", "LIBRO_idlibro"], "idprestamo")
crear_tabla("AUTORES", ["idautor", "nombres", "apellidos", "dni", "modalidad", "autorescol"], "idautor")
crear_tabla("LIBROS_AUTORES", ["libros_idlibros", "autores_idautor", "autores_idautor1"], "libros_idlibros")
crear_tabla("CATEGORIAS", ["idcategoria", "nombre_categoria", "ubicacion"], "idcategoria")
crear_tabla("ROLES", ["idrol", "nombre_rol"], "idrol")

# Ejecutar la aplicación
root.mainloop()
