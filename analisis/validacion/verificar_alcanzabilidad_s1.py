#!/usr/bin/env python3
"""
Verificar alcanzabilidad: ¿Todos los anaqueles son accesibles desde los spawn points?
"""

import json
import numpy as np
import os
from pathlib import Path
from typing import List, Set, Tuple

LIBRE = 0
ANAQUEL = 1
ESTACION = 2
BLOQUEADO = 3

def obtener_ruta_outputs():
    """Detecta automáticamente la ruta a la carpeta outputs."""
    # Si estamos en analisis/validacion/
    script_dir = Path(__file__).parent.parent.parent
    outputs_dir = script_dir / "outputs"
    
    if outputs_dir.exists():
        return str(outputs_dir)
    
    # Si estamos en la raíz del proyecto
    if Path("outputs").exists():
        return "outputs"
    
    raise FileNotFoundError("No se encontró carpeta 'outputs'")

def bfs_alcanzabilidad(grid: np.ndarray, inicio: Tuple[int, int]) -> Set[Tuple[int, int]]:
    """BFS para encontrar todas las celdas alcanzables desde un punto de inicio."""
    alto, ancho = grid.shape
    alcanzables = set()
    cola = [inicio]
    alcanzables.add(inicio)
    
    while cola:
        x, y = cola.pop(0)
        
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = x + dx, y + dy
            
            if 0 <= nx < ancho and 0 <= ny < alto:
                if (nx, ny) not in alcanzables:
                    # Solo podemos movernos a LIBRE o ESTACION
                    if grid[ny, nx] in (LIBRE, ESTACION):
                        alcanzables.add((nx, ny))
                        cola.append((nx, ny))
    
    return alcanzables

def verificar_alcanzabilidad(escenario: str, outputs_dir: str):
    """Verificar si todos los anaqueles son alcanzables."""
    print(f"\n{'='*80}")
    print(f"🔍 VERIFICACIÓN DE ALCANZABILIDAD: {escenario}")
    print(f"{'='*80}\n")
    
    # Cargar archivos - usar el outputs_dir proporcionado
    ruta_layout = os.path.join(outputs_dir, escenario, "layout.npy")
    ruta_spawn = os.path.join(outputs_dir, escenario, "spawn.json")
    ruta_anaqueles = os.path.join(outputs_dir, escenario, "anaqueles.json")
    ruta_estaciones = os.path.join(outputs_dir, escenario, "estaciones.json")
    
    if not all(os.path.exists(r) for r in [ruta_layout, ruta_spawn, ruta_anaqueles, ruta_estaciones]):
        print("❌ Archivos faltantes")
        return
    
    grid = np.load(ruta_layout)
    alto, ancho = grid.shape
    
    with open(ruta_spawn) as f:
        spawns = json.load(f)
    
    with open(ruta_anaqueles) as f:
        anaqueles = json.load(f)
    
    with open(ruta_estaciones) as f:
        estaciones = json.load(f)
    
    print(f"📌 DATOS DEL ESCENARIO:")
    print(f"   Layout: {ancho} × {alto}")
    print(f"   Spawn points: {len(spawns)}")
    print(f"   Anaqueles: {len(anaqueles)}")
    print(f"   Estaciones: {len(estaciones)}")
    
    # Verificar alcanzabilidad desde primer spawn
    if not spawns:
        print("\n❌ No hay spawn points!")
        return
    
    primer_spawn = tuple(spawns[0])
    print(f"\n🚀 Calculando alcanzabilidad desde spawn: {primer_spawn}")
    
    alcanzables = bfs_alcanzabilidad(grid, primer_spawn)
    print(f"   Celdas alcanzables (LIBRE/ESTACION): {len(alcanzables)}")
    
    # Verificar cada anaquel
    anaqueles_alcanzables = 0
    anaqueles_inaccesibles = []
    
    for anaquel in anaqueles:
        anaquel_id = anaquel['anaquel_id']
        ax, ay = anaquel['home']
        
        # Verificar celdas adyacentes (un robot debe poder pararse al lado)
        adyacentes_alcanzables = False
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nx, ny = ax + dx, ay + dy
            if (nx, ny) in alcanzables:
                adyacentes_alcanzables = True
                break
        
        if adyacentes_alcanzables:
            anaqueles_alcanzables += 1
        else:
            anaqueles_inaccesibles.append({
                'id': anaquel_id,
                'pos': (ax, ay)
            })
    
    # Verificar estaciones
    estaciones_alcanzables = 0
    estaciones_inaccesibles = []
    
    for est in estaciones:
        est_id = est['estacion_id']
        dx, dy = est['dock']
        
        if (dx, dy) in alcanzables:
            estaciones_alcanzables += 1
        else:
            estaciones_inaccesibles.append({
                'id': est_id,
                'dock': (dx, dy)
            })
    
    # Reporte
    print(f"\n📊 RESULTADOS:")
    print(f"─" * 80)
    
    # Anaqueles
    pct_anaqueles = (anaqueles_alcanzables / len(anaqueles)) * 100 if anaqueles else 0
    simbolo_anaqueles = "✅" if pct_anaqueles > 98 else "⚠️ " if pct_anaqueles > 90 else "🔴"
    print(f"{simbolo_anaqueles} Anaqueles alcanzables: {anaqueles_alcanzables}/{len(anaqueles)} ({pct_anaqueles:.1f}%)")
    
    if anaqueles_inaccesibles:
        print(f"   🔴 Anaqueles INACCESIBLES: {len(anaqueles_inaccesibles)}")
        if len(anaqueles_inaccesibles) <= 10:
            for a in anaqueles_inaccesibles[:10]:
                print(f"      • Anaquel #{a['id']} en {a['pos']}")
        else:
            print(f"      (Mostrando primeros 10 de {len(anaqueles_inaccesibles)})")
            for a in anaqueles_inaccesibles[:10]:
                print(f"      • Anaquel #{a['id']} en {a['pos']}")
    
    # Estaciones
    pct_estaciones = (estaciones_alcanzables / len(estaciones)) * 100 if estaciones else 0
    simbolo_estaciones = "✅" if pct_estaciones == 100 else "🔴"
    print(f"{simbolo_estaciones} Estaciones alcanzables: {estaciones_alcanzables}/{len(estaciones)} ({pct_estaciones:.1f}%)")
    
    if estaciones_inaccesibles:
        print(f"   🔴 Estaciones INACCESIBLES: {len(estaciones_inaccesibles)}")
        for e in estaciones_inaccesibles:
            print(f"      • Estación #{e['id']} dock en {e['dock']}")
    
    # Análisis de distribución
    print(f"\n📍 DISTRIBUCIÓN ESPACIAL:")
    
    # Verificar si anaqueles inaccesibles están concentrados
    if anaqueles_inaccesibles:
        pos_x = [a['pos'][0] for a in anaqueles_inaccesibles]
        pos_y = [a['pos'][1] for a in anaqueles_inaccesibles]
        
        print(f"   Anaqueles inaccesibles:")
        print(f"      X range: {min(pos_x)} - {max(pos_x)} (ancho total: {ancho})")
        print(f"      Y range: {min(pos_y)} - {max(pos_y)} (alto total: {alto})")
        
        # Detectar si están en una zona específica
        if max(pos_x) - min(pos_x) < ancho * 0.3:
            print(f"      ⚠️  CONCENTRADOS en zona X={min(pos_x)}-{max(pos_x)}")
        if max(pos_y) - min(pos_y) < alto * 0.3:
            print(f"      ⚠️  CONCENTRADOS en zona Y={min(pos_y)}-{max(pos_y)}")
    
    # Diagnóstico
    print(f"\n💡 DIAGNÓSTICO:")
    print(f"─" * 80)
    
    if pct_anaqueles > 98 and pct_estaciones == 100:
        print("✅ Alcanzabilidad CORRECTA")
        print("   Todos los anaqueles y estaciones son accesibles.")
        print("   El problema NO es de conectividad.")
    elif pct_anaqueles > 80:
        print("⚠️  Alcanzabilidad PARCIAL")
        print(f"   {len(anaqueles_inaccesibles)} anaqueles ({100-pct_anaqueles:.1f}%) NO SON ACCESIBLES")
        print("   ESTO EXPLICA por qué ~15% de pedidos no se completan.")
        print("\n   Causa probable:")
        print("   • Zona del almacenaje está fragmentada")
        print("   • Macrobloques aislados entre sí")
        print("   • Cross-aisles no conectan todas las regiones")
    else:
        print("🔴 Alcanzabilidad CRÍTICA")
        print(f"   {len(anaqueles_inaccesibles)} anaqueles ({100-pct_anaqueles:.1f}%) NO SON ACCESIBLES")
        print("   Sistema completamente roto.")
    
    print(f"\n{'='*80}\n")
    
    return {
        'total_anaqueles': len(anaqueles),
        'anaqueles_alcanzables': anaqueles_alcanzables,
        'anaqueles_inaccesibles': len(anaqueles_inaccesibles),
        'pct_alcanzable': pct_anaqueles
    }

