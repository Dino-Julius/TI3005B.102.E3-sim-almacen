#!/usr/bin/env python3
"""
Genera reporte markdown del Entregable 4 (S3) con los tres escenarios:
A) alta densidad, B) burst severo, C) variacion de robots.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs"

SCENARIOS = {
    "A": "S3_alta_densidad_400r",
    "B": "S3_burst_200r_1200",
    "C": "S3_var_400r_1200",
}


def load_metrics(name: str) -> dict:
    path = OUT / name / "metricas.json"
    if not path.exists():
        raise FileNotFoundError(f"No existe {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def pct_delta(new: float, base: float) -> float:
    if base == 0:
        return 0.0
    return ((new - base) / base) * 100.0


def yn(cond: bool) -> str:
    return "Cumple" if cond else "No cumple"


def main() -> None:
    data = {k: load_metrics(v) for k, v in SCENARIOS.items()}

    a = data["A"]
    b = data["B"]
    c = data["C"]

    # Criterios definidos en Entregable 4
    estabilidad_completitud = (
        a.get("tasa_completitud", 0.0) >= 0.95 and c.get(
            "tasa_completitud", 0.0) >= 0.95
    )
    crecimiento_p95_pedido = pct_delta(
        c.get("tiempo_p95_pedido_ticks", 0.0), a.get("tiempo_p95_pedido_ticks", 0.0))
    estabilidad_p95 = crecimiento_p95_pedido <= 35.0
    ratio_deadlock = 0.0
    if a.get("deadlock", 0) > 0:
        ratio_deadlock = c.get("deadlock", 0) / a.get("deadlock", 0)
    estabilidad_deadlock = (a.get("deadlock", 0) == 0 and c.get(
        "deadlock", 0) == 0) or (ratio_deadlock <= 2.0)

    robustez_no_completados = (
        b.get("pedidos_no_completados", 0) <= 0.10 *
        max(1, b.get("pedidos_totales", 1))
    )
    robustez_throughput = b.get("throughput_pedidos_por_1000_ticks", 0.0) > 0.0

    escalabilidad_throughput = pct_delta(c.get("throughput_pedidos_por_1000_ticks", 0.0), a.get(
        "throughput_pedidos_por_1000_ticks", 0.0))
    escalabilidad_p95 = crecimiento_p95_pedido

    report = []
    report.append("# Reporte S3 - Entregable 4")
    report.append("")
    report.append("## 1) Tabla comparativa A/B/C")
    report.append("")
    report.append(
        "| Métrica | A: Alta densidad | B: Burst severo | C: Variación robots |")
    report.append("|---|---:|---:|---:|")

    keys = [
        ("robots", "Robots (diseño)"),
        ("pedidos_completados", "Pedidos completados"),
        ("pedidos_no_completados", "Pedidos no completados"),
        ("tasa_completitud", "Tasa completitud"),
        ("throughput_pedidos_por_1000_ticks", "Throughput (ped/1000 ticks)"),
        ("tiempo_promedio_pedido_ticks", "Tiempo promedio pedido"),
        ("tiempo_mediana_pedido_ticks", "Tiempo mediana pedido"),
        ("tiempo_p90_pedido_ticks", "Tiempo p90 pedido"),
        ("tiempo_p95_pedido_ticks", "Tiempo p95 pedido"),
        ("tiempo_p95_espera_ticks", "Tiempo p95 espera"),
        ("eventos_alto", "Eventos alto"),
        ("deadlock", "Deadlocks"),
        ("distancia_total_celdas", "Distancia total"),
        ("utilizacion_promedio", "Utilización promedio"),
    ]

    for key, label in keys:
        av = a.get(key, "-")
        bv = b.get(key, "-")
        cv = c.get(key, "-")

        if isinstance(av, float):
            av = f"{av:.4f}" if "tasa_" in key else f"{av:.2f}"
        if isinstance(bv, float):
            bv = f"{bv:.4f}" if "tasa_" in key else f"{bv:.2f}"
        if isinstance(cv, float):
            cv = f"{cv:.4f}" if "tasa_" in key else f"{cv:.2f}"

        report.append(f"| {label} | {av} | {bv} | {cv} |")

    report.append("")
    report.append("## 2) Evaluación de criterios (S3)")
    report.append("")
    report.append("### Estabilidad")
    report.append(f"- Completitud A y C >= 95%: {yn(estabilidad_completitud)}")
    report.append(
        f"- Crecimiento p95 pedido (C vs A) <= 35%: {yn(estabilidad_p95)} ({crecimiento_p95_pedido:+.2f}%)")
    report.append(
        f"- Deadlock C no supera 2x de A: {yn(estabilidad_deadlock)}")

    report.append("")
    report.append("### Robustez")
    report.append(f"- Throughput util en B (>0): {yn(robustez_throughput)}")
    report.append(
        f"- No completados en B <= 10%: {yn(robustez_no_completados)}")

    report.append("")
    report.append("### Escalabilidad (C vs A)")
    report.append(f"- Delta throughput: {escalabilidad_throughput:+.2f}%")
    report.append(f"- Delta p95 pedido: {escalabilidad_p95:+.2f}%")

    report.append("")
    report.append("## 3) Conclusión breve")
    report.append("")
    report.append(
        "La mejora A+C se evalúa en estabilidad, robustez y escalabilidad con base en distribución (mediana/p90/p95), no solo promedios.")

    out_file = ROOT / "analisis" / "S3" / "reporte_s3.md"
    out_file.write_text("\n".join(report) + "\n", encoding="utf-8")

    print("[OK] Reporte generado:", out_file)


if __name__ == "__main__":
    main()
