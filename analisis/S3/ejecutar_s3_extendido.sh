#!/bin/bash
# S3 extendido: escenarios de estres con series temporales
# Uso:
#   ./analisis/S3/ejecutar_s3_extendido.sh
#   TICKS_D=60000 TICKS_E=120000 VENTANA=500 ./analisis/S3/ejecutar_s3_extendido.sh

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT_DIR"
export PYTHONPATH="$ROOT_DIR:${PYTHONPATH:-}"

TICKS_D="${TICKS_D:-60000}"
TICKS_E="${TICKS_E:-120000}"
VENTANA="${VENTANA:-500}"

ESC_D="S3_estres_D_200r_6000"
ESC_E="S3_estres_E_200r_12000"

BASE_ESC="S1_baseline_seed1"

for esc in "$ESC_D" "$ESC_E"; do
  mkdir -p "outputs/${esc}"
  cp "outputs/${BASE_ESC}/layout.npy" "outputs/${esc}/"
  cp "outputs/${BASE_ESC}/anaqueles.json" "outputs/${esc}/"
  cp "outputs/${BASE_ESC}/estaciones.json" "outputs/${esc}/"
  cp "outputs/${BASE_ESC}/spawn.json" "outputs/${esc}/"
done

echo "=========================================="
echo "S3 EXTENDIDO - ESCENARIOS DE ESTRES"
echo "=========================================="
echo "D) ${ESC_D} (200 robots, 6000 pedidos, ticks=${TICKS_D})"
echo "E) ${ESC_E} (200 robots, 12000 pedidos, ticks=${TICKS_E})"
echo "Ventana temporal: ${VENTANA} ticks"
echo ""

echo "▶ Escenario D: estres alto"
python generador_pedidos.py --escenario "$ESC_D" --seed 1 --pedidos 6000 --burst
python analisis/S3/registrar_metricas_temporales.py \
  --escenario "$ESC_D" \
  --robots 200 \
  --ticks "$TICKS_D" \
  --seed 1 \
  --ventana "$VENTANA" \
  --modo_asignacion mejora
python analisis/S3/generar_graficas_temporales.py --escenario "$ESC_D"

echo ""
echo "▶ Escenario E: estres extremo"
python generador_pedidos.py --escenario "$ESC_E" --seed 1 --pedidos 12000 --burst
python analisis/S3/registrar_metricas_temporales.py \
  --escenario "$ESC_E" \
  --robots 200 \
  --ticks "$TICKS_E" \
  --seed 1 \
  --ventana "$VENTANA" \
  --modo_asignacion mejora
python analisis/S3/generar_graficas_temporales.py --escenario "$ESC_E"

echo ""
echo "✅ S3 extendido completado"
echo "- Metricas D: outputs/${ESC_D}/metricas.json"
echo "- Series D  : outputs/${ESC_D}/metricas_temporales.json"
echo "- CSV D     : outputs/${ESC_D}/metricas_temporales.csv"
echo "- Metricas E: outputs/${ESC_E}/metricas.json"
echo "- Series E  : outputs/${ESC_E}/metricas_temporales.json"
echo "- CSV E     : outputs/${ESC_E}/metricas_temporales.csv"
echo "- Graficas  : analisis/S3/graficos/${ESC_D} y analisis/S3/graficos/${ESC_E}"
