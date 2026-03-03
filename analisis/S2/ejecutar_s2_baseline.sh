#!/bin/bash
# Ejecutar escenario S2 - Estrés de Flota (BASELINE sin mejora)
# Para correr baseline, primero revertir cambios en sim_core.py
# Ejecutar desde: analisis/S2/

echo "=========================================="
echo "S2 - ESTRÉS DE FLOTA (BASELINE)"
echo "=========================================="
echo ""
echo "IMPORTANTE: Este script requiere código SIN la mejora"
echo "Revertir sim_core.py a versión baseline antes de ejecutar"
echo ""

# Cambiar al directorio raíz del proyecto
cd "$(dirname "$0")/../.." || exit 1

# Usar layout seed1 existente (300x200)
ESCENARIO="seed1"

# S2.1: 20 robots (baseline de referencia)
echo "► S2.1 Baseline: 20 robots..."
python demo_final.py --escenario ${ESCENARIO} --robots 20 --ticks 10000 --salida_metricas outputs/S2_baseline_20r/metricas.json
mkdir -p outputs/S2_baseline_20r
cp outputs/${ESCENARIO}/*.json outputs/S2_baseline_20r/ 2>/dev/null || true
cp outputs/${ESCENARIO}/layout.npy outputs/S2_baseline_20r/ 2>/dev/null || true

# S2.2: 40 robots (x2)
echo "► S2.2 Baseline: 40 robots (x2)..."
python demo_final.py --escenario ${ESCENARIO} --robots 40 --ticks 10000 --salida_metricas outputs/S2_baseline_40r/metricas.json
mkdir -p outputs/S2_baseline_40r
cp outputs/${ESCENARIO}/*.json outputs/S2_baseline_40r/ 2>/dev/null || true
cp outputs/${ESCENARIO}/layout.npy outputs/S2_baseline_40r/ 2>/dev/null || true

# S2.3: 60 robots (x3)
echo "► S2.3 Baseline: 60 robots (x3)..."
python demo_final.py --escenario ${ESCENARIO} --robots 60 --ticks 10000 --salida_metricas outputs/S2_baseline_60r/metricas.json
mkdir -p outputs/S2_baseline_60r
cp outputs/${ESCENARIO}/*.json outputs/S2_baseline_60r/ 2>/dev/null || true
cp outputs/${ESCENARIO}/layout.npy outputs/S2_baseline_60r/ 2>/dev/null || true

# S2.4: 100 robots (x5 - estrés muy alto)
echo "► S2.4 Baseline: 100 robots (x5)..."
python demo_final.py --escenario ${ESCENARIO} --robots 100 --ticks 10000 --salida_metricas outputs/S2_baseline_100r/metricas.json
mkdir -p outputs/S2_baseline_100r
cp outputs/${ESCENARIO}/*.json outputs/S2_baseline_100r/ 2>/dev/null || true
cp outputs/${ESCENARIO}/layout.npy outputs/S2_baseline_100r/ 2>/dev/null || true

# S2.5: 200 robots (x10 - estrés extremo)
echo "► S2.5 Baseline: 200 robots (x10)..."
python demo_final.py --escenario ${ESCENARIO} --robots 200 --ticks 10000 --salida_metricas outputs/S2_baseline_200r/metricas.json
mkdir -p outputs/S2_baseline_200r
cp outputs/${ESCENARIO}/*.json outputs/S2_baseline_200r/ 2>/dev/null || true
cp outputs/${ESCENARIO}/layout.npy outputs/S2_baseline_200r/ 2>/dev/null || true

echo ""
echo "✅ Benchmarks baseline completados"
echo "Resultados en:"
echo "  - outputs/S2_baseline_20r/metricas.json"
echo "  - outputs/S2_baseline_40r/metricas.json"
echo "  - outputs/S2_baseline_60r/metricas.json"
echo "  - outputs/S2_baseline_100r/metricas.json"
echo "  - outputs/S2_baseline_200r/metricas.json"
