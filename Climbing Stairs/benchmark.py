from __future__ import annotations

import csv
import os
import timeit

import matplotlib.pyplot as plt

from implementacion_pesada import formas_escalera_exponencial
from implementacion_optimizada import formas_escalera_o1


RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)

# Para el exponencial usamos n pequeño (si no, se vuelve eterno)
N_EXPONENCIAL = list(range(0, 36, 3))  # 0,3,6,...,33

# Para O(1) podemos usar n muy grande
N_O1 = [1, 5, 10, 50, 100, 500, 1000, 10_000, 100_000]

REPEATS = 7
NUMBER = 1


def avg_time(stmt_callable) -> float:
    times = timeit.repeat(stmt_callable, repeat=REPEATS, number=NUMBER)
    return sum(times) / len(times)


def main():
    rows = []

    print("=== Benchmark: Subir Escaleras (W(n)) ===")
    print("W(n) = #formas de subir n escalones con pasos {1,2}\n")

    # 1) Exponencial
    print("[1/2] Midiendo implementación pesada (exponencial)...")
    for n in N_EXPONENCIAL:
        t = avg_time(lambda: formas_escalera_exponencial(n))
        rows.append(("pesada_exponencial", n, t))
        print(f"n={n:>6} | {t*1e3:>10.3f} ms")

    # 2) O(1) (Binet+Decimal)
    print("\n[2/2] Midiendo implementación optimizada (O(1) con Binet+decimal)...")
    for n in N_O1:
        # Precision dinámica dentro de la función
        t = avg_time(lambda: formas_escalera_o1(n))
        rows.append(("optimizada_o1_binet", n, t))
        print(f"n={n:>6} | {t*1e6:>10.3f} us")

    # CSV
    csv_path = os.path.join(RESULTS_DIR, "benchmark.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["algoritmo", "n", "tiempo_s"])
        w.writerows(rows)
    print(f"\nCSV guardado en: {csv_path}")

    # Plot (separamos series)
    plot_path = os.path.join(RESULTS_DIR, "benchmark.png")

    def series(algo: str):
        xs = [n for (a, n, _) in rows if a == algo]
        ys = [t for (a, _, t) in rows if a == algo]
        return xs, ys

    x1, y1 = series("pesada_exponencial")
    x2, y2 = series("optimizada_o1_binet")

    plt.figure(figsize=(10, 6))
    if x1:
        plt.plot(x1, y1, marker="o", label="Pesada (exponencial)")
    if x2:
        plt.plot(x2, y2, marker="o", label="Optimizada (Binet O(1))")

    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("n (escala log)")
    plt.ylabel("tiempo (s, escala log)")
    plt.title("Benchmark: Subir Escaleras — Exponencial vs O(1)")
    plt.grid(True, which="both", linestyle="--", linewidth=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig(plot_path, dpi=160)
    print(f"Gráfica guardada en: {plot_path}")


if __name__ == "__main__":
    main()