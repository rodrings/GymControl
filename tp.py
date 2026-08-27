from functools import reduce

# Datos iniciales en listas paralelas
login_usernames = [
    "admin", "recepcion1", "recepcion2", "profeyoga", "profebox",
    "profezumba", "coordinador", "ventas1", "ventas2", "consulta"
]
login_passwords = [
    "admin1234", "recep123", "recep456", "yoga2026", "boxeo2026",
    "zumba2026", "coord123", "ventas123", "ventas456", "consulta123"
]

affiliate_names = [
    "Juan Perez", "Maria Juana", "Rodriguez Pol", "Tambussi Fer",
    "Alejandro Esteban", "Sofia Diaz", "Camila Torres", "Joaquin parros",
    "Maria Anjoli", "Mateo retil", "Lucas Gomez", "julio"
]
affiliate_codes = [101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112]
affiliate_ages = [28, 32, 69, 18, 65, 22, 45, 37, 27, 22, 19, 32]
affiliate_types = [1, 3, 2, 1, 2, 1, 1, 1, 3, 3, 2, 3]

gym_class_codes = [201, 202, 203, 204, 205, 206, 207, 208, 209, 210]
gym_class_names = [
    "Yoga", "Crossfit", "Boxeo", "Pilates", "Musculacion", "Spinning",
    "Funcional", "Zumba", "Natacion", "Stretching"
]
gym_class_levels = [1, 3, 2, 1, 2, 2, 3, 1, 2, 1]
gym_class_capacities = [15, 10, 15, 15, 10, 12, 14, 20, 16, 18]

enrollment_codes = [301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311]
enrollment_affiliate_codes = [101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111]
enrollment_gym_class_codes = [205, 204, 201, 201, 201, 203, 203, 203, 205, 204, 201]
enrollment_attendances = [8, 3, 10, 2, 7, 10, 10, 10, 8, 5, 9]
enrollment_status = [1, 1, 2, 1, 1, 2, 2, 2, 1, 1, 1]


#Funciones de matrices
# Genera una matriz de cantidad de afiliados por clase
def affiliates_by_class_matrix():
    matrix = [[] for _ in range(len(gym_class_codes))]
    for i in range(len(enrollment_codes)):
        affilateCode = enrollment_affiliate_codes[i]
        classCode = enrollment_gym_class_codes[i]
        classPos = search_class_position(classCode)
        matrix[classPos].append(affilateCode)
    return matrix
    
def affiliates_by_class():
    print("AFILIADOS POR CLASE")
    matrix = affiliates_by_class_matrix()
    for i in range(len(gym_class_codes)):
        print(f"Clase: {gym_class_names[i]} - Afiliados: {len(matrix[i])}")

# Genera una matriz con las asistencias agrupadas por clase
def attendances_by_class_matrix():
    matrix = [[] for _ in range(len(gym_class_codes))]
    for i in range(len(enrollment_codes)):
        classCode = enrollment_gym_class_codes[i]
        classPos = search_class_position(classCode)
        if classPos != -1:
            matrix[classPos].append(enrollment_attendances[i])
    return matrix

def total_attendances_by_class():
    print("TOTAL DE ASISTENCIAS POR CLASE")
    matrix = attendances_by_class_matrix()
    for i in range(len(gym_class_codes)):
        total = 0
        for j in range(len(matrix[i])):
            total += matrix[i][j]
        print(f"Clase: {gym_class_names[i]} - Total de asistencias: {total}")

# generar una matriz por inscripcion por nivel de clase
def enrollment_by_class_level_matrix():
    matrix = [[] for _ in range(3)]
    for i in range(len(enrollment_codes)):
        class_code = enrollment_gym_class_codes[i]
        class_pos = search_class_position(class_code)
        if class_pos == -1:
            continue
        level = gym_class_levels[class_pos]
        if 1 <= level <= 3:
            matrix[level - 1].append(enrollment_codes[i])
    print("INSCRIPCIONES POR NIVEL DE CLASE")
    for i in range(len(matrix)):
        print(f"Nivel {i + 1}: {len(matrix[i])} inscripciones")

