import re
from functools import reduce

# Índices fijos para cada fila de la matriz
LOGIN_USERNAME, LOGIN_PASSWORD = 0, 1
AFF_NAME, AFF_CODE, AFF_AGE, AFF_TYPE, AFF_PHONE = 0, 1, 2, 3, 4
CLASS_CODE, CLASS_NAME, CLASS_LEVEL, CLASS_CAPACITY = 0, 1, 2, 3
ENR_CODE, ENR_AFFILIATE_CODE, ENR_CLASS_CODE, ENR_ATTENDANCE, ENR_STATUS = 0, 1, 2, 3, 4

# Estructuras matriciales
login_users = [
    ["admin", "admin1234"],
    ["recepcion1", "recep123"],
    ["recepcion2", "recep456"],
    ["profeyoga", "yoga2026"],
    ["profebox", "boxeo2026"],
    ["profezumba", "zumba2026"],
    ["coordinador", "coord123"],
    ["ventas1", "ventas123"],
    ["ventas2", "ventas456"],
    ["consulta", "consulta123"]
]

affiliates = [
    ["Juan Perez", 101, 28, 1, "11-2587-8779"],
    ["Maria Juana", 102, 32, 3, "11-3456-1028"],
    ["Rodriguez Pol", 103, 69, 2, "11-4678-2193"],
    ["Tambussi Fer", 104, 18, 1, "11-5789-3046"],
    ["Alejandro Esteban", 105, 65, 2, "11-6890-4175"],
    ["Sofia Diaz", 106, 22, 1, "11-7123-5684"],
    ["Camila Torres", 107, 45, 1, "11-8234-6795"],
    ["Joaquin parros", 108, 37, 1, "11-9345-7806"],
    ["Maria Anjoli", 109, 27, 3, "11-1467-8920"],
    ["Mateo retil", 110, 22, 3, "11-2578-9031"],
    ["Lucas Gomez", 111, 19, 2, "11-3689-0142"],
    ["julio", 112, 32, 3, "11-4790-1253"]
]

classes = [
    [201, "Yoga", 1, 15],
    [202, "Crossfit", 3, 10],
    [203, "Boxeo", 2, 15],
    [204, "Pilates", 1, 15],
    [205, "Musculacion", 2, 10],
    [206, "Spinning", 2, 12],
    [207, "Funcional", 3, 14],
    [208, "Zumba", 1, 20],
    [209, "Natacion", 2, 16],
    [210, "Stretching", 1, 18]
]

enrollments = [
    [301, 101, 205, 8, 1],
    [302, 102, 204, 3, 1],
    [303, 103, 201, 10, 2],
    [304, 104, 201, 2, 1],
    [305, 105, 201, 7, 1],
    [306, 106, 203, 10, 2],
    [307, 107, 203, 10, 2],
    [308, 108, 203, 10, 2],
    [309, 109, 205, 8, 1],
    [310, 110, 204, 5, 1],
    [311, 111, 201, 9, 1]
]


#Funciones de matrices
# Genera una matriz de cantidad de afiliados por clase
def affiliates_by_class_matrix():
    matrix = [[] for _ in range(len(classes))]
    for i in range(len(enrollments)):
        affilate_code = enrollments[i][ENR_AFFILIATE_CODE]
        class_code = enrollments[i][ENR_CLASS_CODE]
        class_pos = search_class_position(class_code)
        if class_pos != -1:
            matrix[class_pos].append(affilate_code)
    return matrix
    
def affiliates_by_class():
    print("AFILIADOS POR CLASE")
    matrix = affiliates_by_class_matrix()
    for i in range(len(classes)):
        print(f"Clase: {classes[i][CLASS_NAME]} - Afiliados: {len(matrix[i])}")

# Genera una matriz con las asistencias agrupadas por clase
def attendances_by_class_matrix():
    matrix = [[] for _ in range(len(classes))]
    for i in range(len(enrollments)):
        class_code = enrollments[i][ENR_CLASS_CODE]
        class_pos = search_class_position(class_code)
        if class_pos != -1:
            matrix[class_pos].append(enrollments[i][ENR_ATTENDANCE])
    return matrix

def total_attendances_by_class():
    print("TOTAL DE ASISTENCIAS POR CLASE")
    matrix = attendances_by_class_matrix()
    totals = list(map(lambda class_attendances: reduce(lambda accumulated, attendance: accumulated + attendance, class_attendances, 0), matrix))
    for i in range(len(matrix)):
        print(f"Clase: {classes[i][CLASS_NAME]} - Total de asistencias: {totals[i]}")

# generar una matriz por inscripcion por nivel de clase
def enrollment_by_class_level_matrix():
    matrix = [[] for _ in range(3)]
    for i in range(len(enrollments)):
        class_code = enrollments[i][ENR_CLASS_CODE]
        class_pos = search_class_position(class_code)
        if class_pos == -1:
            continue
        level = classes[class_pos][CLASS_LEVEL]
        if 1 <= level <= 3:
            matrix[level - 1].append(enrollments[i][ENR_CODE])
    print("INSCRIPCIONES POR NIVEL DE CLASE")
    for i in range(len(matrix)):
        print(f"Nivel {i + 1}: {len(matrix[i])} inscripciones")

