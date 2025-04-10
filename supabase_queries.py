import os
from dotenv import load_dotenv
from supabase import create_client, Client
from typing import List, Dict, Optional
from datetime import datetime

# Configuración inicial
load_dotenv('variables.env')

# Conexión a Supabase
def conectar_supabase() -> Client:
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("Las variables SUPABASE_URL y SUPABASE_KEY deben estar configuradas en el archivo .env")
    
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = conectar_supabase()

# 1. Mostrar inventario de un local
def mostrar_inventario(local_id: int) -> List[Dict]:
    result = supabase.rpc('obtener_inventario_local', {'local_id': local_id}).execute()
    return result.data

# 2. Mostrar historial de pagos
def historial_pagos(tipo: str, id_entidad: int) -> List[Dict]:
    result = supabase.rpc('obtener_historial_pagos', {
        'tipo_pago': tipo,
        'id_entidad': id_entidad
    }).execute()
    return result.data

# 3. Clientes con cuotas pendientes
def clientes_con_cuotas_pendientes() -> List[Dict]:
    result = supabase.rpc('obtener_clientes_cuotas_pendientes', {}).execute()
    return result.data

# 4. Locales inhabilitados
def locales_inhabilitados() -> List[Dict]:
    result = supabase.rpc('obtener_locales_inhabilitados', {}).execute()
    return result.data

# 5. Locales con mayores ganancias
def locales_mayores_ganancias() -> List[Dict]:
    result = supabase.rpc('obtener_locales_mayores_ganancias', {}).execute()
    return result.data

# 6. Productos más vendidos
def productos_mas_vendidos() -> List[Dict]:
    result = supabase.rpc('obtener_productos_mas_vendidos', {}).execute()
    return result.data

# 7. Pedidos de un local con clientes
def pedidos_por_local(local_id: int) -> List[Dict]:
    result = supabase.rpc('obtener_pedidos_por_local', {'local_id': local_id}).execute()
    return result.data

# 8. Locales por dueño
def locales_por_dueno(dueno_id: int) -> Dict:
    try:
        result = supabase.rpc('obtener_locales_por_dueno', {'dueno_id': dueno_id}).execute()
        if not result.data:
            return {"error": "No se pudo obtener la información"}
        
        response = result.data[0] if isinstance(result.data, list) else result.data
        
        if 'error' in response:
            return response
        
        # Asegurar que locales sea siempre una lista
        if 'locales' not in response or response['locales'] is None:
            response['locales'] = []
        
        return response
    except Exception as e:
        print(f"Error al obtener locales por dueño: {str(e)}")
        return {"error": str(e)}

# Función para mostrar resultados
def mostrar_resultados(data, titulo: str):
    print(f"\n=== {titulo} ===")
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, list):
                print(f"{key}:")
                for item in value:
                    print(f"  - {item}")
            else:
                print(f"{key}: {value}")
    elif isinstance(data, list) and data:
        if isinstance(data[0], dict):
            headers = data[0].keys()
            print(" | ".join(headers))
            print("-" * 50)
            for item in data:
                print(" | ".join(str(item[h]) for h in headers))
        else:
            for item in data:
                print(f"- {item}")
    else:
        print("No se encontraron resultados")
    print("=" * 50)

# Menú interactivo
def menu_principal():
    while True:
        print("\nSistema de Gestión Comercial - Supabase")
        print("1. Mostrar inventario de un local")
        print("2. Mostrar historial de pagos")
        print("3. Clientes con cuotas pendientes")
        print("4. Locales inhabilitados")
        print("5. Locales con mayores ganancias")
        print("6. Productos más vendidos")
        print("7. Pedidos por local")
        print("8. Locales por dueño")
        print("0. Salir")
        
        opcion = input("\nSeleccione una opción: ")
        
        try:
            if opcion == "1":
                local_id = int(input("ID del local: "))
                mostrar_resultados(mostrar_inventario(local_id), f"Inventario del Local {local_id}")
            
            elif opcion == "2":
                tipo = input("Tipo (local/cliente/empleado): ").lower()
                id_entidad = int(input(f"ID del {tipo}: "))
                mostrar_resultados(historial_pagos(tipo, id_entidad), f"Historial de pagos ({tipo} {id_entidad})")
            
            elif opcion == "3":
                mostrar_resultados(clientes_con_cuotas_pendientes(), "Clientes con cuotas pendientes")
            
            elif opcion == "4":
                mostrar_resultados(locales_inhabilitados(), "Locales inhabilitados")
            
            elif opcion == "5":
                mostrar_resultados(locales_mayores_ganancias(), "Locales con mayores ganancias")
            
            elif opcion == "6":
                mostrar_resultados(productos_mas_vendidos(), "Productos más vendidos")
            
            elif opcion == "7":
                local_id = int(input("ID del local: "))
                mostrar_resultados(pedidos_por_local(local_id), f"Pedidos del Local {local_id}")
            
            elif opcion == "8":
                dueno_id = int(input("ID del dueño: "))
                mostrar_resultados(locales_por_dueno(dueno_id), f"Locales del Dueño {dueno_id}")
            
            elif opcion == "0":
                print("Saliendo del sistema...")
                break
            
            else:
                print("Opción no válida. Intente nuevamente.")
        
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    menu_principal()