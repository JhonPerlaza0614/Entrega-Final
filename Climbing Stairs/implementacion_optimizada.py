"""
Implementación OPTIMIZADA para "Subir Escaleras".

Relación con Fibonacci:
  W(n) = F(n+1)

Usamos la fórmula cerrada de Binet:
  F(k) = (phi^k - psi^k) / sqrt(5)

Complejidad (discusión):
- En el sentido "algorítmico" (número de evaluaciones de una fórmula cerrada),
  se considera O(1) porque no hacemos un bucle sobre n.
- En la práctica, si queremos exactitud para n grande, necesitamos alta precisión.
  Con decimal, el costo depende de la precisión requerida y del tamaño del entero
  resultante (cantidad de dígitos), por lo que no es O(1) estricto en el modelo de bits.
  Aun así, es una mejora drástica frente a Θ(φ^n).

Estrategia híbrida:
- si n es pequeño -> float (muy rápido y exacto en ese rango)
- si n es grande  -> decimal con precisión estimada para redondear correctamente
"""

from __future__ import annotations
import math
import decimal
import sys

SQRT5_F = math.sqrt(5.0)
PHI_F = (1.0 + SQRT5_F) / 2.0
PSI_F = (1.0 - SQRT5_F) / 2.0

# Umbral típico donde float deja de ser confiable para Fibonacci exacto
# (depende de plataforma, pero ~70-75 suele funcionar como regla práctica)
FLOAT_SAFE_N = 70


def _fib_binet_float(k: int) -> int:
    if k <= 1:
        return k
    return int(round((PHI_F**k - PSI_F**k) / SQRT5_F))


def _fib_binet_decimal(k: int, precision: int) -> int:
    if k <= 1:
        return k

    decimal.getcontext().prec = precision
    D = decimal.Decimal

    sqrt5 = D(5).sqrt()
    phi = (D(1) + sqrt5) / D(2)
    psi = (D(1) - sqrt5) / D(2)

    # Redondeo al entero más cercano (para obtener F(k) exacto)
    return int((phi**k - psi**k) / sqrt5 + D("0.5"))


def formas_escalera_o1(n: int, precision: int | None = None) -> int:
    """
    Devuelve W(n) en entero exacto.

    Parámetros:
      n: escalones (>=0)
      precision: precisión decimal opcional para n grande.
                 Si no se pasa, se estima automáticamente.

    Retorna:
      W(n) = F(n+1)
    """
    if n < 0:
        raise ValueError("n debe ser >= 0")

    k = n + 1  # W(n) = F(n+1)

    # Para n pequeño, float es exacto y muchísimo más rápido que decimal
    if n <= FLOAT_SAFE_N:
        return _fib_binet_float(k)

    # Para n grande, estimamos precisión si no la pasan.
    # dígitos(F(k)) ≈ k*log10(phi) - log10(sqrt(5)) + 1
    # Sumamos margen para redondeo seguro.
    if precision is None:
        precision = int(k * 0.209) + 25

    return _fib_binet_decimal(k, precision=precision)


def main() -> None:
  n = int(sys.argv[1]) if len(sys.argv) > 1 else 4
  resultado = formas_escalera_o1(n)
  print(f"Para {n} escalones hay {resultado} formas de subirlos.")


if __name__ == "__main__":
  main()