#generar una matriz por cantidad de socios por tipo de socio y clase
def affiliates_by_type_and_class_matrix():
    matrix = [[[] for _ in range(len(classes))] for _ in range(3)]
    for i in range(len(enrollments)):
        affiliate_code = enrollments[i][ENR_AFFILIATE_CODE]
        class_code = enrollments[i][ENR_CLASS_CODE]
        affiliate_pos = search_affiliate_position(affiliate_code)
        class_pos = search_class_position(class_code)
        if affiliate_pos == -1 or class_pos == -1:
            continue
        affiliate_type = affiliates[affiliate_pos][AFF_TYPE]
        if 1 <= affiliate_type <= 3:
            matrix[affiliate_type - 1][class_pos].append(affiliate_code)
    print("AFILIADOS POR TIPO Y CLASE")
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            print(f"Socio {get_type_name(i + 1)} - Clase {classes[j][CLASS_NAME]}: {len(matrix[i][j])} afiliados")

#Funciones de Busqueda
#Funcion de busqueda Binaria
def buscar_clase_binaria():
    print("BÚSQUEDA BINARIA DE CLASE POR CÓDIGO")
    codigo = pedir_entero("Ingrese el código de la clase a buscar: ", "Código inválido, ingrese un número.")

    codigos = [row[CLASS_CODE] for row in classes]
    nombres = [row[CLASS_NAME] for row in classes]
    niveles = [row[CLASS_LEVEL] for row in classes]
    capacidades = [row[CLASS_CAPACITY] for row in classes]

    n = len(codigos)
    for i in range(1, n):
        clave_codigo = codigos[i]
        clave_nombre = nombres[i]
        clave_nivel = niveles[i]
        clave_capacidad = capacidades[i]
        j = i - 1
        while j >= 0 and codigos[j] > clave_codigo:
            codigos[j + 1] = codigos[j]
            nombres[j + 1] = nombres[j]
            niveles[j + 1] = niveles[j]
            capacidades[j + 1] = capacidades[j]
            j -= 1
        codigos[j + 1] = clave_codigo
        nombres[j + 1] = clave_nombre
        niveles[j + 1] = clave_nivel
        capacidades[j + 1] = clave_capacidad

    inicio = 0
    fin = n - 1
    posicion = -1

    while inicio <= fin:
        medio = (inicio + fin) // 2
        if codigos[medio] == codigo:
            posicion = medio
            inicio = fin + 1
        elif codigos[medio] < codigo:
            inicio = medio + 1
        else:
            fin = medio - 1

    if posicion == -1:
        print("Clase no encontrada.")
    else:
        print(f"Clase encontrada:")
        print(f"Código: {codigos[posicion]}, Nombre: {nombres[posicion]}, Nivel: {niveles[posicion]}, Cupos disponibles: {capacidades[posicion]}")

#Funcion de busqueda 2
def buscar_socio_secuencial():
    print("BÚSQUEDA SECUENCIAL DE SOCIO POR CÓDIGO")
    codigo = pedir_entero("Ingrese el código del socio a buscar: ", "Código inválido, ingrese un número.")

    posicion = -1
    for i in range(len(affiliates)):
        if affiliates[i][AFF_CODE] == codigo:
            posicion = i

    if posicion == -1:
        print("Socio no encontrado.")
    else:
        print(f"Socio encontrado en posición {posicion}:")
        print(f"Código: {affiliates[posicion][AFF_CODE]}, Nombre: {affiliates[posicion][AFF_NAME]}, Edad: {affiliates[posicion][AFF_AGE]}, Tipo: {get_type_name(affiliates[posicion][AFF_TYPE])}")

#Funciones de Ordenamiento
#Funcion para ordenar socios por edad usando el método de selección
def ordenar_socios_por_edad():
    afiliados_ordenados = [fila[:] for fila in affiliates]
    n = len(afiliados_ordenados)
    for i in range(n - 1):
        pos_min = i
        for j in range(i + 1, n):
            if afiliados_ordenados[j][AFF_AGE] < afiliados_ordenados[pos_min][AFF_AGE]:
                pos_min = j
        afiliados_ordenados[i], afiliados_ordenados[pos_min] = afiliados_ordenados[pos_min], afiliados_ordenados[i]

    print("SOCIOS ORDENADOS POR EDAD (Selección)")
    for row in afiliados_ordenados:
        print(f"Código: {row[AFF_CODE]}, Nombre: {row[AFF_NAME]}, Edad: {row[AFF_AGE]}, Tipo: {get_type_name(row[AFF_TYPE])}")

#Funcion para ordenar clases por nivel usando el método de inserción
def ordenar_clases_por_nivel():
    clases_ordenadas = [fila[:] for fila in classes]
    n = len(clases_ordenadas)
    for i in range(1, n):
        clave_nivel = clases_ordenadas[i][CLASS_LEVEL]
        clave_fila = clases_ordenadas[i][:]
        j = i - 1
        while j >= 0 and clases_ordenadas[j][CLASS_LEVEL] > clave_nivel:
            clases_ordenadas[j + 1] = clases_ordenadas[j][:]
            j -= 1
        clases_ordenadas[j + 1] = clave_fila

    print("CLASES ORDENADAS POR NIVEL (Inserción)")
    for row in clases_ordenadas:
        print(f"Código: {row[CLASS_CODE]}, Nombre: {row[CLASS_NAME]}, Nivel: {row[CLASS_LEVEL]}, Cupos disponibles: {row[CLASS_CAPACITY]}")

#Función para ordenar inscripciones por asistencias usando el método de burbujeo
def ordenar_inscripciones_por_asistencias():
    inscripciones_ordenadas = [fila[:] for fila in enrollments]
    n = len(inscripciones_ordenadas)
    for i in range(n - 1):
        for j in range(0, n - 1 - i):
            if inscripciones_ordenadas[j][ENR_ATTENDANCE] > inscripciones_ordenadas[j + 1][ENR_ATTENDANCE]:
                inscripciones_ordenadas[j], inscripciones_ordenadas[j + 1] = inscripciones_ordenadas[j + 1], inscripciones_ordenadas[j]

    print("INSCRIPCIONES ORDENADAS POR ASISTENCIAS (Burbujeo)")
    for row in inscripciones_ordenadas:
        print(f"Código: {row[ENR_CODE]}, Socio: {row[ENR_AFFILIATE_CODE]}, Clase: {row[ENR_CLASS_CODE]}, Asistencias: {row[ENR_ATTENDANCE]}, Estado: {row[ENR_STATUS]}")