#generar una matriz por cantidad de socios por tipo de socio y clase
def affiliates_by_type_and_class_matrix():
    matrix = [[[] for _ in range(len(gym_class_codes))] for _ in range(3)]
    for i in range(len(enrollment_codes)):
        affiliate_code = enrollment_affiliate_codes[i]
        class_code = enrollment_gym_class_codes[i]
        affiliate_pos = search_affiliate_position(affiliate_code)
        class_pos = search_class_position(class_code)
        if affiliate_pos == -1 or class_pos == -1:
            continue
        affiliate_type = affiliate_types[affiliate_pos]
        if 1 <= affiliate_type <= 3:
            matrix[affiliate_type - 1][class_pos].append(affiliate_code)
    print("AFILIADOS POR TIPO Y CLASE")
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            print(f"Socio {get_type_name(i + 1)} - Clase {gym_class_names[j]}: {len(matrix[i][j])} afiliados")

#Funciones de Busqueda
#Funcion de busqueda Binaria
def buscar_clase_binaria():
    print("BÚSQUEDA BINARIA DE CLASE POR CÓDIGO")
    codigo = pedir_entero("Ingrese el código de la clase a buscar: ", "Código inválido, ingrese un número.")

    # Primero ordenamos las copias por código (inserción) para poder aplicar búsqueda binaria
    codigos = gym_class_codes[:]
    nombres = gym_class_names[:]
    niveles = gym_class_levels[:]
    capacidades = gym_class_capacities[:]

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

    # búsqueda binaria
    inicio = 0
    fin = n - 1
    posicion = -1

    while inicio <= fin:
        medio = (inicio + fin) // 2
        if codigos[medio] == codigo:
            posicion = medio
            inicio = fin + 1  # fuerza salida del while
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
    for i in range(len(affiliate_codes)):
        if affiliate_codes[i] == codigo:
            posicion = i

    if posicion == -1:
        print("Socio no encontrado.")
    else:
        print(f"Socio encontrado en posición {posicion}:")
        print(f"Código: {affiliate_codes[posicion]}, Nombre: {affiliate_names[posicion]}, Edad: {affiliate_ages[posicion]}, Tipo: {get_type_name(affiliate_types[posicion])}")

#Funciones de Ordenamiento
#Funcion para ordenar socios por edad usando el método de selección
def ordenar_socios_por_edad():
    # Trabajamos sobre copias para no modificar las listas originales
    nombres = affiliate_names[:]
    codigos = affiliate_codes[:]
    edades = affiliate_ages[:]
    tipos = affiliate_types[:]

    n = len(edades)
    for i in range(n - 1):
        pos_min = i
        for j in range(i + 1, n):
            if edades[j] < edades[pos_min]:
                pos_min = j
        # Intercambio en todas las listas paralelas
        edades[i], edades[pos_min] = edades[pos_min], edades[i]
        nombres[i], nombres[pos_min] = nombres[pos_min], nombres[i]
        codigos[i], codigos[pos_min] = codigos[pos_min], codigos[i]
        tipos[i], tipos[pos_min] = tipos[pos_min], tipos[i]

    print("SOCIOS ORDENADOS POR EDAD (Selección)")
    for i in range(n):
        print(f"Código: {codigos[i]}, Nombre: {nombres[i]}, Edad: {edades[i]}, Tipo: {get_type_name(tipos[i])}")

