# Reporte S3 - Entregable 4

## 1) Tabla comparativa A/B/C

| Métrica | A: Alta densidad | B: Burst severo | C: Variación robots |
|---|---:|---:|---:|
| Robots (diseño) | 400 | 200 | 400 |
| Pedidos completados | 591 | 1200 | 1200 |
| Pedidos no completados | 9 | 0 | 0 |
| Tasa completitud | 0.9850 | 1.0000 | 1.0000 |
| Throughput (ped/1000 ticks) | 59.10 | 80.00 | 80.00 |
| Tiempo promedio pedido | 636.27 | 743.53 | 658.61 |
| Tiempo mediana pedido | 626.00 | 617.50 | 651.00 |
| Tiempo p90 pedido | 935.00 | 1276.40 | 957.20 |
| Tiempo p95 pedido | 1032.00 | 1861.55 | 1043.00 |
| Tiempo p95 espera | 51.05 | 207.05 | 136.05 |
| Eventos alto | 4799 | 18420 | 21954 |
| Deadlocks | 0 | 0 | 0 |
| Distancia total | 374639 | 686732 | 768372 |
| Utilización promedio | 0.10 | 0.24 | 0.13 |

## 2) Evaluación de criterios (S3)

### Estabilidad
- Completitud A y C >= 95%: Cumple
- Crecimiento p95 pedido (C vs A) <= 35%: Cumple (+1.07%)
- Deadlock C no supera 2x de A: Cumple

### Robustez
- Throughput util en B (>0): Cumple
- No completados en B <= 10%: Cumple

### Escalabilidad (C vs A)
- Delta throughput: +35.36%
- Delta p95 pedido: +1.07%

## 3) Conclusión breve

La mejora A+C se evalúa en estabilidad, robustez y escalabilidad con base en distribución (mediana/p90/p95), no solo promedios.