#Funciones de validacion entero,flotante, string
#Funcion para Entero
def es_entero(valor):
    try:
        valor = int(valor)
        res = True
    except:
        res = False
    return res

#Funcion para Flotante
def es_flotante(valor):
    try:
        valor = float(valor)
        res = True
    except:
        res = False
    return res

#Funcion para String
def es_string(valor):
    try:
        valor = str(valor)
        res = True
    except:
        res = False
    return res

def es_nombre_clase_valido(nombre):
    return re.match(r"^[A-Za-z]+$", nombre)

def pedir_entero(mensaje, mensaje_error="El dato ingresado debe ser numérico.", minimo=None, maximo=None):
    valor = input(mensaje)
    while not es_entero(valor) or (minimo is not None and int(valor) < minimo) or (maximo is not None and int(valor) > maximo):
        print(mensaje_error)
        valor = input(mensaje)
    return int(valor)

#Funcion para obtener el nombre del nivel de clase a partir del codigo
def get_level_name(level_code):
    if level_code == 1:
        return "Principiante"
    elif level_code == 2:
        return "Intermedio"
    elif level_code == 3:
        return "Avanzado"
    else:
        return "Desconocido"

#Funcion para buscar la posicion de una clase por su codigo, devuelve -1 si no se encuentra

def search_class_position(code):
    position = -1
    for i in range(len(classes)):
        if classes[i][CLASS_CODE] == code:
            position = i
    return position

#Funcion de busqueda de usuario para login
def search_user_position(username):
    position = -1
    for i in range(len(login_users)):
        if re.fullmatch(login_users[i][LOGIN_USERNAME], username, re.IGNORECASE):
            position = i
    return position

#Funcion de login De 3 intentos
def login():
    attempts = 1
    max_attempts = 3

    input_user = input("ingrese su nombre de usuario: ")
    input_passw = input("ingrese su contraseña: ")
    user_position = search_user_position(input_user)

    while (user_position == -1 or login_users[user_position][LOGIN_PASSWORD] != input_passw) and attempts < max_attempts:
        print("El nombre de usuario o la contraseña son incorrectos, por favor vuelva a intentarlo.")
        input_user = input("ingrese su nombre de usuario: ")
        input_passw = input("ingrese su contraseña: ")
        user_position = search_user_position(input_user)
        attempts += 1

    if user_position == -1 or login_users[user_position][LOGIN_PASSWORD] != input_passw:
        print("Has superado el número de intentos permitidos. Acceso bloqueado.")
        return False
    else:
        print("¡Bienvenido al sistema de gestión del gimnasio!")
        return True

#Funcion para mostrar el menu de opciones y validar la opcion ingresada
def input_option():
    print("Opcion 1: sumar afiliado")
    print("Opcion 2: eliminar afiliado")
    print("Opcion 3: modificar afiliado")
    print("Opcion 4: listar afiliados")
    print("Opcion 0: salir")

    option = pedir_entero("Ingrese una opcion: ", "El dato ingresado es erroneo, por favor ingrese una opcion valida.", 0, 4)

    while option < 0 or option > 4:
        print("El dato ingresado es erroneo, por favor ingrese una opcion valida.")

        print("Opcion 1: sumar afiliado")
        print("Opcion 2: eliminar afiliado")
        print("Opcion 3: modificar afiliado")
        print("Opcion 4: listar afiliados")
        print("Opcion 0: salir")

        option = pedir_entero("Ingrese una opcion: ", "El dato ingresado es erroneo, por favor ingrese una opcion valida.", 0, 4)

    return option

#Funcion para sumar afiliados, validando edad y tipo de afiliado
def sumar_afiliados():
    print("SUMAR AFILIADO")
    nombre = input("Nombre completo: ")

    edad = input("Ingrese su edad: ")
    while not es_entero(edad) or int(edad) < 0 or int(edad) > 100:
        print("ERROR, se debe ingresar una edad entre 0 y 100")
        edad = input("Vuelva a ingresar su edad: ")

    affiliate_type = input("Ingrese su tipo (1-Mensual, 2-Libre, 3-Premium): ")
    while not es_entero(affiliate_type) or int(affiliate_type) < 1 or int(affiliate_type) > 3:
        print("ERROR, se debe ingresar un codigo entre 1 y 3")
        affiliate_type = input("Vuelva a ingresar su tipo (1-Mensual, 2-Libre, 3-Premium): ")

    codigo = 101
    if len(affiliates) > 0:
        codigo = affiliates[-1][AFF_CODE] + 1

    affiliates.append([nombre, codigo, int(edad), int(affiliate_type)])

    print(f"Socio '{nombre}' agregado con código {codigo}.")

#Funcion para eliminar afiliados, validando que el codigo exista y confirmando la eliminacion
def eliminar_afiliados():
    print("BAJAR AFILIADO")
    codigo = pedir_entero("Ingrese el código del socio a eliminar: ", "Código inválido, ingrese un número.")
    pos = search_affiliate_position(codigo)
    if pos == -1:
        print("Socio no encontrado.")
    else:
        print(f"¿Seguro que desea eliminar a '{affiliates[pos][AFF_NAME]}'? (s/n)")
        confirm = input()
        if confirm.lower() == "s":
            inscripciones_eliminadas = remove_enrollments_by_affiliate(codigo)
            affiliates.pop(pos)
            print("Socio eliminado.")
            if inscripciones_eliminadas > 0:
                print(f"Se eliminaron {inscripciones_eliminadas} inscripciones asociadas.")
        else:
            print("Operación cancelada.")

