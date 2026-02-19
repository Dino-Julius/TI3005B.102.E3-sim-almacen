# 🏭 Simulación de Almacén - Proyecto TI3005B.102

## 📂 Estructura del Proyecto

```
📦 TI3005B.102.E3-sim-almacen/
├── 📁 analisis/              # Scripts de análisis comparativo
│   ├── generar_todo_visualizaciones.py ⭐ (ejecutar primero)
│   ├── analizador_estadistico.py
│   ├── comparador_visual_seed1_vs_seed42.py
│   ├── analizar_metricas_comparativas.py
│   └── README.md
│
├── 📁 docs/                  # Documentación del análisis
│   ├── PLAN_INTEGRAL_PROYECTO.md ⭐⭐⭐ (leer primero)
│   ├── GUIA_GENERAR_VISUALIZACIONES.md
│   ├── STATUS_PROYECTO.md
│   ├── INDICE_SCRIPTS_Y_DOCUMENTOS.md
│   ├── RESUMEN_VISUAL.txt
│   └── README.md
│
├── 📁 outputs/               # Resultados de simulaciones
│   ├── seed1/ (54 deadlocks)
│   ├── seed42/ (0 deadlocks)
│   ├── seed7-999999/
│   └── reporte_comparacion_visual.html ⭐
│
├── 📁 pruebas/               # Tests del sistema
│
├── 🐍 Código Principal (Simulación)
│   ├── demo_final.py          # Simulación principal
│   ├── sim_core.py            # Motor de simulación
│   ├── a_estrella.py          # Pathfinding
│   ├── tabla_reservas.py      # Coordinación de celdas
│   ├── generador_layout.py    # Generación de layouts
│   ├── generador_pedidos.py   # Generación de pedidos
│   ├── visualiza_simulacion.py # Visualización
│   └── out_paths.py           # Utilidades
│
└── 📄 Configuración
    ├── requirements.txt
    ├── .vscode/tasks.json     # Tasks automatizadas
    └── README.md (este archivo)
```

---

## 🚀 Inicio Rápido

### 1. Lee la Documentación
```bash
# El plan maestro con toda la estrategia
open docs/PLAN_INTEGRAL_PROYECTO.md

# Resumen rápido de 30 segundos
cat docs/RESUMEN_VISUAL.txt
```

### 2. Genera Visualizaciones (15-20 min)
```bash
python analisis/generar_todo_visualizaciones.py

# Luego abre en navegador
open outputs/reporte_comparacion_visual.html
```

### 3. Análisis Estadístico (1 min)
```bash
python analisis/analizador_estadistico.py
open outputs/analisis_estadistico_seed1_vs_seed42.md
```

---

## 📊 Hallazgos Clave

### Problema Identificado
- **seed1:** 54 deadlocks (robots bloqueados mutuamente)
- **seed42:** 0 deadlocks (sistema equilibrado)
- **Otras semillas:** 0 deadlocks (sistema robusto)

→ Expone vulnerabilidad en coordinación multirobótica

### Solución Propuesta
- **Eje elegido:** C - Coordinación Multirobótica
- **Algoritmo:** Sistema de prioridad + Detección de ciclos
- **Mejora esperada:** 60-100% reducción de deadlocks
- **Tiempo estimado:** 3-8 horas de implementación

---

## 🎯 Estructura de Uso

### Para Análisis y Visualización
```bash
cd analisis/
python generar_todo_visualizaciones.py
```

### Para Ejecutar Simulación
```bash
# Generar escenario
python generador_layout.py --escenario test --seed 42 --ancho 120 --alto 80 --estaciones 20
python generador_pedidos.py --escenario test --pedidos 600 --burst

# Ejecutar simulación
python demo_final.py --escenario test --robots 20 --ticks 10000

# Visualizar
python visualiza_simulacion.py --escenario test
```

### Para Ver Documentación
```bash
# Plan integral (leer primero)
open docs/PLAN_INTEGRAL_PROYECTO.md

# Guía de visualizaciones
open docs/GUIA_GENERAR_VISUALIZACIONES.md

# Estado del proyecto
open docs/STATUS_PROYECTO.md
```

---

## 📈 Pipeline Completo (Tasks de VS Code)

Ver `.vscode/tasks.json` para 10+ tasks automatizadas:
- Generar layout
- Generar pedidos
- Ejecutar simulación
- Visualizar
- Pipeline completo

---

## 🛠️ Requisitos

```bash
pip install -r requirements.txt
```

Dependencias principales:
- numpy
- matplotlib
- pillow
- ffmpeg (para videos)

---

## 📚 Documentación Adicional

- **Análisis completo:** `docs/PLAN_INTEGRAL_PROYECTO.md`
- **Guía de uso:** `docs/GUIA_GENERAR_VISUALIZACIONES.md`
- **Scripts de análisis:** `analisis/README.md`
- **Documentación original:** `Info.md`

---

## 👥 Equipo

TI3005B.102 - Tec de Monterrey  
Fecha: Febrero 2026

---

## 📌 Próximos Pasos

1. ✅ Análisis de 10 semillas (completado)
2. ✅ Documentación y scripts (completado)
3. ⏳ Implementación de mejora (Eje C)
4. ⏳ Ejecución de experimentos S1/S2/S3
5. ⏳ Generación de informe final

---

**¿Por dónde empezar?**

```bash
# Opción rápida (30 min)
open docs/PLAN_INTEGRAL_PROYECTO.md
python analisis/generar_todo_visualizaciones.py
open outputs/reporte_comparacion_visual.html

# Opción completa (leer todo)
ls docs/
```

🚀 **¡Adelante!**
