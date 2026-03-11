#!/bin/bash
# Pipeline S2 corregido: comparación 200r baseline vs mejora
# Ejecutar desde: analisis/S2/

set -euo pipefail

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  PIPELINE S2 CORREGIDO (200R): BASELINE VS MEJORA             ║"
echo "║  Ejecutando benchmarks y análisis automáticamente              ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Cambiar a raíz del proyecto
cd "$(dirname "$0")/../.." || exit 1
ROOT_DIR=$(pwd)

echo "📁 Directorio: $ROOT_DIR"
echo ""

# Paso 1: Ejecutar baseline 200r
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "PASO 1: Ejecutar Benchmark Baseline (200r)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "⏳ Esto tomará varios minutos..."
echo ""

cd analisis/S2
chmod +x ejecutar_s2_baseline.sh ejecutar_s2_mejora.sh
./ejecutar_s2_baseline.sh

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "PASO 2: Ejecutar Benchmark Mejora (200r, Eje A + Eje C)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

./ejecutar_s2_mejora.sh

cd ../..

echo ""
echo ""

# Paso 3: Generar análisis
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "PASO 3: Generar Análisis Comparativo"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

python analisis/S2/generar_comparativa_s2.py | tee S2_resultados.txt

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ PIPELINE COMPLETADO"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📊 Resultados:"
echo "  - Baseline: outputs/S2_baseline_200r/metricas.json"
echo "  - Mejora  : outputs/S2_mejora_200r/metricas.json"
echo "  - Análisis: S2_resultados.txt"
echo ""
echo "📝 Próximos pasos:"
echo "  1. Lee S2_resultados.txt"
echo "  2. Copia la tabla comparativa al Entregable 3"
echo "  3. Documenta observaciones y conclusiones"
echo ""
echo "✨ ¡Listo!"
