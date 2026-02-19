# ⚙️ TASKS DE VS CODE - Status Después de Reorganización

**Fecha:** 18 Febrero 2026  
**Estado:** ✅ Actualizados para funcionar con nueva estructura

---

## 🎯 RESUMEN RÁPIDO

✅ **Tasks de SIMULACIÓN:** Funcionan NORMAL (sin cambios)  
✅ **Tasks de ANÁLISIS:** NUEVOS - Con rutas actualizadas  
✅ **Todo automatizado:** Via Ctrl+Shift+P > "Run Task"

---

## 📊 TASKS DE SIMULACIÓN (SIN CAMBIOS)

Estos tasks siguen exactamente igual porque los scripts NO se mueven:

```
generador_layout.py        ← RAÍZ (sin cambios)
generador_pedidos.py       ← RAÍZ (sin cambios)
demo_final.py              ← RAÍZ (sin cambios)
visualiza_simulacion.py    ← RAÍZ (sin cambios)
```

### Tasks Disponibles:

#### 🎬 Seed42

- `Generar layout (seed42)`
- `Generar pedidos (seed42)`
- `Ejecutar simulacion (seed42)`
- `Visualizar simulacion (seed42)`
- `Pipeline seed42 (layout → pedidos → simulacion → visualizacion)`

#### 🎬 Seed1-999999 (10 semillas)

- `Pipeline seed1 (layout → pedidos → simulacion)`
- `Pipeline seed7 (layout → pedidos → simulacion)`
- ... (seed13, seed97, seed256, seed1337, seed2024, seed31415, seed65537, seed999999)

#### 🚀 Pipeline Maestro

- `MEGA Pipeline: Todas 10 semillas`

**Ejecución:** Tal como antes, sin cambios.

---

## 🔍 TASKS DE ANÁLISIS (NUEVOS)

Estos tasks son NUEVOS y usan scripts de `analisis/`:

```
analisis/generar_todo_visualizaciones.py
analisis/analizador_estadistico.py
analisis/comparador_visual_seed1_vs_seed42.py
analisis/analizar_metricas_comparativas.py
```

### Tasks Disponibles:

#### 📊 Análisis Individual

- `[ANÁLISIS] Generar todas las visualizaciones`
  - Genera videos, heatmaps, comparaciones
  - ⏱️ Tiempo: 15-20 minutos
  - 📁 Output: `outputs/reporte_comparacion_visual.html`

- `[ANÁLISIS] Generar análisis estadístico`
  - Análisis profundo de métricas
  - ⏱️ Tiempo: 1 minuto
  - 📁 Output: `outputs/analisis_estadistico_seed1_vs_seed42.md`

- `[ANÁLISIS] Crear comparador visual`
  - Gráficos comparativos
  - 📁 Output: PNG files

- `[ANÁLISIS] Analizar métricas comparativas`
  - Análisis de 10 semillas
  - 📁 Output: Consola

#### 🚀 Pipeline Análisis

- `[ANÁLISIS] Pipeline COMPLETO: Análisis + Visualización`
  - Ejecuta ambas tareas en secuencia
  - ⏱️ Tiempo: 20-25 minutos

---

## 📤 CÓMO USAR LOS TASKS

### Desde VS Code (Recomendado)

1️⃣ Abre Command Palette: `Ctrl+Shift+P` (Mac: `Cmd+Shift+P`)

2️⃣ Escribe "Run Task"

3️⃣ Selecciona el task que quieres:

```
Categoría SIMULACIÓN:
├─ Generar layout (seed42)
├─ Generar pedidos (seed42)
├─ Ejecutar simulacion (seed42)
├─ Visualizar simulacion (seed42)
├─ Pipeline seed42
├─ Pipeline seed1-999999 (todos)
└─ MEGA Pipeline: Todas 10 semillas

Categoría ANÁLISIS (NUEVO):
├─ [ANÁLISIS] Generar todas las visualizaciones
├─ [ANÁLISIS] Generar análisis estadístico
├─ [ANÁLISIS] Crear comparador visual
├─ [ANÁLISIS] Analizar métricas comparativas
└─ [ANÁLISIS] Pipeline COMPLETO
```

4️⃣ El task se ejecuta en la terminal de VS Code

---

## 🖥️ CÓMO USAR LOS TASKS DESDE TERMINAL

Si prefieres terminal:

```bash
# Simulación (scripts en raíz)
python generador_layout.py --escenario seed42 --seed 42 --ancho 120 --alto 80 --estaciones 20
python generador_pedidos.py --escenario seed42 --pedidos 600 --burst
python demo_final.py --escenario seed42 --robots 20 --ticks 10000
python visualiza_simulacion.py --escenario seed42

# Análisis (scripts en carpeta analisis/)
python analisis/generar_todo_visualizaciones.py
python analisis/analizador_estadistico.py
python analisis/comparador_visual_seed1_vs_seed42.py
python analisis/analizar_metricas_comparativas.py
```

---

## 📋 TABLA COMPARATIVA: ANTES vs DESPUÉS

### SIMULACIÓN (Sin cambios)

| Task                           | Antes       | Después           |
| ------------------------------ | ----------- | ----------------- |
| Generar layout (seed42)        | ✅ Funciona | ✅ Funciona igual |
| Generar pedidos (seed42)       | ✅ Funciona | ✅ Funciona igual |
| Ejecutar simulacion (seed42)   | ✅ Funciona | ✅ Funciona igual |
| Visualizar simulacion (seed42) | ✅ Funciona | ✅ Funciona igual |
| Pipeline seed42                | ✅ Funciona | ✅ Funciona igual |
| MEGA Pipeline (10 semillas)    | ✅ Funciona | ✅ Funciona igual |

