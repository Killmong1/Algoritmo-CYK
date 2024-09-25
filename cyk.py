import time
import numpy as np
import matplotlib.pyplot as plt

# Función para verificar si una gramática está en la forma normal de Chomsky (CNF)
def es_cnf(gramatica):
    for produccion in gramatica:
        for regla in gramatica[produccion]:
            if len(regla) == 1 and regla.islower():
                continue
            elif len(regla) == 2 and all(s.isupper() for s in regla):
                continue
            else:
                return False
    return True

# Algoritmo CYK
def cyk(gramatica, cadena):
    n = len(cadena)

    # Crear tabla
    tabla = np.zeros((n, n), dtype=object)
    for i in range(n):
        tabla[i] = [set() for _ in range(n)]

    # Inicialización (primer nivel de la pirámide)
    for i in range(n):
        for variable, reglas in gramatica.items():
            if cadena[i] in reglas:
                tabla[i][i].add(variable)

    # Rellenar la tabla (niveles superiores de la pirámide)
    for largo in range(2, n + 1):  # Largo de la subsecuencia
        for i in range(n - largo + 1):  # Inicio de la subsecuencia
            j = i + largo - 1  # Final de la subsecuencia
            for k in range(i, j):  # División de la subsecuencia
                for variable, reglas in gramatica.items():
                    for regla in reglas:
                        if len(regla) == 2:
                            B, C = regla
                            if B in tabla[i][k] and C in tabla[k + 1][j]:
                                tabla[i][j].add(variable)

    return 'S' in tabla[0][n - 1], tabla

# Gramática en CNF y cadena a verificar
gramatica = {
    'S': ['AB', 'BC'],
    'A': ['BA', 'a'],
    'B': ['CC', 'b'],
    'C': ['AB', 'a']
}
cadena = "baaba"

# Verificar si la gramática está en CNF
if not es_cnf(gramatica):
    print("La gramática no está en la forma normal de Chomsky (CNF)")
else:
    # Medir el tiempo de ejecución
    inicio = time.time()

    # Ejecutar CYK
    pertenece, tabla = cyk(gramatica, cadena)

    fin = time.time()

    # Mostrar el resultado
    print(f"La cadena {'pertenece' if pertenece else 'no pertenece'} al lenguaje.")
    print(f"Tiempo de ejecución: {fin - inicio:.6f} segundos")

    # Complejidad del algoritmo
    n = len(cadena)
    complejidad = n ** 3 * len(gramatica)  # O(n^3 * |G|)
    print(f"Complejidad del algoritmo CYK: O({complejidad})")

    # Generar tiempos de ejecución para diferentes tamaños de cadenas
    tamanos_cadena = list(range(2, 21))
    tiempos_ejecucion = []

    for t in tamanos_cadena:
        cadena_test = "a" * t
        inicio = time.time()
        cyk(gramatica, cadena_test)
        fin = time.time()
        tiempos_ejecucion.append(fin - inicio)

    # Graficar los tiempos de ejecución
    plt.plot(tamanos_cadena, tiempos_ejecucion, marker='o', label="Tiempo de ejecución")
    plt.title("Complejidad del algoritmo CYK")
    plt.xlabel("Tamaño de la cadena (n)")
    plt.ylabel("Tiempo de ejecución (segundos)")
    plt.legend()
    plt.grid(True)

    # Guardar la gráfica en un archivo PNG
    plt.savefig("cyk_complejidad.png")
    print("Gráfica guardada como 'cyk_complejidad.png'")

