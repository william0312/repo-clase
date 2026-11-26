# Definición de los datos

## Origen de los datos

El proyecto combina dos fuentes textuales con funciones distintas:

1. **Comentarios públicos de YouTube sobre Rock al Parque (2023, 2024 y 2025).** Se recuperaron mediante la YouTube Data API v3 con un procedimiento homogéneo por edición: búsqueda de hasta 50 videos ordenados por número de visualizaciones, conservación de los videos cuyo título referencia explícitamente el festival y el año, y extracción de hasta 100 comentarios públicos por video. El resultado se congeló en tres archivos de Excel alojados en Google Drive.
2. **TASS 2020 (corpus externo etiquetado en español).** Se usa como conjunto de entrenamiento y comparación de los modelos de sentimiento. Se distribuye como un ZIP con archivos TSV por país (`es`, `cr`, `mx`, `pe`, `uy`) y por partición (`train`, `dev`).

Los archivos se versionan de forma congelada: cada descarga se verifica con SHA-256 para garantizar que todas las etapas del análisis usan exactamente la misma versión. Los identificadores de Google Drive y los checksums están en `scripts/data_acquisition/main.py`.

## Especificación de los scripts para la carga de datos

| Script | Función |
|---|---|
| `scripts/data_acquisition/main.py` | Descarga los insumos desde Google Drive, verifica SHA-256, descomprime los ZIP y carga los corpus en DataFrames. |
| `scripts/data_acquisition/main.py --resumen` | Imprime dimensiones, distribución por edición y distribución de etiquetas. |

Comandos:

```bash
pip install gdown openpyxl pandas
python scripts/data_acquisition/main.py --data-dir data/raw
python scripts/data_acquisition/main.py --data-dir data/raw --resumen
python scripts/data_acquisition/main.py --solo corpus_completo corpus_etiquetado
```

El script falla de forma explícita si un archivo descargado no coincide con el checksum registrado, de modo que una versión alterada nunca pasa desapercibida.

## Referencias a rutas o bases de datos origen y destino

### Rutas de origen de datos

| Insumo | Archivo | Origen | Destino local |
|---|---|---|---|
| Corpus completo | `dataframe_df.xlsx` | Google Drive (ID en el script) | `data/raw/dataframe_df.xlsx` |
| Muestra etiquetada | `Con_etiqueta.xlsx` | Google Drive | `data/raw/Con_etiqueta.xlsx` |
| Comentarios sin etiqueta | `Sin_etiqueta.xlsx` | Google Drive | `data/raw/Sin_etiqueta.xlsx` |
| TASS 2020 | `Task1-train-dev.zip` | Google Drive | `data/raw/tass/{train,dev}/*.tsv` |

### Estructura de los archivos de origen

- Los tres corpus de Rock al Parque son libros de Excel con una sola hoja y una fila por comentario; cada fila incluye metadatos del video y del comentario (ver `data_dictionary.md`).
- TASS 2020 son archivos TSV sin encabezado, con tres columnas: identificador, texto y polaridad (`N`, `NEU`, `P`).

### Verificación de integridad (versiones congeladas)

| Archivo | Filas | Columnas | SHA-256 |
|---|---|---|---|
| `dataframe_df.xlsx` | 2.706 | 9 | `e0075809db4894bd5c6557b4d8de30c979b86428e5042c96cb026119634bc55d` |
| `Con_etiqueta.xlsx` | 586 | 10 | `68c543f762a188bca7210a83a5d437701749183b1c7f42e0b79c907fe0e8d54d` |
| `Sin_etiqueta.xlsx` | 1.962 | 10 | `98160918dadbf3867e12c4c2d15198cb954448c3a90a45687b74e4f83476a151` |
| `Task1-train-dev.zip` | — | — | `359388d8108b79bd35b02ed5b4cb442935e5e87c992e3db0db5f19af189e99bf` |

### Base de datos de destino

No se utiliza un motor de base de datos. El destino es el sistema de archivos local (`data/raw/`) y, para las etapas posteriores, un conjunto analítico en formato tabular (Parquet/CSV) que se derivará de estos insumos. La carpeta `data/` no se versiona en Git; se reconstruye con el script de adquisición.

## Procedimientos de transformación y limpieza

La limpieza documentada en el análisis exploratorio sigue estos pasos:

1. Normalización de texto: decodificación de entidades HTML, colapso de espacios y eliminación de extremos.
2. Eliminación de comentarios vacíos (1 registro).
3. Eliminación de repeticiones inmediatas: mismo video, autor y texto dentro de una ventana de 5 minutos (4 registros).
4. Eliminación de un comentario en otro idioma sin contenido analizable en español.
5. Eliminación de URL (14 registros); se conservan menciones y hashtags.
6. Detección de idioma y verificación de registros en inglés.

Como resultado, el corpus analítico queda en 2.530 comentarios, de los cuales 580 conservan etiqueta humana tras la depuración y 1.951 se clasifican con el modelo ajustado.


