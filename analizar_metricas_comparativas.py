
import json
import os
from typing import Dict, List

SEMILLAS = [1, 7, 13, 97, 256, 1337, 2024, 31415, 65537, 999999]

def cargar_metricas(escenario: str) -> Dict:
    ruta = os.path.join("outputs", escenario, "metricas.json")
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def main():
    print("=" * 80)
    print("ANÁLISIS COMPARATIVO: 10 SEMILLAS")
    print("=" * 80)
    
    resultados = {}
    for seed in SEMILLAS:
        escenario = f"seed{seed}"
        m = cargar_metricas(escenario)
        if m:
            resultados[seed] = m
            print(f"\n[seed{seed}]")
            print(f"  Pedidos completados: {m['pedidos_completados']}/{m['pedidos_totales']}")
            print(f"  Throughput:          {m['throughput_pedidos_por_1000_ticks']:.2f} pedidos/1000 ticks")
            print(f"  Tiempo promedio:     {m['tiempo_promedio_pedido_ticks']:.2f} ticks")
            print(f"  Utilización robots:  {m['utilizacion_promedio']*100:.2f}%")
            print(f"  Deadlocks:           {m['deadlock']}")
        else:
            print(f"\n[seed{seed}] ⚠️  NO EJECUTADA AÚN")
    
    # Estadísticas globales
    if resultados:
        print("\n" + "=" * 80)
        print("ESTADÍSTICAS GLOBALES")
        print("=" * 80)
        
        throughputs = [m['throughput_pedidos_por_1000_ticks'] for m in resultados.values()]
        tiempos = [m['tiempo_promedio_pedido_ticks'] for m in resultados.values()]
        utilizaciones = [m['utilizacion_promedio'] for m in resultados.values()]
        
        print(f"\nThroughput:")
        print(f"  Min: {min(throughputs):.2f}")
        print(f"  Max: {max(throughputs):.2f}")
        print(f"  Mean: {sum(throughputs)/len(throughputs):.2f}")
        print(f"  Desv.Est: {(sum((x - sum(throughputs)/len(throughputs))**2 for x in throughputs) / len(throughputs))**0.5:.2f}")
        
        print(f"\nTiempo promedio (ticks):")
        print(f"  Min: {min(tiempos):.2f}")
        print(f"  Max: {max(tiempos):.2f}")
        print(f"  Mean: {sum(tiempos)/len(tiempos):.2f}")
        
        print(f"\nUtilización promedio:")
        print(f"  Min: {min(utilizaciones)*100:.2f}%")
        print(f"  Max: {max(utilizaciones)*100:.2f}%")
        print(f"  Mean: {sum(utilizaciones)/len(utilizaciones)*100:.2f}%")

if __name__ == "__main__":
    main()