#!/usr/bin/env python3
"""
Análisis Comparativo S2: Estrés de Flota (Baseline vs Mejora Eje A)

Compara métricas entre baseline y mejora para 20, 40 y 60 robots.
Genera tabla comparativa y análisis de escalabilidad.

Entregable 3 - Marzo 2026
"""

import json
import os
from pathlib import Path
from typing import Dict


def obtener_ruta_outputs():
    """Detecta automáticamente la ruta a la carpeta outputs."""
    script_dir = Path(__file__).parent.parent
    outputs_dir = script_dir / "outputs"
    if not outputs_dir.exists():
        raise FileNotFoundError(f"No se encuentra: {outputs_dir}")
    return outputs_dir


def cargar_metricas(escenario: str) -> Dict:
    """Carga métricas desde un escenario."""
    outputs_dir = obtener_ruta_outputs()
    ruta = outputs_dir / escenario / "metricas.json"

    if not ruta.exists():
        raise FileNotFoundError(f"No se encuentra: {ruta}")

    with open(ruta) as f:
        return json.load(f)


def calcular_mejora(baseline: float, mejora: float) -> tuple:
    """Calcula diferencia absoluta y porcentual."""
    diff = mejora - baseline
    if baseline != 0:
        pct = (diff / baseline) * 100
    else:
        pct = 0.0 if mejora == 0 else float('inf')
    return diff, pct