#Funcion para ordenar clases por nivel usando el método de inserción
def ordenar_clases_por_nivel():
    codigos = gym_class_codes[:]
    nombres = gym_class_names[:]
    niveles = gym_class_levels[:]
    capacidades = gym_class_capacities[:]

    n = len(niveles)
    for i in range(1, n):
        clave_nivel = niveles[i]
        clave_codigo = codigos[i]
        clave_nombre = nombres[i]
        clave_capacidad = capacidades[i]
        j = i - 1
        while j >= 0 and niveles[j] > clave_nivel:
            niveles[j + 1] = niveles[j]
            codigos[j + 1] = codigos[j]
            nombres[j + 1] = nombres[j]
            capacidades[j + 1] = capacidades[j]
            j -= 1
        niveles[j + 1] = clave_nivel
        codigos[j + 1] = clave_codigo
        nombres[j + 1] = clave_nombre
        capacidades[j + 1] = clave_capacidad

    print("CLASES ORDENADAS POR NIVEL (Inserción)")
    for i in range(n):
        print(f"Código: {codigos[i]}, Nombre: {nombres[i]}, Nivel: {niveles[i]}, Cupos disponibles: {capacidades[i]}")

#Función para ordenar inscripciones por asistencias usando el método de burbujeo
def ordenar_inscripciones_por_asistencias():
    codigos = enrollment_codes[:]
    socios = enrollment_affiliate_codes[:]
    clases = enrollment_gym_class_codes[:]
    asistencias = enrollment_attendances[:]
    estados = enrollment_status[:]
    n = len(asistencias)
    for i in range(n - 1):
        for j in range(0, n - 1 - i):
            if asistencias[j] > asistencias[j + 1]:
                asistencias[j], asistencias[j + 1] = asistencias[j + 1], asistencias[j]
                codigos[j], codigos[j + 1] = codigos[j + 1], codigos[j]
                socios[j], socios[j + 1] = socios[j + 1], socios[j]
                clases[j], clases[j + 1] = clases[j + 1], clases[j]
                estados[j], estados[j + 1] = estados[j + 1], estados[j]

    print("INSCRIPCIONES ORDENADAS POR ASISTENCIAS (Burbujeo)")
    for i in range(n):
        print(f"Código: {codigos[i]}, Socio: {socios[i]}, Clase: {clases[i]}, Asistencias: {asistencias[i]}, Estado: {estados[i]}")

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
    for i in range(len(gym_class_codes)):
        if gym_class_codes[i] == code:
            position = i
    return position

#Funcion de busqueda de usuario para login
def search_user_position(username):
    position = -1
    for i in range(len(login_usernames)):
        if login_usernames[i] == username:
            position = i
    return position

#Funcion de login De 3 intentos
def login():
    attempts = 1
    max_attempts = 3

    input_user = input("ingrese su nombre de usuario: ")
    input_passw = input("ingrese su contraseña: ")
    user_position = search_user_position(input_user)

    while (user_position == -1 or login_passwords[user_position] != input_passw) and attempts < max_attempts:
        print("El nombre de usuario o la contraseña son incorrectos, por favor vuelva a intentarlo.")
        input_user = input("ingrese su nombre de usuario: ")
        input_passw = input("ingrese su contraseña: ")
        user_position = search_user_position(input_user)
        attempts += 1

    if user_position == -1 or login_passwords[user_position] != input_passw:
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
    if len(affiliate_codes) > 0:
        codigo = affiliate_codes[-1] + 1

    affiliate_names.append(nombre)
    affiliate_codes.append(codigo)
    affiliate_ages.append(int(edad))
    affiliate_types.append(int(affiliate_type))

    print(f"Socio '{nombre}' agregado con código {codigo}.")

#Funcion para eliminar afiliados, validando que el codigo exista y confirmando la eliminacion
def eliminar_afiliados():
    print("BAJAR AFILIADO")
    codigo = pedir_entero("Ingrese el código del socio a eliminar: ", "Código inválido, ingrese un número.")
    pos = search_affiliate_position(codigo)
    if pos == -1:
        print("Socio no encontrado.")
    else:
        print(f"¿Seguro que desea eliminar a '{affiliate_names[pos]}'? (s/n)")
        confirm = input()
        if confirm.lower() == "s":
            inscripciones_eliminadas = remove_enrollments_by_affiliate(codigo)
            affiliate_names.pop(pos)
            affiliate_codes.pop(pos)
            affiliate_ages.pop(pos)
            affiliate_types.pop(pos)
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
    for i in range(len(affiliate_codes)):
        if affiliate_codes[i] == code:
            position = i
    return position


