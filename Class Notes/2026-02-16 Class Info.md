# Ejes oficiales de mejora

Cada equipo deberá elegir un eje principal de mejora.
La evaluación se centrará prioritariamente en:

## Eje A - Asignación de pedidos

**Decidir**

- Qué robot atiende qué pedido y en qué momento

**Métricas típicamente impactadas**

- Throughput
- Tiempo promedio de ciclo del pedido
- Tiempo de completitud
- Tiempo de utilización de robots

**Ejemplos**

- Asignación basada en costo
- Priorización por antigüedad de un pedido
- Asignación anticipada

## Eje B - Planeación de rutas

Método para calcular la trayectoria de los robots.

**Métricas típicamente impactadas**

- Distancia total recorrida
- Congestión
- Tiempo de espera

**Ejemplos**

- Comparación entre heurísticas admisibles
- Modificación de la función de costo A\*
- Preferencia por pasillos principales o cross-aisles
- Replanificación de rutas

## Eje C - Coordinación multirobótica

Evitar conflictos, bloqueos y comportamientos inestables entre robots.

**Métricas típicamente impactadas**

- Eventos de bloqueo
- Tiempo total en espera
- Estabilidad de sistemas con flotas grandes

**Ejemplos**

- Priorización entre robots (por carga, estación o antigüedad)
- Detección y resolución de deadlocks
- Reglas de derecho de paso

## Eje D - Políticas operativas del almacén

Reglas estructurales del CEDIS sin alterar la validez del benchmark.

**Métricas típicamente impactadas**

- Congestión localizada
- Utilización
- Robustez ante picos de demanda

**Ejemplos**

- Pasillos en un solo sentido
- Zonas de estacionamiento para robots inactivos
- Reposicionamiento proactivo de robots

## Eje E - Instrumentación y análisis avanzado

Cómo se mide, analiza e interpreta el desempeño del sistema.

**Métricas típicamente impactadas**

- Claridad del análisis
- Calidad experimental
- Capacidad de explicar trade-offs

**Ejemplos**

- Nuevas métricas (percentiles, varianza, etc.)
- Métricas por zona del layout
- Análisis temporal (warmup vs. estado estable)

## Reglas de selección del eje

- Cada equipo debe declarar un eje principal de mejora
- El eje elegido debe indicarse explícitamente en el informe final
- Dos o más equipos pueden elegir el mismo eje sin penalización
- La evaluación se centrará en la calidad de la mejora implementada

## Escenarios de evaluación

### S1 - Baseline operativo

Establecer una referencia controlada.

**Uso**

- Comparación baseline vs mejora
- Generación obligatoria de video y heatmap

### S2 - Estrés de flota

Evaluar escalabilidad y congestión.

**Características**

- Mismo layout y pedidos que S1
- Incremento del número de robots (x2, x3, etc.)
- Misma semilla

**Uso**

- Análisis de congestión
- Detección de bloqueos y livelocks

### S3 - Estrés de demanda

Evaluar respuesta a picos de pedidos.

**Características**

- Mismo layout que S1
- Incremento del número de pedidos
- Número intermedio de robots
- Misma semilla

**Uso**

- Análisis de throughput
- Estabilidad temporal
- Degradación controlada del desempeño

## Reglas de comparación experimental

Cada escenario debe ejecutarse:

- Una vez con baseline
- Una vez con la versión mejorada

Las comparaciones deben realizarse bajo condiciones idénticas.

Si una mejora optimiza una métrica y degrada otra, el equipo debe reportarlo explícitamente y analizar el trade-off.

## Evidencia mínima requerida

**Escenario S1 (obligatorio)**

- Métrica baseline y escenario mejorado
- Video de la simulación al menos de la versión mejorada
- Heatmap de tráfico

**Escenarios S2 y S3**

- Métricas comparativas
- Video

## Definición de modificación válida

Una modificación es válida si:

- No consiste en cambios puramente visuales o cosméticos
- Modifica al menos uno de los 5 ejes de mejora
- Tiene al least una métrica cuantitativa
- Puede compararse directamente contra el baseline
- Es reproducible (mismo escenario, misma semilla, mismos resultados)

Se puede hacer modificaciones en otros ejes. El eje principal tendrá mayor peso en la calificación.
