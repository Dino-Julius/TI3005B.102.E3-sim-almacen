# Reporte de Insights (sin rerun)

Este reporte usa exclusivamente outputs ya existentes.

## Escenarios con metricas cargadas
- S2 Baseline 200r: completitud=0.9667, throughput=58.00, p95=1018.25, eventos_alto=97331
- S2 Mejora 200r: completitud=0.9850, throughput=59.10, p95=1047.00, eventos_alto=4928
- S3 A 400r/600p: completitud=0.9850, throughput=59.10, p95=1032.00, eventos_alto=4799
- S3 B 200r/1200p: completitud=1.0000, throughput=80.00, p95=1861.55, eventos_alto=18420
- S3 C 400r/1200p: completitud=1.0000, throughput=80.00, p95=1043.00, eventos_alto=21954

## Graficas generadas
- analisis/insights/graficos/latencia_percentiles.png
- analisis/insights/graficos/congestion_normalizada.png
- analisis/insights/graficos/eficiencia_distancia.png
- analisis/insights/graficos/replan_vs_congestion.png
- analisis/insights/graficos/perfil_demanda_ticks.png
- analisis/insights/graficos/top_estaciones_carga.png

## Heatmaps disponibles (ya existentes)
- S2 Mejora 200r: outputs/S2_mejora_200r/heatmap_visitas.png, outputs/S2_mejora_200r/heatmap_esperas.png, outputs/S2_mejora_200r/heatmap_ratio.png

## Faltantes detectados
- Ninguno
