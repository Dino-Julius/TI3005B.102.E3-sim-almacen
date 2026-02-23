#!/usr/bin/env python3
"""
SCRIPT MAESTRO: Genera visualizaciones y análisis comparativo en una sola ejecución
Ejecuta: python generar_todo_visualizaciones.py
"""
import subprocess
import sys
import os
import json
import time

def ejecutar_comando(cmd, descripcion):
    """Ejecuta comando y reporta resultado"""
    print(f"\n{'='*80}")
    print(f"▶️  {descripcion}")
    print(f"{'='*80}")
    print(f"Comando: {' '.join(cmd)}")
    print()
    
    try:
        inicio = time.time()
        resultado = subprocess.run(cmd, capture_output=False, text=True, timeout=600)
        duracion = time.time() - inicio
        
        if resultado.returncode == 0:
            print(f"\n✅ ÉXITO - Completado en {duracion:.1f}s")
            return True
        else:
            print(f"\n❌ FALLO - Código de salida: {resultado.returncode}")
            return False
    except subprocess.TimeoutExpired:
        print(f"\n⏱️  TIMEOUT - Tomó demasiado tiempo")
        return False
    except KeyboardInterrupt:
        print(f"\n⚠️  INTERRUMPIDO por usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return False

def verificar_archivos(ruta, expected_files):
    """Verifica si los archivos esperados existen"""
    existentes = []
    faltantes = []
    
    for archivo in expected_files:
        ruta_completa = os.path.join(ruta, archivo)
        if os.path.exists(ruta_completa):
            existentes.append(archivo)
        else:
            faltantes.append(archivo)
    
    return existentes, faltantes

def main():
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*20 + "🏭 GENERADOR COMPLETO DE VISUALIZACIONES" + " "*18 + "║")
    print("║" + " "*15 + "seed1 (54 deadlocks) + seed42 (0 deadlocks)" + " "*20 + "║")
    print("╚" + "="*78 + "╝")
    
    os.chdir(os.path.dirname(os.path.abspath(__file__)) or ".")
    
    # PASO 1: Verificar qué existe
    print("\n📋 PASO 1: Verificando archivos existentes...")
    print("-" * 80)
    
    seed1_visuales, seed1_falta = verificar_archivos("outputs/seed1", ["simulacion.mp4", "heatmap_esperas.png", "heatmap_visitas.png", "heatmap_ratio.png"])
    seed42_visuales, seed42_falta = verificar_archivos("outputs/seed42", ["simulacion.mp4", "heatmap_esperas.png", "heatmap_visitas.png", "heatmap_ratio.png"])
    
    print(f"\n📁 seed1:")
    print(f"   ✅ Tiene: {seed1_visuales if seed1_visuales else 'NINGUNO'}")
    print(f"   ❌ Falta: {seed1_falta if seed1_falta else 'NINGUNO'}")
    
    print(f"\n📁 seed42:")
    print(f"   ✅ Tiene: {seed42_visuales if seed42_visuales else 'NINGUNO'}")
    print(f"   ❌ Falta: {seed42_falta if seed42_falta else 'NINGUNO'}")
    
    # PASO 2: Generar visualizaciones faltantes
    print("\n" + "="*80)
    print("🎬 PASO 2: Generando visualizaciones faltantes...")
    print("="*80)
    
    resultados = {
        "seed1_visual": True if not seed1_falta else False,
        "seed42_visual": True if not seed42_falta else False,
    }
    
    if seed1_falta:
        print(f"\n⚠️  seed1 falta visualizaciones. Generando...")
        exito = ejecutar_comando(
            ["python", "visualiza_simulacion.py", "--escenario", "seed1"],
            "Generando visualizaciones para seed1 (con 54 deadlocks)"
        )
        resultados["seed1_visual"] = exito
        if exito:
            # Verificar nuevamente
            _, seed1_falta = verificar_archivos("outputs/seed1", ["simulacion.mp4", "heatmap_esperas.png"])
            if not seed1_falta:
                print("✅ seed1 ahora tiene todas las visualizaciones")
    else:
        print("✅ seed1 ya tiene todas las visualizaciones")
    
    if seed42_falta:
        print(f"\n⚠️  seed42 falta visualizaciones. Generando...")
        exito = ejecutar_comando(
            ["python", "visualiza_simulacion.py", "--escenario", "seed42"],
            "Generando visualizaciones para seed42 (con 0 deadlocks)"
        )
        resultados["seed42_visual"] = exito
        if exito:
            _, seed42_falta = verificar_archivos("outputs/seed42", ["simulacion.mp4", "heatmap_esperas.png"])
            if not seed42_falta:
                print("✅ seed42 ahora tiene todas las visualizaciones")
    else:
        print("✅ seed42 ya tiene todas las visualizaciones")
    
    # PASO 3: Generar comparaciones visuales
    print("\n" + "="*80)
    print("🔍 PASO 3: Generando análisis comparativo...")
    print("="*80)
    
    if resultados["seed1_visual"] and resultados["seed42_visual"]:
        exito = ejecutar_comando(
            ["python", "comparador_visual_seed1_vs_seed42.py"],
            "Creando comparación visual lado a lado"
        )
        resultados["comparacion"] = exito
    else:
        print("⚠️  Saltando comparación (faltan visualizaciones de base)")
        resultados["comparacion"] = False
    
    # RESUMEN FINAL
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*25 + "📊 RESUMEN FINAL" + " "*36 + "║")
    print("╠" + "="*78 + "╣")
    
    resumen = [
        ("seed1 visualizaciones", "seed1_visual"),
        ("seed42 visualizaciones", "seed42_visual"),
        ("Análisis comparativo", "comparacion"),
    ]
    
    for nombre, clave in resumen:
        estado = "✅ GENERADO" if resultados.get(clave, False) else "❌ FALLO/NO EJECUTADO"
        print(f"║ {nombre:<40} {estado:<36} ║")
    
    print("╚" + "="*78 + "╝")
    
    # Mostrar dónde están los archivos
    if resultados["comparacion"]:
        print("\n" + "="*80)
        print("📁 ARCHIVOS GENERADOS:")
        print("="*80)
        
        output_dir = "outputs"
        archivos_comparacion = [
            f for f in os.listdir(output_dir) 
            if f.startswith("comparacion_") and f.endswith(".png")
        ]
        
        print("\n🖼️  Imágenes de comparación:")
        for archivo in sorted(archivos_comparacion):
            tam = os.path.getsize(os.path.join(output_dir, archivo)) / (1024*1024)
            print(f"   📊 {archivo} ({tam:.1f} MB)")
        
        if os.path.exists(os.path.join(output_dir, "reporte_comparacion_visual.html")) or os.path.exists("../reporte_comparacion_visual.html"):
            print(f"\n📄 Reporte HTML (⭐ ABRIR ESTO):")
            print(f"   📋 reporte_comparacion_visual.html (abre en navegador)")
        
        print("\n🎬 Videos disponibles:")
        print(f"   🎥 outputs/seed1/simulacion.mp4 (ver bloqueos/deadlocks)")
        print(f"   🎥 outputs/seed42/simulacion.mp4 (baseline sin deadlocks)")
        
        print("\n" + "="*80)
        print("\n🚀 PRÓXIMOS PASOS:")
        print("\n   1. Abre en navegador:")
        print("      open ../reporte_comparacion_visual.html")
        print("\n   2. Ve los videos para comparar visualmente los deadlocks:")
        print("      open outputs/seed1/simulacion.mp4")
        print("      open outputs/seed42/simulacion.mp4")
        print("\n   3. Revisa las imágenes PNG de comparación en outputs/")
        print("\n" + "="*80)
    else:
        print("\n⚠️  No se generó el análisis comparativo. Revisa los errores arriba.")
        print("\nPuedes intentar ejecutar manualmente:")
        print("   python comparador_visual_seed1_vs_seed42.py")

if __name__ == "__main__":
    main()
