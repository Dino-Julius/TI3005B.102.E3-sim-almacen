#!/bin/bash
# Ejecutar escenario S2 - Estrés de Flota con MEJORA Eje A
# Ejecutar desde: analisis/S2/

echo "=========================================="
echo "S2 - ESTRÉS DE FLOTA (CON MEJORA EJE A)"
echo "=========================================="
echo ""

# Cambiar al directorio raíz del proyecto
cd "$(dirname "$0")/../.." || exit 1

# Usar layout seed1 existente (300x200)
ESCENARIO="seed1"

# S2.1: 20 robots (referencia con mejora)
echo "► S2.1 Mejora: 20 robots..."
python demo_final.py --escenario ${ESCENARIO} --robots 20 --ticks 10000 --salida_metricas outputs/S2_mejora_20r/metricas.json
mkdir -p outputs/S2_mejora_20r
cp outputs/${ESCENARIO}/*.json outputs/S2_mejora_20r/ 2>/dev/null || true
cp outputs/${ESCENARIO}/layout.npy outputs/S2_mejora_20r/ 2>/dev/null || true

# S2.2: 40 robots (x2 - estrés moderado)
echo "► S2.2 Mejora: 40 robots (x2)..."
python demo_final.py --escenario ${ESCENARIO} --robots 40 --ticks 10000 --salida_metricas outputs/S2_mejora_40r/metricas.json
mkdir -p outputs/S2_mejora_40r
cp outputs/${ESCENARIO}/*.json outputs/S2_mejora_40r/ 2>/dev/null || true
cp outputs/${ESCENARIO}/layout.npy outputs/S2_mejora_40r/ 2>/dev/null || true

# S2.3: 60 robots (x3 - estrés alto)
echo "► S2.3 Mejora: 60 robots (x3)..."
python demo_final.py --escenario ${ESCENARIO} --robots 60 --ticks 10000 --salida_metricas outputs/S2_mejora_60r/metricas.json
mkdir -p outputs/S2_mejora_60r
cp outputs/${ESCENARIO}/*.json outputs/S2_mejora_60r/ 2>/dev/null || true
cp outputs/${ESCENARIO}/layout.npy outputs/S2_mejora_60r/ 2>/dev/null || true

# S2.4: 100 robots (x5 - estrés muy alto)
echo "► S2.4 Mejora: 100 robots (x5)..."
python demo_final.py --escenario ${ESCENARIO} --robots 100 --ticks 10000 --salida_metricas outputs/S2_mejora_100r/metricas.json
mkdir -p outputs/S2_mejora_100r
cp outputs/${ESCENARIO}/*.json outputs/S2_mejora_100r/ 2>/dev/null || true
cp outputs/${ESCENARIO}/layout.npy outputs/S2_mejora_100r/ 2>/dev/null || true

# S2.5: 200 robots (x10 - estrés extremo)
echo "► S2.5 Mejora: 200 robots (x10)..."
python demo_final.py --escenario ${ESCENARIO} --robots 200 --ticks 10000 --salida_metricas outputs/S2_mejora_200r/metricas.json
mkdir -p outputs/S2_mejora_200r
cp outputs/${ESCENARIO}/*.json outputs/S2_mejora_200r/ 2>/dev/null || true
cp outputs/${ESCENARIO}/layout.npy outputs/S2_mejora_200r/ 2>/dev/null || true

echo ""
echo "✅ Benchmarks con mejora completados"
echo "Resultados en:"
echo "  - outputs/S2_mejora_20r/metricas.json"
echo "  - outputs/S2_mejora_40r/metricas.json"
echo "  - outputs/S2_mejora_60r/metricas.json"
echo "  - outputs/S2_mejora_100r/metricas.json"
echo "  - outputs/S2_mejora_200r/metricas.json"
echo ""
echo "Siguiente paso: python analisis/S2/generar_comparativa_s2.py"
