# 📊 GUÍA: Generar Visualizaciones y Comparación seed1 vs seed42

## 🎯 Objetivo

Generar videos y análisis visuales para comparar:

- **seed1**: Con 54 deadlocks (problema visible)
- **seed42**: Con 0 deadlocks (baseline)

---

## 🚀 OPCIÓN 1: Ejecutar TODO de una vez (RECOMENDADO)

```bash
python generar_todo_visualizaciones.py
```

**Qué hace:**

1. ✅ Verifica qué visualizaciones ya existen
2. ✅ Genera seed1/simulacion.mp4 y heatmaps (si falta)
3. ✅ Genera comparaciones visuales lado a lado
4. ✅ Crea reporte HTML interactivo

**Tiempo estimado:** 10-20 minutos (depende de ffmpeg)

---

## 🚀 OPCIÓN 2: Paso a paso (Si algo falla)

### Paso 1: Generar visualización para seed1

```bash
python visualiza_simulacion.py --escenario seed1
```

Genera: `outputs/seed1/simulacion.mp4`, heatmaps PNG

### Paso 2: Verificar que seed42 existe

```bash
ls outputs/seed42/simulacion.mp4
```

Si no existe, genéralo:

```bash
python visualiza_simulacion.py --escenario seed42
```

### Paso 3: Generar comparación visual

```bash
python comparador_visual_seed1_vs_seed42.py
```

Genera:

- Gráficos comparativos de métricas
- Heatmaps lado a lado
- Reporte HTML

---

## 📁 Archivos que se generarán

Después de ejecutar, en `outputs/` tendrás:

```
outputs/
├── seed1/
│   ├── simulacion.mp4               ⭐ Video con deadlocks
│   ├── heatmap_esperas.png          🔥 Dónde pasan más tiempo (rojo = espera)
│   ├── heatmap_visitas.png          📍 Zonas más visitadas
│   └── heatmap_ratio.png            📈 Eficiencia por zona
│
├── seed42/
│   ├── simulacion.mp4               ⭐ Video sin deadlocks (baseline)
│   ├── heatmap_esperas.png
│   ├── heatmap_visitas.png
│   └── heatmap_ratio.png
│
├── comparacion_seed1_vs_seed42_metricas.png    📊 Gráfico comparativo
├── comparacion_heatmap_esperas_seed1_vs_seed42.png
├── comparacion_heatmap_visitas_seed1_vs_seed42.png
├── comparacion_heatmap_ratio_seed1_vs_seed42.png
│
└── reporte_comparacion_visual.html              ⭐⭐⭐ ABRIR ESTO EN NAVEGADOR
```

---

## 🌐 Cómo ver los resultados

### 1️⃣ Reporte HTML (MEJOR FORMA)

```bash
# macOS
open outputs/reporte_comparacion_visual.html

# Linux/Windows
start outputs/reporte_comparacion_visual.html
```

Muestra:

- Comparación lado a lado de métricas
- Heatmaps visuales
- Análisis de diferencias
- Conclusiones

### 2️⃣ Videos (Para ver el movimiento)

```bash
# Ver seed1 con 54 deadlocks
open outputs/seed1/simulacion.mp4

# Ver seed42 sin deadlocks
open outputs/seed42/simulacion.mp4
```

En los videos podrás ver:

- Robots moviéndose
- **Robots bloqueados en seed1** (se quedan quietos)
- Diferencia visual clara

### 3️⃣ Imágenes PNG (Análisis estático)

Abre `outputs/comparacion_*.png` en orden:

1. `comparacion_seed1_vs_seed42_metricas.png` - Datos numéricos
2. `comparacion_heatmap_*.png` - Visualización de zonas

---

## 📊 Qué esperar ver

### En los Gráficos de Métricas:

```
Deadlocks:
- seed1:  [████████████████████████████ 54]   ← PROBLEMA ROJO
- seed42: []                                   ← BASELINE VERDE

Throughput (casi idéntico):
- seed1:  [████████████ 59.60]
- seed42: [████████████ 59.70]

Tiempo promedio (parecido):
- seed1:  770.73 ticks
- seed42: 774.60 ticks
```

### En los Heatmaps (Colores):

- **Rojo 🔴**: Zonas con mucha espera/congestión → seed1
- **Verde 🟢**: Distribución equilibrada → seed42
- **Azul 🔵**: Alta actividad / eficiente → ambos

---

## 🎓 Interpretación (Para tu informe)

**seed1 expone que:**

1. ❌ El layout de seed1 genera **cuellos de botella naturales**
2. ❌ Sin coordinación, los robots se **bloquean mutuamente (54 veces)**
3. ✅ Pero aún completa 99.3% de pedidos (596/600)

**seed42 demuestra que:**

1. ✅ El layout es equilibrado
2. ✅ No hay deadlocks naturales con 20 robots
3. ✅ Sistema estable

**Implicación para Eje C (Coordinación):**

- Mejora en seed42: Probablemente ninguna (0 → 0 deadlocks)
- **Mejora en seed1: DRAMÁTICA** (54 → 0-20 deadlocks) = **60-100% de mejora**

---

## 🔧 Si algo no funciona

### Si faltan archivos en seed1:

Primero verifica que la simulación de seed1 existe:

```bash
ls outputs/seed1/metricas.json
```

Si existe pero no hay visualización, ejecuta:

```bash
python visualiza_simulacion.py --escenario seed1 --verbose
```

### Si ffmpeg falla:

El script intenta generar video MP4. Si falla (ffmpeg no instalado):

```bash
# Instalar ffmpeg
conda install -c conda-forge ffmpeg
# o
brew install ffmpeg

# Luego reintenta
python visualiza_simulacion.py --escenario seed1
```

### Si hay errores en Python:

Verifica que tienes todas las dependencias:

```bash
pip install matplotlib pillow numpy
```

---

## ⏱️ Duración estimada

| Paso                         | Tiempo            |
| ---------------------------- | ----------------- |
| Generar video seed1          | 5-10 min          |
| Generar video seed42         | 0 min (ya existe) |
| Generar heatmaps             | 2-3 min           |
| Crear comparaciones gráficas | 1-2 min           |
| **TOTAL**                    | **10-20 min**     |

---

## 📋 Checklist

Después de ejecutar, verifica:

- [ ] `outputs/seed1/simulacion.mp4` existe (>50 MB)
- [ ] `outputs/seed42/simulacion.mp4` existe
- [ ] `outputs/comparacion_*.png` se crearon (4+ imágenes)
- [ ] `outputs/reporte_comparacion_visual.html` se abrió correctamente
- [ ] Puedes ver en HTML: métricas, heatmaps, conclusiones

---

## 💡 Próximas acciones

Después de ver las visualizaciones:

1. ✅ Confirmar que seed1 tiene problema real (54 deadlocks es visible)
2. ✅ Decidir hacer mejora con Eje C (Coordinación)
3. ✅ Implementar sistema de prioridad o detección de ciclos
4. ✅ Ejecutar simulación mejorada y comparar nuevamente

---

**¿Ejecutar ahora?**

```bash
python generar_todo_visualizaciones.py
```

Luego abre:

```bash
open outputs/reporte_comparacion_visual.html
```

🚀 ¡Adelante!