#Funcion para obtener el nombre del tipo de afiliado a partir del codigo
def get_type_name(type_code):
    if type_code == 1:
        return "Mensual"
    elif type_code == 2:
        return "Libre"
    elif type_code == 3:
        return "Premium"
    else:
        return "Desconocido"

#Funcion para buscar la posicion de un afiliado por su codigo, devuelve -1 si no se encuentra
def search_affiliate_position(code):
    position = -1
    for i in range(len(affiliates)):
        if affiliates[i][AFF_CODE] == code:
            position = i
    return position


def remove_enrollment_at(position):
    enrollments.pop(position)


def remove_enrollments_by_affiliate(affiliate_code):
    deleted_count = 0
    for i in range(len(enrollments) - 1, -1, -1):
        if enrollments[i][ENR_AFFILIATE_CODE] == affiliate_code:
            remove_enrollment_at(i)
            deleted_count += 1
    return deleted_count


def remove_enrollments_by_class(class_code):
    deleted_count = 0
    for i in range(len(enrollments) - 1, -1, -1):
        if enrollments[i][ENR_CLASS_CODE] == class_code:
            remove_enrollment_at(i)
            deleted_count += 1
    return deleted_count

#Funcion para modificar afiliados, validando que el codigo exista y permitiendo modificar nombre, edad y tipo de afiliado
def modify_affiliate():
    print("MODIFICAR AFILIADO")
    codigo = pedir_entero("Ingrese el código del socio a modificar: ", "Código inválido, ingrese un número.")
    pos = search_affiliate_position(codigo)
    if pos == -1:
        print("Socio no encontrado.")
    else:
        print(f"Socio actual: {affiliates[pos][AFF_NAME]}, {affiliates[pos][AFF_AGE]} años, {get_type_name(affiliates[pos][AFF_TYPE])}")
        nombre = input(f"Nuevo nombre (si para mantener '{affiliates[pos][AFF_NAME]}'): ")
        if nombre != "si":
            affiliates[pos][AFF_NAME] = nombre
        edad = input(f"Nueva edad (si para mantener {affiliates[pos][AFF_AGE]}): ")
        if edad != "si":
            while not es_entero(edad) or int(edad) < 0 or int(edad) > 100:
                print("ERROR, se debe ingresar una edad entre 0 y 100")
                edad = input("Nueva edad: ")
            affiliates[pos][AFF_AGE] = int(edad)
        print("Tipos: 1-Mensual  2-Libre  3-Premium")
        type_code = input(f"Nuevo tipo (si para mantener {affiliates[pos][AFF_TYPE]}): ")
        if type_code != "si":
            while not es_entero(type_code) or int(type_code) < 1 or int(type_code) > 3:
                print("ERROR, se debe ingresar un codigo entre 1 y 3")
                type_code = input("Nuevo tipo: ")
            affiliates[pos][AFF_TYPE] = int(type_code)
        print(f"Socio modificado: {affiliates[pos][AFF_NAME]}, {affiliates[pos][AFF_AGE]} años, {get_type_name(affiliates[pos][AFF_TYPE])}")

#Funcion para listar afiliados, mostrando codigo, nombre, edad y tipo de afiliado
def list_affiliates():
    print("LISTA DE AFILIADOS")
    for i in range(len(affiliates)):
        print(f"Código: {affiliates[i][AFF_CODE]}, Nombre: {affiliates[i][AFF_NAME]}, Edad: {affiliates[i][AFF_AGE]}, Tipo: {get_type_name(affiliates[i][AFF_TYPE])}")

#Funcion para sumar clases, validando nivel y capacidad, y asignando un codigo automaticamente
def sumar_clase():
    print("\nSUMAR CLASE")
    nombre = input("Nombre de la clase: ").strip()
    while not es_nombre_clase_valido(nombre):
        print("ERROR, ingrese una o más palabras formadas solamente por letras")
        nombre = input("Nombre de la clase: ").strip()

    nivel = input("Nivel (1-Principiante, 2-Intermedio, 3-Avanzado): ")
    while not es_entero(nivel) or int(nivel) < 1 or int(nivel) > 3:
        print("ERROR, ingresar nivel entre 1 y 3")
        nivel = input("Nivel (1-Principiante, 2-Intermedio, 3-Avanzado): ")
    nivel = int(nivel)

    capacidad = input("Cupos disponibles: ")
    while not es_entero(capacidad) or int(capacidad) < 1:
        print("ERROR, ingresar un número mayor a 0")
        capacidad = input("Cupos disponibles: ")
    capacidad = int(capacidad)

    codigo = 201 if len(classes) == 0 else classes[-1][CLASS_CODE] + 1
    classes.append([codigo, nombre, nivel, capacidad])

    print(f"Clase '{nombre}' agregada con código {codigo}.")

#Funcion para eliminar clases, validando que el codigo exista y confirmando la eliminacion
def eliminar_clase():
    print("\nELIMINAR CLASE")
    codigo = input("Ingrese el código de la clase a eliminar: ")
    if not es_entero(codigo):
        print("Código inválido.")
        return
    pos = search_class_position(int(codigo))
    if pos == -1:
        print("Clase no encontrada.")
    else:
        confirm = input(f"¿Seguro que desea eliminar la clase '{classes[pos][CLASS_NAME]}'? (s/n): ")
        if confirm.lower() == "s":
            class_code = classes[pos][CLASS_CODE]
            inscripciones_eliminadas = remove_enrollments_by_class(class_code)
            classes.pop(pos)
            print("Clase eliminada.")
            if inscripciones_eliminadas > 0:
                print(f"Se eliminaron {inscripciones_eliminadas} inscripciones asociadas.")
        else:
            print("Operación cancelada.")