def main():
    print("\n🔍 VERIFICADOR DE ALCANZABILIDAD S1")
    print("="*80)
    print("Este script verifica si todos los anaqueles son accesibles desde spawn points.\n")
    
    outputs_dir = obtener_ruta_outputs()
    print(f"📁 Usando outputs de: {outputs_dir}\n")
    
    escenarios = [
        "S1_baseline_seed42",
        "S1_baseline_seed1"
    ]
    
    resultados = {}
    
    for escenario in escenarios:
        res = verificar_alcanzabilidad(escenario, outputs_dir)
        if res:
            resultados[escenario] = res
    
    # Resumen final
    print("\n" + "="*80)
    print("📋 RESUMEN COMPARATIVO")
    print("="*80)
    
    for esc, res in resultados.items():
        seed = "seed42" if "seed42" in esc else "seed1"
        print(f"\n{seed}:")
        print(f"  Anaqueles alcanzables: {res['anaqueles_alcanzables']}/{res['total_anaqueles']} ({res['pct_alcanzable']:.1f}%)")
        print(f"  Anaqueles inaccesibles: {res['anaqueles_inaccesibles']}")
    
    print("\n" + "="*80)
    print("💡 CONCLUSIÓN:")
    print("="*80)
    
    if all(r['pct_alcanzable'] > 98 for r in resultados.values()):
        print("✅ NO es problema de alcanzabilidad")
        print("   El problema debe estar en otro lugar (timeout, lógica de asignación, etc.)")
    else:
        print("🔴 SÍ es problema de alcanzabilidad")
        print("   Algunos anaqueles están físicamente aislados del resto del almacén.")
        print("\n   SOLUCIÓN:")
        print("   1. Aumentar cross-aisles (más conectores horizontales)")
        print("   2. Verificar que macrobloques estén conectados entre sí")
        print("   3. Aumentar pasillos principales (más conectores verticales)")
    
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
