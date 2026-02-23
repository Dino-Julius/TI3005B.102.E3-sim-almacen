# Carpeta de Análisis - Estructura Organizada

Esta carpeta contiene todos los scripts de análisis y diagnóstico del simulador de almacén, organizados por tipo de análisis.

---

## 📁 Estructura de Carpetas

```
analisis/
├── diagnosticos/
│   ├── diagnostico_layout.py
│   └── outputs/                    # PNG con anotaciones técnicas
│
├── comparativas/
│   ├── generar_comparativas_visuales.py
│   └── outputs/                    # PNG comparativos (layouts y métricas)
│
├── validacion/
│   ├── verificar_alcanzabilidad_s1.py
│   └── reportes/                   # Reportes de validación
│
├── metricas/
│   ├── analizar_metricas_s1.py
│   ├── analizador_estadistico.py
│   ├── analizar_metricas_comparativas.py
│   └── reportes/                   # Análisis generados
│
├── Outputs Raíz (generados automáticamente)
│   ├── analisis_estadistico_seed1_vs_seed42.md
│   ├── comparacion_seed1_vs_seed42_metricas.png
│   └── reporte_comparacion_visual.html
│
├── Scripts Legacy (análisis de 10 semillas)
│   ├── comparador_visual_seed1_vs_seed42.py
│   ├── generar_todo_visualizaciones.py
│   └── generar_visualizaciones_seed1.py
│
└── README.md                       # Este archivo
```

---

## 🛠️ Scripts Principales (Migrados)

### 1. Diagnósticos de Layout

**`diagnosticos/diagnostico_layout.py`**

Visualizaciones detalladas de layouts con anotaciones técnicas.

```bash
python analisis/diagnosticos/diagnostico_layout.py --escenario S1_baseline_seed1
```

**Salida:** `analisis/diagnosticos/outputs/diagnostico_layout_{escenario}.png`

---

### 2. Comparativas Visuales

**`comparativas/generar_comparativas_visuales.py`**

Comparativas lado a lado (120×80 vs 300×200).

```bash
python analisis/comparativas/generar_comparativas_visuales.py --seed seed1
```

**Salida:**

- `analisis/comparativas/outputs/comparativa_layouts_{seed}.png`
- `analisis/comparativas/outputs/comparativa_metricas_{seed}.png`

---

### 3. Validación de Alcanzabilidad

**`validacion/verificar_alcanzabilidad_s1.py`**

Verifica accesibilidad de anaqueles usando BFS.

```bash
python analisis/validacion/verificar_alcanzabilidad_s1.py
```

**Salida:** Consola (sin archivo) - Verifica S1_baseline_seed1 y S1_baseline_seed42

---

### 4. Análisis de Métricas

**`metricas/analizar_metricas_s1.py`**

Comparación de métricas 120×80 vs 300×200 con diagnóstico.

```bash
python analisis/metricas/analizar_metricas_s1.py
```

**Salida:** Consola con tabla comparativa

---

## 📊 Scripts Legacy (Análisis de 10 Semillas)

Estos scripts fueron usados en el análisis inicial que identificó seed1 con 54 deadlocks:

### **`comparador_visual_seed1_vs_seed42.py`**

- Comparación visual seed1 vs seed42
- Genera: `analisis/comparacion_seed1_vs_seed42_metricas.png`
- Genera: `analisis/reporte_comparacion_visual.html` ⭐
- Ejecutar: `python analisis/comparador_visual_seed1_vs_seed42.py`

### **`analizador_estadistico.py`**

- Análisis estadístico profundo
- Genera: `analisis/analisis_estadistico_seed1_vs_seed42.md`
- Ejecutar: `python analisis/analizador_estadistico.py`

### **`analizar_metricas_comparativas.py`**

- Análisis rápido de 10 semillas
- Ejecutar: `python analisis/analizar_metricas_comparativas.py`

### **`generar_todo_visualizaciones.py`**

- Script maestro que ejecuta todo
- Ejecutar: `python analisis/generar_todo_visualizaciones.py`

