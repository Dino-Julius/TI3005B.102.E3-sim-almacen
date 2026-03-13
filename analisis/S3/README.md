# S3 - Entregable 4 (Estabilidad, robustez y escalabilidad)

Este módulo ejecuta los tres escenarios de S3 sobre la versión mejorada (Eje A + Eje C) y genera un reporte comparativo en markdown.

## Escenarios

- A: `S3_alta_densidad_400r` (400 robots, 600 pedidos, 10,000 ticks)
- B: `S3_burst_200r_1200` (200 robots, 1,200 pedidos, 15,000 ticks)
- C: `S3_var_400r_1200` (400 robots, 1,200 pedidos, 15,000 ticks)

## Ejecución rápida

### Opción recomendada (sin cambiar datos existentes)

```bash
./analisis/S3/ejecutar_s3.sh --solo-reporte
```

Esta opción:

- no vuelve a correr simulaciones,
- usa los `metricas.json` ya existentes,
- actualiza `analisis/S3/reporte_s3.md`.

### Opción completa (regenera A/B/C + reporte)

```bash
./analisis/S3/ejecutar_s3.sh
```

## Salidas

- `outputs/S3_alta_densidad_400r/metricas.json`
- `outputs/S3_burst_200r_1200/metricas.json`
- `outputs/S3_var_400r_1200/metricas.json`
- `analisis/S3/reporte_s3.md`

## Solo generar reporte (si ya corriste los 3 escenarios)

```bash
python analisis/S3/generar_reporte_s3.py
```

## Resultados actuales (desde reporte_s3.md)

### Tabla comparativa A/B/C

| Métrica                     | A: Alta densidad | B: Burst severo | C: Variación robots |
| --------------------------- | ---------------: | --------------: | ------------------: |
| Robots (diseño)             |              400 |             200 |                 400 |
| Pedidos completados         |              591 |            1200 |                1200 |
| Pedidos no completados      |                9 |               0 |                   0 |
| Tasa completitud            |           0.9850 |          1.0000 |              1.0000 |
| Throughput (ped/1000 ticks) |            59.10 |           80.00 |               80.00 |
| Tiempo promedio pedido      |           636.27 |          743.53 |              658.61 |
| Tiempo mediana pedido       |           626.00 |          617.50 |              651.00 |
| Tiempo p90 pedido           |           935.00 |         1276.40 |              957.20 |
| Tiempo p95 pedido           |          1032.00 |         1861.55 |             1043.00 |
| Tiempo p95 espera           |            51.05 |          207.05 |              136.05 |
| Eventos alto                |             4799 |           18420 |               21954 |
| Deadlocks                   |                0 |               0 |                   0 |
| Distancia total             |           374639 |          686732 |              768372 |
| Utilización promedio        |             0.10 |            0.24 |                0.13 |

### Evaluación de criterios S3

- Estabilidad: Cumple
  - Completitud A y C >= 95%
  - Crecimiento p95 pedido (C vs A) <= 35%: +1.07%
  - Deadlock C no supera 2x de A
- Robustez: Cumple
  - Throughput útil en B (>0)
  - No completados en B <= 10%
- Escalabilidad (C vs A)
  - Delta throughput: +35.36%
  - Delta p95 pedido: +1.07%

Conclusión breve: la mejora A+C cumple estabilidad, robustez y escalabilidad usando métricas de distribución (mediana/p90/p95), no solo promedios.

## S3 extendido (estres + series temporales)

Este flujo ejecuta escenarios de estres alto (D y E) y guarda métricas temporales por ventana.

- D: `S3_estres_D_200r_6000` (200 robots, 6000 pedidos)
- E: `S3_estres_E_200r_12000` (200 robots, 12000 pedidos)

### Ejecutar escenarios D/E con series temporales

```bash
./analisis/S3/ejecutar_s3_extendido.sh
```

Opcional: sobre-escribir ticks y ventana temporal

```bash
TICKS_D=60000 TICKS_E=120000 VENTANA=500 ./analisis/S3/ejecutar_s3_extendido.sh
```

### Salidas generadas

- `outputs/S3_estres_D_200r_6000/metricas.json`
- `outputs/S3_estres_D_200r_6000/metricas_temporales.json`
- `outputs/S3_estres_D_200r_6000/metricas_temporales.csv`
- `outputs/S3_estres_E_200r_12000/metricas.json`
- `outputs/S3_estres_E_200r_12000/metricas_temporales.json`
- `outputs/S3_estres_E_200r_12000/metricas_temporales.csv`
- `analisis/S3/graficos/S3_estres_D_200r_6000/*.png`
- `analisis/S3/graficos/S3_estres_E_200r_12000/*.png`

### Ejecutar solo una simulacion temporal (modo manual)

```bash
python analisis/S3/registrar_metricas_temporales.py \
  --escenario S3_estres_D_200r_6000 \
  --robots 200 \
  --ticks 60000 \
  --seed 1 \
  --ventana 500 \
  --modo_asignacion mejora
```

### Generar graficas desde un JSON temporal

```bash
python analisis/S3/generar_graficas_temporales.py --escenario S3_estres_D_200r_6000
```

## Estructura de S3

```text
analisis/S3/
├── README.md
├── ejecutar_s3.sh
├── ejecutar_s3_extendido.sh
├── generar_reporte_s3.py
├── registrar_metricas_temporales.py
├── generar_graficas_temporales.py
├── reporte_s3.md
└── graficos/
```