def remove_enrollment_at(position):
    enrollment_codes.pop(position)
    enrollment_affiliate_codes.pop(position)
    enrollment_gym_class_codes.pop(position)
    enrollment_attendances.pop(position)
    enrollment_status.pop(position)


def remove_enrollments_by_affiliate(affiliate_code):
    deleted_count = 0
    for i in range(len(enrollment_codes) - 1, -1, -1):
        if enrollment_affiliate_codes[i] == affiliate_code:
            remove_enrollment_at(i)
            deleted_count += 1
    return deleted_count


def remove_enrollments_by_class(class_code):
    deleted_count = 0
    for i in range(len(enrollment_codes) - 1, -1, -1):
        if enrollment_gym_class_codes[i] == class_code:
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
        print(f"Socio actual: {affiliate_names[pos]}, {affiliate_ages[pos]} años, {get_type_name(affiliate_types[pos])}")
        nombre = input(f"Nuevo nombre (si para mantener '{affiliate_names[pos]}'): ")
        if nombre != "si":
            affiliate_names[pos] = nombre
        edad = input(f"Nueva edad (si para mantener {affiliate_ages[pos]}): ")
        if edad != "si":
            while not es_entero(edad) or int(edad) < 0 or int(edad) > 100:
                print("ERROR, se debe ingresar una edad entre 0 y 100")
                edad = input("Nueva edad: ")
            affiliate_ages[pos] = int(edad)
        print("Tipos: 1-Mensual  2-Libre  3-Premium")
        type_code = input(f"Nuevo tipo (si para mantener {affiliate_types[pos]}): ")
        if type_code != "si":
            while not es_entero(type_code) or int(type_code) < 1 or int(type_code) > 3:
                print("ERROR, se debe ingresar un codigo entre 1 y 3")
                type_code = input("Nuevo tipo: ")
            affiliate_types[pos] = int(type_code)
        print(f"Socio modificado: {affiliate_names[pos]}, {affiliate_ages[pos]} años, {get_type_name(affiliate_types[pos])}")

#Funcion para listar afiliados, mostrando codigo, nombre, edad y tipo de afiliado
def list_affiliates():
    print("LISTA DE AFILIADOS")
    for i in range(len(affiliate_names)):
        print(f"Código: {affiliate_codes[i]}, Nombre: {affiliate_names[i]}, Edad: {affiliate_ages[i]}, Tipo: {get_type_name(affiliate_types[i])}")