### **`generar_visualizaciones_seed1.py`**

- Visualizaciones específicas para seed1
- Ejecutar: `python analisis/generar_visualizaciones_seed1.py`

---

## 🚀 Uso Rápido

### Desde la raíz del proyecto:

```bash
# 1. Diagnósticos
python analisis/diagnosticos/diagnostico_layout.py --escenario S1_baseline_seed1

# 2. Comparativas visuales
python analisis/comparativas/generar_comparativas_visuales.py --seed seed1

# 3. Validación de alcanzabilidad
python analisis/validacion/verificar_alcanzabilidad_s1.py

# 4. Análisis de métricas
python analisis/metricas/analizar_metricas_s1.py

# 5. Scripts legacy (si necesitas el análisis de 10 semillas)
python analisis/comparador_visual_seed1_vs_seed42.py
python analisis/analizador_estadistico.py
python analisis/generar_todo_visualizaciones.py
```

### Ver outputs generados:

```bash
# Diagnósticos
ls -lh analisis/diagnosticos/outputs/

# Comparativas
ls -lh analisis/comparativas/outputs/

# Reportes en raíz
ls -lh analisis/*.{md,html,png}
```

---

## 📁 Outputs Generados

### En Subcarpetas (Nuevos Scripts)

```
analisis/diagnosticos/outputs/
  └── diagnostico_layout_S1_baseline_seed1.png
  └── diagnostico_layout_S1_baseline_seed42.png

analisis/comparativas/outputs/
  ├── comparativa_layouts_seed1.png
  ├── comparativa_metricas_seed1.png
  ├── comparacion_heatmap_visitas_seed1_vs_seed42.png
  ├── comparacion_heatmap_esperas_seed1_vs_seed42.png
  └── comparacion_heatmap_ratio_seed1_vs_seed42.png

analisis/metricas/reportes/
  └── (reportes de análisis)
```

### En Raíz de analisis/ (Scripts Legacy)

```
analisis/
├── analisis_estadistico_seed1_vs_seed42.md ⭐
├── comparacion_seed1_vs_seed42_metricas.png
└── reporte_comparacion_visual.html ⭐⭐ (abre en navegador)
```

---

## 📝 Notas Importantes

1. **Auto-detección de paths:** Todos los scripts detectan automáticamente la ubicación de `outputs/` sin importar dónde se ejecuten

2. **Nomenclatura oficial:**
   - Originales: `seed1`, `seed42`
   - S1 Baseline: `S1_baseline_seed1`, `S1_baseline_seed42`
   - **NO existe S0**

3. **Requisitos previos:** Los escenarios deben estar generados en `outputs/`:

   ```bash
   python demo_final.py --escenario seed1
   python visualiza_simulacion.py --escenario seed1
   ```

4. **Reporte HTML interactivo:** Abre `analisis/reporte_comparacion_visual.html` en navegador para ver comparación visual

---

## ✅ Checklist de Ejecución

Para obtener todos los análisis y visualizaciones:

```bash
# Paso 1: Generar escenarios (si no existen)
python demo_final.py --escenario seed1
python visualiza_simulacion.py --escenario seed1
python demo_final.py --escenario S1_baseline_seed1
python visualiza_simulacion.py --escenario S1_baseline_seed1

# Paso 2: Ejecutar análisis nuevos
python analisis/diagnosticos/diagnostico_layout.py --escenario S1_baseline_seed1
python analisis/comparativas/generar_comparativas_visuales.py --seed seed1
python analisis/validacion/verificar_alcanzabilidad_s1.py
python analisis/metricas/analizar_metricas_s1.py

# Paso 3: Ejecutar script legacy (opcional, para reporte completo)
python analisis/generar_todo_visualizaciones.py

# Paso 4: Ver resultados
open analisis/reporte_comparacion_visual.html
```

---

## 🔧 Reorganización Automática

Si los archivos aún están sueltos en `outputs/`, ejecuta:

```bash
bash organizar_outputs.sh
```

Si los scripts están en raíz, ejecuta:

```bash
bash reorganizar_analisis.sh
```
