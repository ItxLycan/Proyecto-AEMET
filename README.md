# Proyecto AEMET

Proyecto de portfolio que simula una migración de una base de datos on-premise (Oracle) a Azure, utilizando **Azure Data Factory** para orquestar procesos de **ETL/ELT**. Como caso de uso real para poblar el modelo de datos, se integra la **API pública de AEMET OpenData** (predicción meteorológica por municipios).

## Objetivo del proyecto

Demostrar el ciclo de trabajo de un Data Engineer:
- Diseño de un modelo de datos relacional en Oracle.
- Ingesta de datos desde una fuente externa (API REST).
- Procesos de extracción, transformación y carga.
- Preparación del terreno para una futura migración a Azure (Data Factory, Synapse/SQL, Data Lake).

## Arquitectura de datos

El proyecto distingue dos tipos de carga de datos, con un criterio de diseño diferente en cada caso:

### 1. Seed data / Datos de referencia (carga única)
Comunidades autónomas y provincias son **datos maestros prácticamente inmutables** (equivalentes a una dimensión de tipo 0 en modelado dimensional). Se cargan una única vez desde un fichero JSON estático, sin necesidad de un pipeline recurrente ni de una fuente externa dinámica.

- `Pipelines/ETL_AUT_COMM` → Carga de comunidades autónomas (`AUT_COMM`)
- `Pipelines/ETL_PROVINCE` → Carga de provincias (`PROVINCE`), relacionadas con `AUT_COMM`

### 2. ETL real (extracción desde API externa)
Los municipios se obtienen dinámicamente desde la **API de AEMET OpenData**, que mantiene su propio catálogo (~8.124 municipios) con identificadores propios distintos del estándar INE. Aquí sí se aplican las tres fases de un ETL:

- **Extract:** llamada a la API REST de AEMET.
- **Transform:** normalización de texto, mapeo de provincia → `ID_PROV`, validación de datos.
- **Load:** inserción idempotente en `MUNICIPALITY`.

- `Pipelines/ETL_MUNICIPALITIES` → Carga de municipios (`MUNICIPIOS`) desde la API de AEMET

## Modelo de datos

Tablas principales en Oracle (`Model and Tables Oracle/Oracle Tables`):

| Tabla | Descripción |
|---|---|
| `Comunidad_Autonoma` | Comunidades autónomas de España |
| `Provincia` | Provincias, relacionadas con su comunidad autónoma |
| `Municipios` | Municipios según catálogo de AEMET, relacionados con su provincia |
| `Centro_meteorologico` | Estaciones/centros meteorológicos |
| `Estado_Centro_meteorologico` | Estado operativo de los centros meteorológicos |
| `Reporte_del_tiempo` | Datos de predicción/observación obtenidos de la API |

*(Diagrama entidad-relación disponible en `Model and Tables Oracle/Data Model`)*

## Tecnologías utilizadas

- **Python** (extracción, transformación y carga de datos)
- **Oracle Database** (almacenamiento origen)
- **AEMET OpenData API** (fuente de datos externa)
- **Azure Data Factory** *(próxima fase: orquestación de la migración a Azure)*

## Estado del proyecto

- [x] Modelo de datos en Oracle
- [x] Carga de datos de referencia (CCAA, provincias)
- [ ] ETL de municipios desde API de AEMET
- [ ] ETL de Centros meteorologicos desde API de AEMET
- [ ] Ingesta de datos de predicción/observación meteorológica
- [ ] Migración a Azure con Data Factory

## Próximos pasos

1. Completar el ETL de municipios.
2. Diseñar el pipeline de ingesta de predicciones meteorológicas (datos que sí cambian frecuentemente → ETL incremental).
3. Trasladar la orquestación a Azure Data Factory.