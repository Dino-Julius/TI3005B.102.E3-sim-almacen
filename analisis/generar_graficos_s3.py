#!/usr/bin/env python3
"""
Genera gráficos comparativos para Entregable 4
Salida: analisis/S3/graficos/*.png
"""

import json
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "outputs"
GRAFICOS = ROOT / "analisis" / "S3" / "graficos"
GRAFICOS.mkdir(parents=True, exist_ok=True)

# ============================================================================
# 1) DATOS S2: Baseline 200r vs Mejora 200r
# ============================================================================
s2_baseline = {
    "pedidos_completados": 580,
    "pedidos_totales": 600,
    "tasa_completitud": 0.967,
    "throughput_pedidos_por_1000_ticks": 58.0,
    "tiempo_p95_pedido_ticks": 945,
    "eventos_alto": 97331,
    "deadlock": 0,
}

s2_mejora = {
    "pedidos_completados": 591,
    "pedidos_totales": 600,
    "tasa_completitud": 0.985,
    "throughput_pedidos_por_1000_ticks": 59.1,
    "tiempo_p95_pedido_ticks": 1032,
    "eventos_alto": 4928,
    "deadlock": 0,
}

# ============================================================================
# 2) DATOS S3: Escenarios A, B, C (desde metricas.json)
# ============================================================================
s3_scenarios = {}
for esc, folder in [
    ("A: Alta densidad (400r/600p)", "S3_alta_densidad_400r"),
    ("B: Burst severo (200r/1200p)", "S3_burst_200r_1200"),
    ("C: Var. carga+flota (400r/1200p)", "S3_var_400r_1200"),
]:
    path = OUT / folder / "metricas.json"
    if path.exists():
        s3_scenarios[esc] = json.loads(path.read_text(encoding="utf-8"))
    else:
        print(f"⚠️  No encontrado: {path}")

# ============================================================================
# Gráfico 1: S2 - Comparativa Baseline vs Mejora (Completitud, Throughput, p95)
# ============================================================================
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle('S2 - Corrección Entregable 3: Baseline vs Mejora (200 robots, 600 pedidos)',
             fontsize=14, fontweight='bold')

# Completitud
ax = axes[0]
x = [0, 1]
y = [s2_baseline["tasa_completitud"] * 100,
     s2_mejora["tasa_completitud"] * 100]
bars = ax.bar(x, y, color=["#e74c3c", "#2ecc71"],
              width=0.6, edgecolor="black", linewidth=1.5)
