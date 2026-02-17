#!/usr/bin/env python3
"""
Script para generar visualizaciones (video + heatmaps) para seed1
Luego permite comparar visualmente con seed42
"""
import subprocess
import sys
import os

def generar_visualizacion(escenario: str):
    """Genera video y heatmaps para una semilla"""
    print(f"\n{'='*80}")
    print(f"GENERANDO VISUALIZACIONES PARA {escenario.upper()}")
    print(f"{'='*80}")
    
    cmd = ["python", "visualiza_simulacion.py", "--escenario", escenario]
    
    try:
        print(f"\nEjecutando: {' '.join(cmd)}")
        resultado = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if resultado.returncode == 0:
            print(f"✅ {escenario} - Visualización completada exitosamente")
            print(f"\nArchivos generados en: outputs/{escenario}/")
            listar_outputs(escenario)
            return True
        else:
            print(f"❌ Error en {escenario}")
            print(f"STDOUT: {resultado.stdout}")
            print(f"STDERR: {resultado.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print(f"❌ Timeout: La generación de {escenario} tardó demasiado")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def listar_outputs(escenario: str):
    """Lista archivos generados"""
    ruta = os.path.join("outputs", escenario)
    if os.path.exists(ruta):
        archivos = os.listdir(ruta)
        archivos_visuales = [a for a in archivos if a.endswith(('.png', '.mp4'))]
        print(f"Archivos visuales ({len(archivos_visuales)}):")
        for archivo in sorted(archivos_visuales):
            tam = os.path.getsize(os.path.join(ruta, archivo)) / (1024*1024)
            print(f"  - {archivo} ({tam:.1f} MB)")

def main():
    print("\n" + "="*80)
    print(" GENERADOR DE VISUALIZACIONES PARA COMPARACIÓN")
    print("="*80)
    
    # Generar visualizaciones
    resultado_seed1 = generar_visualizacion("seed1")
    resultado_seed42 = generar_visualizacion("seed42")
    
    print("\n" + "="*80)
    print(" RESUMEN")
    print("="*80)
    
    print(f"\nseed1  (54 deadlocks): {'✅ LISTA' if resultado_seed1 else '❌ FALLA'}")
    print(f"seed42 (0 deadlocks):  {'✅ LISTA' if resultado_seed42 else '❌ MISSING'}")
    
    if resultado_seed1 and resultado_seed42:
        print("\n✅ Ambas semillas están listas para comparación visual")
        print("\nPróximo paso: Ejecutar comparador visual")
        print("  python comparador_visual_seed1_vs_seed42.py")
    else:
        print("\n⚠️  Algunas visualizaciones no se generaron correctamente")

if __name__ == "__main__":
    main()
