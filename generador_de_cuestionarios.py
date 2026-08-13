""" Modulo json que permite trabajar creando y leyendo archivos de dicho formato
https://docs.python.org/3/library/json.html
"""
import json
import os
from inputimeout import inputimeout, TimeoutOccurred


def cargar_preguntas(listado_preguntas):
    """ Funcion que retorna el listado de preguntas seleccionadas """
    return listado_preguntas

def mostrar_pregunta(pregunta):
    """ Funcion que muestra la pregunta por consola """
    print("\n",pregunta)

def obtener_respuesta():
    """ Funcion que obtiene la respuesta y la valida.
    Ademas agrega un limite de tiempo para la respuesta
    utilizando la libreria inputimeout https://pypi.org/project/inputimeout/
    """

    respuestas_posibles = ["A","B","C","D"]
    try:
        # El parametro prompt debe contener el mensaje que se vera en consola
        # El parametro timeout debe contener el tiempo limite para realizar la accion en segundoo
        validar_respuesta = inputimeout(prompt="\nIngrese su respuesta: ", timeout=10).upper()
        while validar_respuesta not in respuestas_posibles:
            # pylint: disable=line-too-long
            validar_respuesta = inputimeout(prompt="Debe ingresar una respuesta valida (A, B, C o D): ", timeout=10).upper()

        return validar_respuesta

    except TimeoutOccurred:
        print("\n¡Se acabo el tiempo para responder!")
        return None

def corregir_respuesta(respuesta, correcta):
    """ Funcion que verifica si la respuesta ingresada es correcto """
    if respuesta == correcta:
        print("Respuesta correcta")
        return True

    print("Respuesta incorrecta")
    return None


def mostrar_resultados(aciertos, total):
    """ Funcion que muestra el numero total de preguntas, la cantidad de aciertos,
    el porcentaje de aciertos y una valoracion final
    """
    print(f"\nTotal de preguntas: {total}")
    print(f"Aciertos: {aciertos}")
    porcentaje_aciertos = (aciertos*100)/total
    print(f"Porcentaje de aciertos: {porcentaje_aciertos}%")

    match True:
        case _ if porcentaje_aciertos == 100:
            print("¡Perfecto! Obtuviste la puntuación máxima!")
        case _ if porcentaje_aciertos >= 90:
            print("Exelente trabajo")
        case _ if porcentaje_aciertos >= 80:
            print("¡Muy bien!")
        case _ if porcentaje_aciertos >= 60:
            print("¡Buen intento! Aun tienes mucho para mejorar")
        case _:
            print("¡Sigue practicando y vuelve a intentarlo!")

    datos_usuario = f"{nombre_usuario}: {preguntas_correctas} puntos"
    # La funcion open recibe como primer parametro el nombre del archivo. El segundo parametro es
    # el modo: "r" para lectura, "w" para escritura y "a" para escribir al final del archivo. El
    # parametro encoding indica que juego de caracteres utilizar para realizar operaciones sobre
    # el archivo.
    with open("resultados_de_usuarios.txt", "a", encoding="utf-8") as archivo_resultados:
        archivo_resultados.write(datos_usuario + "\n")



def menu():
    """ Funcion que muestra por consola el menu principal de la aplicacion """
    print("""
### MENÚ ###
1 - Empezar cuestionario (Tienes 10 segundos para ingresar la respuesta)
2 - Ranking
3 - Salir
""")

    seleccion = int(input("Seleccione una opcion: "))
    while (seleccion < 1 or seleccion > 3):
        seleccion = int(input("Debe ingresar una respuesta valida (1, 2 o 3): "))

    return seleccion

def seleccionar_tema():
    """ Funcion que muestra por consola el menu para seleccionar el tema del cuestionario """
    print("""
### SELECCIONE UN CUESTIONARIO ###
1 - Paises y capitales
2 - Universo Mario Bros
3 - Universo Pokemon
""")

    tema_seleccionado = int(input("Seleccione un tema: "))

    while (tema_seleccionado < 1 or tema_seleccionado >3):
        tema_seleccionado = int(input("Debe ingresar una respuesta valida (1, 2 o 3): "))

    match tema_seleccionado:
        case 1:
            nombre_tema = "cuestionarios/paises_y_capitales.json"
        case 2:
            nombre_tema = "cuestionarios/mario_bros.json"
        case 3:
            nombre_tema = "cuestionarios/pokemon.json"

    with open(nombre_tema, 'r', encoding='utf-8') as archivo_tema:
        datos = json.load(archivo_tema)

    return datos

def agregar_a_ranking(nombre, puntos):
    """ Funcion que agrega el nombre de usuario y los puntos obtenidos al archivo ranking.json """
    puntos_usuario = {"usuario": nombre, "puntos": puntos}

    print(puntos_usuario)

    if os.path.exists("ranking.json") and os.path.getsize("ranking.json") > 0:
        with open("ranking.json", 'r', encoding='utf-8') as archivo_ranking:
            ranking = json.load(archivo_ranking)
    else:
        ranking = []

    ranking.append(puntos_usuario)

    with open("ranking.json", 'w', encoding='utf-8') as archivo_ranking:
        json.dump(ranking, archivo_ranking, indent=4)

    return ranking

def obtener_puntos(usuario):
    """ Funcion toma un usuarioy lo retorna a la funcion ver_ranking para ordenar
    los usuarios por puntuacion obtenida"""
    return usuario["puntos"]

def ver_ranking(ranking_usuarios):
    """ Funcion que lee los datos del archivo ranking.json, los ordena de forma descendente
    y los muestra por consola
    """
    ranking_descendente = sorted(ranking_usuarios, key=obtener_puntos, reverse=True)

    print("\n### RANKING ###")
    for usuario in ranking_descendente:
        print(f"{usuario['usuario']}: {usuario['puntos']} puntos")


preguntas_correctas = 0
preguntas_totales = 0
nombre_usuario = input("Ingrese su nombre: ")

while True:

    opcion_seleccionada = menu()

    if opcion_seleccionada == 1:
        preguntas = cargar_preguntas(seleccionar_tema())
        preguntas_correctas = 0
        preguntas_totales = len(preguntas)

        for items in preguntas:
            mostrar_pregunta(items["pregunta"])
            opciones = items["opciones"]
            for opcion in opciones:
                print(opcion)
            respuesta_obtenida = obtener_respuesta()
            respuesta_correcta = corregir_respuesta(respuesta_obtenida,items["respuesta_correcta"])
            if respuesta_correcta:
                preguntas_correctas += 1

        agregar_a_ranking(nombre_usuario, preguntas_correctas)
        mostrar_resultados(preguntas_correctas, preguntas_totales)

    elif opcion_seleccionada == 2:
        if os.path.exists("ranking.json") and os.path.getsize("ranking.json") > 0:
            with open("ranking.json", 'r', encoding='utf-8') as archivo:
                datos_ranking = json.load(archivo)
                ver_ranking(datos_ranking)
        else:
            print("El ranking esta vacio")

    elif opcion_seleccionada == 3:
        print("Has abandonado el juego")
        break
    else:
        print("Has seleccionado una opcion no valida. Vuelve a intentarlo")
