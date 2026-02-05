import pandas as pd
import sqlalchemy
from sqlalchemy import create_engine
import urllib
import random

# ==========================================
# 1. CONFIGURACIÓN (¡PON TUS DATOS AQUÍ!)
# ==========================================
SERVER = 'juan1.database.windows.net'  # Tu servidor
DATABASE = 'free-sql-db-9389715'       # Tu base de datos
USERNAME = 'tu_usuario_admin'          # El usuario que creaste
PASSWORD = 'tu_password_fuerte'        # La contraseña
DRIVER = '{ODBC Driver 17 for SQL Server}' # Usualmente este viene instalado por defecto

# Cadena de conexión segura para Azure
connection_string = f'DRIVER={DRIVER};SERVER={SERVER};PORT=1433;DATABASE={DATABASE};UID={USERNAME};PWD={PASSWORD}'
params = urllib.parse.quote_plus(connection_string)
engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

# ==========================================
# 2. GENERADOR DE DATOS SUCIOS (Simulamos el Excel)
# ==========================================
def crear_datos_fake():
    print("--- 1. Generando Excel 'Sucio' Simulado ---")
    data = {
        'County_Raw': ['  SALTA norte ', 'Jujuy minera', 'catamarca-west', 'NEUQUEN', None],
        'Infrastructure_Score': ['8.5', '3,2', '9.0', 'sin dato', '5.5'], # Mezcla de comas, puntos y texto
        'Political_Score': [7, 4, 8, 2, 6],
        'Date_Report': ['2024/01/01', '01-02-2024', '2024.03.15', 'invalid', '2024-05-20']
    }
    df = pd.DataFrame(data)
    df.to_csv('input_sucio.csv', index=False)
    print("   -> Archivo 'input_sucio.csv' creado con éxito.\n")
    return df

# ==========================================
# 3. TRANSFORMACIÓN (Limpieza con Pandas)
# ==========================================
def limpiar_datos():
    print("--- 2. Iniciando Transformación (ETL) ---")
    
    # Leemos el CSV sucio
    df = pd.read_csv('input_sucio.csv')
    
    # A. Limpieza de Texto (County)
    # Quitamos espacios, ponemos mayúsculas y quitamos nulos
    df['County_Clean'] = df['County_Raw'].str.strip().str.upper().fillna('DESCONOCIDO')
    
    # B. Limpieza de Numéricos (Infraestructura)
    # Reemplazamos comas por puntos y forzamos a numérico. Los errores (texto) se vuelven NaN.
    df['Infra_Clean'] = df['Infrastructure_Score'].astype(str).str.replace(',', '.')
    df['Infra_Clean'] = pd.to_numeric(df['Infra_Clean'], errors='coerce').fillna(0)
    
    # C. Cálculo de Score Final (Lógica de Negocio)
    # Promedio simple entre Infra y Político
    df['Score_Final'] = (df['Infra_Clean'] + df['Political_Score']) / 2
    
    # D. Seleccionamos solo las columnas listas para SQL
    # Mapeamos a las columnas de tu tabla GEO_ADMIN_MASTER (simulado)
    df_final = pd.DataFrame()
    df_final['County_Name'] = df['County_Clean']
    df_final['State_Province'] = 'N/A' # Dato dummy
    df_final['Country'] = 'Argentina'
    df_final['Region_Geografica'] = 'Noroeste' # Hardcodeado para el ejemplo
    
    print("   -> Datos limpiados. Ejemplo:")
    print(df_final.head(3))
    print("\n")
    return df_final

# ==========================================
# 4. CARGA (Load to Azure SQL)
# ==========================================
def cargar_a_sql(df):
    print("--- 3. Cargando a Azure SQL ---")
    try:
        # Usamos 'append' para agregar datos a la tabla existente
        df.to_sql('GEO_ADMIN_MASTER', con=engine, if_exists='append', index=False)
        print("   -> ¡ÉXITO! Datos cargados en la tabla 'GEO_ADMIN_MASTER'.")
        print("   -> Ve a Azure Data Studio o VS Code y haz un SELECT para verificar.")
    except Exception as e:
        print(f"   -> ERROR CRÍTICO: {e}")

# ==========================================
# EJECUCIÓN PRINCIPAL
# ==========================================
if __name__ == "__main__":
    crear_datos_fake()   # Paso 1
    df_limpio = limpiar_datos() # Paso 2
    cargar_a_sql(df_limpio)     # Paso 3