#Funcion para modificar clases
def modify_clase():
    print("MODIFICAR CLASE")
    codigo = input("Ingrese el código de la clase a modificar: ")
    if not es_entero(codigo):
        print("Código inválido.")
        return
    pos = search_class_position(int(codigo))
    if pos == -1:
        print("Clase no encontrada.")
    else:
        print(f"Clase actual: {classes[pos][CLASS_NAME]}, Nivel: {get_level_name(classes[pos][CLASS_LEVEL])}, Cupos disponibles: {classes[pos][CLASS_CAPACITY]}")
        nombre = input(f"Nuevo nombre (si para mantener '{classes[pos][CLASS_NAME]}'): ").strip()
        if nombre != "si":
            while not es_nombre_clase_valido(nombre):
                print("ERROR, ingrese una o más palabras formadas solamente por letras")
                nombre = input("Nuevo nombre: ").strip()
            classes[pos][CLASS_NAME] = nombre
        nivel = input(f"Nuevo nivel -1-Principiante 2-Intermedio 3-Avanzado- (si para mantener {get_level_name(classes[pos][CLASS_LEVEL])}): ")
        if nivel != "si":
            while not es_entero(nivel) or int(nivel) < 1 or int(nivel) > 3:
                print("ERROR, nivel entre 1 y 3")
                nivel = input("Nuevo nivel: ")
            classes[pos][CLASS_LEVEL] = int(nivel)
        capacidad = input(f"Nuevos cupos disponibles (si para mantener {classes[pos][CLASS_CAPACITY]}): ")
        if capacidad != "si":
            while not es_entero(capacidad) or int(capacidad) < 1:
                print("ERROR, ingresar un número mayor a 0")
                capacidad = input("Nuevos cupos disponibles: ")
            classes[pos][CLASS_CAPACITY] = int(capacidad)
        print(f"Clase modificada: {classes[pos][CLASS_NAME]}, Nivel: {get_level_name(classes[pos][CLASS_LEVEL])}, Cupos disponibles: {classes[pos][CLASS_CAPACITY]}")

#Funcion listar clases, mostrando codigo, nombre, nivel y capacidad
def list_clases():
    print("LISTA DE CLASES")
    print(f"{'Código':<10} {'Nombre':<20} {'Nivel':<18} {'Cupos disponibles'}")
    print("-" * 58)
    for i in range(len(classes)):
        print(f"{classes[i][CLASS_CODE]:<10} {classes[i][CLASS_NAME]:<20} {get_level_name(classes[i][CLASS_LEVEL]):<18} {classes[i][CLASS_CAPACITY]}")

def does_class_code_exist(code):
    for row in classes:
        if row[CLASS_CODE] == code:
            return True
    return False

def does_affiliate_code_exist(code):
    for row in affiliates:
        if row[AFF_CODE] == code:
            return True
    return False

#Funcion para dar de alta una inscripcion
def alta_inscripcion():
    list_clases()
    class_code = pedir_entero("Ingrese el código de la clase a la que desea inscribirse: ", "por favor ingrese un código válido.")
    while not does_class_code_exist(class_code):
        print("por favor ingrese un código válido.")
        class_code = pedir_entero("Ingrese el código de la clase a la que desea inscribirse: ", "por favor ingrese un código válido.")
    class_pos = search_class_position(class_code)
    if classes[class_pos][CLASS_CAPACITY] <= 0:
        print("No hay cupos disponibles para esa clase.")
        return
    list_affiliates()
    affiliate_code = pedir_entero("Ingrese su código de afiliado: ", "por favor ingrese un código de afiliado válido.")
    while not does_affiliate_code_exist(affiliate_code):
        print("por favor ingrese un código de afiliado válido.")
        affiliate_code = pedir_entero("Ingrese su código de afiliado: ", "por favor ingrese un código de afiliado válido.")

    codigo = 301 if len(enrollments) == 0 else enrollments[-1][ENR_CODE] + 1
    enrollments.append([codigo, int(affiliate_code), int(class_code), 0, 1])
    classes[class_pos][CLASS_CAPACITY] -= 1

#Funcion para listar inscripciones
def list_inscripciones():
    print("LISTA DE INSCRIPCIONES")
    print(f"{'Código':<10} {'Socio':<20} {'Clase':<20} {'Asistencias':<12} {'Estado'}")
    print("-" * 80)
    for i in range(len(enrollments)):
        affiliate_pos = search_affiliate_position(enrollments[i][ENR_AFFILIATE_CODE])
        class_pos = search_class_position(enrollments[i][ENR_CLASS_CODE])
        affiliate_name = affiliates[affiliate_pos][AFF_NAME] if affiliate_pos != -1 else "Socio inexistente"
        class_name = classes[class_pos][CLASS_NAME] if class_pos != -1 else "Clase inexistente"
        print(f"{enrollments[i][ENR_CODE]:<10} {affiliate_name:<20} {class_name:<20} {enrollments[i][ENR_ATTENDANCE]:<12} {'Activa' if enrollments[i][ENR_STATUS] == 1 else 'Inactiva'}")

