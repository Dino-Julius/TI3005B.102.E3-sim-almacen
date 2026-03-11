#!/usr/bin/env python3
"""
Genera insights y graficas con los outputs existentes, sin rerun de simulaciones.

Entradas (si existen):
- outputs/*/metricas.json
- outputs/*/pedidos.json
- outputs/*/heatmap_*.png

Salidas:
- analisis/insights/graficos/*.png
- analisis/insights/reporte_insights.md
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs"
INSIGHTS_DIR = ROOT / "analisis" / "insights"
GRAFICOS_DIR = INSIGHTS_DIR / "graficos"
INSIGHTS_DIR.mkdir(parents=True, exist_ok=True)
GRAFICOS_DIR.mkdir(parents=True, exist_ok=True)

SCENARIOS = {
    "S2_baseline_200r": "S2 Baseline 200r",
    "S2_mejora_200r": "S2 Mejora 200r",
    "S3_alta_densidad_400r": "S3 A 400r/600p",
    "S3_burst_200r_1200": "S3 B 200r/1200p",
    "S3_var_400r_1200": "S3 C 400r/1200p",
}

HEATMAP_FILES = ["heatmap_visitas.png",
                 "heatmap_esperas.png", "heatmap_ratio.png"]


def load_json(path: Path) -> Dict:
    return json.loads(path.read_text(encoding="utf-8"))


def scenario_paths(scenario: str) -> Tuple[Path, Path]:
    sdir = OUT / scenario
    return sdir / "metricas.json", sdir / "pedidos.json"


def collect_data() -> Tuple[Dict[str, Dict], Dict[str, Dict], List[str]]:
    metrics: Dict[str, Dict] = {}
    orders: Dict[str, Dict] = {}
    missing: List[str] = []

    for scenario in SCENARIOS:
        mpath, ppath = scenario_paths(scenario)
        if mpath.exists():
            metrics[scenario] = load_json(mpath)
        else:
            missing.append(f"Falta metricas.json en {scenario}")

        if ppath.exists():
            orders[scenario] = load_json(ppath)
        else:
            missing.append(f"Falta pedidos.json en {scenario}")

    return metrics, orders, missing


def plot_latency_percentiles(metrics: Dict[str, Dict]) -> Path | None:
    keys = ["tiempo_mediana_pedido_ticks",
            "tiempo_p90_pedido_ticks", "tiempo_p95_pedido_ticks"]
    labels = ["p50", "p90", "p95"]

    scenarios = [s for s in SCENARIOS if s in metrics]
    if not scenarios:
        return None

    x = np.arange(len(scenarios))
    width = 0.25

    fig, ax = plt.subplots(figsize=(12, 5))
    for idx, (k, lbl) in enumerate(zip(keys, labels)):
        values = [metrics[s].get(k, 0.0) for s in scenarios]
        ax.bar(x + (idx - 1) * width, values, width=width, label=lbl)

    ax.set_xticks(x)
    ax.set_xticklabels([SCENARIOS[s]
                       for s in scenarios], rotation=15, ha="right")
    ax.set_ylabel("Ticks")
    ax.set_title("Latencia por percentiles (pedido)")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()

    out = GRAFICOS_DIR / "latencia_percentiles.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out


def plot_normalized_congestion(metrics: Dict[str, Dict]) -> Path | None:
    scenarios = [s for s in SCENARIOS if s in metrics]
    if not scenarios:
        return None

    labels = [SCENARIOS[s] for s in scenarios]
    per_100_orders = []
    per_1000_ticks = []

    for s in scenarios:
        m = metrics[s]
        high = float(m.get("eventos_alto", 0))
        total = max(float(m.get("pedidos_totales", 1)), 1.0)
        ticks = max(float(m.get("tick_final", 1)), 1.0)
        per_100_orders.append((high / total) * 100.0)
        per_1000_ticks.append((high / ticks) * 1000.0)

    x = np.arange(len(labels))
    width = 0.38
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.bar(x - width / 2, per_100_orders, width=width,
           label="Eventos alto / 100 pedidos")
    ax.bar(x + width / 2, per_1000_ticks, width=width,
           label="Eventos alto / 1000 ticks")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=15, ha="right")
    ax.set_title("Congestion normalizada")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()

    out = GRAFICOS_DIR / "congestion_normalizada.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out


def plot_distance_efficiency(metrics: Dict[str, Dict]) -> Path | None:
    scenarios = [s for s in SCENARIOS if s in metrics]
    if not scenarios:
        return None

    labels = [SCENARIOS[s] for s in scenarios]
    values = []
    for s in scenarios:
        m = metrics[s]
        dist = float(m.get("distancia_total_celdas", 0))
        done = max(float(m.get("pedidos_completados", 1)), 1.0)
        values.append(dist / done)

    fig, ax = plt.subplots(figsize=(11, 4.8))
    bars = ax.bar(labels, values)
    ax.set_ylabel("Celdas por pedido completado")
    ax.set_title("Eficiencia de distancia")
    ax.grid(axis="y", alpha=0.3)
    plt.xticks(rotation=15, ha="right")

    for b, v in zip(bars, values):
        ax.text(b.get_x() + b.get_width() / 2, v,
                f"{v:.1f}", ha="center", va="bottom", fontsize=9)

    plt.tight_layout()
    out = GRAFICOS_DIR / "eficiencia_distancia.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out


def plot_replan_vs_congestion(metrics: Dict[str, Dict]) -> Path | None:
    scenarios = [s for s in SCENARIOS if s in metrics]
    if not scenarios:
        return None

    x = [float(metrics[s].get("replaneaciones_bloqueo", 0)) for s in scenarios]
    y = [float(metrics[s].get("eventos_alto", 0)) for s in scenarios]

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(x, y)
    for s, xv, yv in zip(scenarios, x, y):
        ax.annotate(
            SCENARIOS[s], (xv, yv), textcoords="offset points", xytext=(5, 5), fontsize=8)

    ax.set_xlabel("Replaneaciones por bloqueo")
    ax.set_ylabel("Eventos alto")
    ax.set_title("Replaneacion vs congestion")
    ax.grid(alpha=0.3)
    plt.tight_layout()

    out = GRAFICOS_DIR / "replan_vs_congestion.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out


def plot_order_arrival_profile(orders: Dict[str, Dict]) -> Path | None:
    scenarios = [s for s in ["S2_mejora_200r",
                             "S3_burst_200r_1200", "S3_var_400r_1200"] if s in orders]
    if not scenarios:
        return None

    fig, axes = plt.subplots(len(scenarios), 1, figsize=(
        10, 3.2 * len(scenarios)), sharex=False)
    if len(scenarios) == 1:
        axes = [axes]

    for ax, s in zip(axes, scenarios):
        ticks = [p.get("tick_creacion", 0)
                 for p in orders[s].get("pedidos", [])]
        if ticks:
            ax.hist(ticks, bins=20)
        ax.set_title(f"Perfil temporal de demanda - {SCENARIOS[s]}")
        ax.set_xlabel("tick_creacion")
        ax.set_ylabel("# pedidos")
        ax.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    out = GRAFICOS_DIR / "perfil_demanda_ticks.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out


def plot_station_concentration(orders: Dict[str, Dict]) -> Path | None:
    scenarios = [s for s in ["S2_mejora_200r",
                             "S3_burst_200r_1200", "S3_var_400r_1200"] if s in orders]
    if not scenarios:
        return None

    fig, axes = plt.subplots(
        len(scenarios), 1, figsize=(10, 3.2 * len(scenarios)))
    if len(scenarios) == 1:
        axes = [axes]

    for ax, s in zip(axes, scenarios):
        estaciones = [p.get("estacion_id")
                      for p in orders[s].get("pedidos", [])]
        c = Counter(estaciones)
        top = c.most_common(10)
        labels = [str(k) for k, _ in top]
        vals = [v for _, v in top]
        ax.bar(labels, vals)
        ax.set_title(f"Top estaciones por carga - {SCENARIOS[s]}")
        ax.set_xlabel("estacion_id")
        ax.set_ylabel("# pedidos")
        ax.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    out = GRAFICOS_DIR / "top_estaciones_carga.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return out


def find_available_heatmaps() -> Dict[str, List[Path]]:
    found: Dict[str, List[Path]] = {}
    for scenario in SCENARIOS:
        sdir = OUT / scenario
        available = []
        for fname in HEATMAP_FILES:
            p = sdir / fname
            if p.exists():
                available.append(p)
        if available:
            found[scenario] = available
    return found


def write_report(
    metrics: Dict[str, Dict],
    orders: Dict[str, Dict],
    missing: List[str],
    generated: List[Path],
    available_heatmaps: Dict[str, List[Path]],
) -> Path:
    lines: List[str] = []
    lines.append("# Reporte de Insights (sin rerun)")
    lines.append("")
    lines.append("Este reporte usa exclusivamente outputs ya existentes.")
    lines.append("")

    lines.append("## Escenarios con metricas cargadas")
    for s in SCENARIOS:
        if s in metrics:
            m = metrics[s]
            lines.append(
                f"- {SCENARIOS[s]}: completitud={m.get('tasa_completitud', 0):.4f}, "
                f"throughput={m.get('throughput_pedidos_por_1000_ticks', 0):.2f}, "
                f"p95={m.get('tiempo_p95_pedido_ticks', 0):.2f}, eventos_alto={m.get('eventos_alto', 0)}"
            )
    lines.append("")

    lines.append("## Graficas generadas")
    for p in generated:
        lines.append(f"- {p.relative_to(ROOT)}")
    lines.append("")

    lines.append("## Heatmaps disponibles (ya existentes)")
    if available_heatmaps:
        for s, items in available_heatmaps.items():
            rels = ", ".join(str(x.relative_to(ROOT)) for x in items)
            lines.append(f"- {SCENARIOS[s]}: {rels}")
    else:
        lines.append(
            "- No se encontraron heatmaps en los escenarios configurados.")
    lines.append("")

    lines.append("## Faltantes detectados")
    if missing:
        for m in missing:
            lines.append(f"- {m}")
    else:
        lines.append("- Ninguno")

    out = INSIGHTS_DIR / "reporte_insights.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


def main() -> None:
    metrics, orders, missing = collect_data()

    generated: List[Path] = []
    for fn in [
        plot_latency_percentiles,
        plot_normalized_congestion,
        plot_distance_efficiency,
        plot_replan_vs_congestion,
    ]:
        out = fn(metrics)
        if out is not None:
            generated.append(out)

    for fn in [plot_order_arrival_profile, plot_station_concentration]:
        out = fn(orders)
        if out is not None:
            generated.append(out)

    heatmaps = find_available_heatmaps()
    report = write_report(metrics, orders, missing, generated, heatmaps)

    print("[OK] Insights generados:")
    for p in generated:
        print(" -", p.relative_to(ROOT))
    print("[OK] Reporte:", report.relative_to(ROOT))


if __name__ == "__main__":
    main()
