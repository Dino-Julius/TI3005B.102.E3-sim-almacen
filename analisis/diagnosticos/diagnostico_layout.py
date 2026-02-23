#!/usr/bin/env python3
"""
Script de diagnóstico: Visualizar y analizar layouts
Para layouts escalados 300×200 usar nomenclatura: S1_baseline_{seed}

Ejemplos:
    python diagnostico_layout.py --escenario S1_baseline_seed1
    python diagnostico_layout.py --escenario S1_baseline_seed42
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import os
from pathlib import Path

# Constantes (deben coincidir con generador_layout.py)
LIBRE = 0
ANAQUEL = 1
ESTACION = 2
BLOQUEADO = 3

NOMBRE_CELDA = {
    0: "LIBRE",
    1: "ANAQUEL",
    2: "ESTACION",
    3: "BLOQUEADO"
}

def obtener_ruta_outputs():
    """Detecta automáticamente la ruta a la carpeta outputs."""
    # Si estamos en analisis/diagnosticos/
    script_dir = Path(__file__).parent.parent.parent
    outputs_dir = script_dir / "outputs"
    
    if outputs_dir.exists():
        return str(outputs_dir)
    
    # Si estamos en la raíz del proyecto
    if Path("outputs").exists():
        return "outputs"
    
    raise FileNotFoundError("No se encontró carpeta 'outputs'")

def analizar_layout(escenario, titulo, outputs_dir):
    """Analizar y visualizar un layout."""
    print(f"\n{'='*80}")
    print(f"📊 ANÁLISIS: {titulo}")
    print(f"{'='*80}")
    
    # Cargar grid usando el outputs_dir proporcionado
    ruta_layout = os.path.join(outputs_dir, escenario, "layout.npy")
    if not os.path.exists(ruta_layout):
        print(f"❌ No encontrado: {ruta_layout}")
        return False
    
    grid = np.load(ruta_layout)
    height, width = grid.shape
    
    # Estadísticas básicas
    libres = np.sum(grid == LIBRE)
    anaqueles = np.sum(grid == ANAQUEL)
    estaciones = np.sum(grid == ESTACION)
    bloqueados = np.sum(grid == BLOQUEADO)
    
    print(f"\n🔹 DIMENSIONES:")
    print(f"   Tamaño: {width} × {height}")
    print(f"   Área: {width * height} m²")
    
    print(f"\n🔹 COMPOSICIÓN:")
    print(f"   LIBRE (navegable):  {libres:6d} ({100*libres/(width*height):.1f}%)")
    print(f"   ANAQUEL (racks):    {anaqueles:6d} ({100*anaqueles/(width*height):.1f}%)")
    print(f"   ESTACION (pickup):  {estaciones:6d} ({100*estaciones/(width*height):.1f}%)")
    print(f"   BLOQUEADO (border): {bloqueados:6d} ({100*bloqueados/(width*height):.1f}%)")
    
    # Análisis de conectividad
    print(f"\n🔹 CONECTIVIDAD:")
    
    # Buscar spawn points
    ruta_spawn = f"outputs/{escenario}/spawn.json"
    try:
        with open(ruta_spawn) as f:
            spawns = json.load(f)
        print(f"   Spawn points: {len(spawns)}")
        
        # Distribution de spawns
        if spawns:
            spawn_x = [s[0] for s in spawns]
            spawn_y = [s[1] for s in spawns]
            print(f"   X range: {min(spawn_x)}-{max(spawn_x)}")
            print(f"   Y range: {min(spawn_y)}-{max(spawn_y)}")
    except:
        print(f"   ❌ No se pudieron leer spawn points")
    
    # Análisis de pasillos
    print(f"\n🔹 PASILLOS PRINCIPALES:")
    
    # Contar pasillos verticales principales (primeras columnas LIBRE)
    pasillos_vert = 0
    for x in range(min(20, width)):
        if np.sum(grid[:, x] == LIBRE) > height * 0.7:
            pasillos_vert += 1
    
    # Contar pasillos horizontales (últimas filas, zona de estaciones)
    pasillos_horiz = 0
    for y in range(max(0, height-20), height):
        if np.sum(grid[y, :] == LIBRE) > width * 0.5:
            pasillos_horiz += 1
    
    print(f"   Pasillos verticales importantes (primeras 20 cols): {pasillos_vert}")
    print(f"   Pasillos horizontales importantes (últimas 20 filas): {pasillos_horiz}")
    
    # Cross-aisles (pasillos cada 10 filas)
    cross_aisles = 0
    for y in range(0, height, 10):
        # Contar si hay un pasillo horizontal ancho
        if np.sum(grid[y:y+2, :] == LIBRE) > width * 0.5:
            cross_aisles += 1
    print(f"   Cross-aisles detectados (cada ~10 filas): {cross_aisles}")
    
    # Zona de parking/carga
    print(f"\n🔹 ZONA PARKING/CARGA:")
    # Buscar rectángulo grande de LIBRE en esquina inferior-izquierda
    for x_start in range(0, min(50, width)):
        for y_start in range(max(0, height-50), height):
            # Contar rectángulo de LIBRE
            for dx in range(5, 50):
                for dy in range(5, 50):
                    x_end = x_start + dx
                    y_end = y_start + dy
                    if x_end < width and y_end < height:
                        subgrid = grid[y_start:y_end, x_start:x_end]
                        libres_sub = np.sum(subgrid == LIBRE)
                        ratio_libres = libres_sub / (dx * dy)
                        if ratio_libres > 0.8 and dx > 15 and dy > 10:
                            print(f"   Zona detectada: ({x_start},{y_start}) → ({x_end},{y_end})")
                            print(f"   Tamaño: {dx}×{dy}, {libres_sub}/{dx*dy} células libres ({ratio_libres*100:.0f}%)")
    
    # Conexión parking ↔ almacenaje
    print(f"\n🔹 CONEXIÓN PARKING ↔ ALMACENAJE:")
    # Buscar corredores de conexión
    for x in range(0, width):
        col_libres = np.sum(grid[:, x] == LIBRE)
        if col_libres > height * 0.8:  # Casi todo libre (pasillo vertical)
            print(f"   Columna {x}: {col_libres}/{height} libres (pasillo vertical principal)")
            if x > 20:
                break  # Solo los primeros pasillos principales
    
    # Visualizar
    print(f"\n🔹 GENERANDO VISUALIZACIÓN...")
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))
    
    # Subplot 1: Mapa del layout
    ax1 = axes[0]
    cmap = plt.cm.get_cmap('tab10')
    colors = {
        LIBRE: [1, 1, 1],      # Blanco
        ANAQUEL: [0.2, 0.2, 0.8],  # Azul oscuro
        ESTACION: [0, 1, 0],   # Verde
        BLOQUEADO: [0.5, 0.5, 0.5]  # Gris
    }
    
    grid_visual = np.zeros((*grid.shape, 3))
    for val, color in colors.items():
        mask = grid == val
        grid_visual[mask] = color
    
    ax1.imshow(grid_visual, origin='upper')
    ax1.set_title(f"Layout {titulo}\n{width}×{height} ({width*height} m²)", fontsize=14, fontweight='bold')
    ax1.set_xlabel("X (ancho)")
    ax1.set_ylabel("Y (alto)")
    
    # Subplot 2: Densidad de LIBRE (navegable)
    ax2 = axes[1]
    # Calcular densidad local de células libres (ventana 20×20)
    window = 20
    density = np.zeros((height - window, width - window))
    for y in range(height - window):
        for x in range(width - window):
            subgrid = grid[y:y+window, x:x+window]
            density[y, x] = np.sum(subgrid == LIBRE) / (window * window)
    
    im = ax2.imshow(density, cmap='RdYlGn', origin='upper', vmin=0, vmax=1)
    ax2.set_title(f"Densidad Local de Navegabilidad\n(ventana {window}×{window})", 
                  fontsize=14, fontweight='bold')
    ax2.set_xlabel("X (ancho)")
    ax2.set_ylabel("Y (alto)")
    plt.colorbar(im, ax=ax2, label="Fracción de celdas libres")
    
    plt.tight_layout()
    # Guardar en outputs/ dentro de la carpeta de diagnósticos
    os.makedirs("outputs", exist_ok=True)
    output_file = f"outputs/diagnostico_layout_{escenario}.png"
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"   ✅ Guardado: {output_file}")
    plt.close()
    
    return True

def comparar_layouts(outputs_dir):
    """Comparar los dos layouts."""
    print(f"\n\n{'='*80}")
    print(f"📈 COMPARACIÓN LAYOUTS")
    print(f"{'='*80}")
    
    escenarios = [
        ("S1_baseline_seed42", "seed42 - S1 Baseline (300×200)"),
        ("S1_baseline_seed1", "seed1 - S1 Baseline (300×200)")
    ]
    
    for escenario, titulo in escenarios:
        analizar_layout(escenario, titulo, outputs_dir)

if __name__ == "__main__":
    print("\n🔍 DIAGNOSTICADOR DE LAYOUT S1")
    print("="*80)
    print("Este script analiza los layouts para identificar problemas de conectividad")
    print("y explica por qué throughput bajó y deadlocks desaparecieron.\n")
    
    outputs_dir = obtener_ruta_outputs()
    print(f"📂 Usando outputs de: {outputs_dir}\n")
    
    comparar_layouts(outputs_dir)
    
    print(f"\n\n{'='*80}")
    print("📋 RESUMEN DIAGNÓSTICO")
    print(f"{'='*80}")
    print("\nBusca en los archivos generados:")
    print("  • diagnostico_layout_S1_baseline_seed42.png")
    print("  • diagnostico_layout_S1_baseline_seed1.png")
    print("\nObserva:")
    print("  1. ¿Hay zonas completamente desconectadas? (islas en rojo)")
    print("  2. ¿La zona de parking está aislada? (color diferente)")
    print("  3. ¿Hay suficientes pasillos horizontales? (cross-aisles)")
    print("  4. ¿El corredor de conexión es ancho suficiente?")
    print("\n" + "="*80)