##Funcionm para listar clases de un socio
def clases_de_socio(affiliate_code): 
    """
    Obtiene la lista de las clases activas en las que se encuentra inscripto un socio.
    Parámetros:
        affiliate_code (int): Código de identificación del socio.
    Retorna:
        list[str]: Lista con los nombres de las clases activas a las que asiste el socio.
    """

    posiciones = list(filter(
        lambda i: enrollments[i][ENR_AFFILIATE_CODE] == affiliate_code and enrollments[i][ENR_STATUS] == 1,
        range(len(enrollments))
    ))
    nombre_clases = list(map(
        lambda i: classes[search_class_position(enrollments[i][ENR_CLASS_CODE])][CLASS_NAME],
        posiciones
    ))
    return nombre_clases

def listar_clases_socio():
    """
    Muestra las clases activas de un socio específico.
    Solicita por consola el código del socio, verifica su existencia en la lista
    de afiliados e imprime la lista de sus clases activas o un mensaje si no posee ninguna.
    Parámetros:
        No recibe parámetros (interactúa con el usuario para obtener el código del socio).
    """
    print("Clases de un socio")
    codigo = pedir_entero("Ingrese el codigo del socio: ","Codigo invalido, ingresar un numero")
    pos = search_affiliate_position(codigo)
    if pos == -1:
        print("Error,socio no encontrado")
        return
    clases = clases_de_socio(codigo)
    if not clases:
        print("El socio no tiene clases activas")
    else:
        print(f"El socio {affiliates[pos][AFF_NAME]} tiene las clases: {', '.join(clases)}")

#Funcion opciones de clases, mostrando el menu y validando la opcion ingresada
def input_clases_option():
    print("--- GESTIÓN DE CLASES ---")
    print("Opcion 1: Sumar clase")
    print("Opcion 2: Eliminar clase")
    print("Opcion 3: Modificar clase")
    print("Opcion 4: Listar clases")
    print("Opcion 0: Volver al menu principal")
    raw_option = input("Ingrese una opción: ")
    while not es_entero(raw_option) or int(raw_option) < 0 or int(raw_option) > 4:
        print("La opción ingresada es errónea, por favor ingrese una opción válida.")
        print("Opcion 1: Sumar clase")
        print("Opcion 2: Eliminar clase")
        print("Opcion 3: Modificar clase")
        print("Opcion 4: Listar clases")
        print("Opcion 0: Volver al menu principal")
        raw_option = input("Ingrese una opción: ")
    option = int(raw_option)
    return option

#Funcion menu de clases, mostrando el menu de opciones y ejecutando la opcion seleccionada hasta que se elija volver al menu principal
def clases_menu():
    option = input_clases_option()
    while option != 0:
        if option == 1:
            sumar_clase()
        elif option == 2:
            eliminar_clase()
        elif option == 3:
            modify_clase()
        elif option == 4:
            list_clases()
        option = input_clases_option()

#Funcion opciones de afiliados, mostrando el menu y validando la opcion ingresada
def input_affiliate_option():
    print("--- GESTIÓN DE AFILIADOS ---")
    print("Opcion 1: sumar afiliado")
    print("Opcion 2: eliminar afiliado")
    print("Opcion 3: modificar afiliado")
    print("Opcion 4: listar afiliados")
    print("Opcion 0: Volver al menu principal")

    raw_option = input("Ingrese una opción: ")

    while not es_entero(raw_option) or int(raw_option) < 0 or int(raw_option) > 4:
        print("La opción ingresada es errónea, por favor ingrese una opción válida.")

        print("Opcion 1: sumar afiliado")
        print("Opcion 2: eliminar afiliado")
        print("Opcion 3: modificar afiliado")
        print("Opcion 4: listar afiliados")
        print("Opcion 0: Volver al menu principal")

        raw_option = input("Ingrese una opción: ")
    option = int(raw_option)
    return option

#Funcion menu de afiliados, mostrando el menu de opciones y ejecutando la opcion seleccionada hasta que se elija volver al menu principal
def affiliate_menu():
    option = input_affiliate_option()
    while option != 0:
        if option == 1:
            sumar_afiliados()
        elif option == 2:
            eliminar_afiliados()
        elif option == 3:
            modify_affiliate()
        elif option == 4:
            list_affiliates()
        option = input_affiliate_option()

#Funcion opciones de inscripciones, mostrando el menu y validando la opcion ingresada
def input_inscription_option():
    print("--- GESTIÓN DE INSCRIPCIONES ---")
    print("Opcion 1: Alta inscripción")
    print("Opcion 2: Baja inscripción")
    print("Opcion 3: Modificar inscripción")
    print("Opcion 4: Listar inscripciones")
    print("Opcion 5: Listar clases de un socio") ## Agrego nueva funcion que llama a la funcion clases_de_socio para listar clases por socio
    print("Opcion 0: Volver al menu principal")
    raw_option = input("Ingrese una opción: ")
    while not es_entero(raw_option) or int(raw_option) < 0 or int(raw_option) > 5:
        print("La opción ingresada es errónea, por favor ingrese una opción válida.")
        print("Opcion 1: Alta inscripción")
        print("Opcion 2: Baja inscripción")
        print("Opcion 3: Modificar inscripción")
        print("Opcion 4: Listar inscripciones")
        print("Opcion 5: Listar clases de un socio")
        print("Opcion 0: Volver al menu principal")
        raw_option = input("Ingrese una opción: ")
    option = int(raw_option)
    return option

