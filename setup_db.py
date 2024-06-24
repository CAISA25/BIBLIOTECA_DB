import sqlite3

# Conexión a la base de datos (creará un archivo si no existe)
conn = sqlite3.connect('biblioteca.db')
cursor = conn.cursor()

# Crear tablas
cursor.execute('''
    CREATE TABLE IF NOT EXISTS USUARIO (
        idusuario INTEGER PRIMARY KEY AUTOINCREMENT,
        dni TEXT NOT NULL,
        nombre TEXT NOT NULL,
        apellido TEXT NOT NULL,
        contraseña TEXT NOT NULL,
        direccion TEXT NOT NULL,
        celular TEXT NOT NULL,
        roles INTEGER NOT NULL,
        autores_idautor INTEGER,
        libros_autores_libros_idlibros INTEGER,
        libros_autores_autores_idautor INTEGER
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS LIBRO (
        idlibro INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        autores TEXT NOT NULL,
        edicion TEXT NOT NULL,
        descripcion TEXT NOT NULL,
        año INTEGER NOT NULL,
        numero_paginas INTEGER NOT NULL,
        categoria_idcategoria INTEGER,
        categorias_idcategorias INTEGER,
        autores_idautor INTEGER
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS PRESTAMOS (
        idprestamo INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha_prestamo TEXT NOT NULL,
        fecha_entrega TEXT NOT NULL,
        libros_idlibros INTEGER NOT NULL,
        usuario_idusuario INTEGER NOT NULL,
        USUARIOS_idusuario INTEGER,
        LIBRO_idlibro INTEGER
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS AUTORES (
        idautor INTEGER PRIMARY KEY AUTOINCREMENT,
        nombres TEXT NOT NULL,
        apellidos TEXT NOT NULL,
        dni TEXT NOT NULL,
        modalidad TEXT NOT NULL,
        autorescol TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS LIBROS_AUTORES (
        libros_idlibros INTEGER NOT NULL,
        autores_idautor INTEGER NOT NULL,
        autores_idautor1 INTEGER NOT NULL,
        PRIMARY KEY (libros_idlibros, autores_idautor, autores_idautor1)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS CATEGORIAS (
        idcategoria INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_categoria TEXT NOT NULL,
        ubicacion TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS ROLES (
        idrol INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_rol TEXT NOT NULL
    )
''')

# Guardar los cambios y cerrar la conexión
conn.commit()
conn.close()
