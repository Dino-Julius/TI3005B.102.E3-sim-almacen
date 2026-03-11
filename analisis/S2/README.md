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

---

## Ejecución Rápida

### Opción recomendada (sin cambiar datos existentes)

```bash
./analisis/S2/ejecutar_pipeline_s2.sh --solo-analisis
```

Genera/actualiza:

- `analisis/S2/S2_resultados.txt`
- salida en consola de `analisis/S2/generar_comparativa_s2.py`

Usa los datos ya existentes en:

- `outputs/S2_baseline_200r/metricas.json`
- `outputs/S2_mejora_200r/metricas.json`

### Opción 2: Regenerar benchmark + comparativa

```bash
./analisis/S2/ejecutar_pipeline_s2.sh
```

### Opción 3: Solo comparativa (directo)

```bash
python analisis/S2/generar_comparativa_s2.py | tee analisis/S2/S2_resultados.txt
```

## Resultados Clave

### Métricas del Caso Único (200r)

| Métrica                        | Baseline 200r   | Mejora 200r     | Δ                |
| ------------------------------ | --------------- | --------------- | ---------------- |
| **Pedidos completados**        | 580/600 (96.7%) | 591/600 (98.5%) | +11 (+1.9%)      |
| **Tiempo promedio**            | 641.5 ticks     | 644.0 ticks     | +2.5 (+0.4%)     |
| **Throughput**                 | 58.00           | 59.10           | +1.10 (+1.9%)    |
| **Tiempo de espera**           | 486.7 ticks     | 24.6 ticks      | -462.0 (-94.9%)  |
| **Utilización promedio**       | 23.4%           | 19.2%           | -4.1 (-17.8%)    |
| **Distancia total**            | 369,376 celdas  | 378,782 celdas  | +9,406 (+2.5%)   |
| **Deadlocks**                  | 0               | 0               | +0 (+0.0%)       |
| **Eventos alto**               | 97,331          | 4,928           | -92,403 (-94.9%) |
| **Replaneaciones por bloqueo** | 0               | 327             | +327 (+inf%)     |

Fuente: `analisis/S2/S2_resultados.txt`

---

## 📂 Estructura de Archivos

```
analisis/S2/
├── README.md                          ← Este archivo
├── ejecutar_pipeline_s2.sh           ← Script único (completo o solo análisis)
├── generar_comparativa_s2.py         ← Análisis comparativo
└── S2_resultados.txt                 ← Último reporte generado

outputs/S2_*/
├── metricas.json                      ← Datos principales
├── pedidos.json                       ← Detalles de órdenes
├── anaqueles.json                     ← Configuración de almacenamiento
├── estaciones.json                    ← Puntos de entrega
└── spawn.json                         ← Posiciones iniciales
```