#Funcion para dar de baja una inscripcion, validando que el codigo de inscripcion exista y confirmando la baja
def baja_inscripcion():
    print("BAJA DE INSCRIPCIÓN")
    codigo = pedir_entero("Ingrese el código de la inscripción a dar de baja: ", "Código inválido, ingrese un número.")
    pos = search_inscription_position(codigo)
    if pos == -1:
        print("Inscripción no encontrada.")
    elif enrollments[pos][ENR_STATUS] == 2:
        print("La inscripción ya estaba finalizada.")
    else:
        affiliate_pos = search_affiliate_position(enrollments[pos][ENR_AFFILIATE_CODE])
        class_pos = search_class_position(enrollments[pos][ENR_CLASS_CODE])
        affiliate_name = affiliates[affiliate_pos][AFF_NAME] if affiliate_pos != -1 else "Socio inexistente"
        class_name = classes[class_pos][CLASS_NAME] if class_pos != -1 else "Clase inexistente"
        confirm = input(f"¿Seguro que desea dar de baja la inscripción del socio '{affiliate_name}' en la clase '{class_name}' ? (s/n): ")
        if confirm.lower() == "s":
            enrollments[pos][ENR_STATUS] = 2
            if class_pos != -1:
                classes[class_pos][CLASS_CAPACITY] += 1
            print("Inscripción dada de baja.")
        else:
            print("Operación cancelada.")

#Funcion para buscar la posicion de una inscripcion por su codigo, devuelve -1 si no se encuentra
def search_inscription_position(code):
    position = -1
    for i in range(len(enrollments)):
        if enrollments[i][ENR_CODE] == code:
            position = i
    return position
#Funcion para modificar una inscripcion
def modify_inscripcion():
    print("MODIFICAR INSCRIPCIÓN")
    codigo = pedir_entero("Ingrese el código de la inscripción a modificar: ", "Código inválido, ingrese un número.")
    pos = search_inscription_position(codigo)
    if pos == -1:
        print("Inscripción no encontrada.")
    else:
        estado_anterior = enrollments[pos][ENR_STATUS]
        class_pos = search_class_position(enrollments[pos][ENR_CLASS_CODE])
        affiliate_pos = search_affiliate_position(enrollments[pos][ENR_AFFILIATE_CODE])
        affiliate_name = affiliates[affiliate_pos][AFF_NAME] if affiliate_pos != -1 else "Socio inexistente"
        class_name = classes[class_pos][CLASS_NAME] if class_pos != -1 else "Clase inexistente"
        print(f"Inscripción actual: Socio '{affiliate_name}', Clase '{class_name}', Asistencias: {enrollments[pos][ENR_ATTENDANCE]}, Estado: {'Activa' if enrollments[pos][ENR_STATUS] == 1 else 'Inactiva'}")
        asistencias = input(f"Nuevas asistencias (si para mantener {enrollments[pos][ENR_ATTENDANCE]}): ")
        if asistencias != "si":
            while not es_entero(asistencias) or int(asistencias) < 0:
                print("ERROR, las asistencias deben ser un número mayor o igual a 0")
                asistencias = input("Nuevas asistencias: ")
            enrollments[pos][ENR_ATTENDANCE] = int(asistencias)
        estado = input(f"Nuevo estado -1-Activa 2-Inactiva- (si para mantener {'Activa' if enrollments[pos][ENR_STATUS] == 1 else 'Inactiva'}): ")
        if estado != "si":
            while not es_entero(estado) or int(estado) < 1 or int(estado) > 2:
                print("ERROR, estado entre 1 y 2")
                estado = input("Nuevo estado: ")
            nuevo_estado = int(estado)
            if estado_anterior == 1 and nuevo_estado == 2:
                enrollments[pos][ENR_STATUS] = nuevo_estado
                if class_pos != -1:
                    classes[class_pos][CLASS_CAPACITY] += 1
            elif estado_anterior == 2 and nuevo_estado == 1:
                if class_pos == -1:
                    print("No se puede activar porque la clase no existe.")
                elif classes[class_pos][CLASS_CAPACITY] <= 0:
                    print("No hay cupos disponibles para activar esta inscripción.")
                else:
                    enrollments[pos][ENR_STATUS] = nuevo_estado
                    classes[class_pos][CLASS_CAPACITY] -= 1
            else:
                enrollments[pos][ENR_STATUS] = nuevo_estado
        affiliate_pos = search_affiliate_position(enrollments[pos][ENR_AFFILIATE_CODE])
        class_pos = search_class_position(enrollments[pos][ENR_CLASS_CODE])
        affiliate_name = affiliates[affiliate_pos][AFF_NAME] if affiliate_pos != -1 else "Socio inexistente"
        class_name = classes[class_pos][CLASS_NAME] if class_pos != -1 else "Clase inexistente"
        print(f"Inscripción modificada: Socio '{affiliate_name}', Clase '{class_name}', Asistencias: {enrollments[pos][ENR_ATTENDANCE]}, Estado: {'Activa' if enrollments[pos][ENR_STATUS] == 1 else 'Inactiva'}")
#Funcion de menu de inscripciones
def inscription_menu():
    option = input_inscription_option()
    while option != 0:
        if option == 1:
            alta_inscripcion()
        elif option == 2:
            baja_inscripcion()
        elif option == 3:
            modify_inscripcion()
        elif option == 4:
            list_inscripciones()
        elif option == 5: 
            listar_clases_socio()
        option = input_inscription_option()

