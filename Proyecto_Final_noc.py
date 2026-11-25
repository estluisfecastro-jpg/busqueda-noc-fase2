# ==============================================================================
# PUNTO B: SOLUCIÓN APLICADA AL CASO DE ESTUDIO (DIAGNÓSTICO DE INCIDENTES NOC)
# ==============================================================================

class PropKB_NOC:
    """Base de Conocimiento Declarativa para el Centro de Operaciones de Red (NOC)."""
    def __init__(self):
        self.hechos = set()   # Perceptos observados en el instante t
        self.reglas = []      # Reglas normativas: (lista_premisas, conclusion)

    def tell(self, hecho: str):
        """Inserta un percepto nuevo en la Base de Conocimiento."""
        self.hechos.add(hecho)
        print(f"  TELL({hecho})")

    def agregar_regla(self, premisas: list, conclusion: str):
        """Registra una regla condicional (premisas -> conclusión) en la KB."""
        self.reglas.append((premisas, conclusion))

    def ask(self, consulta: str):
        """Ejecuta encadenamiento hacia adelante (Modus Ponens) para responder consultas."""
        inferidos = set(self.hechos)
        traza = []
        cambio = True
        while cambio:
            cambio = False
            for premisas, conclusion in self.reglas:
                if conclusion not in inferidos and all(p in inferidos for p in premisas):
                    inferidos.add(conclusion)
                    traza.append(f"{' & '.join(premisas)} ==> {conclusion}  ⇒  {conclusion}")
                    cambio = True
        return (consulta in inferidos), inferidos - self.hechos, traza


def evaluar_imperativo(perdida_paquetes: float, saturacion_recursos: float) -> list:
    """Enfoque tradicional imperativo (if-else) para comparación técnica."""
    acciones = []
    if perdida_paquetes > 5.0 and saturacion_recursos > 85.0:
        acciones.append("CLASIFICAR_ALERTA_COMO_PRIORITARIA")
        acciones.append("CONSULTAR_HISTORIAL_DE_INCIDENTES")
        acciones.append("REVISAR_PROCEDIMIENTO_OPERATIVO_AUTORIZADO")
        acciones.append("GENERAR_RECOMENDACION_DE_DIAGNOSTICO")
    return acciones


if __name__ == "__main__":
    
 #----------------------------------------------------------------------------
    # 1. Inicialización de la KB del agente NOC con 6 proposiciones y 4 reglas
 #----------------------------------------------------------------------------

    kb_noc = PropKB_NOC()
    kb_noc.agregar_regla(["PerdidaPaquetes", "SaturacionRecursos"], "AlertaPrioritaria")
    kb_noc.agregar_regla(["AlertaPrioritaria"], "HistorialConsultado")
    kb_noc.agregar_regla(["AlertaPrioritaria"], "POARevisado")
    kb_noc.agregar_regla(["HistorialConsultado", "POARevisado"], "DiagnosticoEmitido")

    consultas_acciones = [
        ("AlertaPrioritaria", "CLASIFICAR_ALERTA_COMO_PRIORITARIA"),
        ("HistorialConsultado", "CONSULTAR_HISTORIAL_DE_INCIDENTES"),
        ("POARevisado", "REVISAR_PROCEDIMIENTO_OPERATIVO_AUTORIZADO"),
        ("DiagnosticoEmitido", "GENERAR_RECOMENDACION_DE_DIAGNOSTICO")
    ]

    # --------------------------------------------------------------------------
    # INSTANTE t = 0: Pérdida de paquetes alta, pero saturación moderada (65%)
    # --------------------------------------------------------------------------

    print("=== t = 0 | Incidente NOC-001 ===")
    metricas_t0 = {"perdida_paquetes": 8.0, "saturacion_recursos": 65.0}
    print(f"Métricas: {metricas_t0}")
    if metricas_t0["perdida_paquetes"] > 5.0:
        kb_noc.tell("PerdidaPaquetes")

    acciones_t0 = []
    estados_t0 = set()
    for prop, accion in consultas_acciones:
        res, estados_t0, _ = kb_noc.ask(prop)
        print(f"  ASK({prop}) → {res}   [{accion}]")
        if res:
            acciones_t0.append(accion)

    print(f"Estados inferidos: {sorted(estados_t0)}")
    print(f"¿AlertaPrioritaria?    {'AlertaPrioritaria' in estados_t0}")
    print(f"¿DiagnosticoEmitido?   {'DiagnosticoEmitido' in estados_t0}")
    print(f"Acciones recomendadas: {acciones_t0}\n")

    # --------------------------------------------------------------------------
    # INSTANTE t = 1: Saturación sube al 92% -> Se dispara toda la cadena lógica
    # --------------------------------------------------------------------------

    print("=== t = 1 | Actualización del incidente NOC-001 ===")
    metricas_t1 = {"perdida_paquetes": 8.0, "saturacion_recursos": 92.0}
    print(f"Métricas: {metricas_t1}")
    if metricas_t1["saturacion_recursos"] > 85.0:
        kb_noc.tell("SaturacionRecursos")

    acciones_t1 = []
    estados_t1 = set()
    traza_noc = []
    for prop, accion in consultas_acciones:
        res, estados_t1, traza_noc = kb_noc.ask(prop)
        print(f"  ASK({prop}) → {res}   [{accion}]")
        if res:
            acciones_t1.append(accion)

    print(f"Estados inferidos: {sorted(estados_t1)}")
    print(f"¿AlertaPrioritaria?    {'AlertaPrioritaria' in estados_t1}")
    print(f"¿DiagnosticoEmitido?   {'DiagnosticoEmitido' in estados_t1}")
    print(f"Acciones recomendadas: {acciones_t1}\n")

    print("Traza de inferencia del NOC:")
    for i, paso in enumerate(traza_noc, 1):
        print(f"  {i}. {paso}")

    print("\nComparación imperativa t=0:", evaluar_imperativo(**metricas_t0))
    print("Comparación imperativa t=1:", evaluar_imperativo(**metricas_t1))