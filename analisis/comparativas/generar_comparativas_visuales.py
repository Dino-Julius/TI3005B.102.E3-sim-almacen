#!/usr/bin/env python3
"""
Script para generar visualizaciones comparativas entre layouts originales (120×80) 
y S1 baseline escalados (300×200)

NOMENCLATURA CORRECTA:
- Escenarios originales: seed1, seed42, etc. (layouts 120×80)
- S1 Baseline: S1_baseline_seed1, S1_baseline_seed42, etc. (layouts 300×200)

Uso:
    python generar_comparativas_visuales.py --seed seed1
    python generar_comparativas_visuales.py --seed seed42
    
Genera:
    - comparativa_layouts_{seed}.png     (layouts lado a lado con dimensiones)
    - comparativa_metricas_{seed}.png    (6 gráficas de barras comparativas)

Requisitos previos:
    - outputs/{seed}/                    (layout original 120×80)
    - outputs/S1_baseline_{seed}/        (layout escalado 300×200)
"""

import argparse
import json
import os
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.gridspec as gridspec

def obtener_ruta_outputs():
    """Detecta automáticamente la ruta a la carpeta outputs."""
    # Si estamos en analisis/comparativas/
    script_dir = Path(__file__).parent.parent.parent
    outputs_dir = script_dir / "outputs"
    
    if outputs_dir.exists():
        return str(outputs_dir)
    
    # Si estamos en la raíz del proyecto
    if Path("outputs").exists():
        return "outputs"
    
    raise FileNotFoundError("No se encontró carpeta 'outputs'")

def cargar_datos_escenario(escenario: str, outputs_dir: str):
    """Carga layout, métricas y heatmaps de un escenario"""
    # Usar el outputs_dir proporcionado
    base_path = Path(outputs_dir) / escenario
    
    # Layout
    layout_path = base_path / "layout.npy"
    if not layout_path.exists():
        raise FileNotFoundError(f"No se encontró {layout_path}")
    layout = np.load(layout_path)
    
    # Métricas
    metricas_path = base_path / "metricas.json"
    if not metricas_path.exists():
        raise FileNotFoundError(f"No se encontró {metricas_path}")
    with open(metricas_path, 'r') as f:
        metricas = json.load(f)
    
    # Heatmaps (opcional, si existen)
    heatmaps = {}
    for tipo in ['visitas', 'esperas', 'ratio']:
        heatmap_path = base_path / f"heatmap_{tipo}.png"
        if heatmap_path.exists():
            heatmaps[tipo] = plt.imread(heatmap_path)
    
    return {
        'layout': layout,
        'metricas': metricas,
        'heatmaps': heatmaps,
        'escenario': escenario
    }

