# HOMEWORK1 1 BANU CLAUDIU-RĂZVAN

from math import sqrt
import sys
sys.stdout.reconfigure(encoding="utf-8")

# 1. PARSAREA SISTEMULUI DE ECUAȚII (1 punct)

def parse_system(file_path):
    """Citește sistemul din fișier și întoarce matricea A și vectorul B."""
    pozitie = {"x": 0, "y": 1, "z": 2}      # în ce coloană merge fiecare necunoscută
    A = []
    B = []

    with open(file_path, "r") as fisier:
        for linie in fisier:
            linie = linie.strip()
            if linie == "":                  # sărim peste rândurile goale
                continue

            stanga, dreapta = linie.split("=")   # "2x + 3y - z" și "5"
            rand = [0.0, 0.0, 0.0]               # coeficienții pentru x, y, z
            semn = 1                             # semnul termenului curent

            for termen in stanga.split():        # termenii sunt separați prin spații
                if termen == "+":
                    semn = 1
                elif termen == "-":
                    semn = -1
                else:
                    necunoscuta = termen[-1]     # ultima literă: x, y sau z
                    coeficient = termen[:-1]     # ce e înaintea literei: "2", "", "-"
                    if coeficient == "" or coeficient == "+":
                        valoare = 1.0            # "x" înseamnă 1x
                    elif coeficient == "-":
                        valoare = -1.0           # "-x" înseamnă -1x
                    else:
                        valoare = float(coeficient)
                    rand[pozitie[necunoscuta]] = semn * valoare
                    semn = 1                     # resetăm semnul pentru termenul următor

            A.append(rand)
            B.append(float(dreapta))

    return A, B

# 2. OPERAȚII CU MATRICE ȘI VECTORI (5 puncte)

def determinant(m):
    """Determinantul unei matrice 3x3, cu formula din enunț (dezvoltare după primul rând)."""
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
            - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


def trace(m):
    """Urma matricei: suma elementelor de pe diagonala principală."""
    return m[0][0] + m[1][1] + m[2][2]


def norm(v):
    """Norma euclidiană a vectorului: radical din suma pătratelor."""
    return sqrt(v[0] ** 2 + v[1] ** 2 + v[2] ** 2)


def transpose(m):
    """Transpusa: rândurile devin coloane (elementul [i][j] ajunge pe [j][i])."""
    rezultat = []
    for j in range(3):
        rand_nou = []
        for i in range(3):
            rand_nou.append(m[i][j])
        rezultat.append(rand_nou)
    return rezultat


def multiply(m, v):
    """Înmulțirea matrice * vector: fiecare rând al matricei se înmulțește cu vectorul."""
    rezultat = []
    for i in range(3):
        suma = 0.0
        for j in range(3):
            suma += m[i][j] * v[j]
        rezultat.append(suma)
    return rezultat

# 3. REZOLVARE CU REGULA LUI CRAMER (1 punct)


def replace_column(m, coloana, v):
    """Întoarce o copie a matricei m în care coloana dată este înlocuită cu vectorul v."""
    copie = []
    for i in range(3):
        rand = m[i][:]             # copiem rândul, ca să nu stricăm matricea originală
        rand[coloana] = v[i]
        copie.append(rand)
    return copie


def solve_cramer(A, B):
    """x = det(Ax)/det(A), y = det(Ay)/det(A), z = det(Az)/det(A)."""
    det_A = determinant(A)
    if det_A == 0:
        raise ValueError("det(A) = 0: sistemul nu are soluție unică.")

    solutie = []
    for coloana in range(3):
        A_inlocuit = replace_column(A, coloana, B)      # Ax, apoi Ay, apoi Az
        solutie.append(determinant(A_inlocuit) / det_A)
    return solutie

# 4. REZOLVARE PRIN INVERSARE (3 puncte)

def minor(m, i, j):
    """Minorul M_ij: matricea 2x2 rămasă după ce scoatem rândul i și coloana j."""
    rezultat = []
    for r in range(3):
        if r == i:
            continue
        rand = []
        for c in range(3):
            if c == j:
                continue
            rand.append(m[r][c])
        rezultat.append(rand)
    return rezultat


def determinant_2x2(m):
    """Determinantul unei matrice 2x2: ad - bc."""
    return m[0][0] * m[1][1] - m[0][1] * m[1][0]


def cofactor_matrix(m):
    """Matricea cofactorilor: fiecare element devine (-1)^(i+j) * det(M_ij)."""
    rezultat = []
    for i in range(3):
        rand = []
        for j in range(3):
            rand.append((-1) ** (i + j) * determinant_2x2(minor(m, i, j)))
        rezultat.append(rand)
    return rezultat


def adjugate(m):
    """Adjuncta: transpusa matricei cofactorilor."""
    return transpose(cofactor_matrix(m))


def inverse(m):
    """Inversa: A^(-1) = (1 / det(A)) * adj(A)."""
    det_m = determinant(m)
    if det_m == 0:
        raise ValueError("det(A) = 0: matricea nu are inversă.")

    adj = adjugate(m)
    rezultat = []
    for i in range(3):
        rand = []
        for j in range(3):
            rand.append(adj[i][j] / det_m)
        rezultat.append(rand)
    return rezultat


def solve_inversion(A, B):
    """X = A^(-1) * B."""
    return multiply(inverse(A), B)


# AFIȘARE ȘI RULARE

def print_matrix(nume, m):
    print(nume + " =")
    for rand in m:
        print("   ", [round(valoare, 4) for valoare in rand])


if __name__ == "__main__":
    # 1. Parsare
    A, B = parse_system("system.txt")
    print("--- 1. Parsare ---")
    print_matrix("A", A)
    print("B =", B)

    # 2. Operații
    print("\n--- 2. Operații cu matrice și vectori ---")
    print("det(A)   =", determinant(A))
    print("Trace(A) =", trace(A))
    print("||B||    =", round(norm(B), 4))
    print_matrix("Transpusa lui A", transpose(A))
    print("A * B    =", multiply(A, B))

    # 3. Cramer
    print("\n--- 3. Regula lui Cramer ---")
    x, y, z = solve_cramer(A, B)
    print(f"x = {x:.4f}, y = {y:.4f}, z = {z:.4f}")

    # 4. Inversare
    print("\n--- 4. Inversare ---")
    print_matrix("Matricea cofactorilor", cofactor_matrix(A))
    print_matrix("adj(A)", adjugate(A))
    print_matrix("Inversa lui A", inverse(A))
    x, y, z = solve_inversion(A, B)
    print(f"x = {x:.4f}, y = {y:.4f}, z = {z:.4f}")

    # Verificare: A * X trebuie să dea înapoi B
    print("\n--- Verificare ---")
    print("A * X =", [round(valoare, 4) for valoare in multiply(A, [x, y, z])])
    print("B     =", B)
