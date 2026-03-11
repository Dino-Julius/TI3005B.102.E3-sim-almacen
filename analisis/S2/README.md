# Análisis S2: Mejora de Asignación y Coordinación - Entregable 3

## 📋 Tabla de Contenidos

1. [Descripción](#descripción)
2. [Acceso a Documentación](#acceso-a-documentación)
3. [Ejecución Rápida](#ejecución-rápida)
4. [Resultados Clave](#resultados-clave)

## Descripción

**Entregable 3**: Diseño e implementación de mejora combinada en asignación de pedidos y coordinación local (Eje A + Eje C), incluyendo prioridad local de movimiento y replaneación cuando persiste bloqueo.

### Hipótesis Validadas

| #   | Hipótesis          | Meta  | Resultado | Estado         |
| --- | ------------------ | ----- | --------- | -------------- |
| H1  | Tiempo promedio    | ≥-30% | +0.4%     | ❌ NO CUMPLIDO |
| H2  | Distancia total    | ≥-20% | +2.5%     | ❌ NO CUMPLIDO |
| H3  | Completitud (200r) | ≥95%  | 98.5%     | ✅ CUMPLIDO    |

### Corrección de Retro (alcance S2)

Para cerrar la retro del Entregable 3, S2 se reporta con un solo caso comparativo:

- Baseline 200 robots: `outputs/S2_baseline_200r/metricas.json`
- Mejora 200 robots: `outputs/S2_mejora_200r/metricas.json`

La matriz 20/40/60/100/200 queda como evidencia técnica histórica, pero no como base principal del reporte corregido.

## Acceso a Documentación

Para el cierre de S2 y la transición a S3, los documentos vigentes en este repositorio son:

- [README.md](../../README.md): guía general del proyecto y flujo base de ejecución.
- [Entregable 4. Estabilidad, robustez y escalabilidad.md](../../Entregable%204.%20Estabilidad,%20robustez%20y%20escalabilidad.md): síntesis de S2 corregido y plan/criterios de S3.

---

## Ejecución Rápida

### Opción 1: Ejecutar mejora A+C (caso único 200r)

```bash
python demo_final.py --escenario S2_mejora_200r --robots 200 --ticks 10000 --modo_asignacion mejora
# Resultados en: outputs/S2_mejora_200r/metricas.json
```

### Opción 2: Ejecutar comparación corregida (caso único 200r)

```bash
./analisis/S2/ejecutar_s2_baseline.sh
./analisis/S2/ejecutar_s2_mejora.sh
python analisis/S2/generar_comparativa_s2.py
```

### Opción 3: Pipeline completo automatizado

```bash
./analisis/S2/ejecutar_pipeline_s2.sh
```

## Resultados Clave

### Métricas del Caso Único (200r)

| Métrica                        | Baseline 200r   | Mejora 200r     | Lectura                   |
| ------------------------------ | --------------- | --------------- | ------------------------- |
| **Pedidos completados**        | 580/600 (96.7%) | 591/600 (98.5%) | Mejora de servicio        |
| **Throughput**                 | 58.0            | 59.1            | Mejora ligera             |
| **Tiempo promedio**            | 641.5 ticks     | 644.0 ticks     | Trade-off (+0.4%)         |
| **Distancia total**            | 369,376 celdas  | 378,782 celdas  | Trade-off (+2.5%)         |
| **Eventos alto**               | 97,331          | 4,928           | Fuerte mejora (-94.9%)    |
| **Deadlocks**                  | 0               | 0               | Sin cambio                |
| **Replaneaciones por bloqueo** | 0               | 327             | Activas en mejora (Eje C) |

---

## 📂 Estructura de Archivos

```
analisis/S2/
├── README.md                          ← Este archivo
├── ejecutar_s2_mejora.sh             ← Script mejora (caso único 200r)
├── ejecutar_s2_baseline.sh           ← Script baseline (caso único 200r)
├── ejecutar_pipeline_s2.sh           ← Automatización completa
└── generar_comparativa_s2.py         ← Análisis comparativo

outputs/S2_*/
├── metricas.json                      ← Datos principales
├── pedidos.json                       ← Detalles de órdenes
├── anaqueles.json                     ← Configuración de almacenamiento
├── estaciones.json                    ← Puntos de entrega
└── spawn.json                         ← Posiciones iniciales

outputs/visualizaciones/
├── grafico_comparativo_s2.png
├── tabla_metricas_s2.png
└── heatmap_congestión_s2.png
```

---

## Troubleshooting

**Error: "No module named 'sim_core'"**

```bash
cd /ruta/al/proyecto
python demo_final.py --escenario S2_mejora_200r --robots 200 --ticks 10000 --modo_asignacion mejora
```

**Error: "File exists"**

```bash
rm -rf outputs/S2_mejora_200r
./analisis/S2/ejecutar_s2_mejora.sh
```

**Verificar integridad de datos**

```bash
python -c "import json; print(json.load(open('outputs/S2_mejora_200r/metricas.json')))"
```

En la salida de métricas de mejora deben aparecer:

- `coordinacion_eje_c: prioridad_local_movimiento+replaneacion_bloqueo`
- `replaneaciones_bloqueo`
- `umbral_replan_bloqueo`

**Reejecutar baseline sin revertir código**

```bash
python demo_final.py --escenario seed1 --robots 200 --ticks 10000 --modo_asignacion baseline --salida_metricas outputs/S2_baseline_200r/metricas.json
```

---

## 📊 Próximos Pasos

1. **Revisar** [Entregable 4. Estabilidad, robustez y escalabilidad.md](../../Entregable%204.%20Estabilidad,%20robustez%20y%20escalabilidad.md) para criterios S3
2. **Validar** resultados en `outputs/S2_mejora_200r/metricas.json`
3. **Generar** visualizaciones: `python generar_todo_visualizaciones.py`
4. **Preparar** presentación con gráficos y tabla de resultados

---

**Estado**: ✅ COMPLETO Y LISTO PARA ENTREGA  
**Última actualización**: Marzo 2026  
**Validación**: Completitud y congestión mejoran; tiempo y distancia presentan trade-off

---

## 📚 Documentación

- [README.md](../../README.md)
- [Entregable 4. Estabilidad, robustez y escalabilidad.md](../../Entregable%204.%20Estabilidad,%20robustez%20y%20escalabilidad.md)
