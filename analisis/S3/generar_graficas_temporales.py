#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
from typing import List

import matplotlib.pyplot as plt


def _load_series(path: Path) -> dict:
    if not path.exists():
        raise FileNotFoundError(f"No existe {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def _extract(series: dict, key: str) -> List:
    return [v.get(key) for v in series.get("ventanas", [])]


def _save_plot(x, y, title: str, y_label: str, out_path: Path) -> None:
    plt.figure(figsize=(10, 4))
    plt.plot(x, y, linewidth=2)
    plt.title(title)
    plt.xlabel("tick")
    plt.ylabel(y_label)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    plt.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--escenario",
        type=str,
        default=None,
        help="Nombre del escenario para buscar outputs/<escenario>/metricas_temporales.json",
    )
    parser.add_argument("--entrada_json", type=str, default=None)
    parser.add_argument("--salida_dir", type=str, default=None)
    args = parser.parse_args()

    if not args.entrada_json and not args.escenario:
        raise SystemExit("Debes especificar --escenario o --entrada_json")

    if args.entrada_json:
        in_path = Path(args.entrada_json)
    else:
        in_path = Path("outputs") / args.escenario / "metricas_temporales.json"

    series = _load_series(in_path)
    escenario = series.get("escenario", args.escenario or "escenario")

    if args.salida_dir:
        out_dir = Path(args.salida_dir)
    else:
        out_dir = Path("analisis") / "S3" / "graficos" / str(escenario)
    out_dir.mkdir(parents=True, exist_ok=True)

    ticks = _extract(series, "tick_fin")

    throughput = _extract(series, "throughput_ventana")
    cola = _extract(series, "pedidos_pendientes_cola")
    congestion = _extract(series, "eventos_congestion_ventana")
    p95_pedido = _extract(series, "p95_pedido_ventana")

    _save_plot(
        ticks,
        throughput,
        f"Throughput por ventana ({escenario})",
        "pedidos/1000 ticks",
        out_dir / "throughput_vs_tiempo.png",
    )

    _save_plot(
        ticks,
        cola,
        f"Pedidos en cola ({escenario})",
        "pedidos pendientes",
        out_dir / "cola_vs_tiempo.png",
    )

    _save_plot(
        ticks,
        congestion,
        f"Eventos de congestion por ventana ({escenario})",
        "eventos",
        out_dir / "congestion_vs_tiempo.png",
    )

    _save_plot(
        ticks,
        p95_pedido,
        f"p95 tiempo por pedido (ventana) ({escenario})",
        "ticks",
        out_dir / "p95_pedido_vs_tiempo.png",
    )

    print(f"[OK] Graficas en: {out_dir}")


if __name__ == "__main__":
    main()
