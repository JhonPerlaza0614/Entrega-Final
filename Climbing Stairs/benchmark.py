from __future__ import annotations

import csv
import os
import timeit
from typing import Optional

import matplotlib.pyplot as plt

from implementacion_pesada import formas_escalera_exponencial
from implementacion_optimizada import formas_escalera_o1


RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)

# Misma lista para ambos algoritmos
N_VALUES = [1, 2, 3, 5, 10, 15, 20, 25, 30, 35, 50, 100, 500, 1000, 10_000, 100_000]

REPEATS = 7
NUMBER = 1

# Límite para no “matar” el benchmark con el exponencial
EXP_MAX_N = 35


def avg_time(callable_stmt) -> float:
    times = timeit.repeat(callable_stmt, repeat=REPEATS, number=NUMBER)
    return sum(times) / len(times)


def time_maybe(func, n: int) -> Optional[float]:
    """Mide tiempo o devuelve None si se decide omitir (skip)."""
    if func is formas_escalera_exponencial and n > EXP_MAX_N:
        return None
    return avg_time(lambda: func(n))


def write_summary(path: str) -> None:
    text = f"""Benchmark: Subir Escaleras (W(n) = F(n+1))

Algoritmos comparados:
- pesada_exponencial: recursión ingenua sin memoización
  Tiempo: Θ(φ^n) (exponencial), 
  Espacio: O(n) por recursión
- optimizada_o1: fórmula cerrada (Binet) con modo híbrido (float/decimal)
  "O(1)" en número de pasos matemáticos, pero con decimal el costo real depende
  de la precisión (tamaño del número).

Configuración:
- N_VALUES = {N_VALUES}
- REPEATS  = {REPEATS}
- NUMBER   = {NUMBER}
- EXP_MAX_N = {EXP_MAX_N}  (para n > EXP_MAX_N el exponencial se marca como skip)

Archivos generados:
- results/benchmark.csv
- results/benchmark.png (log-log)
- results/benchmark_small.png (zoom hasta EXP_MAX_N)
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def plot_loglog(rows, path: str, title: str, limit_x: int | None = None) -> None:
    plt.figure(figsize=(10, 6))

    def plot_series(algo: str, label: str):
        xs = [n for (a, n, t) in rows if a == algo and t is not None]
        ys = [t for (a, _, t) in rows if a == algo and t is not None]
        if limit_x is not None:
            xs, ys = zip(*[(x, y) for (x, y) in zip(xs, ys) if x <= limit_x]) if xs else ([], [])
        if xs:
            plt.plot(xs, ys, marker="o", label=label)

    plot_series("pesada_exponencial", "Pesada (recursión ingenua, exponencial)")
    plot_series("optimizada_o1", "Optimizada (Binet híbrida: float/decimal)")

    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("n (escala log)")
    plt.ylabel("tiempo (s, escala log)")
    plt.title(title)
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig(path, dpi=160)


def main():
    rows = []

    print("=== Benchmark: Subir Escaleras ===")
    print(f"Nota: el exponencial se omite (skip) para n > {EXP_MAX_N}.")
    print("Nota 2: la versión optimizada usa float (n pequeño) y decimal (n grande).\n")

    for n in N_VALUES:
        t_exp = time_maybe(formas_escalera_exponencial, n)
        t_o1 = time_maybe(formas_escalera_o1, n)

        # Validación de correctitud cuando ambos existen
        if t_exp is not None:
            assert formas_escalera_exponencial(n) == formas_escalera_o1(n)

        rows.append(("pesada_exponencial", n, t_exp))
        rows.append(("optimizada_o1", n, t_o1))

        exp_str = "skip" if t_exp is None else f"{t_exp*1e3:.3f} ms"
        o1_str = f"{t_o1*1e6:.3f} us" if t_o1 is not None else "ERR"
        print(f"n={n:>7} | exp: {exp_str:>12} | opt: {o1_str:>12}")

    # CSV (guardamos vacío como string "skip")
    csv_path = os.path.join(RESULTS_DIR, "benchmark.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["algoritmo", "n", "tiempo_s"])
        for algo, n, t in rows:
            w.writerow([algo, n, "skip" if t is None else f"{t:.12f}"])
    print(f"\nCSV guardado en: {csv_path}")

    # Resumen
    summary_path = os.path.join(RESULTS_DIR, "benchmark_summary.txt")
    write_summary(summary_path)
    print(f"Resumen guardado en: {summary_path}")

    # Plot principal (log-log) con todos los puntos medidos
    plot_path = os.path.join(RESULTS_DIR, "benchmark.png")
    plot_loglog(
        rows,
        plot_path,
        title="Benchmark: Subir Escaleras — Exponencial vs 'O(1)' (misma lista N)",
        limit_x=None,
    )
    print(f"Gráfica guardada en: {plot_path}")

    # Plot zoom: solo hasta EXP_MAX_N (para comparar ambos sin escalas tan extremas)
    plot_small_path = os.path.join(RESULTS_DIR, "benchmark_small.png")
    plot_loglog(
        rows,
        plot_small_path,
        title=f"Benchmark (zoom): n ≤ {EXP_MAX_N} — Exponencial vs 'O(1)'",
        limit_x=EXP_MAX_N,
    )
    print(f"Gráfica (zoom) guardada en: {plot_small_path}")


if __name__ == "__main__":
    main()