ax.set_ylim(90, 102)
ax.set_ylabel("Completitud (%)", fontsize=11, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(["Baseline", "Mejora"])
ax.grid(axis='y', alpha=0.3)
for i, (bar, val) in enumerate(zip(bars, y)):
    ax.text(bar.get_x() + bar.get_width()/2, val + 0.5, f"{val:.1f}%",
            ha="center", va="bottom", fontweight="bold")

# Throughput
ax = axes[1]
y = [s2_baseline["throughput_pedidos_por_1000_ticks"],
     s2_mejora["throughput_pedidos_por_1000_ticks"]]
bars = ax.bar(x, y, color=["#e74c3c", "#2ecc71"],
              width=0.6, edgecolor="black", linewidth=1.5)
ax.set_ylabel("Throughput (ped/1000 ticks)", fontsize=11, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(["Baseline", "Mejora"])
ax.grid(axis='y', alpha=0.3)
for i, (bar, val) in enumerate(zip(bars, y)):
    ax.text(bar.get_x() + bar.get_width()/2, val + 0.5, f"{val:.1f}",
            ha="center", va="bottom", fontweight="bold")

# p95 Pedido
ax = axes[2]
y = [s2_baseline["tiempo_p95_pedido_ticks"],
     s2_mejora["tiempo_p95_pedido_ticks"]]
bars = ax.bar(x, y, color=["#e74c3c", "#2ecc71"],
              width=0.6, edgecolor="black", linewidth=1.5)
ax.set_ylabel("Tiempo p95 (ticks)", fontsize=11, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(["Baseline", "Mejora"])
ax.grid(axis='y', alpha=0.3)
for i, (bar, val) in enumerate(zip(bars, y)):
    ax.text(bar.get_x() + bar.get_width()/2, val + 20, f"{val:.0f}",
            ha="center", va="bottom", fontweight="bold")

plt.tight_layout()
plt.savefig(GRAFICOS / "S2_baseline_vs_mejora.png",
            dpi=150, bbox_inches="tight")
print(f"✓ Guardado: {GRAFICOS / 'S2_baseline_vs_mejora.png'}")
plt.close()

# ============================================================================
# Gráfico 2: S2 - Eventos de congestión (log scale)
# ============================================================================
fig, ax = plt.subplots(figsize=(10, 6))
x = [0, 1]
y = [s2_baseline["eventos_alto"], s2_mejora["eventos_alto"]]
bars = ax.bar(x, y, color=["#e74c3c", "#2ecc71"],
              width=0.6, edgecolor="black", linewidth=1.5)
ax.set_ylabel("Eventos de congestión (escala log)",
              fontsize=12, fontweight='bold')
ax.set_yscale("log")
ax.set_xticks(x)
ax.set_xticklabels(["Baseline", "Mejora"])
ax.set_title("S2 - Eventos de alto (congestión severa)",
             fontsize=13, fontweight='bold')
ax.grid(axis='y', alpha=0.3, which='both')
for i, (bar, val) in enumerate(zip(bars, y)):
    reduction = ((s2_baseline["eventos_alto"] - val) /
                 s2_baseline["eventos_alto"] * 100) if i > 0 else 0
    if reduction > 0:
        label = f"{val:,}\n(-{reduction:.0f}%)"
    else:
        label = f"{val:,}"
    ax.text(bar.get_x() + bar.get_width()/2, val * 1.3, label,
            ha="center", va="bottom", fontweight="bold", fontsize=10)

plt.tight_layout()
plt.savefig(GRAFICOS / "S2_eventos_congestión.png",
            dpi=150, bbox_inches="tight")
print(f"✓ Guardado: {GRAFICOS / 'S2_eventos_congestión.png'}")
plt.close()

# ============================================================================
# Gráfico 3: S3 - Escenarios A/B/C - Completitud y Throughput
# ============================================================================
if len(s3_scenarios) == 3:
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('S3 - Escenarios A/B/C: Completitud y Throughput',
                 fontsize=14, fontweight='bold')

    escenarios_label = ["A: Alta densidad\n(400r/600p)",
                        "B: Burst severo\n(200r/1200p)",
                        "C: Var. carga\n(400r/1200p)"]
    x = list(range(len(s3_scenarios)))

    # Completitud
    ax = axes[0]
    y = [v.get("tasa_completitud", 0) * 100 for v in s3_scenarios.values()]
    colors = ["#3498db", "#f39c12", "#9b59b6"]
    bars = ax.bar(x, y, color=colors, edgecolor="black", linewidth=1.5)
    ax.set_ylim(95, 102)
    ax.set_ylabel("Completitud (%)", fontsize=11, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(escenarios_label)
    ax.grid(axis='y', alpha=0.3)
    for bar, val in zip(bars, y):
        ax.text(bar.get_x() + bar.get_width()/2, val + 0.2, f"{val:.2f}%",
                ha="center", va="bottom", fontweight="bold", fontsize=10)

    # Throughput
    ax = axes[1]
    y = [v.get("throughput_pedidos_por_1000_ticks", 0)
         for v in s3_scenarios.values()]
    bars = ax.bar(x, y, color=colors, edgecolor="black", linewidth=1.5)
    ax.set_ylabel("Throughput (ped/1000 ticks)",
                  fontsize=11, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(escenarios_label)
    ax.grid(axis='y', alpha=0.3)
    for bar, val in zip(bars, y):
        ax.text(bar.get_x() + bar.get_width()/2, val + 1, f"{val:.1f}",
                ha="center", va="bottom", fontweight="bold", fontsize=10)

    plt.tight_layout()
    plt.savefig(GRAFICOS / "S3_completitud_throughput.png",
                dpi=150, bbox_inches="tight")
    print(f"✓ Guardado: {GRAFICOS / 'S3_completitud_throughput.png'}")
    plt.close()

# ============================================================================
# Gráfico 4: S3 - Tiempo p95 y Eventos de congestión
# ============================================================================
if len(s3_scenarios) == 3:
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle('S3 - Estabilidad: p95 pedido y eventos de congestión',
                 fontsize=14, fontweight='bold')

    x = list(range(len(s3_scenarios)))
    escenarios_label = ["A: 400r/600p", "B: 200r/1200p", "C: 400r/1200p"]
    colors = ["#3498db", "#f39c12", "#9b59b6"]

    # p95 Pedido
    ax = axes[0]
    y = [v.get("tiempo_p95_pedido_ticks", 0) for v in s3_scenarios.values()]
    bars = ax.bar(x, y, color=colors, edgecolor="black", linewidth=1.5)
    ax.set_ylabel("Tiempo p95 (ticks)", fontsize=11, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(escenarios_label)
    ax.grid(axis='y', alpha=0.3)
    for bar, val in zip(bars, y):
        ax.text(bar.get_x() + bar.get_width()/2, val + 30, f"{val:.0f}",
                ha="center", va="bottom", fontweight="bold", fontsize=10)

    # Eventos (log scale)
    ax = axes[1]
    y = [v.get("eventos_alto", 0) for v in s3_scenarios.values()]
    bars = ax.bar(x, y, color=colors, edgecolor="black", linewidth=1.5)
    ax.set_ylabel("Eventos de congestión (log)",
                  fontsize=11, fontweight='bold')
    ax.set_yscale("log")
    ax.set_xticks(x)
    ax.set_xticklabels(escenarios_label)
    ax.grid(axis='y', alpha=0.3, which='both')
    for bar, val in zip(bars, y):
        ax.text(bar.get_x() + bar.get_width()/2, val * 1.3, f"{val:,}",
                ha="center", va="bottom", fontweight="bold", fontsize=9)

    plt.tight_layout()
    plt.savefig(GRAFICOS / "S3_estabilidad_p95_eventos.png",
                dpi=150, bbox_inches="tight")
    print(f"✓ Guardado: {GRAFICOS / 'S3_estabilidad_p95_eventos.png'}")
    plt.close()

# ============================================================================
# Gráfico 5: S3 - Escalabilidad (A vs C)
# ============================================================================
if len(s3_scenarios) >= 2:
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle('S3 - Escalabilidad: Escenario A (control) vs C (scaled up)',
                 fontsize=14, fontweight='bold')

    data = list(s3_scenarios.values())
    a = data[0]  # A
    c = data[2]  # C

    # Robots
    ax = axes[0]
    x = [0, 1]
    y = [a.get("robots", 0), c.get("robots", 0)]
    bars = ax.bar(x, y, color=["#3498db", "#9b59b6"],
                  edgecolor="black", linewidth=1.5)
    ax.set_ylabel("Cantidad de robots", fontsize=11, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(["A: Control", "C: Escalado"])
    ax.grid(axis='y', alpha=0.3)
    for bar, val in zip(bars, y):
        ax.text(bar.get_x() + bar.get_width()/2, val + 5, f"{val:.0f}",
                ha="center", va="bottom", fontweight="bold")

    # Throughput
    ax = axes[1]
    y = [a.get("throughput_pedidos_por_1000_ticks", 0),
         c.get("throughput_pedidos_por_1000_ticks", 0)]
    bars = ax.bar(x, y, color=["#3498db", "#9b59b6"],
                  edgecolor="black", linewidth=1.5)
    ax.set_ylabel("Throughput (ped/1000 ticks)",
                  fontsize=11, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(["A: Control", "C: Escalado"])
    ax.grid(axis='y', alpha=0.3)
    delta = (y[1] - y[0]) / y[0] * 100 if y[0] > 0 else 0
    label_str = f"{y[1]:.1f}\n(+{delta:.0f}%)" if delta > 0 else f"{y[1]:.1f}"
    ax.text(1, y[1] + 1, label_str, ha="center",
            va="bottom", fontweight="bold", fontsize=10)
    for bar, val in zip(bars, y):
        ax.text(bar.get_x() + bar.get_width()/2, val + 1, f"{val:.1f}",
                ha="center", va="bottom", fontweight="bold", fontsize=10)

    # p95 Pedido (estabilidad de cola)
    ax = axes[2]
    y = [a.get("tiempo_p95_pedido_ticks", 0),
         c.get("tiempo_p95_pedido_ticks", 0)]
    bars = ax.bar(x, y, color=["#3498db", "#9b59b6"],
                  edgecolor="black", linewidth=1.5)
    ax.set_ylabel("Tiempo p95 (ticks)", fontsize=11, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(["A: Control", "C: Escalado"])
    ax.grid(axis='y', alpha=0.3)
    delta = (y[1] - y[0]) / y[0] * 100 if y[0] > 0 else 0
    label_str = f"{y[1]:.0f}\n({delta:+.1f}%)"
    ax.text(1, y[1] + 30, label_str, ha="center",
            va="bottom", fontweight="bold", fontsize=10)
    for bar, val in zip(bars, y):
        ax.text(bar.get_x() + bar.get_width()/2, val + 30, f"{val:.0f}",
                ha="center", va="bottom", fontweight="bold", fontsize=10)

    plt.tight_layout()
    plt.savefig(GRAFICOS / "S3_escalabilidad_AvsC.png",
                dpi=150, bbox_inches="tight")
    print(f"✓ Guardado: {GRAFICOS / 'S3_escalabilidad_AvsC.png'}")
    plt.close()

print("\n✅ Todos los gráficos generados en: analisis/S3/graficos/")
