import json
from inputimeout import inputimeout, TimeoutOccurred


def cargar_preguntas(listado_preguntas):
    return listado_preguntas

def mostrar_pregunta(pregunta):
    print("\n",pregunta)

def obtener_respuesta():
    """ Funcion que obtiene la respuesta y la valida. Ademas agrega un limite de tiempo para la respuesta
    utilizando la libreria inputimeout https://pypi.org/project/inputimeout/
"""
    try:
        validar_respuesta = inputimeout(prompt="\nIngrese su respuesta: ", timeout=8).upper()
        while validar_respuesta != "A" and validar_respuesta != "B" and validar_respuesta != "C" and validar_respuesta != "D":
            validar_respuesta = inputimeout(prompt="Debe ingresar una respuesta valida (A, B, C o D): ", timeout=5).upper()

        return validar_respuesta

    except TimeoutOccurred:
        print("\n¡Se acabo el tiempo para responder!")
        return None

def corregir_respuesta(respuesta, correcta):
    if respuesta == correcta:
        print("Respuesta correcta")
        return True

    print("Respuesta incorrecta")


def mostrar_resultados(aciertos, total):
    print(f"\nTotal de preguntas: {total}")
    print(f"Aciertos: {aciertos}")
    print(f"Porcentaje de aciertos: {(aciertos*100)/total}%")



def menu():
    print("""
### MENÚ ###
1 - Empezar cuestionario (Tienes 8 segundos para ingresar la respuesta)
2 - Salir
""")

    seleccion = int(input("Seleccione una opcion: "))
    return seleccion

def seleccionar_tema():
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

    with open(nombre_tema, 'r', encoding='utf-8') as archivo:
        datos = json.load(archivo)

    return datos

preguntas = cargar_preguntas(seleccionar_tema())
preguntas_correctas = 0
PREGUNTAS_TOTALES = len(preguntas)

opcion_seleccionada = menu()

while opcion_seleccionada != 2:

    if opcion_seleccionada == 1:
        for items in preguntas:
            mostrar_pregunta(items["pregunta"])
            opciones = items["opciones"]
            for opcion in opciones:
                print(opcion)
            respuesta_obtenida = obtener_respuesta()
            respuesta_correcta = corregir_respuesta(respuesta_obtenida,items["respuesta_correcta"])
            if respuesta_correcta:
                preguntas_correctas += 1

    opcion_seleccionada = menu()

mostrar_resultados(preguntas_correctas, PREGUNTAS_TOTALES)
