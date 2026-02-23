#!/usr/bin/env python3
"""
Comparador Visual: seed1 (54 deadlocks) vs seed42 (0 deadlocks)
Genera análisis lado a lado de heatmaps y métricas
"""
import json
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.gridspec import GridSpec
from PIL import Image
import sys

def cargar_metricas(escenario: str) -> dict:
    """Carga métricas JSON"""
    ruta = os.path.join("outputs", escenario, "metricas.json")
    if not os.path.exists(ruta):
        print(f"⚠️  {ruta} no encontrado")
        return None
    with open(ruta, 'r') as f:
        return json.load(f)

def cargar_imagen(escenario: str, nombre_archivo: str):
    """Carga imagen PNG"""
    ruta = os.path.join("outputs", escenario, nombre_archivo)
    if not os.path.exists(ruta):
        print(f"⚠️  {ruta} no encontrado")
        return None
    return Image.open(ruta)

def generar_comparacion_metricas():
    """Genera gráfico comparativo de métricas"""
    m1 = cargar_metricas("seed1")
    m42 = cargar_metricas("seed42")
    
    if not m1 or not m42:
        print("❌ No se pueden cargar métricas")
        return
    
    # Datos para graficar
    metricas_nombres = [
        "Deadlocks",
        "Pedidos Completados",
        "Throughput\n(ped/1000 ticks)",
        "Tiempo Promedio\n(ticks)",
        "Utilización\nRobots (%)"
    ]
    
    seed1_valores = [
        m1['deadlock'],
        m1['pedidos_completados'],
        m1['throughput_pedidos_por_1000_ticks'],
        m1['tiempo_promedio_pedido_ticks'],
        m1['utilizacion_promedio'] * 100
    ]
    
    seed42_valores = [
        m42['deadlock'],
        m42['pedidos_completados'],
        m42['throughput_pedidos_por_1000_ticks'],
        m42['tiempo_promedio_pedido_ticks'],
        m42['utilizacion_promedio'] * 100
    ]
    
    # Normalizar para visualización de barras (excepto donde tenga sentido)
    # Deadlocks: mostrar como está
    # Demás: mostrar porcentaje de diferencia
    
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    fig.suptitle("Comparación Visual: seed1 (54 deadlocks) vs seed42 (0 deadlocks)", 
                 fontsize=16, fontweight='bold')
    
    # Gráfico 1: Deadlocks (TODO: eliminar uno)
    ax = axes[0, 0]
    x = ["seed1", "seed42"]
    y = [m1['deadlock'], m42['deadlock']]
    colores = ['#ff4444', '#44ff44']
    barras = ax.bar(x, y, color=colores, edgecolor='black', linewidth=2)
    ax.set_ylabel("Cantidad", fontsize=11, fontweight='bold')
    ax.set_title("Deadlocks\n(MENOR = MEJOR)", fontsize=12, fontweight='bold')
    ax.set_ylim(0, max(y) * 1.2)
    for i, (barra, valor) in enumerate(zip(barras, y)):
        ax.text(barra.get_x() + barra.get_width()/2, barra.get_height() + 1, 
                f"{int(valor)}", ha='center', va='bottom', fontweight='bold', fontsize=12)
    ax.grid(axis='y', alpha=0.3)
    
    # Gráfico 2: Pedidos Completados
    ax = axes[0, 1]
    x = ["seed1", "seed42"]
    y = [m1['pedidos_completados'], m42['pedidos_completados']]
    barras = ax.bar(x, y, color=['#ffaa44', '#44aaff'], edgecolor='black', linewidth=2)
    ax.set_ylabel("Pedidos", fontsize=11, fontweight='bold')
    ax.set_title("Pedidos Completados\n(MAYOR = MEJOR)", fontsize=12, fontweight='bold')
    ax.set_ylim(594, 600)
    for barra, valor in zip(barras, y):
        ax.text(barra.get_x() + barra.get_width()/2, barra.get_height() + 0.1, 
                f"{int(valor)}", ha='center', va='bottom', fontweight='bold', fontsize=11)
    ax.grid(axis='y', alpha=0.3)
    
    # Gráfico 3: Throughput
    ax = axes[0, 2]
    x = ["seed1", "seed42"]
    y = [m1['throughput_pedidos_por_1000_ticks'], m42['throughput_pedidos_por_1000_ticks']]
    barras = ax.bar(x, y, color=['#ffaa44', '#44aaff'], edgecolor='black', linewidth=2)
    ax.set_ylabel("Pedidos/1000 ticks", fontsize=11, fontweight='bold')
    ax.set_title("Throughput\n(MAYOR = MEJOR)", fontsize=12, fontweight='bold')
    ax.set_ylim(59.4, 60.0)
    for barra, valor in zip(barras, y):
        ax.text(barra.get_x() + barra.get_width()/2, barra.get_height() + 0.05, 
                f"{valor:.2f}", ha='center', va='bottom', fontweight='bold', fontsize=10)
    ax.grid(axis='y', alpha=0.3)
    
    # Gráfico 4: Tiempo Promedio
    ax = axes[1, 0]
    x = ["seed1", "seed42"]
    y = [m1['tiempo_promedio_pedido_ticks'], m42['tiempo_promedio_pedido_ticks']]
    barras = ax.bar(x, y, color=['#ffaa44', '#44aaff'], edgecolor='black', linewidth=2)
    ax.set_ylabel("Ticks", fontsize=11, fontweight='bold')
    ax.set_title("Tiempo Promedio/Pedido\n(MENOR = MEJOR)", fontsize=12, fontweight='bold')
    ax.set_ylim(760, 800)
    for barra, valor in zip(barras, y):
        ax.text(barra.get_x() + barra.get_width()/2, barra.get_height() + 1, 
                f"{valor:.1f}", ha='center', va='bottom', fontweight='bold', fontsize=10)
    ax.grid(axis='y', alpha=0.3)
    
    # Gráfico 5: Utilización
    ax = axes[1, 1]
    x = ["seed1", "seed42"]
    y = [m1['utilizacion_promedio'] * 100, m42['utilizacion_promedio'] * 100]
    barras = ax.bar(x, y, color=['#ffaa44', '#44aaff'], edgecolor='black', linewidth=2)
    ax.set_ylabel("Porcentaje (%)", fontsize=11, fontweight='bold')
    ax.set_title("Utilización Promedio\n(CONTEXTO)", fontsize=12, fontweight='bold')
    ax.set_ylim(48, 55)
    for barra, valor in zip(barras, y):
        ax.text(barra.get_x() + barra.get_width()/2, barra.get_height() + 0.2, 
                f"{valor:.2f}%", ha='center', va='bottom', fontweight='bold', fontsize=10)
    ax.grid(axis='y', alpha=0.3)
    
    # Gráfico 6: Tabla de diferencias
    ax = axes[1, 2]
    ax.axis('off')
    
    tabla_datos = [
        ["Métrica", "seed1", "seed42", "Diferencia"],
        ["Deadlocks", str(int(m1['deadlock'])), str(int(m42['deadlock'])), 
         f"{m1['deadlock'] - m42['deadlock']:.0f} (PEOR)"],
        ["Pedidos", f"{int(m1['pedidos_completados'])}", 
         f"{int(m42['pedidos_completados'])}", 
         f"{m42['pedidos_completados'] - m1['pedidos_completados']:.0f}"],
        ["Throughput", f"{m1['throughput_pedidos_por_1000_ticks']:.2f}", 
         f"{m42['throughput_pedidos_por_1000_ticks']:.2f}", 
         f"{m42['throughput_pedidos_por_1000_ticks'] - m1['throughput_pedidos_por_1000_ticks']:.2f}"],
        ["T.Promedio", f"{m1['tiempo_promedio_pedido_ticks']:.1f}", 
         f"{m42['tiempo_promedio_pedido_ticks']:.1f}", 
         f"{m1['tiempo_promedio_pedido_ticks'] - m42['tiempo_promedio_pedido_ticks']:.1f}"],
    ]
    
    tabla = ax.table(cellText=tabla_datos, cellLoc='center', loc='center',
                     colWidths=[0.25, 0.25, 0.25, 0.25])
    tabla.auto_set_font_size(False)
    tabla.set_fontsize(9)
    tabla.scale(1, 2)
    
    # Colorear encabezado
    for i in range(4):
        tabla[(0, i)].set_facecolor('#333333')
        tabla[(0, i)].set_text_props(weight='bold', color='white')
    
    # Colorear filas
    for i in range(1, len(tabla_datos)):
        for j in range(4):
            if i == 1:  # Deadlocks
                tabla[(i, j)].set_facecolor('#ffdddd' if j < 3 else '#ffaaaa')
            else:
                tabla[(i, j)].set_facecolor('#ffffdd' if j % 2 else '#ffffcc')
    
    ax.set_title("Tabla Resumen", fontsize=12, fontweight='bold', pad=20)
    
    plt.tight_layout()
    ruta_salida = "../comparacion_seed1_vs_seed42_metricas.png"
    plt.savefig(ruta_salida, dpi=150, bbox_inches='tight')
    print(f"✅ Comparación de métricas guardada: {ruta_salida}")
    plt.close()