#Funcion para sumar clases, validando nivel y capacidad, y asignando un codigo automaticamente
def sumar_clase():
    print("\nSUMAR CLASE")
    nombre = input("Nombre de la clase: ")

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

    codigo = 201 if len(gym_class_codes) == 0 else gym_class_codes[-1] + 1

    gym_class_codes.append(codigo)
    gym_class_names.append(nombre)
    gym_class_levels.append(nivel)
    gym_class_capacities.append(capacidad)

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
        confirm = input(f"¿Seguro que desea eliminar la clase '{gym_class_names[pos]}'? (s/n): ")
        if confirm.lower() == "s":
            class_code = gym_class_codes[pos]
            inscripciones_eliminadas = remove_enrollments_by_class(class_code)
            gym_class_codes.pop(pos)
            gym_class_names.pop(pos)
            gym_class_levels.pop(pos)
            gym_class_capacities.pop(pos)
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
        print(f"Clase actual: {gym_class_names[pos]}, Nivel: {get_level_name(gym_class_levels[pos])}, Cupos disponibles: {gym_class_capacities[pos]}")
        nombre = input(f"Nuevo nombre (si para mantener '{gym_class_names[pos]}'): ")
        if nombre != "si":
            gym_class_names[pos] = nombre
        nivel = input(f"Nuevo nivel -1-Principiante 2-Intermedio 3-Avanzado- (si para mantener {get_level_name(gym_class_levels[pos])}): ")
        if nivel != "si":
            while not es_entero(nivel) or int(nivel) < 1 or int(nivel) > 3:
                print("ERROR, nivel entre 1 y 3")
                nivel = input("Nuevo nivel: ")
            gym_class_levels[pos] = int(nivel)
        capacidad = input(f"Nuevos cupos disponibles (si para mantener {gym_class_capacities[pos]}): ")
        if capacidad != "si":
            while not es_entero(capacidad) or int(capacidad) < 1:
                print("ERROR, ingresar un número mayor a 0")
                capacidad = input("Nuevos cupos disponibles: ")
            gym_class_capacities[pos] = int(capacidad)
        print(f"Clase modificada: {gym_class_names[pos]}, Nivel: {get_level_name(gym_class_levels[pos])}, Cupos disponibles: {gym_class_capacities[pos]}")

#Funcion listar clases, mostrando codigo, nombre, nivel y capacidad
def list_clases():
    print("LISTA DE CLASES")
    print(f"{'Código':<10} {'Nombre':<20} {'Nivel':<18} {'Cupos disponibles'}")
    print("-" * 58)
    for i in range(len(gym_class_codes)):
        print(f"{gym_class_codes[i]:<10} {gym_class_names[i]:<20} {get_level_name(gym_class_levels[i]):<18} {gym_class_capacities[i]}")

def does_class_code_exist(code):
    for gym_code in gym_class_codes:
        if gym_code == code:
            return True
    return False

def does_affiliate_code_exist(code):
    for affiliate_code in affiliate_codes:
        if affiliate_code == code:
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
    if gym_class_capacities[class_pos] <= 0:
        print("No hay cupos disponibles para esa clase.")
        return
    list_affiliates()
    affiliate_code = pedir_entero("Ingrese su código de afiliado: ", "por favor ingrese un código de afiliado válido.")
    while not does_affiliate_code_exist(affiliate_code):
        print("por favor ingrese un código de afiliado válido.")
        affiliate_code = pedir_entero("Ingrese su código de afiliado: ", "por favor ingrese un código de afiliado válido.")

    enrollment_codes.append(301 if len(enrollment_codes) == 0 else enrollment_codes[-1] + 1)
    enrollment_gym_class_codes.append(int(class_code))
    enrollment_affiliate_codes.append(int(affiliate_code))
    enrollment_status.append(1)
    enrollment_attendances.append(0)
    gym_class_capacities[class_pos] -= 1

#Funcion para listar inscripciones
def list_inscripciones():
    print("LISTA DE INSCRIPCIONES")
    print(f"{'Código':<10} {'Socio':<20} {'Clase':<20} {'Asistencias':<12} {'Estado'}")
    print("-" * 80)
    for i in range(len(enrollment_codes)):
        affiliate_pos = search_affiliate_position(enrollment_affiliate_codes[i])
        class_pos = search_class_position(enrollment_gym_class_codes[i])
        affiliate_name = affiliate_names[affiliate_pos] if affiliate_pos != -1 else "Socio inexistente"
        class_name = gym_class_names[class_pos] if class_pos != -1 else "Clase inexistente"
        print(f"{enrollment_codes[i]:<10} {affiliate_name:<20} {class_name:<20} {enrollment_attendances[i]:<12} {'Activa' if enrollment_status[i] == 1 else 'Inactiva'}")

##Funcionm para listar clases de un socio
def clases_de_socio(affiliate_code): 
    posiciones = list(filter(
        lambda i: enrollment_affiliate_codes[i] == affiliate_code and enrollment_status[i] == 1,
        range(len(enrollment_codes))
    ))
    nombre_clases = list(map(
        lambda i: gym_class_names[search_class_position(enrollment_gym_class_codes[i])],
        posiciones
    ))
    return nombre_clases

