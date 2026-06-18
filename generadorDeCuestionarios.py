import json

with open('cuestionarios/paises_y_capitales.json', 'r', encoding='utf-8') as archivo:
    datos = json.load(archivo)

def cargar_preguntas(listado_preguntas):
    return listado_preguntas

def mostrar_pregunta(pregunta):
    print(pregunta)

def obtener_respuesta():
    validar_respuesta = input("Ingrese su respuesta: ").upper()
    while validar_respuesta != "A" and validar_respuesta != "B" and validar_respuesta != "C" and validar_respuesta != "D":
        validar_respuesta = input("Debe ingresar una respuesta valida (A, B, C o D): ").upper()

    return validar_respuesta

def corregir_respuesta(respuesta, correcta):
    if respuesta == correcta:
        print("Respuesta correcta")
        return True
    else:
        print("Respuesta incorrecta")


def mostrar_resultados(aciertos, total):
    print(f"Total de preguntas: {total}")
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

opcion_seleccionada = menu()

preguntas = cargar_preguntas(datos)
preguntas_correctas = 0
PREGUNTAS_TOTALES = len(preguntas)

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
