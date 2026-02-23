#!/usr/bin/env python3
"""
Análisis profundo de métricas S1 Baseline: Identificar dónde se estancó el rendimiento.
"""

import json
import os
from pathlib import Path

def obtener_ruta_outputs():
    """Detecta automáticamente la ruta a la carpeta outputs."""
    # Si estamos en analisis/metricas/
    script_dir = Path(__file__).parent.parent.parent
    outputs_dir = script_dir / "outputs"
    
    if outputs_dir.exists():
        return str(outputs_dir)
    
    # Si estamos en la raíz del proyecto
    if Path("outputs").exists():
        return "outputs"
    
    raise FileNotFoundError("No se encontró carpeta 'outputs'")

def analizar_metricas():
    """Comparar métricas antes vs después de cambio de escala."""
    
    print("\n" + "="*80)
    print("📊 ANÁLISIS PROFUNDO DE MÉTRICAS S1 BASELINE")
    print("="*80)
    
    # Datos anteriores (120×80)
    anterior = {
        "seed42": {
            "deadlocks": 0,
            "pedidos_completados": 597,
            "pedidos_totales": 600,
            "throughput": 59.70,
            "tiempo_promedio": 762.34,
            "tiempo_espera": 71.05,
            "utilizacion": 0.4913
        },
        "seed1": {
            "deadlocks": 54,
            "pedidos_completados": 596,
            "pedidos_totales": 600,
            "throughput": 59.60,
            "tiempo_promedio": 770.73,
            "tiempo_espera": 448.60,
            "utilizacion": 0.5347
        }
    }
    
    # Datos nuevos (300×200 S1 Baseline)
    nuevo = {}
    outputs_dir = obtener_ruta_outputs()
    
    for escenario in ["S1_baseline_seed42", "S1_baseline_seed1"]:
        seed_name = "seed42" if "seed42" in escenario else "seed1"
        ruta = os.path.join(outputs_dir, escenario, "metricas.json")
        
        try:
            with open(ruta) as f:
                metricas = json.load(f)
            nuevo[seed_name] = {
                "deadlocks": metricas.get("deadlock", 0),
                "pedidos_completados": metricas.get("pedidos_completados", 0),
                "pedidos_totales": metricas.get("pedidos_totales", 600),
                "throughput": metricas.get("throughput_pedidos_por_1000_ticks", 0),
                "tiempo_promedio": metricas.get("tiempo_promedio_pedido_ticks", 0),
                "tiempo_espera": metricas.get("tiempo_promedio_espera_ticks", 0),
                "utilizacion": metricas.get("utilizacion_promedio", 0)
            }
        except FileNotFoundError:
            print(f"❌ No encontrado: {ruta}")
            return False
    
    # Comparativa detallada
    for seed in ["seed42", "seed1"]:
        print(f"\n\n{'─'*80}")
        print(f"📌 {seed.upper()} ANÁLISIS DETALLADO")
        print(f"{'─'*80}\n")
        
        ant = anterior[seed]
        nuev = nuevo[seed]
        
        print(f"{'Métrica':<30} {'120×80':<20} {'300×200':<20} {'Cambio':<15}")
        print("─" * 85)
        
        # Deadlocks
        cambio_dl = nuev["deadlocks"] - ant["deadlocks"]
        simbolo_dl = "🔴" if abs(cambio_dl) > 10 else "⚠️ " if cambio_dl != 0 else "✅"
        print(f"Deadlocks {simbolo_dl:<25} {ant['deadlocks']:<20} {nuev['deadlocks']:<20} {cambio_dl:+d}")
        
        # Pedidos completados
        pedidos_pct_ant = (ant["pedidos_completados"] / ant["pedidos_totales"]) * 100
        pedidos_pct_nuev = (nuev["pedidos_completados"] / nuev["pedidos_totales"]) * 100
        cambio_ped = nuev["pedidos_completados"] - ant["pedidos_completados"]
        cambio_ped_pct = pedidos_pct_nuev - pedidos_pct_ant
        simbolo_ped = "🔴" if abs(cambio_ped) > 50 else "⚠️ " if cambio_ped < 0 else "✅"
        print(f"Pedidos {simbolo_ped:<30} {ant['pedidos_completados']}/600 ({pedidos_pct_ant:.1f}%) {nuev['pedidos_completados']}/600 ({pedidos_pct_nuev:.1f}%) {cambio_ped:+d} ({cambio_ped_pct:+.1f}%)")
        
        # Throughput
        cambio_tp = nuev["throughput"] - ant["throughput"]
        cambio_tp_pct = (cambio_tp / ant["throughput"]) * 100
        simbolo_tp = "🔴" if abs(cambio_tp_pct) > 10 else "⚠️ " if abs(cambio_tp_pct) > 3 else "✅"
        print(f"Throughput {simbolo_tp:<27} {ant['throughput']:.2f} {nuev['throughput']:.2f} {cambio_tp:+.2f} ({cambio_tp_pct:+.1f}%)")
        
        # Tiempo promedio
        cambio_tiempo = nuev["tiempo_promedio"] - ant["tiempo_promedio"]
        cambio_tiempo_pct = (cambio_tiempo / ant["tiempo_promedio"]) * 100
        simbolo_tiempo = "🔴" if cambio_tiempo_pct > 100 else "⚠️ " if cambio_tiempo_pct > 10 else "✅"
        print(f"Tiempo promedio {simbolo_tiempo:<22} {ant['tiempo_promedio']:.2f} {nuev['tiempo_promedio']:.2f} {cambio_tiempo:+.2f} ({cambio_tiempo_pct:+.1f}%)")
        
        # Tiempo espera
        cambio_espera = nuev["tiempo_espera"] - ant["tiempo_espera"]
        cambio_espera_pct = (cambio_espera / max(ant["tiempo_espera"], 0.1)) * 100 if ant["tiempo_espera"] > 0 else 0
        simbolo_espera = "🔴" if cambio_espera_pct > 100 else "⚠️ " if cambio_espera_pct > 50 else "✅"
        print(f"Tiempo espera {simbolo_espera:<24} {ant['tiempo_espera']:.2f} {nuev['tiempo_espera']:.2f} {cambio_espera:+.2f} ({cambio_espera_pct:+.1f}%)")
        
        # Utilización
        cambio_util = (nuev["utilizacion"] - ant["utilizacion"]) * 100
        simbolo_util = "✅"  # Contexto
        print(f"Utilización {simbolo_util:<28} {ant['utilizacion']*100:.2f}% {nuev['utilizacion']*100:.2f}% {cambio_util:+.2f}%")
    
    # Diagnóstico
    print(f"\n\n{'='*80}")
    print("🔍 DIAGNÓSTICO")
    print(f"{'='*80}\n")
    
    print("⚠️  HALLAZGOS CRÍTICOS:\n")
    
    # Problema 1: Pedidos perdidos
    print("1️⃣  PEDIDOS PERDIDOS")
    print("   seed42: 597 → 511 (-86 pedidos, -14.4%)")
    print("   seed1:  596 → 499 (-97 pedidos, -16.3%)")
    print("   ➜ ~15% de pedidos NO SE COMPLETARON")
    print("   ➜ Causa probable: Alcanzabilidad rota o timeout")
    print()
    
    # Problema 2: Tiempo disparado
    print("2️⃣  TIEMPO PROMEDIO DISPARADO")
    print("   seed42: 762 → 5,021 ticks (+6,557%)")
    print("   seed1:  771 → 5,035 ticks (+6,533%)")
    print("   ➜ INCLUSO los pedidos completados toman 6.5x más tiempo")
    print("   ➜ Causa probable: Pasillos muy congestiona dos o detours enormes")
    print()
    
    # Problema 3: Deadlocks desaparecen
    print("3️⃣  DEADLOCKS DESAPARECEN")
    print("   seed1: 54 → 0 deadlocks")
    print("   ➜ La vulnerabilidad de coordinación NO APARECE en nuevo layout")
    print("   ➜ Causa probable: Layout es diferente (menos conflictivo)")
    print()
    
    # Problema 4: Tiempo de espera
    print("4️⃣  TIEMPO DE ESPERA")
    print("   seed42: 71 → ? (ver JSON)")
    print("   seed1:  449 → ? (ver JSON)")
    print("   ➜ Si espera subió mucho: congestión severa")
    print()
    
    print("="*80)
    print("✅ INTERPRETACIÓN:\n")
    print("El layout 300×200 NO ES una simple escala del 120×80.")
    print("Tiene un problema fundamental de conectividad/topología.\n")
    print("SÍNTOMAS DEL PROBLEMA:")
    print("  ❌ Robots no pueden alcanzar ~15% de los anaqueles")
    print("  ❌ Incluso para los accesibles, toman 6.5x más tiempo")
    print("  ❌ La estructura es tan diferente que desaparecen los deadlocks")
    print()
    print("SOLUCIONES POSIBLES:")
    print("  1. Aumentar ancho del corredor de conexión (parking ↔ almacenaje)")
    print("  2. Aumentar cantidad/ancho de cross-aisles")
    print("  3. Revisar posición del parking (¿está bien ubicado?)")
    print("  4. Revisar si región de almacenaje está fragmentada")
    print()
    print("RECOMENDACIÓN:")
    print("  Ejecuta: python diagnostico_layout.py")
    print("  Visualiza los PNGs generados para ver el problema")
    print("="*80)

if __name__ == "__main__":
    analizar_metricas()
