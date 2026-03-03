#!/bin/bash
# Pipeline completo S2: Estrés de Flota - Entregable 3
# Ejecutar desde: analisis/S2/

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║  PIPELINE COMPLETO S2: ESTRÉS DE FLOTA - ENTREGABLE 3         ║"
echo "║  Ejecutando benchmarks y análisis automáticamente               ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Cambiar a raíz del proyecto
cd "$(dirname "$0")/../.." || exit 1
ROOT_DIR=$(pwd)

echo "📁 Directorio: $ROOT_DIR"
echo ""

# Paso 1: Ejecutar benchmarks
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "PASO 1: Ejecutar Benchmarks Mejora"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "⏳ Esto tomará aproximadamente 60 minutos..."
echo ""

cd analisis/S2
chmod +x ejecutar_s2_mejora.sh
./ejecutar_s2_mejora.sh

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Error durante la ejecución de benchmarks"
    exit 1
fi

cd ../..

echo ""
echo ""

# Paso 2: Generar análisis
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "PASO 2: Generar Análisis Comparativo"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

python analisis/S2/generar_comparativa_s2.py | tee S2_resultados.txt

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Error durante la generación de análisis"
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ PIPELINE COMPLETADO"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📊 Resultados:"
echo "  - Benchmarks: outputs/S2_mejora_*/metricas.json"
echo "  - Análisis: S2_resultados.txt"
echo ""
echo "📝 Próximos pasos:"
echo "  1. Lee S2_resultados.txt"
echo "  2. Copia la tabla comparativa al Entregable 3"
echo "  3. Documenta observaciones y conclusiones"
echo ""
echo "📚 Documentación disponible:"
echo "  - analisis/S2/REPORTE_FINAL_S2.md"
echo "  - analisis/S2/docs/DOCUMENTACION_TECNICA_MEJORA_EJE_A.md"
echo "  - analisis/S2/docs/GUIA_EJECUCION_S2.md"
echo "  - analisis/S2/docs/RESUMEN_EJECUTIVO.md"
echo ""
echo "✨ ¡Listo!"
