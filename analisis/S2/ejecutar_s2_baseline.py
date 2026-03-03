#!/usr/bin/env python3
"""
Script: Ejecutar S2 Baseline
Propósito: Generar datos de baseline (sin optimizaciones Eje A) para comparativa
Ubicación: analisis/S2/
Ejecución: python3 ejecutar_s2_baseline.py
"""

import subprocess
import sys
from pathlib import Path
import shutil

# Navegar a raíz del proyecto
PROJECT_ROOT = Path(__file__).parent.parent.parent
print(f"📊 EJECUTANDO BENCHMARK S2 BASELINE (sin optimizaciones)")
print(f"Directorio de trabajo: {PROJECT_ROOT}")
print("="*60)
print()

# Configuraciones a ejecutar
CONFIGS = [
    ("20r", 20),
    ("40r", 40),
    ("60r", 60),
    ("100r", 100),
    ("200r", 200),
]

ESCENARIO = "seed1"
TICKS = 10000

failed = []
success = []

for label, robots in CONFIGS:
    print(f"▶️  Ejecutando S2_baseline_{label} ({robots} robots)...")

    try:
        # Ejecutar simulación
        result = subprocess.run(
            [
                sys.executable, "demo_final.py",
                "--escenario", ESCENARIO,
                "--robots", str(robots),
                "--ticks", str(TICKS),
            ],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            timeout=600,  # 10 minutos máx por config
            text=True
        )

        if result.returncode == 0:
            # Copiar archivos al directorio de baseline
            output_dir = PROJECT_ROOT / f"outputs/S2_baseline_{label}"
            output_dir.mkdir(parents=True, exist_ok=True)

            source_dir = PROJECT_ROOT / f"outputs/{ESCENARIO}"
            if source_dir.exists():
                for file in source_dir.glob("*.json"):
                    shutil.copy(file, output_dir)
                for file in source_dir.glob("*.npy"):
                    shutil.copy(file, output_dir)

            print(f"✅ S2_baseline_{label} completado")
            success.append(label)
        else:
            print(f"❌ Error en S2_baseline_{label}")
            print(f"   stdout: {result.stdout[:200]}")
            print(f"   stderr: {result.stderr[:200]}")
            failed.append(label)

    except subprocess.TimeoutExpired:
        print(f"❌ Timeout en S2_baseline_{label} (>10min)")
        failed.append(label)
    except Exception as e:
        print(f"❌ Excepción en S2_baseline_{label}: {e}")
        failed.append(label)

    print()

print("="*60)
print(f"✅ Benchmark baseline finalizado")
print()
print(f"Exitosos: {len(success)}/5")
for label in success:
    print(f"  ✓ outputs/S2_baseline_{label}/metricas.json")

if failed:
    print(f"\nFallidos: {len(failed)}/5")
    for label in failed:
        print(f"  ✗ S2_baseline_{label}")

print()
print("Próximo paso:")
print("  python analisis/S2/generar_comparativa_s2.py")
print()
