#!/usr/bin/env python3
from sim_core import Pedido, SimAlmacen, cargar_layout
from out_paths import asegurar_dirs_de_salidas
import argparse
import csv
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _ruta_por_escenario(escenario: str, nombre_archivo: str) -> str:
    return os.path.join("outputs", escenario, nombre_archivo)


def cargar_pedidos(ruta: str) -> List[Pedido]:
    with open(ruta, "r", encoding="utf-8") as f:
        data = json.load(f)

    pedidos: List[Pedido] = []
    for p in data.get("pedidos", []):
        pedidos.append(
            Pedido(
                pedido_id=int(p["pedido_id"]),
                anaquel_id=int(p["anaquel_id"]),
                estacion_id=int(p["estacion_id"]),
                tick_creacion=int(p.get("tick_creacion", 0)),
            )
        )
    return pedidos


def _p95(values: List[float]) -> Optional[float]:
    if not values:
        return None
    return float(np.percentile(np.array(values, dtype=float), 95))


def _snapshot(
    sim: SimAlmacen,
    tick_inicio: int,
    tick_fin: int,
    prev_completados: int,
    prev_eventos_alto: int,
    prev_ticks_espera: List[int],
    prev_ticks_ocupado: List[int],
    prev_tick_snapshot: int,
) -> Dict:
    completados = [p for p in sim.pedidos if p.tick_completado is not None]
    completados_n = len(completados)

    completados_ventana = completados_n - prev_completados
    ticks_ventana = tick_fin - prev_tick_snapshot

    tiempos_pedido_acum = [
        (p.tick_completado - p.tick_creacion) for p in completados
    ]

    tiempos_pedido_ventana = [
        (p.tick_completado - p.tick_creacion)
        for p in completados
        if p.tick_completado is not None
        and prev_tick_snapshot < p.tick_completado <= tick_fin
    ]

    ticks_espera_actual = [r.ticks_espera for r in sim.lista_robots]
    ticks_espera_ventana = [
        curr - prev
        for curr, prev in zip(ticks_espera_actual, prev_ticks_espera)
    ]

    ticks_ocupado_actual = [r.ticks_ocupado for r in sim.lista_robots]
    ticks_ocupado_ventana = [
        curr - prev
        for curr, prev in zip(ticks_ocupado_actual, prev_ticks_ocupado)
    ]

    utilizacion_acum = float(
        np.mean([r.ticks_ocupado / max(1, tick_fin) for r in sim.lista_robots])
    ) if sim.lista_robots else 0.0

    utilizacion_ventana = float(
        np.mean([v / max(1, ticks_ventana) for v in ticks_ocupado_ventana])
    ) if ticks_ocupado_ventana else 0.0

    throughput_ventana = 0.0
    if ticks_ventana > 0:
        throughput_ventana = completados_ventana / (ticks_ventana / 1000.0)

    pedidos_pendientes_cola = len(sim.pendientes) + len(sim.no_liberados)
    pedidos_en_proceso = sum(
        1 for r in sim.lista_robots if r.pedido_id is not None)

    return {
        "tick_inicio": tick_inicio,
        "tick_fin": tick_fin,
        "ticks_ventana": ticks_ventana,
        "throughput_ventana": throughput_ventana,
        "pedidos_completados_ventana": completados_ventana,
        "pedidos_completados_acumulados": completados_n,
        "pedidos_pendientes_cola": pedidos_pendientes_cola,
        "pedidos_en_proceso": pedidos_en_proceso,
        "p95_pedido_ventana": _p95(tiempos_pedido_ventana),
        "p95_pedido_acumulado": _p95(tiempos_pedido_acum),
        "p95_espera_ventana": _p95(ticks_espera_ventana),
        "p95_espera_acumulado": _p95(ticks_espera_actual),
        "eventos_congestion_ventana": sim.eventos_alto - prev_eventos_alto,
        "deadlocks_acumulados": sim.conteo_deadlock,
        "utilizacion_ventana": utilizacion_ventana,
        "utilizacion_acumulada": utilizacion_acum,
    }