def listar_clases_socio():
    print("Clases de un socio")
    codigo = pedir_entero("Ingrese el codigo del socio: ","Codigo invalido, ingresar un numero",)
    pos = search_affiliate_position(codigo)
    if pos == -1:
        print("Error,socio no encontrado")
        return
    clases = clases_de_socio(codigo)
    if not clases:
        print("El socio no tiene clases activas")
    else:
        print(f"El socio {affiliate_names[pos]} tiene las clases: {', '.join(clases)}")

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
    elif enrollment_status[pos] == 2:
        print("La inscripción ya estaba finalizada.")
    else:
        confirm = input(f"¿Seguro que desea dar de baja la inscripción del socio '{affiliate_names[search_affiliate_position(enrollment_affiliate_codes[pos])]}' en la clase '{gym_class_names[search_class_position(enrollment_gym_class_codes[pos])]}' ? (s/n): ")
        if confirm.lower() == "s":
            enrollment_status[pos] = 2
            gym_class_capacities[search_class_position(enrollment_gym_class_codes[pos])] += 1
            print("Inscripción dada de baja.")
        else:
            print("Operación cancelada.")

#Funcion para buscar la posicion de una inscripcion por su codigo, devuelve -1 si no se encuentra
def search_inscription_position(code):
    position = -1
    for i in range(len(enrollment_codes)):
        if enrollment_codes[i] == code:
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
        estado_anterior = enrollment_status[pos]
        class_pos = search_class_position(enrollment_gym_class_codes[pos])
        print(f"Inscripción actual: Socio '{affiliate_names[search_affiliate_position(enrollment_affiliate_codes[pos])]}', Clase '{gym_class_names[search_class_position(enrollment_gym_class_codes[pos])]}', Asistencias: {enrollment_attendances[pos]}, Estado: {'Activa' if enrollment_status[pos] == 1 else 'Inactiva'}")
        asistencias = input(f"Nuevas asistencias (si para mantener {enrollment_attendances[pos]}): ")
        if asistencias != "si":
            while not es_entero(asistencias) or int(asistencias) < 0:
                print("ERROR, las asistencias deben ser un número mayor o igual a 0")
                asistencias = input("Nuevas asistencias: ")
            enrollment_attendances[pos] = int(asistencias)
        estado = input(f"Nuevo estado -1-Activa 2-Inactiva- (si para mantener {'Activa' if enrollment_status[pos] == 1 else 'Inactiva'}): ")
        if estado != "si":
            while not es_entero(estado) or int(estado) < 1 or int(estado) > 2:
                print("ERROR, estado entre 1 y 2")
                estado = input("Nuevo estado: ")
            nuevo_estado = int(estado)
            if estado_anterior == 1 and nuevo_estado == 2:
                enrollment_status[pos] = nuevo_estado
                if class_pos != -1:
                    gym_class_capacities[class_pos] += 1
            elif estado_anterior == 2 and nuevo_estado == 1:
                if class_pos == -1:
                    print("No se puede activar porque la clase no existe.")
                elif gym_class_capacities[class_pos] <= 0:
                    print("No hay cupos disponibles para activar esta inscripción.")
                else:
                    enrollment_status[pos] = nuevo_estado
                    gym_class_capacities[class_pos] -= 1
            else:
                enrollment_status[pos] = nuevo_estado
        print(f"Inscripción modificada: Socio '{affiliate_names[search_affiliate_position(enrollment_affiliate_codes[pos])]}', Clase '{gym_class_names[search_class_position(enrollment_gym_class_codes[pos])]}', Asistencias: {enrollment_attendances[pos]}, Estado: {'Activa' if enrollment_status[pos] == 1 else 'Inactiva'}")
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
