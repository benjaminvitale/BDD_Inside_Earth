# BDD_Inside_Earth
Demo de mi base de datos para Inside Earth


## Descripción del Proyecto
Prueba de Concepto diseñada para estructurar, limpiar y migrar datos geológicos y operativos desde fuentes no estructuradas (Excel/Legacy) hacia una arquitectura moderna en la nube.

## Objetivo
Transformar datos dispersos en una Fuente Única de Verdad capaz de alimentar dashboards de Business Intelligence y modelos de decisión de inversión.

## Arquitectura
* **Database:** Azure SQL (Modelo Relacional 3FN).
* **ETL:** Python (Pandas + SQLAlchemy) con estrategia de procesamiento por lotes (Chunking).
* **Orquestación:** (Simulado) Scripts modulares para ingesta incremental.

## Estructura de la Base de Datos
El modelo de datos sigue un enfoque jerárquico para asegurar integridad referencial:
1.  **Geo Master:** Entidad raíz (Ubicación).
2.  **Screening:** Filtros de viabilidad inicial.
3.  **Project Master:** Ejecución técnica y operativa.
4.  **Investment Output:** Resultados financieros y de riesgo.

## Cómo reproducir
1. Ejecutar el script `sql/01_init_database.sql` en una instancia de Azure SQL o SQL Server.
2. Configurar las credenciales en el script de Python (variables de entorno).
3. Ejecutar el pipeline de carga.
