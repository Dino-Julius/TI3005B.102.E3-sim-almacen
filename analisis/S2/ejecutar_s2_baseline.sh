#!/bin/bash
# Ejecutar escenario S2 - Estrés de Flota (BASELINE sin mejora)
# Ejecutar desde: analisis/S2/

set -euo pipefail

echo "=========================================="
echo "S2 - ESTRÉS DE FLOTA (BASELINE)"
echo "=========================================="
echo ""
echo "Modo reproducible: baseline"
echo ""

# Cambiar al directorio raíz del proyecto
cd "$(dirname "$0")/../.." || exit 1

# Usar layout seed1 existente (300x200)
ESCENARIO="seed1"

# S2 corregido por retro: caso único 200 robots
echo "► S2 Baseline corregido: 200 robots..."
python demo_final.py --escenario ${ESCENARIO} --robots 200 --ticks 10000 --modo_asignacion baseline --salida_metricas outputs/S2_baseline_200r/metricas.json
mkdir -p outputs/S2_baseline_200r
cp outputs/${ESCENARIO}/anaqueles.json outputs/S2_baseline_200r/ 2>/dev/null || true
cp outputs/${ESCENARIO}/estaciones.json outputs/S2_baseline_200r/ 2>/dev/null || true
cp outputs/${ESCENARIO}/pedidos.json outputs/S2_baseline_200r/ 2>/dev/null || true
cp outputs/${ESCENARIO}/spawn.json outputs/S2_baseline_200r/ 2>/dev/null || true
cp outputs/${ESCENARIO}/layout.npy outputs/S2_baseline_200r/ 2>/dev/null || true

echo ""
echo "✅ Benchmarks baseline completados"
echo "Resultados en:"
echo "  - outputs/S2_baseline_200r/metricas.json"
