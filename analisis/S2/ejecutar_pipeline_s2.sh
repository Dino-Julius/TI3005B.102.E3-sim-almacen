#!/bin/bash
# Pipeline S2 corregido: comparación 200r baseline vs mejora
# Uso:
#   ./analisis/S2/ejecutar_pipeline_s2.sh               # Reejecuta baseline+mejora y genera comparativa
#   ./analisis/S2/ejecutar_pipeline_s2.sh --solo-analisis  # Solo usa métricas existentes

set -euo pipefail

SOLO_ANALISIS=0
if [[ "${1:-}" == "--solo-analisis" ]]; then
	SOLO_ANALISIS=1
fi

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  PIPELINE S2 CORREGIDO (200R): BASELINE VS MEJORA             ║"
if [[ "$SOLO_ANALISIS" -eq 1 ]]; then
	echo "║  Modo: solo análisis (NO ejecuta simulaciones)                ║"
else
	echo "║  Modo: completo (simulaciones + análisis)                     ║"
fi
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Cambiar a raíz del proyecto
cd "$(dirname "$0")/../.." || exit 1
ROOT_DIR=$(pwd)
ANALISIS_S2_DIR="$ROOT_DIR/analisis/S2"
S2_RESULTADOS="$ANALISIS_S2_DIR/S2_resultados.txt"

echo "📁 Directorio: $ROOT_DIR"
echo ""

if [[ "$SOLO_ANALISIS" -eq 0 ]]; then
	ESCENARIO="seed1"

	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	echo "PASO 1: Ejecutar Benchmark Baseline (200r)"
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	echo "⏳ Esto tomará varios minutos..."
	echo ""

	python demo_final.py --escenario ${ESCENARIO} --robots 200 --ticks 10000 --modo_asignacion baseline --salida_metricas outputs/S2_baseline_200r/metricas.json
	mkdir -p outputs/S2_baseline_200r
	cp outputs/${ESCENARIO}/anaqueles.json outputs/S2_baseline_200r/ 2>/dev/null || true
	cp outputs/${ESCENARIO}/estaciones.json outputs/S2_baseline_200r/ 2>/dev/null || true
	cp outputs/${ESCENARIO}/pedidos.json outputs/S2_baseline_200r/ 2>/dev/null || true
	cp outputs/${ESCENARIO}/spawn.json outputs/S2_baseline_200r/ 2>/dev/null || true
	cp outputs/${ESCENARIO}/layout.npy outputs/S2_baseline_200r/ 2>/dev/null || true

	echo ""
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	echo "PASO 2: Ejecutar Benchmark Mejora (200r, Eje A + Eje C)"
	echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	echo ""

	python demo_final.py --escenario ${ESCENARIO} --robots 200 --ticks 10000 --modo_asignacion mejora --salida_metricas outputs/S2_mejora_200r/metricas.json
	mkdir -p outputs/S2_mejora_200r
	cp outputs/${ESCENARIO}/anaqueles.json outputs/S2_mejora_200r/ 2>/dev/null || true
	cp outputs/${ESCENARIO}/estaciones.json outputs/S2_mejora_200r/ 2>/dev/null || true
	cp outputs/${ESCENARIO}/pedidos.json outputs/S2_mejora_200r/ 2>/dev/null || true
	cp outputs/${ESCENARIO}/spawn.json outputs/S2_mejora_200r/ 2>/dev/null || true
	cp outputs/${ESCENARIO}/layout.npy outputs/S2_mejora_200r/ 2>/dev/null || true

	echo ""
fi

if [[ ! -f outputs/S2_baseline_200r/metricas.json || ! -f outputs/S2_mejora_200r/metricas.json ]]; then
	echo "❌ Faltan métricas para comparar."
	echo "   Requeridos:"
	echo "   - outputs/S2_baseline_200r/metricas.json"
	echo "   - outputs/S2_mejora_200r/metricas.json"
	echo "   Ejecuta sin --solo-analisis para generarlos."
	exit 1
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "PASO 3: Generar Análisis Comparativo"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

python analisis/S2/generar_comparativa_s2.py | tee "$S2_RESULTADOS"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ PIPELINE COMPLETADO"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📊 Resultados:"
echo "  - Baseline: outputs/S2_baseline_200r/metricas.json"
echo "  - Mejora  : outputs/S2_mejora_200r/metricas.json"
echo "  - Análisis: analisis/S2/S2_resultados.txt"
echo ""
