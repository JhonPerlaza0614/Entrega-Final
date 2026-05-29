"""
Implementación PESADA (exponencial) para el problema "Subir Escaleras".

Problema:
  W(n) = #formas de subir n escalones con pasos {1, 2}
  W(n) = W(n-1) + W(n-2), con W(0)=1, W(1)=1

Esta versión es la recursión ingenua SIN memoización.

Complejidad:
- Tiempo: Exponencial. Más precisamente, T(n) = Θ(φ^n), donde φ≈1.618.
  (A veces se describe con la cota superior O(2^n).)
  Importante: NO es O(n^2).
- Espacio: O(n) por la profundidad de la recursión.

Nota:
- Esta implementación se usa para demostrar la explosión combinatoria y
  contrastar con una solución de tiempo constante (fórmula cerrada) o cercana.
"""

def formas_escalera_exponencial(n: int) -> int:
    if n < 0:
        raise ValueError("n debe ser >= 0")
    if n <= 1:
        return 1
    return formas_escalera_exponencial(n - 1) + formas_escalera_exponencial(n - 2)