def _write_csv(path: str, rows: List[Dict]) -> None:
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--robots", type=int, default=200)
    parser.add_argument("--ticks", type=int, default=15000)
    parser.add_argument("--ventana", type=int, default=500)
    parser.add_argument(
        "--modo_asignacion",
        type=str,
        choices=["baseline", "mejora"],
        default="mejora",
    )
    parser.add_argument(
        "--escenario",
        type=str,
        default="S3_extendido",
        help="Nombre del escenario. Lee de outputs/<escenario>/ y escribe resultados ahi.",
    )

    parser.add_argument("--layout", type=str, default=None)
    parser.add_argument("--estaciones", type=str, default=None)
    parser.add_argument("--anaqueles", type=str, default=None)
    parser.add_argument("--spawn", type=str, default=None)
    parser.add_argument("--pedidos", type=str, default=None)

    parser.add_argument("--salida_metricas", type=str, default=None)
    parser.add_argument("--salida_temporal_json", type=str, default=None)
    parser.add_argument("--salida_temporal_csv", type=str, default=None)

    args = parser.parse_args()

    ruta_layout = args.layout or _ruta_por_escenario(
        args.escenario, "layout.npy")
    ruta_estaciones = args.estaciones or _ruta_por_escenario(
        args.escenario, "estaciones.json")
    ruta_anaqueles = args.anaqueles or _ruta_por_escenario(
        args.escenario, "anaqueles.json")
    ruta_spawn = args.spawn or _ruta_por_escenario(
        args.escenario, "spawn.json")
    ruta_pedidos = args.pedidos or _ruta_por_escenario(
        args.escenario, "pedidos.json")

    ruta_metricas = args.salida_metricas or _ruta_por_escenario(
        args.escenario, "metricas.json"
    )
    ruta_temporal_json = args.salida_temporal_json or _ruta_por_escenario(
        args.escenario, "metricas_temporales.json"
    )
    ruta_temporal_csv = args.salida_temporal_csv or _ruta_por_escenario(
        args.escenario, "metricas_temporales.csv"
    )

    asegurar_dirs_de_salidas(
        [ruta_metricas, ruta_temporal_json, ruta_temporal_csv])

    grid, estacion_dock, anaquel_home, spawns = cargar_layout(
        ruta_layout, ruta_estaciones, ruta_anaqueles, ruta_spawn
    )
    pedidos = cargar_pedidos(ruta_pedidos)

    sim = SimAlmacen(
        grid=grid,
        estacion_dock=estacion_dock,
        anaquel_home=anaquel_home,
        robots=args.robots,
        puntos_spawn=spawns,
        pedidos=pedidos,
        seed=args.seed,
        modo_asignacion=args.modo_asignacion,
    )

    ventanas: List[Dict] = []
    prev_completados = 0
    prev_eventos_alto = 0
    prev_ticks_espera = [0 for _ in sim.lista_robots]
    prev_ticks_ocupado = [0 for _ in sim.lista_robots]
    prev_tick_snapshot = 0

    for _ in range(args.ticks):
        sim.step()
        if sim.tick % args.ventana == 0 or sim.tick == args.ticks:
            tick_inicio = prev_tick_snapshot + 1
            tick_fin = sim.tick
            snapshot = _snapshot(
                sim,
                tick_inicio,
                tick_fin,
                prev_completados,
                prev_eventos_alto,
                prev_ticks_espera,
                prev_ticks_ocupado,
                prev_tick_snapshot,
            )
            ventanas.append(snapshot)

            prev_completados = snapshot["pedidos_completados_acumulados"]
            prev_eventos_alto = sim.eventos_alto
            prev_ticks_espera = [r.ticks_espera for r in sim.lista_robots]
            prev_ticks_ocupado = [r.ticks_ocupado for r in sim.lista_robots]
            prev_tick_snapshot = tick_fin

    metricas_finales = sim.metricas()
    with open(ruta_metricas, "w", encoding="utf-8") as f:
        json.dump(metricas_finales, f, indent=2, ensure_ascii=True)

    salida_temporal = {
        "escenario": args.escenario,
        "seed": args.seed,
        "robots": args.robots,
        "ticks": args.ticks,
        "ventana": args.ventana,
        "modo_asignacion": args.modo_asignacion,
        "metricas_finales": metricas_finales,
        "ventanas": ventanas,
    }

    with open(ruta_temporal_json, "w", encoding="utf-8") as f:
        json.dump(salida_temporal, f, indent=2, ensure_ascii=True)

    _write_csv(ruta_temporal_csv, ventanas)

    print(f"[OK] Escenario: {args.escenario}")
    print(f"[OK] Metricas final: {ruta_metricas}")
    print(f"[OK] Series temporales (JSON): {ruta_temporal_json}")
    print(f"[OK] Series temporales (CSV) : {ruta_temporal_csv}")


if __name__ == "__main__":
    main()
