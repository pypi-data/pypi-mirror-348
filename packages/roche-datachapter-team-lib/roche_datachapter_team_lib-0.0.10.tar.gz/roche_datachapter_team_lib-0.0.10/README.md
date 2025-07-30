# Roche Data Chapter Team Library

## Description

Una biblioteca modular en Python desarrollada para estandarizar y simplificar la creación de procesos ETL y automatizaciones. Pensada para equipos de datos que requieren integraciones con múltiples fuentes, soporte de logs y trazabilidad, y herramientas de administración de jobs SQL.

## Características principales

### 🔌 Conectores de Base de Datos
- Conexiones automáticas a SQL Server, Oracle, SAP HANA, MySQL, Snowflake y Redshift utilizando variables de entorno para parametrización segura.
- Soporte de ejecución de consultas personalizadas y procedimientos almacenados.
- Lectura directa a `pandas.DataFrame` o listas JSON.

### 📊 Transformaciones de Datos
- Conversión robusta de fechas, números, nulos y tipos de datos desde hojas de cálculo o APIs externas.
- Estándares predefinidos para Google Sheets y Excel.

### 📤 Google API Services
- Lectura/escritura en hojas de Google Sheets.
- Carga y descarga de archivos desde Google Drive.
- Manejo de credenciales OAuth2 y reintentos automáticos.

### 📩 Email Automation con AppSheet
- Gestión automatizada del envío de emails usando AppSheet como backend.
- Soporte para archivos adjuntos en Google Drive (PDF, Excel, TXT).

### 📁 Generación de Excel
- Creación de archivos Excel multiformato con estilo, desde múltiples `DataFrame`.
- Ancho de columnas y formatos aplicados automáticamente.

### 📅 SQL Server Agent Job Manager
- Creación, actualización y administración de SQL Jobs directamente desde Python.
- Utilidad especialmente útil para entornos corporativos que ejecutan ETLs como tareas programadas.

### 📑 Logging persistente
- Sistema de log en archivos `.log` y persistencia opcional en base de datos.
- Integrado con `JobExecution` y `JobExecutionLog`.

## Usage
Está pensada para ser utilizado como requisito en cualquier proyecto ETL en Python.

## Support
- Ignacio Castillo (ignacio.castillo@roche.com)
- Lucas Frías (lucas.frias@roche.com)
- Uciel Bustamante (uciel.bustamante@contractors.roche.com)
- Sara Fernandez (sara.fernandez.sf1@roche.com)
- Diego Pedro (diego.pedro@contractors.roche.com)

## Authors and acknowledgment
Lucas Frías (lucas.frias@roche.com)
Uciel Bustamante (uciel.bustamante@contractors.roche.com)