import json

def cargar_preguntas(listado_preguntas):
    return listado_preguntas

def mostrar_pregunta(pregunta):
    print("\n",pregunta)

def obtener_respuesta():
    validar_respuesta = input("\nIngrese su respuesta: ").upper()
    while validar_respuesta != "A" and validar_respuesta != "B" and validar_respuesta != "C" and validar_respuesta != "D":
        validar_respuesta = input("Debe ingresar una respuesta valida (A, B, C o D): ").upper()

    return validar_respuesta

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
1 - Empezar cuestionario
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
