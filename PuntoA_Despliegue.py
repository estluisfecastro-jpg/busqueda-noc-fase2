from itertools import product

# ==============================================================================
# PUNTO A: RETO MULTIPARADIGMA - DESPLIEGUE SEGURO EN INFRAESTRUCTURA CLOUD
# ==============================================================================

# 1. ENFOQUE 1: LÓGICA PROPOSICIONAL (TABLA DE VERDAD Y MODUS PONENS)

proposiciones = {
    "P": "El microservicio supera las pruebas unitarias",
    "Q": "El microservicio supera la validación de seguridad estática (SAST)",
    "R": "La pre-producción está habilitada",
    "S": "Existe aprobación del líder técnico",
    "T": "El despliegue a producción está autorizado",
    "U": "La autenticación de doble factor (MFA) está activa en accesos administrativos"
}

print("=== ENFOQUE 1: LÓGICA PROPOSICIONAL ===")
for k, v in proposiciones.items():
    print(f"{k}: {v}")

def implica(a, b):
    return (not a) or b

def fmt(val):
    return "V" if val else "F"

print("\nEvaluación de modelos de la Base de Conocimiento (KB):")
print(" P Q R S T U | R1 R2 R3 | Hechos(P∧Q∧S) | KB")
modelos_validos = []

for vals in product([True, False], repeat=6):
    P, Q, R, S, T, U = vals
    r1 = implica(P and Q, R)
    r2 = implica(R and S, T)
    r3 = implica(T, U)
    hechos = P and Q and S
    kb = r1 and r2 and r3 and hechos
    if kb:
        modelos_validos.append({"P": P, "Q": Q, "R": R, "S": S, "T": T, "U": U})
    if P and Q and S:  # Muestra las filas críticas donde los hechos son verdaderos
        print(f" {fmt(P)} {fmt(Q)} {fmt(R)} {fmt(S)} {fmt(T)} {fmt(U)} |  {fmt(r1)}  {fmt(r2)}  {fmt(r3)} |       {fmt(hechos)}        |  {fmt(kb)}")

print("\nModelos que hacen verdadera la KB:", modelos_validos)
print("¿KB |= T (despliegue autorizado)?", all(m["T"] for m in modelos_validos))
print("¿KB |= U (MFA activo)?          ", all(m["U"] for m in modelos_validos))

# Deducción paso a paso mediante Modus Ponens

print("\nDeducción paso a paso (Modus Ponens):")
derivados = {"P", "Q", "S"}
print(" 1. P            (hecho: percepto)")
print(" 2. Q            (hecho: percepto)")
print(" 3. S            (hecho: percepto)")
if "P" in derivados and "Q" in derivados:
    derivados.add("R")
    print(" 4. P∧Q  ←  ∧-Introducción de (P) y (Q)")
    print(" 5. R    ←  Modus Ponens con R1: (P∧Q)→R y (P∧Q)")
if "R" in derivados and "S" in derivados:
    derivados.add("T")
    print(" 6. R∧S  ←  ∧-Introducción de (R) y (S)")
    print(" 7. T    ←  Modus Ponens con R2: (R∧S)→T y (R∧S)")
if "T" in derivados:
    derivados.add("U")
    print(" 8. U    ←  Modus Ponens con R3: T→U y (T)")

print(f"\nConclusión: T ∈ derivados: {'T' in derivados} | U ∈ derivados: {'U' in derivados}")


# 2. ENFOQUE 2: LÓGICA DE PRIMER ORDEN (UNIFICACIÓN)

print("\n=== ENFOQUE 2: LÓGICA DE PRIMER ORDEN (LPO) ===")
def es_variable(x):
    return isinstance(x, str) and x.islower()

def unify(x, y, theta=None):
    if theta is None:
        theta = {}
    if theta is None:
        return None
    if x == y:
        return theta
    if es_variable(x):
        return unify_var(x, y, theta)
    if es_variable(y):
        return unify_var(y, x, theta)
    if isinstance(x, tuple) and isinstance(y, tuple) and len(x) == len(y):
        return unify(x[1:], y[1:], unify(x[0], y[0], theta))
    return None

def unify_var(var, x, theta):
    if var in theta:
        return unify(theta[var], x, theta)
    if x in theta:
        return unify(var, theta[x], theta)
    if occur_check(var, x, theta):
        return None
    nuevo_theta = dict(theta)
    nuevo_theta[var] = x
    return nuevo_theta

def occur_check(var, x, theta):
    if var == x:
        return True
    if es_variable(x) and x in theta:
        return occur_check(var, theta[x], theta)
    if isinstance(x, tuple):
        return any(occur_check(var, arg, theta) for arg in x)
    return False

print("UNIFY(PasaUnitarias(x), PasaUnitarias(PagosSvc)) =", unify(("PasaUnitarias", "x"), ("PasaUnitarias", "PagosSvc")))
print("UNIFY(AccesoAdmin(a, PagosSvc), AccesoAdmin(AdminConsola, PagosSvc)) =", unify(("AccesoAdmin", "a", "PagosSvc"), ("AccesoAdmin", "AdminConsola", "PagosSvc")))
print("UNIFY(PreProduccion(x), AprobadoLider(PagosSvc)) =", unify(("PreProduccion", "x"), ("AprobadoLider", "PagosSvc")))
print("UNIFY(x, F(x)) =", unify("x", ("F", "x")))


# 3. ENFOQUE 3: AGENTE BASADO EN CONOCIMIENTO (PropKB TELL-ASK)

print("\n=== ENFOQUE 3: KB-AGENT (TELL - ASK) ===")
class PropKB:
    def __init__(self):
        self.hechos = set()
        self.reglas = []

    def tell(self, hecho):
        self.hechos.add(hecho)
        print(f"  TELL({hecho})")

    def agregar_regla(self, premisas, conclusion):
        self.reglas.append((premisas, conclusion))

    def ask(self, consulta):
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
        return (consulta in inferidos), traza

kb_cloud = PropKB()
kb_cloud.agregar_regla(["P", "Q"], "R")
kb_cloud.agregar_regla(["R", "S"], "T")
kb_cloud.agregar_regla(["T"], "U")

print("t=0 · Percepto: pruebas unitarias OK y SAST OK (sin aprobación del líder)")
kb_cloud.tell("P")
kb_cloud.tell("Q")
for prop, accion in [("R", "HABILITAR_PRE_PRODUCCION"), ("T", "AUTORIZAR_DESPLIEGUE_PRODUCCION"), ("U", "ACTIVAR_MFA_ACCESOS_ADMIN")]:
    res, _ = kb_cloud.ask(prop)
    print(f"  ASK({prop}) → {res}   [{accion}]")

print("\nt=1 · Percepto: llega la aprobación del líder técnico")
kb_cloud.tell("S")
traza_final = []
for prop, accion in [("R", "HABILITAR_PRE_PRODUCCION"), ("T", "AUTORIZAR_DESPLIEGUE_PRODUCCION"), ("U", "ACTIVAR_MFA_ACCESOS_ADMIN")]:
    res, traza_final = kb_cloud.ask(prop)
    print(f"  ASK({prop}) → {res}   [{accion}]")

print("\nTraza de inferencia:")
for i, paso in enumerate(traza_final, 1):
    print(f"  {i}. {paso}")