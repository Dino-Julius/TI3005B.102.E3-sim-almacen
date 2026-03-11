#!/usr/bin/env python3
"""
Generador de gráficos simplificado para Entregable 4
Requiere: matplotlib, numpy
"""

import json
from pathlib import Path
import sys

try:
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
    import matplotlib.pyplot as plt
    import numpy as np
except ImportError:
    print("⚠️  matplotlib no disponible. Instalando...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install",
                   "matplotlib", "numpy", "-q"], check=False)
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import numpy as np

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "outputs"
GRAFICOS = ROOT / "analisis" / "S3" / "graficos"
GRAFICOS.mkdir(parents=True, exist_ok=True)

# Datos S2
s2_data = {
    "Baseline": {"completitud": 96.7, "throughput": 58.0, "p95": 945, "eventos": 97331},
    "Mejora": {"completitud": 98.5, "throughput": 59.1, "p95": 1032, "eventos": 4928}
}

# Datos S3 desde archivos JSON
s3_files = {
    "A": OUT / "S3_alta_densidad_400r" / "metricas.json",
    "B": OUT / "S3_burst_200r_1200" / "metricas.json",
    "C": OUT / "S3_var_400r_1200" / "metricas.json"
}

s3_data = {}
for key, path in s3_files.items():
    if path.exists():
        s3_data[key] = json.loads(path.read_text())
    else:
        print(f"⚠️  No encontrado: {path}")

print("Generando gráficos...")

# Gráfico 1: S2 Baseline vs Mejora
if True:
    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    fig.suptitle('S2 - Corrección E3: Baseline vs Mejora (200r, 600p)',
                 fontsize=12, fontweight='bold')

    axes[0].bar(['Baseline', 'Mejora'], [96.7, 98.5],
                color=['#e74c3c', '#2ecc71'])
    axes[0].set_ylabel('Completitud (%)')
    axes[0].set_ylim(95, 100)
    axes[0].grid(axis='y', alpha=0.3)

    axes[1].bar(['Baseline', 'Mejora'], [58.0, 59.1],
                color=['#e74c3c', '#2ecc71'])
    axes[1].set_ylabel('Throughput (ped/1000 ticks)')
    axes[1].grid(axis='y', alpha=0.3)

    axes[2].bar(['Baseline', 'Mejora'], [945, 1032],
                color=['#e74c3c', '#2ecc71'])
    axes[2].set_ylabel('p95 pedido (ticks)')
    axes[2].grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(GRAFICOS / "S2_baseline_vs_mejora.png",
                dpi=100, bbox_inches="tight")
    print("✓ S2_baseline_vs_mejora.png")
    plt.close()

# Gráfico 2: S2 Congestión (log)
if True:
    fig, ax = plt.subplots(figsize=(8, 5))
    eventos = [97331, 4928]
    ax.bar(['Baseline', 'Mejora'], eventos, color=['#e74c3c', '#2ecc71'])
    ax.set_ylabel('Eventos de congestión (escala log)')
    ax.set_yscale('log')
    ax.set_title('S2 - Eventos de alto (congestión severa)', fontweight='bold')
    ax.grid(axis='y', alpha=0.3, which='both')
    plt.tight_layout()
    plt.savefig(GRAFICOS / "S2_eventos_congestión.png",
                dpi=100, bbox_inches="tight")
    print("✓ S2_eventos_congestión.png")
    plt.close()

# Gráfico 3: S3 Completitud y Throughput
if len(s3_data) >= 3:
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    fig.suptitle('S3 - Escenarios A/B/C: Completitud y Throughput',
                 fontweight='bold')

    labels = ['A: 400r/600p', 'B: 200r/1.2k', 'C: 400r/1.2k']
    valores_a, valores_b = [], []

    for k in ['A', 'B', 'C']:
        valores_a.append(s3_data[k].get('tasa_completitud', 0) * 100)
        valores_b.append(s3_data[k].get(
            'throughput_pedidos_por_1000_ticks', 0))

    axes[0].bar(labels, valores_a, color=['#3498db', '#f39c12', '#9b59b6'])
    axes[0].set_ylabel('Completitud (%)')
    axes[0].set_ylim(95, 102)
    axes[0].grid(axis='y', alpha=0.3)

    axes[1].bar(labels, valores_b, color=['#3498db', '#f39c12', '#9b59b6'])
    axes[1].set_ylabel('Throughput (ped/1000 ticks)')
    axes[1].grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(GRAFICOS / "S3_completitud_throughput.png",
                dpi=100, bbox_inches="tight")
    print("✓ S3_completitud_throughput.png")
    plt.close()

# Gráfico 4: S3 p95 y congestión
if len(s3_data) >= 3:
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    fig.suptitle('S3 - Estabilidad: p95 pedido y eventos', fontweight='bold')

    labels = ['A', 'B', 'C']
    valores_p95, valores_eventos = [], []

    for k in labels:
        valores_p95.append(s3_data[k].get('tiempo_p95_pedido_ticks', 0))
        valores_eventos.append(s3_data[k].get('eventos_alto', 0))

    axes[0].bar(labels, valores_p95, color=['#3498db', '#f39c12', '#9b59b6'])
    axes[0].set_ylabel('Tiempo p95 (ticks)')
    axes[0].grid(axis='y', alpha=0.3)

    axes[1].bar(labels, valores_eventos, color=[
                '#3498db', '#f39c12', '#9b59b6'])
    axes[1].set_ylabel('Eventos de congestión')
    axes[1].set_yscale('log')
    axes[1].grid(axis='y', alpha=0.3, which='both')

    plt.tight_layout()
    plt.savefig(GRAFICOS / "S3_estabilidad_p95_eventos.png",
                dpi=100, bbox_inches="tight")
    print("✓ S3_estabilidad_p95_eventos.png")
    plt.close()

# Gráfico 5: S3 Escalabilidad A vs C
if len(s3_data) >= 3:
    fig, axes = plt.subplots(1, 3, figsize=(13, 4))
    fig.suptitle('S3 - Escalabilidad: A (control) vs C (escalado)',
                 fontweight='bold')

    a = s3_data['A']
    c = s3_data['C']

    # Robots
    axes[0].bar(['A', 'C'], [a.get('robots', 0), c.get(
        'robots', 0)], color=['#3498db', '#9b59b6'])
    axes[0].set_ylabel('Robots')
    axes[0].grid(axis='y', alpha=0.3)

    # Throughput
    tp_a = a.get('throughput_pedidos_por_1000_ticks', 0)
    tp_c = c.get('throughput_pedidos_por_1000_ticks', 0)
    axes[1].bar(['A', 'C'], [tp_a, tp_c], color=['#3498db', '#9b59b6'])
    axes[1].set_ylabel('Throughput (ped/1k ticks)')
    axes[1].grid(axis='y', alpha=0.3)

    # p95
    p95_a = a.get('tiempo_p95_pedido_ticks', 0)
    p95_c = c.get('tiempo_p95_pedido_ticks', 0)
    axes[2].bar(['A', 'C'], [p95_a, p95_c], color=['#3498db', '#9b59b6'])
    axes[2].set_ylabel('p95 pedido (ticks)')
    axes[2].grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(GRAFICOS / "S3_escalabilidad_AvsC.png",
                dpi=100, bbox_inches="tight")
    print("✓ S3_escalabilidad_AvsC.png")
    plt.close()

print("\n✅ Gráficos generados en: analisis/S3/graficos/")