def generar_tabla_comparativa():
    """Genera tabla comparativa markdown."""

    print("\n" + "="*80)
    print("📊 COMPARATIVA S2: BASELINE VS MEJORA EJE A")
    print("="*80 + "\n")

    escenarios = [
        ("20r", "S2_baseline_20r", "S2_mejora_20r"),
        ("40r", "S2_baseline_40r", "S2_mejora_40r"),
        ("60r", "S2_baseline_60r", "S2_mejora_60r"),
        ("100r", "S2_baseline_100r", "S2_mejora_100r"),
        ("200r", "S2_baseline_200r", "S2_mejora_200r"),
    ]

    # Cargar todas las métricas
    datos = {}
    for label, base_esc, mejora_esc in escenarios:
        try:
            datos[label] = {
                'baseline': cargar_metricas(base_esc),
                'mejora': cargar_metricas(mejora_esc)
            }
        except FileNotFoundError as e:
            print(f"⚠️  Error cargando {label}: {e}")
            return

    # Generar tabla
    print("## 1. TABLA COMPARATIVA DE MÉTRICAS CLAVE\n")
    print("| Métrica | Config | Baseline | Mejora | Δ | Δ% |")
    print("|---------|--------|----------|--------|---|-----|")

    metricas_clave = [
        ("pedidos_completados", "Pedidos Completados", "d", False),
        ("tiempo_promedio_pedido_ticks", "Tiempo Promedio (ticks)", ".1f", True),
        ("throughput_pedidos_por_1000_ticks",
         "Throughput (p/1000t)", ".2f", False),
        ("tiempo_promedio_espera_ticks", "Tiempo Espera (ticks)", ".1f", True),
        ("utilizacion_promedio", "Utilización (%)", ".1f", False),
        ("distancia_total_celdas", "Distancia Total (celdas)", "d", True),
        ("deadlock", "Deadlocks", "d", True),
        ("eventos_alto", "Eventos Alto", "d", True),
    ]

    for metrica_key, metrica_nombre, fmt, menor_mejor in metricas_clave:
        for label, _, _ in escenarios:
            if label not in datos:
                continue

            base_val = datos[label]['baseline'].get(metrica_key, 0)
            mejora_val = datos[label]['mejora'].get(metrica_key, 0)

            # Formatear utilización como porcentaje
            if metrica_key == "utilizacion_promedio":
                base_val *= 100
                mejora_val *= 100

            diff, pct = calcular_mejora(base_val, mejora_val)

            # Determinar símbolo de mejora
            if pct < -5:
                simbolo = "✅" if menor_mejor else "❌"
            elif pct > 5:
                simbolo = "❌" if menor_mejor else "✅"
            else:
                simbolo = "➖"

            # Formatear valores
            if fmt == "d":
                base_str = f"{int(base_val)}"
                mejora_str = f"{int(mejora_val)}"
                diff_str = f"{int(diff):+d}"
            else:
                base_str = f"{base_val:{fmt}}"
                mejora_str = f"{mejora_val:{fmt}}"
                diff_str = f"{diff:+{fmt}}"

            print(
                f"| {metrica_nombre} | {label} | {base_str} | {mejora_str} | {diff_str} | {pct:+.1f}% {simbolo} |")

    print("\n## 2. ANÁLISIS DE ESCALABILIDAD\n")

    # Análisis de pedidos completados
    print("### 📦 Completitud de Pedidos\n")
    for label, _, _ in escenarios:
        if label not in datos:
            continue
        base = datos[label]['baseline']['pedidos_completados']
        mejora = datos[label]['mejora']['pedidos_completados']
        total = datos[label]['baseline']['pedidos_totales']

        base_pct = (base / total) * 100
        mejora_pct = (mejora / total) * 100
        diff_pct = mejora_pct - base_pct

        print(f"**{label}:**")
        print(f"- Baseline: {base}/{total} ({base_pct:.1f}%)")
        print(f"- Mejora: {mejora}/{total} ({mejora_pct:.1f}%)")
        print(f"- Δ: {diff_pct:+.1f}% {'✅' if diff_pct > 0 else '➖'}")
        print()

    # Análisis de tiempo promedio
    print("### ⏱️  Tiempo Promedio por Pedido\n")
    for label, _, _ in escenarios:
        if label not in datos:
            continue
        base = datos[label]['baseline']['tiempo_promedio_pedido_ticks']
        mejora = datos[label]['mejora']['tiempo_promedio_pedido_ticks']

        if base is None or mejora is None:
            continue

        diff, pct = calcular_mejora(base, mejora)

        print(f"**{label}:**")
        print(f"- Baseline: {base:.1f} ticks")
        print(f"- Mejora: {mejora:.1f} ticks")
        print(f"- Δ: {diff:+.1f} ticks ({pct:+.1f}%) {'✅' if diff < 0 else '❌'}")
        print()

    # Análisis de distancia total
    print("### 🚗 Distancia Total Recorrida\n")
    for label, _, _ in escenarios:
        if label not in datos:
            continue
        base = datos[label]['baseline']['distancia_total_celdas']
        mejora = datos[label]['mejora']['distancia_total_celdas']

        diff, pct = calcular_mejora(base, mejora)

        print(f"**{label}:**")
        print(f"- Baseline: {base:,} celdas")
        print(f"- Mejora: {mejora:,} celdas")
        print(f"- Δ: {diff:+,} celdas ({pct:+.1f}%) {'✅' if diff < 0 else '❌'}")
        print()

    # Análisis de congestión
    print("### 🚦 Eventos de Congestión (Deadlocks + Alto)\n")
    for label, _, _ in escenarios:
        if label not in datos:
            continue
        base_dl = datos[label]['baseline']['deadlock']
        mejora_dl = datos[label]['mejora']['deadlock']
        base_alto = datos[label]['baseline']['eventos_alto']
        mejora_alto = datos[label]['mejora']['eventos_alto']

        base_total = base_dl + base_alto
        mejora_total = mejora_dl + mejora_alto

        diff, pct = calcular_mejora(base_total, mejora_total)

        print(f"**{label}:**")
        print(
            f"- Baseline: {base_total:,} eventos (DL:{base_dl}, Alto:{base_alto})")
        print(
            f"- Mejora: {mejora_total:,} eventos (DL:{mejora_dl}, Alto:{mejora_alto})")
        print(f"- Δ: {diff:+,} eventos ({pct:+.1f}%) {'✅' if diff < 0 else '❌'}")
        print()

    print("\n## 3. CONCLUSIONES\n")

    # Calcular mejoras promedio
    mejoras_tiempo = []
    mejoras_distancia = []
    mejoras_completitud = []

    for label in ["20r", "40r", "60r", "100r", "200r"]:
        if label not in datos:
            continue

        # Tiempo
        base_t = datos[label]['baseline']['tiempo_promedio_pedido_ticks']
        mejora_t = datos[label]['mejora']['tiempo_promedio_pedido_ticks']
        if base_t and mejora_t:
            _, pct_t = calcular_mejora(base_t, mejora_t)
            mejoras_tiempo.append(pct_t)

        # Distancia
        base_d = datos[label]['baseline']['distancia_total_celdas']
        mejora_d = datos[label]['mejora']['distancia_total_celdas']
        _, pct_d = calcular_mejora(base_d, mejora_d)
        mejoras_distancia.append(pct_d)

        # Completitud
        base_c = datos[label]['baseline']['pedidos_completados']
        mejora_c = datos[label]['mejora']['pedidos_completados']
        _, pct_c = calcular_mejora(base_c, mejora_c)
        mejoras_completitud.append(pct_c)

    if mejoras_tiempo:
        print(
            f"**Tiempo Promedio:** {sum(mejoras_tiempo)/len(mejoras_tiempo):+.1f}% promedio")
    if mejoras_distancia:
        print(
            f"**Distancia Total:** {sum(mejoras_distancia)/len(mejoras_distancia):+.1f}% promedio")
    if mejoras_completitud:
        print(
            f"**Completitud:** {sum(mejoras_completitud)/len(mejoras_completitud):+.1f}% promedio")

    print("\n### Validación de Hipótesis (Entregable 3):\n")
    print("| Objetivo | Meta | Resultado | Estado |")
    print("|----------|------|-----------|---------|")

    # Hipótesis tiempo
    if mejoras_tiempo:
        avg_tiempo = sum(mejoras_tiempo) / len(mejoras_tiempo)
        estado_t = "✅ Cumplido" if avg_tiempo <= - \
            20 else "⚠️  Parcial" if avg_tiempo < 0 else "❌ No cumplido"
        print(f"| Reducir Tiempo | -30% | {avg_tiempo:+.1f}% | {estado_t} |")

    # Hipótesis distancia
    if mejoras_distancia:
        avg_dist = sum(mejoras_distancia) / len(mejoras_distancia)
        estado_d = "✅ Cumplido" if avg_dist <= - \
            20 else "⚠️  Parcial" if avg_dist < 0 else "❌ No cumplido"
        print(f"| Reducir Distancia | -20% | {avg_dist:+.1f}% | {estado_d} |")

    # Hipótesis completitud
    if datos.get("200r"):  # Usar el caso más estresante (200 robots)
        mejora_200_comp = datos["200r"]['mejora']['pedidos_completados']
        total_200 = datos["200r"]['mejora']['pedidos_totales']
        pct_comp = (mejora_200_comp / total_200) * 100
        estado_c = "✅ Cumplido" if pct_comp >= 95 else "⚠️  Parcial"
        print(
            f"| Completitud ≥95% (200r) | 95% | {pct_comp:.1f}% | {estado_c} |")
    elif datos.get("60r"):  # Fallback al anterior
        mejora_60_comp = datos["60r"]['mejora']['pedidos_completados']
        total_60 = datos["60r"]['mejora']['pedidos_totales']
        pct_comp = (mejora_60_comp / total_60) * 100
        estado_c = "✅ Cumplido" if pct_comp >= 95 else "⚠️  Parcial"
        print(
            f"| Completitud ≥95% (60r) | 95% | {pct_comp:.1f}% | {estado_c} |")

    print("\n" + "="*80)
    print("✅ Análisis completado")
    print("="*80 + "\n")


if __name__ == "__main__":
    generar_tabla_comparativa()