# Implementacion de Busquedas
# En la consigna pone aplicarse sobre datos numericos, por lo que la busqueda se aplicara en los codigos de clase
# Funcion de menu de busqueda
def menu_busqueda():
    print("--- MENÚ DE BÚSQUEDA ---")
    print("Opción 1: Buscar clase por código (Binaria)")
    print("Opción 2: Buscar socio por código (Secuencial)")
    print("Opción 0: Volver al menú principal")
    raw_option = input("Ingrese una opción: ")
    while not es_entero(raw_option) or int(raw_option) < 0 or int(raw_option) > 2:
        print("La opción ingresada es errónea, por favor ingrese una opción válida.")
        print("--- MENÚ DE BÚSQUEDA ---")
        print("Opción 1: Buscar clase por código (Binaria)")
        print("Opción 2: Buscar socio por código (Secuencial)")
        print("Opción 0: Volver al menú principal")
        raw_option = input("Ingrese una opción: ")
    return int(raw_option)

# Funcion de opción de busqueda, mostrando el menu de opciones de busqueda anterior
def opcion_menu_busqueda():
    option = menu_busqueda()
    while option != 0:
        if option == 1:
            buscar_clase_binaria()
        elif option == 2:
            buscar_socio_secuencial()
        option = menu_busqueda()

#Funcion de menu de ordenamiento
def menu_ordenamiento():
    print("--- MENÚ DE ORDENAMIENTO ---")
    print("Opción 1: Ordenar socios por edad (Selección)")
    print("Opción 2: Ordenar clases por nivel (Inserción)")
    print("Opción 3: Ordenar inscripciones por asistencias (Burbujeo)")
    print("Opción 0: Volver al menú principal")
    raw_option = input("Ingrese una opción: ")
    while not es_entero(raw_option) or int(raw_option) < 0 or int(raw_option) > 3:
        print("La opción ingresada es errónea, por favor ingrese una opción válida.")
        print("--- MENÚ DE ORDENAMIENTO ---")
        print("Opción 1: Ordenar socios por edad (Selección)")
        print("Opción 2: Ordenar clases por nivel (Inserción)")
        print("Opción 3: Ordenar inscripciones por asistencias (Burbujeo)")
        print("Opción 0: Volver al menú principal")
        raw_option = input("Ingrese una opción: ")
    return int(raw_option)

#Funcion de opción de ordenamiento, mostrando el menu de opciones y ejecutando la opcion seleccionada hasta que se elija volver al menu principal
def opcion_menu_ordenamiento():
    option = menu_ordenamiento()
    if option == 1:
        ordenar_socios_por_edad()
    elif option == 2:
        ordenar_clases_por_nivel()
    elif option == 3:
        ordenar_inscripciones_por_asistencias()

def input_matrix_option():
    print("--- MENÚ DE CÁLCULOS ESTADÍSTICOS MATRICIALES ---")
    print("Opción 1: Matriz de cantidad de afiliados por clase")
    print("Opción 2: Matriz de cantidad de inscripciones por nivel de clase")
    print("Opción 3: Total de asistencias por clase")
    print("Opción 4: Matriz de cantidad de afiliados por tipo y clase")
    print("Opción 0: Volver al menú principal")
    rawOption = input("Ingrese una opción: ")
    while not es_entero(rawOption) or int(rawOption) < 0 or int(rawOption) > 4:
        print("La opción ingresada es errónea, por favor ingrese una opción válida.")
        print("--- MENÚ DE CÁLCULOS ESTADÍSTICOS MATRICIALES ---")
        print("Opción 1: Matriz de cantidad de afiliados por clase")
        print("Opción 2: Matriz de cantidad de inscripciones por nivel de clase")
        print("Opción 3: Total de asistencias por clase")
        print("Opción 4: Matriz de cantidad de afiliados por tipo y clase")
        print("Opción 0: Volver al menú principal")
        rawOption = input("Ingrese una opción: ")
    return int(rawOption)

def matrix_menu():
    option = input_matrix_option()
    while option != 0:
        if option == 1:
            affiliates_by_class()
        elif option == 2:
            enrollment_by_class_level_matrix()
        elif option == 3:
            total_attendances_by_class()
        elif option == 4:
            affiliates_by_type_and_class_matrix()
        option = input_matrix_option()

#Funcion para mostrar el menu de opciones principal y validar la opcion ingresada
def input_main_option():
    print("--- MENU PRINCIPAL ---")
    print("Opción 1: Gestión de afiliados")
    print("Opción 2: Gestión de clases")
    print("Opción 3: Gestión de inscripciones")
    print("Opción 4: Ordenamiento")
    print("Opción 5: Búsqueda")
    print("Opción 6: Cálculos estadísticos matriciales")
    print("Opción 0: Salir")
    raw_option = input("Ingrese una opción: ")
    while not es_entero(raw_option) or int(raw_option) < 0 or int(raw_option) > 6:
        print("La opción ingresada es errónea, por favor ingrese una opción válida.")
        print("--- MENU PRINCIPAL ---")
        print("Opción 1: Gestión de afiliados")
        print("Opción 2: Gestión de clases")
        print("Opción 3: Gestión de inscripciones")
        print("Opción 4: Ordenamiento")
        print("Opción 5: Búsqueda")
        print("Opción 6: Cálculos estadísticos matriciales")
        print("Opción 0: Salir")
        raw_option = input("Ingrese una opción: ")
    option = int(raw_option)
    return option

#Funcion menu principal, mostrando el menu de opciones y ejecutando la opcion seleccionada hasta que se elija salir
def main_menu():
    option = input_main_option()
    while option != 0:
        if option == 1:
            affiliate_menu()
        elif option == 2:
            clases_menu()
        elif option == 3:
            inscription_menu()
        elif option == 4:
            opcion_menu_ordenamiento()
        elif option == 5:
            opcion_menu_busqueda()
        elif option == 6:
            matrix_menu()
        option = input_main_option()


# Programa principal
valid_login = login()

if valid_login:
    main_menu()
    print("¡Gracias por usar el sistema de gestión del gimnasio! Hasta luego.")