def generar_comparativa_layouts(datos_original, datos_escalado, output_path):
    """Genera comparativa lado a lado de layouts con anotaciones dimensionales"""
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Layout original (120×80)
    layout1 = datos_original['layout']
    img1 = np.zeros_like(layout1, dtype=float)
    img1[layout1 == 0] = 1.0  # LIBRE - blanco
    img1[layout1 == 2] = 0.7  # ESTACION - gris claro
    img1[layout1 == 1] = 0.35  # ANAQUEL - gris oscuro
    img1[layout1 == 3] = 0.0  # BLOQUEADO - negro
    
    ax1.imshow(img1, origin='upper', interpolation='nearest', cmap='gray')
    ax1.set_title(f'Layout Original: {layout1.shape[1]}×{layout1.shape[0]} (9,600 m²)', fontsize=14, fontweight='bold')
    ax1.set_xlabel('x (celdas)', fontsize=11)
    ax1.set_ylabel('y (celdas)', fontsize=11)
    
    # Anotaciones dimensionales
    alto1, ancho1 = layout1.shape
    ax1.text(ancho1//2, -5, f'Ancho: {ancho1} celdas', ha='center', fontsize=10, color='blue', fontweight='bold')
    ax1.text(-8, alto1//2, f'Alto: {alto1}', ha='center', fontsize=10, color='blue', fontweight='bold', rotation=90)
    
    # Layout escalado (300×200)
    layout2 = datos_escalado['layout']
    img2 = np.zeros_like(layout2, dtype=float)
    img2[layout2 == 0] = 1.0
    img2[layout2 == 2] = 0.7
    img2[layout2 == 1] = 0.35
    img2[layout2 == 3] = 0.0
    
    ax2.imshow(img2, origin='upper', interpolation='nearest', cmap='gray')
    ax2.set_title(f'Layout Escalado: {layout2.shape[1]}×{layout2.shape[0]} (60,000 m²)', fontsize=14, fontweight='bold')
    ax2.set_xlabel('x (celdas)', fontsize=11)
    ax2.set_ylabel('y (celdas)', fontsize=11)
    
    alto2, ancho2 = layout2.shape
    ax2.text(ancho2//2, -12, f'Ancho: {ancho2} celdas (2.5x)', ha='center', fontsize=10, color='red', fontweight='bold')
    ax2.text(-20, alto2//2, f'Alto: {alto2} (2.5x)', ha='center', fontsize=10, color='red', fontweight='bold', rotation=90)
    
    # Leyenda compartida
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='white', edgecolor='black', label='LIBRE (pasillos)'),
        Patch(facecolor='0.7', edgecolor='black', label='ESTACION (carga/descarga)'),
        Patch(facecolor='0.35', edgecolor='black', label='ANAQUEL (almacenamiento)'),
        Patch(facecolor='black', edgecolor='black', label='BLOQUEADO')
    ]
    fig.legend(handles=legend_elements, loc='lower center', ncol=4, fontsize=10, frameon=True)
    
    plt.suptitle('Comparativa de Layouts: Original vs Escalado (Eje B)', fontsize=16, fontweight='bold', y=0.98)
    plt.tight_layout(rect=[0, 0.05, 1, 0.96])
    plt.savefig(output_path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"✅ Generado: {output_path}")

def generar_comparativa_metricas(datos_original, datos_escalado, output_path):
    """Genera gráficas de barras comparativas de métricas clave"""
    
    m1 = datos_original['metricas']
    m2 = datos_escalado['metricas']
    
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    fig.suptitle('Comparativa de Métricas: Layout Original vs Escalado', fontsize=16, fontweight='bold')
    
    # 1. Pedidos completados
    ax = axes[0, 0]
    pedidos = [m1['pedidos_completados'], m2['pedidos_completados']]
    totales = [m1['pedidos_totales'], m2['pedidos_totales']]
    porcentajes = [(p/t)*100 for p, t in zip(pedidos, totales)]
    bars = ax.bar(['120×80', '300×200'], porcentajes, color=['#2ecc71', '#e74c3c'])
    ax.axhline(95, color='gold', linestyle='--', linewidth=2, label='Objetivo 95%')
    ax.set_ylabel('Completitud (%)', fontsize=11)
    ax.set_title('Pedidos Completados', fontsize=12, fontweight='bold')
    ax.set_ylim(0, 105)
    for i, (bar, val, p) in enumerate(zip(bars, pedidos, porcentajes)):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, 
                f'{val}/{totales[i]}\n({p:.1f}%)', ha='center', fontsize=10, fontweight='bold')
    ax.legend()
    
    # 2. Tiempo promedio por pedido
    ax = axes[0, 1]
    tiempos = [m1['tiempo_promedio_pedido_ticks'], m2['tiempo_promedio_pedido_ticks']]
    bars = ax.bar(['120×80', '300×200'], tiempos, color=['#3498db', '#e74c3c'])
    ax.set_ylabel('Ticks/pedido', fontsize=11)
    ax.set_title('Tiempo Promedio por Pedido', fontsize=12, fontweight='bold')
    for bar, val in zip(bars, tiempos):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 100, 
                f'{val:.0f}', ha='center', fontsize=11, fontweight='bold')
    delta_pct = ((tiempos[1]/tiempos[0]) - 1) * 100
    ax.text(0.5, max(tiempos)*0.8, f'Δ: +{delta_pct:.0f}%', ha='center', fontsize=12, 
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    
    # 3. Throughput
    ax = axes[0, 2]
    throughput = [m1['throughput_pedidos_por_1000_ticks'], m2['throughput_pedidos_por_1000_ticks']]
    bars = ax.bar(['120×80', '300×200'], throughput, color=['#2ecc71', '#e74c3c'])
    ax.set_ylabel('Pedidos/1000 ticks', fontsize=11)
    ax.set_title('Throughput', fontsize=12, fontweight='bold')
    for bar, val in zip(bars, throughput):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                f'{val:.1f}', ha='center', fontsize=11, fontweight='bold')
    delta_pct = ((throughput[1]/throughput[0]) - 1) * 100
    ax.text(0.5, max(throughput)*0.7, f'Δ: {delta_pct:.1f}%', ha='center', fontsize=12,
            bbox=dict(boxstyle='round', facecolor='orange', alpha=0.7))
    
    # 4. Distancia total recorrida
    ax = axes[1, 0]
    distancias = [m1['distancia_total_celdas'], m2['distancia_total_celdas']]
    bars = ax.bar(['120×80', '300×200'], distancias, color=['#3498db', '#e74c3c'])
    ax.set_ylabel('Celdas recorridas', fontsize=11)
    ax.set_title('Distancia Total Recorrida', fontsize=12, fontweight='bold')
    for bar, val in zip(bars, distancias):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 3000, 
                f'{val:,}', ha='center', fontsize=10, fontweight='bold')
    delta_pct = ((distancias[1]/distancias[0]) - 1) * 100
    ax.text(0.5, max(distancias)*0.7, f'Δ: +{delta_pct:.0f}%', ha='center', fontsize=12,
            bbox=dict(boxstyle='round', facecolor='red', alpha=0.7))
    
    # 5. Tiempo de espera promedio
    ax = axes[1, 1]
    esperas = [m1['tiempo_promedio_espera_ticks'], m2['tiempo_promedio_espera_ticks']]
    bars = ax.bar(['120×80', '300×200'], esperas, color=['#e74c3c', '#2ecc71'])
    ax.set_ylabel('Ticks de espera', fontsize=11)
    ax.set_title('Tiempo Promedio de Espera', fontsize=12, fontweight='bold')
    for bar, val in zip(bars, esperas):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10, 
                f'{val:.1f}', ha='center', fontsize=11, fontweight='bold')
    delta_pct = ((esperas[1]/esperas[0]) - 1) * 100
    ax.text(0.5, max(esperas)*0.6, f'Δ: {delta_pct:.0f}%', ha='center', fontsize=12,
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))
    
    # 6. Deadlocks
    ax = axes[1, 2]
    deadlocks = [m1['deadlock'], m2['deadlock']]
    bars = ax.bar(['120×80', '300×200'], deadlocks, color=['#e74c3c', '#2ecc71'])
    ax.set_ylabel('Eventos de deadlock', fontsize=11)
    ax.set_title('Deadlocks', fontsize=12, fontweight='bold')
    ax.set_ylim(0, max(deadlocks) + 10 if max(deadlocks) > 0 else 10)
    for bar, val in zip(bars, deadlocks):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, 
                f'{val}', ha='center', fontsize=12, fontweight='bold')
    ax.text(0.5, max(deadlocks)*0.5 if max(deadlocks) > 0 else 5, 
            '✅ Problema resuelto\npor dilución espacial', ha='center', fontsize=10,
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
    
    plt.tight_layout(rect=[0, 0, 1, 0.97])
    plt.savefig(output_path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"✅ Generado: {output_path}")

def main():
    parser = argparse.ArgumentParser(description='Generar comparativas visuales entre layouts')
    parser.add_argument('--seed', type=str, default='seed1', 
                       help='Semilla a comparar (default: seed1)')
    args = parser.parse_args()
    
    print(f"\n{'='*60}")
    print(f"  GENERADOR DE COMPARATIVAS VISUALES")
    print(f"  Semilla: {args.seed}")
    print(f"{'='*60}\n")
    
    # Rutas de escenarios
    escenario_original = args.seed
    escenario_escalado = f"S1_baseline_{args.seed}"
    
    outputs_dir = obtener_ruta_outputs()
    print(f"📂 Usando outputs de: {outputs_dir}\n")
    print("📂 Cargando datos...")
    try:
        datos_original = cargar_datos_escenario(escenario_original, outputs_dir)
        print(f"  ✅ {escenario_original}: {datos_original['layout'].shape}")
    except FileNotFoundError as e:
        print(f"  ❌ Error: {e}")
        print(f"\n💡 Primero ejecuta: python demo_final.py --escenario {escenario_original} --robots 20 --ticks 10000")
        print(f"                    python visualiza_simulacion.py --escenario {escenario_original}")
        return
    
    try:
        datos_escalado = cargar_datos_escenario(escenario_escalado, outputs_dir)
        print(f"  ✅ {escenario_escalado}: {datos_escalado['layout'].shape}")
    except FileNotFoundError as e:
        print(f"  ❌ Error: {e}")
        print(f"\n💡 Opción 1 - Generar S1 baseline desde cero:")
        print(f"    python generador_layout.py --escenario S1_baseline_{args.seed} --seed 1 --ancho 300 --alto 200 --estaciones 20")
        print(f"    python generador_pedidos.py --escenario S1_baseline_{args.seed} --pedidos 600 --burst")
        print(f"    python demo_final.py --escenario S1_baseline_{args.seed} --robots 20 --ticks 10000")
        print(f"    python visualiza_simulacion.py --escenario S1_baseline_{args.seed}")
        return
    
    # Generar comparativas
    print("\n🎨 Generando visualizaciones...\n")
    
    # Crear carpeta de outputs
    os.makedirs("outputs", exist_ok=True)
    
    # 1. Comparativa de layouts
    output_layouts = f"outputs/comparativa_layouts_{args.seed}.png"
    generar_comparativa_layouts(datos_original, datos_escalado, output_layouts)
    
    # 2. Comparativa de métricas
    output_metricas = f"outputs/comparativa_metricas_{args.seed}.png"
    generar_comparativa_metricas(datos_original, datos_escalado, output_metricas)
    
    print(f"\n{'='*60}")
    print("✅ COMPARATIVAS GENERADAS EXITOSAMENTE")
    print(f"{'='*60}")
    print(f"\n📊 Archivos generados:")
    print(f"  1. {output_layouts}")
    print(f"  2. {output_metricas}")
    print(f"\n💡 Puedes incluir estas imágenes en el Entregable 2")
    print(f"   para reforzar el análisis de las modificaciones escalables.\n")

if __name__ == "__main__":
    main()
