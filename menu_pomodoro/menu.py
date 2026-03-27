import time
import json

tarea_lista = {}

def temporizador(segundos):
    while segundos:
        mins, segs = divmod(segundos, 60)
        formato_tiempo = f'{mins:02d}:{segs:02d}'
        print(f"Tiempo restante: {formato_tiempo}", end="\r")
        time.sleep(1)
        segundos -= 1
    print("\n¡Tiempo cumplido! Fin del conteo.")
    print("¡Tarea completada! Te has ganado un descanso de 5 minutos.")

'''En esta parte del programa se reciben los datos del usuario y los cambio a forma 
de texto para que se puedan guardar en un archivo JSON y luego se pueda leer para mostrar las tareas al usuario'''
def agregar_tareas():
    print("\n--- Configuración de Tareas ---")
    try:
        cantidad = int(input("¿Cuántas tareas deseas agregar? "))
        for i in range(cantidad):
            nombre = input(f"Nombre de la tarea {i + 1}: ")
            # Usamos el número como llave para facilitar la selección
            id_tarea = str(len(tarea_lista) + 1)
            tarea_lista[id_tarea] = {"nombre": nombre, "estado": "Falta realizar"}
        guardar_tareas(tarea_lista)
        print("¡Tareas guardadas correctamente!")
         
    except ValueError:
        print("Por favor, ingresa un número válido.")

"""
    Toma el diccionario de tareas y lo guarda en el archivo JSON.
    'w' significa 'write' (escribir), lo que sobrescribe el archivo con los datos nuevos.
"""
def guardar_tareas(tareas):
    with open('tareas.json', 'w') as archivo:
        json.dump(tareas, archivo)

def gestionar_pomodoro():
    while True:
   # 1. Verificar si todas las tareas están realizadas antes de mostrar el menú
        todas_listas = all(tarea['estado'] == "Realizado" for tarea in tarea_lista.values())
        
        if todas_listas and len(tarea_lista) > 0:
            print("\n" + "="*50)
            print("¡FELICIDADES! HAS TERMINADO TODAS TUS TAREAS.")
            print("Avanzaste con todo, ¡tómate el día libre!")
            print("="*50)
            break # Sale del bucle y termina el programa

        print("\n--- Tareas Pendientes (Cargadas de JSON) ---")
        for id_tarea, datos in tarea_lista.items():
            print(f"{id_tarea}. {datos['nombre']} [{datos['estado']}]")
        
        try:
            # MODIFICADO: JSON guarda las llaves como texto ("1", "2"), 
            # así que no usamos int() aquí para la selección.
            seleccion = input("\n¿Cuál tarea deseas comenzar? (Número o 's' para salir): ")
            
            if seleccion.lower() == 's': break

            if seleccion in tarea_lista:
                # Verificar si ya está realizada
                if tarea_lista[seleccion]['estado'] == "Realizado":
                    print("Esta tarea ya fue completada.")
                    continue
                nombre_tarea = tarea_lista[seleccion]['nombre']
                tiempo_m = int(input(f"¿Cuántos minutos para '{nombre_tarea}'?: "))
                
                print(f"\nEnfoque iniciado: {nombre_tarea}")
                temporizador(tiempo_m * 60)
                
                # MODIFICADO: Eliminamos la tarea del diccionario en memoria
              # CAMBIO: En lugar de usar .pop() para borrar, cambiamos el valor del estado
                tarea_lista[seleccion]['estado'] = "Realizado"
                # MODIFICADO: ¡IMPORTANTE! Guardamos los cambios en el archivo JSON
                # para que la tarea desaparezca permanentemente del disco.
                guardar_tareas(tarea_lista) 
                
                print(f"\n--- '{nombre_tarea}': Realizado. ---")
                
            else:
                print("Ese número de tarea no existe en tu lista.")
        except ValueError:
            print("Entrada no válida. El tiempo debe ser un número.")
            
    if not tarea_lista:
        print("\n¡Felicidades! Tu archivo JSON está vacío. ¡Día completado!")

if __name__ == "__main__":
    print("Bienvenido a la aplicación Pomodoro")
    agregar_tareas()
    gestionar_pomodoro()