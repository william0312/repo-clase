# Diccionario de datos

Convenciones: `str` = texto; `int` = entero; `datetime` = fecha y hora. Los conteos corresponden a la versión congelada verificada con SHA-256 (ver `data_definition.md`).

## Base de datos 1 — Corpus completo de Rock al Parque (`dataframe_df.xlsx`)

2.706 filas × 9 columnas. Un registro por comentario público de YouTube.

| Variable | Descripción | Tipo | Rango / valores | Fuente |
|---|---|---|---|---|
| `Año_Edición` | Edición del festival a la que se asocia el video | int | 2023, 2024, 2025 | YouTube Data API |
| `Video_ID` | Identificador del video de YouTube | str | 11 caracteres | YouTube Data API |
| `Video` | Título del video | str | Texto libre | YouTube Data API |
| `Fecha_Video` | Fecha y hora de publicación del video | datetime | 2023-11-09 a 2025-07-24 | YouTube Data API |
| `Comentario_ID` | Identificador del comentario | str | Único por comentario | YouTube Data API |
| `Autor` | Identificador público del autor | str | `@usuario` | YouTube Data API |
| `Comentario` | Texto del comentario | str | Texto libre; 1 nulo | YouTube Data API |
| `Fecha_Comentario` | Fecha y hora de publicación del comentario | datetime | 2023-11-09 a 2026-09-13 | YouTube Data API |
| `Likes` | Me gusta recibidos por el comentario | int | ≥ 0 | YouTube Data API |

Distribución por edición: 814 (2023), 1.212 (2024), 680 (2025). Videos únicos: 110. Autores únicos: 2.366.

## Base de datos 2 — Muestra etiquetada manualmente (`Con_etiqueta.xlsx`)

586 filas × 10 columnas. Subconjunto del corpus completo con etiqueta humana de polaridad.

| Variable | Descripción | Tipo | Rango / valores | Fuente |
|---|---|---|---|---|
| `Año_Edición` | Edición del festival | int | 2023, 2024, 2025 | Corpus completo |
| `Video_ID` | Identificador del video | str | 11 caracteres | Corpus completo |
| `Video` | Título del video | str | Texto libre | Corpus completo |
| `Fecha_Video` | Fecha del video | str | Fecha en formato local | Corpus completo |
| `Comentario_ID` | Identificador del comentario | str | Único | Corpus completo |
| `Autor` | Identificador público del autor | str | `@usuario` | Corpus completo |
| `Comentario` | Texto del comentario | str | Texto libre | Corpus completo |
| `Fecha_Comentario` | Fecha del comentario | str | Fecha en formato local | Corpus completo |
| `Likes` | Me gusta del comentario | int | ≥ 0 | Corpus completo |
| `categoria` | Polaridad asignada manualmente | str | `P` (positivo), `NEU` (neutro), `N` (negativo) | Anotación manual |

Distribución: 169 comentarios de 2023, 196 de 2024 y 221 de 2025. Etiquetas: `P` = 327, `N` = 139, `NEU` = 120.

Criterio de anotación: `P` expresa aprobación, satisfacción o valoración favorable; `N` expresa rechazo, crítica o valoración desfavorable; `NEU` corresponde a comentarios informativos, preguntas o menciones sin carga valorativa clara.

> Nota: en esta hoja las columnas de fecha están almacenadas como texto, por lo que deben convertirse con `pd.to_datetime(..., errors="coerce")` antes de cualquier análisis temporal.

## Base de datos 3 — Comentarios sin etiqueta (`Sin_etiqueta.xlsx`)

1.962 filas × 10 columnas. Comentarios sin anotación humana, clasificados posteriormente con el modelo ajustado.

| Variable | Descripción | Tipo | Rango / valores | Fuente |
|---|---|---|---|---|
| `Año_Edición` | Edición del festival | int | 2023, 2024, 2025 | Corpus completo |
| `Video_ID` | Identificador del video | str | 11 caracteres | Corpus completo |
| `Video` | Título del video | str | Texto libre | Corpus completo |
| `Fecha_Video` | Fecha del video | str | Fecha en formato local | Corpus completo |
| `Comentario_ID` | Identificador del comentario | str | Único | Corpus completo |
| `Autor` | Identificador público del autor | str | `@usuario` | Corpus completo |
| `Comentario` | Texto del comentario | str | Texto libre; 1 nulo | Corpus completo |
| `Fecha_Comentario` | Fecha del comentario | str | Fecha en formato local | Corpus completo |
| `Likes` | Me gusta del comentario | int | ≥ 0 | Corpus completo |
| `Idioma_Detectado` | Idioma detectado automáticamente | str | `Español`, `Inglés`, `Portugués`, otros | `langdetect` |

## Base de datos 4 — TASS 2020 (`Task1-train-dev.zip` → `tass/`)

Archivos TSV sin encabezado, uno por país y partición. Se cargan con:

```python
pd.read_csv(ruta, sep="\t", header=None, names=["id", "texto", "polaridad"])
```

| Variable | Descripción | Tipo | Rango / valores | Fuente |
|---|---|---|---|---|
| `id` | Identificador del tuit | str | Numérico de 18 dígitos | TASS 2020 |
| `texto` | Texto del tuit | str | Texto libre en español | TASS 2020 |
| `polaridad` | Polaridad etiquetada | str | `N`, `NEU`, `P` | TASS 2020 |
| `split` | Partición de origen | str | `train`, `dev` | Nombre de carpeta |
| `pais` | Variedad de español | str | `es`, `cr`, `mx`, `pe`, `uy` | Nombre de archivo |

El campo `split` y `pais` se agregan al cargar; no están en el archivo original. La partición `test` no se distribuye en este ZIP: el conjunto de prueba se construye a partir de `dev`.

## Correspondencia entre etiquetas

| TASS 2020 | Muestra Rock al Parque | Significado |
|---|---|---|
| `P` | `P` | Positivo |
| `NEU` | `NEU` | Neutro |
| `N` | `N` | Negativo |

## Variables derivadas previstas

| Variable | Definición | Uso |
|---|---|---|
| `texto_normalizado` | Texto tras limpieza (minúsculas, sin URL ni caracteres especiales) | TF-IDF + SVM |
| `texto_robertuito` | Texto tras normalización de menciones, hashtags y emojis | RoBERTuito |
| `polaridad_final` | Etiqueta humana o predicción del modelo | Corpus analítico |
| `fuente` | `Humana` o `RoBERTuito` | Trazabilidad de la etiqueta |
| `prob_P`, `prob_NEU`, `prob_N` | Probabilidad estimada por clase | Indicadores agregados |
