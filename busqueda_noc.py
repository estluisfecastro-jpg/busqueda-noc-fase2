import time
from collections import deque
import heapq

# ==========================================
# 1. ESTRUCTURA DEL GRAFO Y PROBLEMA DEL NOC
# ==========================================
grafo_noc = {
    'Inicio_Alerta': [('Filtrar_Severidad', 1)],
    'Filtrar_Severidad': [('Consultar_Antecedentes', 2), ('Revisar_POA', 3)],
    'Consultar_Antecedentes': [('Validar_Metricas_Recursos', 2), ('Cruzar_Historial', 1)],
    'Revisar_POA': [('Validar_Metricas_Recursos', 1), ('Identificar_Area_Responsable', 2)],
    'Cruzar_Historial': [('Generar_Diagnostico_Preliminar', 2)],
    'Validar_Metricas_Recursos': [('Generar_Diagnostico_Preliminar', 1)],
    'Identificar_Area_Responsable': [('Generar_Diagnostico_Preliminar', 2)],
    'Generar_Diagnostico_Preliminar': []  # Estado Meta
}

heuristica_noc = {
    'Inicio_Alerta': 4,
    'Filtrar_Severidad': 3,
    'Consultar_Antecedentes': 2,
    'Revisar_POA': 2,
    'Cruzar_Historial': 1,
    'Validar_Metricas_Recursos': 1,
    'Identificar_Area_Responsable': 1,
    'Generar_Diagnostico_Preliminar': 0
}

ESTADO_INICIAL = 'Inicio_Alerta'
ESTADO_META = 'Generar_Diagnostico_Preliminar'

# ==========================================
# 2. ALGORITMOS DE BÚSQUEDA
# ==========================================

def busqueda_bfs(grafo, inicio, meta):
    """Búsqueda en Anchura (BFS) - Cola FIFO"""
    inicio_tiempo = time.perf_counter()
    cola = deque([(inicio, [inicio], 0)])
    visitados = set()
    nodos_expandidos = 0

    while cola:
        nodo_actual, camino, costo = cola.popleft()
        nodos_expandidos += 1
        if nodo_actual == meta:
            tiempo_ejecucion = (time.perf_counter() - inicio_tiempo) * 1000
            return camino, costo, nodos_expandidos, tiempo_ejecucion

        if nodo_actual not in visitados:
            visitados.add(nodo_actual)
            for vecino, peso in grafo.get(nodo_actual, []):
                if vecino not in visitados:
                    cola.append((vecino, camino + [vecino], costo + peso))
    return None, 0, nodos_expandidos, 0


def busqueda_dfs(grafo, inicio, meta):
    """Búsqueda en Profundidad (DFS) - Pila LIFO"""
    inicio_tiempo = time.perf_counter()
    pila = [(inicio, [inicio], 0)]
    visitados = set()
    nodos_expandidos = 0

    while pila:
        nodo_actual, camino, costo = pila.pop()
        nodos_expandidos += 1
        if nodo_actual == meta:
            tiempo_ejecucion = (time.perf_counter() - inicio_tiempo) * 1000
            return camino, costo, nodos_expandidos, tiempo_ejecucion

        if nodo_actual not in visitados:
            visitados.add(nodo_actual)
            for vecino, peso in reversed(grafo.get(nodo_actual, [])):
                if vecino not in visitados:
                    pila.append((vecino, camino + [vecino], costo + peso))
    return None, 0, nodos_expandidos, 0


def busqueda_astar(grafo, heuristica, inicio, meta):
    """Algoritmo A* - Cola de Prioridad f(n) = g(n) + h(n)"""
    inicio_tiempo = time.perf_counter()
    cola_prioridad = [(heuristica[inicio], 0, inicio, [inicio])]
    visitados = {}
    nodos_expandidos = 0

    while cola_prioridad:
        f_cost, g_cost, nodo_actual, camino = heapq.heappop(cola_prioridad)
        nodos_expandidos += 1
        if nodo_actual == meta:
            tiempo_ejecucion = (time.perf_counter() - inicio_tiempo) * 1000
            return camino, g_cost, nodos_expandidos, tiempo_ejecucion

        if nodo_actual not in visitados or g_cost < visitados[nodo_actual]:
            visitados[nodo_actual] = g_cost
            for vecino, peso in grafo.get(nodo_actual, []):
                nuevo_g = g_cost + peso
                nuevo_f = nuevo_g + heuristica.get(vecino, 0)
                heapq.heappush(cola_prioridad, (nuevo_f, nuevo_g, vecino, camino + [vecino]))
    return None, 0, nodos_expandidos, 0


# ==========================================
# 3. EJECUCIÓN EXPERIMENTAL
# ==========================================
if __name__ == '__main__':
    print("=" * 70)
    print(" EJECUCIÓN EXPERIMENTAL DE ALGORITMOS DE BÚSQUEDA - AGENTE NOC ")
    print("=" * 70)

    c_bfs, g_bfs, n_bfs, t_bfs = busqueda_bfs(grafo_noc, ESTADO_INICIAL, ESTADO_META)
    c_dfs, g_dfs, n_dfs, t_dfs = busqueda_dfs(grafo_noc, ESTADO_INICIAL, ESTADO_META)
    c_ast, g_ast, n_ast, t_ast = busqueda_astar(grafo_noc, heuristica_noc, ESTADO_INICIAL, ESTADO_META)

    print(f"\n{'Algoritmo':<15} | {'Nodos Expandidos':<18} | {'Tiempo (ms)':<12} | {'Costo Total (g)':<15}")
    print("-" * 70)
    print(f"{'BFS':<15} | {n_bfs:<18} | {t_bfs:<12.4f} | {g_bfs:<15}")
    print(f"{'DFS':<15} | {n_dfs:<18} | {t_dfs:<12.4f} | {g_dfs:<15}")
    print(f"{'A*':<15} | {n_ast:<18} | {t_ast:<12.4f} | {g_ast:<15}")
    print("-" * 70)

    print("\n[Rutas Obtenidas]")
    print(f"Ruta BFS: {' -> '.join(c_bfs)}")
    print(f"Ruta DFS: {' -> '.join(c_dfs)}")
    print(f"Ruta A*:  {' -> '.join(c_ast)}")