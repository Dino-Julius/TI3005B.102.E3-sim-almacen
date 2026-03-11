# S3 - Entregable 4 (Estabilidad, robustez y escalabilidad)

Este módulo ejecuta los tres escenarios de S3 sobre la versión mejorada (Eje A + Eje C) y genera un reporte comparativo en markdown.

## Escenarios

- A: `S3_alta_densidad_400r` (400 robots, 600 pedidos, 10,000 ticks)
- B: `S3_burst_200r_1200` (200 robots, 1,200 pedidos, 15,000 ticks)
- C: `S3_var_400r_1200` (400 robots, 1,200 pedidos, 15,000 ticks)

## Ejecutar todo

```bash
chmod +x analisis/S3/ejecutar_s3.sh
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
