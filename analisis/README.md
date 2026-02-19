# 📊 Scripts de Análisis

Este directorio contiene scripts para analizar y comparar las simulaciones.

## Scripts Principales

### 🎯 generar_todo_visualizaciones.py
**Propósito:** Script maestro que genera todas las visualizaciones
**Ejecutar:** `python generar_todo_visualizaciones.py`
**Genera:**
- Videos de simulación
- Heatmaps de congestión
- Comparaciones visuales
- Reporte HTML interactivo

### 📊 analizador_estadistico.py
**Propósito:** Análisis estadístico profundo de métricas
**Ejecutar:** `python analizador_estadistico.py`
**Genera:** `outputs/analisis_estadistico_seed1_vs_seed42.md`

### 🔍 comparador_visual_seed1_vs_seed42.py
**Propósito:** Crea comparaciones visuales lado a lado
**Genera:** Imágenes PNG y reporte HTML

### 📈 analizar_metricas_comparativas.py
**Propósito:** Análisis rápido de métricas de 10 semillas
**Ejecutar:** `python analizar_metricas_comparativas.py`

## Ejecución desde este directorio

```bash
# Cambiar a directorio raíz del proyecto
cd ..

# Ejecutar scripts
python analisis/generar_todo_visualizaciones.py
python analisis/analizador_estadistico.py
```

## Notas
- Estos scripts fueron creados para el análisis de 10 semillas
- Identificaron que seed1 tiene 54 deadlocks (problema crítico)
- Justifican selección de Eje C (Coordinación Multirobótica)
