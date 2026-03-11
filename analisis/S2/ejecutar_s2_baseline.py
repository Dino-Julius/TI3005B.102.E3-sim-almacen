#!/usr/bin/env python3
"""
Script: Ejecutar S2 Baseline
Propósito: Generar datos baseline corregidos (caso único 200r) para comparativa
Ubicación: analisis/S2/
Ejecución: python3 ejecutar_s2_baseline.py
"""

import subprocess
import sys
from pathlib import Path
import shutil

# Navegar a raíz del proyecto
PROJECT_ROOT = Path(__file__).parent.parent.parent
print("📊 EJECUTANDO BENCHMARK S2 BASELINE (caso único 200r)")
print(f"Directorio de trabajo: {PROJECT_ROOT}")
print("="*60)
print()

ESCENARIO = "seed1"
TICKS = 10000
ROBOTS = 200
LABEL = "200r"

output_dir = PROJECT_ROOT / "outputs/S2_baseline_200r"
output_dir.mkdir(parents=True, exist_ok=True)

print(f"▶️  Ejecutando S2_baseline_{LABEL} ({ROBOTS} robots)...")

try:
    # Ejecutar simulación baseline reproducible
    result = subprocess.run(
        [
            sys.executable, "demo_final.py",
            "--escenario", ESCENARIO,
            "--robots", str(ROBOTS),
            "--ticks", str(TICKS),
            "--modo_asignacion", "baseline",
            "--salida_metricas", "outputs/S2_baseline_200r/metricas.json",
        ],
        cwd=str(PROJECT_ROOT),
        capture_output=True,
        timeout=1200,
        text=True,
    )

    if result.returncode != 0:
        print("❌ Error en S2_baseline_200r")
        print(f"   stdout: {result.stdout[:400]}")
        print(f"   stderr: {result.stderr[:400]}")
        sys.exit(1)

    source_dir = PROJECT_ROOT / f"outputs/{ESCENARIO}"
    if source_dir.exists():
        for name in ["anaqueles.json", "estaciones.json", "pedidos.json", "spawn.json", "layout.npy"]:
            src = source_dir / name
            if src.exists():
                shutil.copy(src, output_dir)

    print("✅ S2_baseline_200r completado")

except subprocess.TimeoutExpired:
    print("❌ Timeout en S2_baseline_200r (>20min)")
    sys.exit(1)
except Exception as e:
    print(f"❌ Excepción en S2_baseline_200r: {e}")
    sys.exit(1)

print("="*60)
print(f"✅ Benchmark baseline finalizado")
print()
print("Exitosos: 1/1")
print("  ✓ outputs/S2_baseline_200r/metricas.json")

print()
print("Próximo paso:")
print("  python analisis/S2/generar_comparativa_s2.py")
print()
