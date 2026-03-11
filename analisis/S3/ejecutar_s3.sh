#!/bin/bash
# Entregable 4 (S3): estabilidad, robustez y escalabilidad
# Ejecutar desde la raiz del proyecto: ./analisis/S3/ejecutar_s3.sh

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT_DIR"

echo "=========================================="
echo "S3 - ENTREGABLE 4 (MEJORA A+C)"
echo "=========================================="
echo ""
echo "Escenarios:"
echo "  A) S3_alta_densidad_400r   (400 robots, 600 pedidos, 10k ticks)"
echo "  B) S3_burst_200r_1200      (200 robots, 1200 pedidos, 15k ticks)"
echo "  C) S3_var_400r_1200        (400 robots, 1200 pedidos, 15k ticks)"
echo ""

# 1) Preparar escenarios con el mismo layout de referencia (seed1)
for esc in S3_alta_densidad_400r S3_burst_200r_1200 S3_var_400r_1200; do
  mkdir -p "outputs/${esc}"
  cp outputs/seed1/layout.npy "outputs/${esc}/"
  cp outputs/seed1/anaqueles.json "outputs/${esc}/"
  cp outputs/seed1/estaciones.json "outputs/${esc}/"
  cp outputs/seed1/spawn.json "outputs/${esc}/"
done

echo "[OK] Layout base copiado a escenarios S3"

echo ""
echo "▶ Escenario A: alta densidad"
python generador_pedidos.py --escenario S3_alta_densidad_400r --seed 1 --pedidos 600 --burst
python demo_final.py --escenario S3_alta_densidad_400r --robots 400 --ticks 10000 --modo_asignacion mejora --salida_metricas outputs/S3_alta_densidad_400r/metricas.json

echo ""
echo "▶ Escenario B: burst severo"
python generador_pedidos.py --escenario S3_burst_200r_1200 --seed 1 --pedidos 1200 --burst
python demo_final.py --escenario S3_burst_200r_1200 --robots 200 --ticks 15000 --modo_asignacion mejora --salida_metricas outputs/S3_burst_200r_1200/metricas.json

echo ""
echo "▶ Escenario C: variacion de robots"
python generador_pedidos.py --escenario S3_var_400r_1200 --seed 1 --pedidos 1200 --burst
python demo_final.py --escenario S3_var_400r_1200 --robots 400 --ticks 15000 --modo_asignacion mejora --salida_metricas outputs/S3_var_400r_1200/metricas.json

echo ""
echo "▶ Generando reporte comparativo S3..."
python analisis/S3/generar_reporte_s3.py

echo ""
echo "✅ S3 completado"
echo "- Métricas A: outputs/S3_alta_densidad_400r/metricas.json"
echo "- Métricas B: outputs/S3_burst_200r_1200/metricas.json"
echo "- Métricas C: outputs/S3_var_400r_1200/metricas.json"
echo "- Reporte   : analisis/S3/reporte_s3.md"