def generar_comparacion_heatmaps():
    """Genera comparación lado a lado de heatmaps"""
    
    img_types = ['heatmap_esperas', 'heatmap_visitas', 'heatmap_ratio']
    
    for img_type in img_types:
        print(f"\nGenerando comparación: {img_type}")
        
        img1 = cargar_imagen("seed1", f"{img_type}.png")
        img42 = cargar_imagen("seed42", f"{img_type}.png")
        
        if img1 is None or img42 is None:
            print(f"⚠️  No se encontraron imágenes para {img_type}")
            continue
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
        
        ax1.imshow(img1)
        ax1.set_title(f"{img_type.replace('heatmap_', '').upper()}\nseed1 (54 deadlocks)", 
                     fontsize=14, fontweight='bold', color='darkred')
        ax1.axis('off')
        
        ax2.imshow(img42)
        ax2.set_title(f"{img_type.replace('heatmap_', '').upper()}\nseed42 (0 deadlocks)", 
                     fontsize=14, fontweight='bold', color='darkgreen')
        ax2.axis('off')
        
        plt.suptitle(f"Comparación Visual: {img_type.upper()}", fontsize=16, fontweight='bold', y=0.98)
        plt.tight_layout()
        
        ruta_salida = f"outputs/comparacion_{img_type}_seed1_vs_seed42.png"
        plt.savefig(ruta_salida, dpi=100, bbox_inches='tight')
        print(f"✅ {ruta_salida}")
        plt.close()

