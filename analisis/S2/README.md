# 📁 S2: Estrés de Flota - Benchmarks con Múltiples Robots

**Proyecto:** TI3005B.102 - Simulación de Almacén  
**Entregable:** 3 - Diseño e Implementación de la Mejora  
**Eje Intervenido:** A - Asignación de Pedidos

---

## 📖 DOCUMENTACIÓN COMPLETA

**Todo lo que necesitas está en un solo archivo:**

👉 **[DOCUMENTACION_COMPLETA_S2.md](DOCUMENTACION_COMPLETA_S2.md)**

Incluye:

- ✅ Resumen ejecutivo y validación de hipótesis
- ✅ Implementación técnica detallada
- ✅ Guía de ejecución paso a paso
- ✅ Resultados completos y análisis
- ✅ Generación de videos

---

## 🚀 Ejecución Rápida

### Para ejecutar todo automáticamente:

```bash
cd analisis/S2
chmod +x ejecutar_pipeline_s2.sh
./ejecutar_pipeline_s2.sh
```

**Tiempo:** ~60 minutos (5 simulaciones de 10,000 ticks cada una)

### Para generar video de 200 robots:

```bash
python visualiza_simulacion.py \
  --escenario S2_mejora_200r \
  --robots 200 \
  --ticks 10000 \
  --pasos_por_frame 25 \
  --fps 30
```

---

## 📂 Scripts Disponibles

| Script                      | Propósito                          |
| --------------------------- | ---------------------------------- |
| `ejecutar_pipeline_s2.sh`   | Pipeline completo automatizado     |
| `ejecutar_s2_mejora.sh`     | Solo benchmarks mejora (5 configs) |
| `ejecutar_s2_baseline.sh`   | Solo benchmarks baseline           |
| `generar_comparativa_s2.py` | Análisis comparativo               |

---

## 📊 Resultados (Resumen)

| Métrica            | Meta | Resultado  | Estado      |
| ------------------ | ---- | ---------- | ----------- |
| Tiempo Promedio    | -30% | **-40.5%** | ✅ SUPERADO |
| Distancia Total    | -20% | **-68.9%** | ✅ SUPERADO |
| Completitud (200r) | ≥95% | **99.3%**  | ✅ SUPERADO |

**Ver análisis completo en:** [DOCUMENTACION_COMPLETA_S2.md](DOCUMENTACION_COMPLETA_S2.md#4-resultados-y-análisis)

---

## 🆘 Troubleshooting

| Problema           | Solución                                                                                       |
| ------------------ | ---------------------------------------------------------------------------------------------- |
| Layout no existe   | `python generador_layout.py --escenario seed1 --seed 1 --ancho 350 --alto 250 --estaciones 30` |
| Pedidos no existen | `python generador_pedidos.py --escenario seed1 --pedidos 600 --burst`                          |
| Simulación lenta   | Normal con 100+ robots (10-15 min cada una)                                                    |

**Ver más en:** [DOCUMENTACION_COMPLETA_S2.md](DOCUMENTACION_COMPLETA_S2.md#34-troubleshooting)

---

**Última actualización:** Marzo 2026

---

## ✅ Resultados Obtenidos

| Objetivo                  | Meta | Resultado | Estado      |
| ------------------------- | ---- | --------- | ----------- |
| Reducir Tiempo Promedio   | -30% | -40.5%    | ✅ SUPERADO |
| Reducir Distancia Total   | -20% | -68.9%    | ✅ SUPERADO |
| Mantener Completitud ≥95% | 95%  | 99.3%     | ✅ SUPERADO |

Ver [REPORTE_FINAL_S2.md](REPORTE_FINAL_S2.md) para análisis detallado.

---

## 📚 Documentación

- **[REPORTE_FINAL_S2.md](REPORTE_FINAL_S2.md)** - Análisis completo con hallazgos
- **[docs/DOCUMENTACION_TECNICA_MEJORA_EJE_A.md](docs/DOCUMENTACION_TECNICA_MEJORA_EJE_A.md)** - Especificación técnica
- **[docs/GUIA_EJECUCION_S2.md](docs/GUIA_EJECUCION_S2.md)** - Guía paso a paso
- **[docs/RESUMEN_EJECUTIVO.md](docs/RESUMEN_EJECUTIVO.md)** - Resumen de implementación