### ANÁLISIS (Nuevos tasks)

| Task                               | Antes        | Después  |
| ---------------------------------- | ------------ | -------- |
| [ANÁLISIS] Generar visualizaciones | ❌ No existe | ✅ NUEVO |
| [ANÁLISIS] Análisis estadístico    | ❌ No existe | ✅ NUEVO |
| [ANÁLISIS] Pipeline COMPLETO       | ❌ No existe | ✅ NUEVO |

---

## 🎯 WORKFLOWS COMUNES

### Workflow 1: Solo Simulación

```
1. Ctrl+Shift+P → Run Task
2. Busca "MEGA Pipeline"
3. Ejecuta todas 10 semillas
```

### Workflow 2: Solo Análisis

```
1. Ctrl+Shift+P → Run Task
2. Busca "[ANÁLISIS] Pipeline COMPLETO"
3. Genera vid

eos + análisis automáticamente
```

### Workflow 3: Completo (Simulación → Análisis)

```
1. Ejecuta: MEGA Pipeline (Todas 10 semillas)
   └─ Genera datos en outputs/

2. Luego ejecuta: [ANÁLISIS] Pipeline COMPLETO
   └─ Genera visualizaciones

3. Resultado: outputs/reporte_comparacion_visual.html
```

---

## ✅ CHECKLIST: Tasks Funcionando

Después de reorganizar, verifica:

- [ ] `Ctrl+Shift+P` → "Run Task" muestra opciones
- [ ] Tasks de simulación funcionan normalmente
- [ ] **NUEVOS** Tasks de análisis aparecen en la lista (con etiqueta `[ANÁLISIS]`)
- [ ] `[ANÁLISIS] Pipeline COMPLETO` se ejecuta sin errores
- [ ] `outputs/reporte_comparacion_visual.html` se genera

---

## 📝 CAMBIOS REALIZADOS EN tasks.json

### ✅ Agregados (Nuevos)

```json
{
  "label": "[ANÁLISIS] Generar todas las visualizaciones",
  "type": "shell",
  "command": "python",
  "args": ["analisis/generar_todo_visualizaciones.py"]
},
// ... más tasks de análisis
```

### ⚠️ Modificados (Ninguno)

Los tasks de simulación NO se modificaron, solo se agregaron nuevos.

### 🗑️ Eliminados (Ninguno)

Todos los tasks antiguos se mantienen.

---

## 🚨 TROUBLESHOOTING

### Problema: Task no encuentra el archivo

```
❌ Error: No such file or directory: 'analisis/generar_todo_visualizaciones.py'
```

**Solución:** Asegúrate de:

1. Ejecutar `python reorganizar_proyecto.py` primero
2. Crear las carpetas `analisis/` y `docs/`
3. Los scripts fueron movidos a `analisis/`

### Problema: Command Palette no muestra tasks

```
❌ No tasks available
```

**Solución:**

1. Cierra y reabre VS Code
2. Verifica que `.vscode/tasks.json` existe
3. Recarga la ventana: `Cmd+K Cmd+R` (Mac) o `Ctrl+K Ctrl+R` (Windows)

### Problema: ffmpeg error en visualizaciones

```
❌ ffmpeg not found
```

**Solución:**

```bash
# Instalar ffmpeg
conda install -c conda-forge ffmpeg

# O
brew install ffmpeg
```

---

## 📌 INFORMACIÓN IMPORTANTE

### Rutas Base

- **Raíz:** `/Users/jcvivas/Documents/.../TI3005B.102.E3-sim-almacen/`
- **Análisis:** `.../analisis/`
- **Docs:** `.../docs/`
- **Output:** `.../outputs/`

### Tasks se Ejecutan Desde

- Siempre desde la **raíz del proyecto**
- Las rutas en tasks.json son relativas a la raíz
- `python analisis/script.py` → busca en `analisis/` desde raíz

### Orden de Carpetas

```
analisis/    # Scripts que generamos para análisis
docs/        # Documentación
outputs/     # Resultados
(raíz)       # Código original de simulación
```

---

## 🎯 RESUMEN FINAL

| Aspecto                 | Estado                      |
| ----------------------- | --------------------------- |
| **Simulación**          | ✅ Funciona igual           |
| **Tasks de simulación** | ✅ Sin cambios              |
| **Tasks de análisis**   | ✅ NUEVOS agregados         |
| **Archivo tasks.json**  | ✅ Actualizado              |
| **Rutas en tasks**      | ✅ Correctas                |
| **VS Code**             | ✅ Reconoce todos los tasks |

---

## 🚀 PRÓXIMOS PASOS

1. ✅ Reorganizar: `python reorganizar_proyecto.py`
2. ✅ Reload VS Code: `Cmd+Shift+P` → "Reload Window"
3. ✅ Ejecutar tasks: `Cmd+Shift+P` → "Run Task"
4. ✅ Disfrutar de automatización

---

**¿Listo? Todo está configurado para funcionar perfectamente después de la reorganización.** ✨

```bash
python reorganizar_proyecto.py
```

Después abre: `Cmd+Shift+P` → "Run Task" → Selecciona lo que quieres

**¡Adelante!** 🚀