def generar_reporte_html():
    """Genera reporte HTML visual"""
    html_content = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Comparación Visual: seed1 vs seed42</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: #333;
                padding: 20px;
            }
            .container {
                max-width: 1400px;
                margin: 0 auto;
                background: white;
                border-radius: 10px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.3);
                padding: 30px;
            }
            h1 {
                text-align: center;
                color: #333;
                margin-bottom: 30px;
                font-size: 2.5em;
            }
            .info-box {
                background: #f0f4ff;
                border-left: 5px solid #667eea;
                padding: 15px;
                margin-bottom: 25px;
                border-radius: 5px;
            }
            .seed-comparison {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
                margin-bottom: 30px;
            }
            .seed-card {
                border-radius: 8px;
                padding: 20px;
                text-align: center;
            }
            .seed-card.seed1 {
                background: #ffebee;
                border: 3px solid #d32f2f;
            }
            .seed-card.seed42 {
                background: #e8f5e9;
                border: 3px solid #388e3c;
            }
            .seed-card h2 {
                margin-top: 0;
                font-size: 1.8em;
            }
            .seed-card .metric {
                font-size: 2em;
                font-weight: bold;
                margin: 10px 0;
            }
            .seed-card .label {
                font-size: 0.9em;
                color: #666;
            }
            .seed1 .metric {
                color: #d32f2f;
            }
            .seed42 .metric {
                color: #388e3c;
            }
            .comparison-img {
                width: 100%;
                margin: 20px 0;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }
            .section {
                margin: 40px 0;
            }
            .section h2 {
                border-bottom: 3px solid #667eea;
                padding-bottom: 10px;
                margin-bottom: 20px;
                color: #333;
            }
            .conclusion {
                background: #fff3e0;
                border-left: 5px solid #f57c00;
                padding: 20px;
                border-radius: 5px;
                margin-top: 30px;
                font-size: 1.1em;
                line-height: 1.6;
            }
            .footer {
                text-align: center;
                margin-top: 40px;
                color: #999;
                font-size: 0.9em;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏭 Análisis Comparativo Visual</h1>
            <h2 style="text-align: center; color: #667eea; margin-top: -10px;">
                seed1 (54 deadlocks) vs seed42 (0 deadlocks)
            </h2>
            
            <div class="info-box">
                <strong>📌 Contexto:</strong> Se ejecutó la simulación con 10 semillas diferentes para 
                identificar variabilidad. seed1 generó 54 deadlocks (bloqueos de robots) mientras que 
                seed42 no generó ninguno. Esta comparación visual permite entender el impacto real de 
                los deadlocks en el almacén simulado.
            </div>
            
            <div class="section">
                <h2>📊 Comparación de Métricas Clave</h2>
                <img src="comparacion_seed1_vs_seed42_metricas.png" alt="Comparación de métricas" class="comparison-img">
                
                <div class="seed-comparison">
                    <div class="seed-card seed1">
                        <h2>seed1</h2>
                        <div class="label">Deadlocks (PROBLEMA)</div>
                        <div class="metric">54</div>
                        <hr>
                        <div class="label">Pedidos Completados</div>
                        <div class="metric">596/600</div>
                        <div class="label">Throughput</div>
                        <div class="metric">59.60</div>
                    </div>
                    <div class="seed-card seed42">
                        <h2>seed42</h2>
                        <div class="label">Deadlocks (BASELINE)</div>
                        <div class="metric">0</div>
                        <hr>
                        <div class="label">Pedidos Completados</div>
                        <div class="metric">597/600</div>
                        <div class="label">Throughput</div>
                        <div class="metric">59.70</div>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2>🔥 Heatmap: Tiempo de Espera</h2>
                <p>Muestra dónde los robots pasan más tiempo esperando. zones en rojo = más espera</p>
                <img src="comparacion_heatmap_esperas_seed1_vs_seed42.png" alt="Heatmap de esperas" class="comparison-img">
                <p><strong>Observación:</strong> seed1 (izq) muestra áreas rojas más intensas, indicando 
                puntos calientes donde los robots se bloquean mutuamente.</p>
            </div>
            
            <div class="section">
                <h2>📍 Heatmap: Visitas de Robots</h2>
                <p>Muestra cuántas veces robots visitan cada celda. Zonas azules = alta congestión.</p>
                <img src="comparacion_heatmap_visitas_seed1_vs_seed42.png" alt="Heatmap de visitas" class="comparison-img">
                <p><strong>Observación:</strong> seed1 muestra distribución más concentrada (cuello de botella)</p>
            </div>
            
            <div class="section">
                <h2>📈 Heatmap: Ratio de Actividad</h2>
                <p>Métrica normalizaada: combina visitas y esperas. Indica eficiencia por zona.</p>
                <img src="comparacion_heatmap_ratio_seed1_vs_seed42.png" alt="Heatmap de ratio" class="comparison-img">
                <p><strong>Observación:</strong> seed1 tiene zonas con color inconsistente (ineficiencia)</p>
            </div>
            
            <div class="section">
                <h2>🎬 Videos Disponibles</h2>
                <p>Para ver la simulación en acción:</p>
                <ul>
                    <li><strong>outputs/seed1/simulacion.mp4</strong> - seed1 con 54 deadlocks (PROBLEMA VISIBLE)</li>
                    <li><strong>outputs/seed42/simulacion.mp4</strong> - seed42 con 0 deadlocks (BASELINE)</li>
                </ul>
                <p style="font-size: 0.9em; color: #666;">
                    💡 En los videos, los deadlocks aparecen como robots que se quedan quietos 
                    en pasillos sin poder avanzar ni retroceder.
                </p>
            </div>
            
            <div class="conclusion">
                <strong>🎯 Conclusión Principal:</strong>
                <p>seed1 expone una vulnerabilidad clara del algoritmo baseline: la falta de 
                coordinación efectiva lleva a 54 deadlocks (bloqueos de robots). Los heatmaps 
                visualizan cómo ciertos pasillos y zonas se convierten en cuellos de botella 
                naturales donde los robots se atrapan mutuamente sin poder resolverlo.</p>
                
                <p style="margin-top: 15px;"><strong>Implicación para mejora (Eje C):</strong>
                Una estrategia de coordinación multirobótica (priorización, detección de ciclos, 
                reglas de derecho de paso) podría eliminar o reducir significativamente estos 54 
                deadlocks, resultando en una mejora del ~100% en esta métrica.</p>
            </div>
            
            <div class="footer">
                <p>Generado automáticamente el 16 Feb 2026 | TI3005B.102 - Simulación de Almacén</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    with open("../reporte_comparacion_visual.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print("✅ Reporte HTML generado: ../reporte_comparacion_visual.html")

def main():
    print("\n" + "="*80)
    print(" COMPARADOR VISUAL: seed1 (54 deadlocks) vs seed42 (0 deadlocks)")
    print("="*80)
    
    # Verificar que las visualizaciones existen
    print("\n1️⃣  Verificando archivos...")
    seed1_files = os.listdir("outputs/seed1")
    seed42_files = os.listdir("outputs/seed42")
    
    print(f"  seed1: {len([f for f in seed1_files if f.endswith(('.png', '.mp4'))])} visuales")
    print(f"  seed42: {len([f for f in seed42_files if f.endswith(('.png', '.mp4'))])} visuales")
    
    # Generar comparaciones
    print("\n2️⃣  Generando comparación de métricas...")
    generar_comparacion_metricas()
    
    print("\n3️⃣  Generando comparación de heatmaps...")
    generar_comparacion_heatmaps()
    
    print("\n4️⃣  Generando reporte HTML...")
    generar_reporte_html()
    
    print("\n" + "="*80)
    print(" ✅ COMPARACIÓN VISUAL COMPLETADA")
    print("="*80)
    print("\n📁 Archivos generados:")
    print("  - ../comparacion_seed1_vs_seed42_metricas.png")
    print("  - outputs/comparacion_heatmap_*.png (3 archivos)")
    print("  - ../reporte_comparacion_visual.html ⭐")
    print("\n🌐 Abre el HTML en navegador para ver reporte interactivo:")
    print("  open ../reporte_comparacion_visual.html")
    print("\n" + "="*80)

if __name__ == "__main__":
    main()
