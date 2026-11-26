# Recepción digital de Rock al Parque (2023–2025)

Proyecto de ciencia de datos para comparar la recepción digital de las ediciones 2023, 2024 y 2025 del festival Rock al Parque, a partir del análisis de sentimiento sobre comentarios públicos de YouTube.

**Beneficiario potencial:** IDARTES (Instituto Distrital de las Artes).
**Dominio:** sector público / gestión cultural.

## Problema

La evaluación del festival se apoya en indicadores cuantitativos (asistencia, alcance, visualizaciones), que no muestran de forma estructurada cómo varía la recepción expresada por las audiencias en canales digitales. El proyecto clasifica los comentarios en Positivo (P), Neutro (NEU) y Negativo (N), y compara estadísticamente la distribución del sentimiento entre ediciones.

## Enfoque

- **Datos:** comentarios públicos de YouTube (2023, 2024, 2025) recuperados con criterios homogéneos; muestra etiquetada manualmente de 586 comentarios; corpus TASS 2020 para entrenamiento.
- **Modelos:** TF-IDF + SVM lineal (línea base), RoBERTa-base-BNE y RoBERTuito con *fine-tuning*.
- **Análisis:** chi-cuadrado de independencia, V de Cramér y comparaciones por pares con corrección de Holm.
- **Metodología:** TDSP, con un flujo de trabajo alineado con CRISP-DM.

## Estructura del repositorio

```
docs/
  business_understanding/   Project charter y definición del problema
  data/                     Definición, diccionario y resumen de datos
  modeling/                 Modelos base y reporte del modelo final
  deployment/               Documentación del despliegue
  acceptance/               Informe de salida
data/                       Datos locales (no versionados; se reconstruyen)
scripts/                    Scripts ejecutables por etapa
src/                        Código fuente del proyecto (paquete Python)
```

## Estado

| Fase TDSP | Estado |
|---|---|
| Entendimiento del negocio | Completo — semana 1 |
| Entendimiento y preparación de datos | En curso — semana 1 |
| Modelado | Pendiente |
| Despliegue | Pendiente |
| Aceptación | Pendiente |

## Equipo

- William Mora
- Jorge Esau Tierradentro

Curso: Proyecto Aplicado — Universidad Nacional de Colombia.

## Datos

El proyecto usa cuatro insumos de datos, todos versionados de forma congelada en Google Drive:

| Insumo | Archivo | Uso |
|---|---|---|
| Corpus completo de Rock al Parque | `dataframe_df.xlsx` | Universo de comentarios (2.706) |
| Muestra etiquetada manualmente | `Con_etiqueta.xlsx` | Evaluación en el dominio (586) |
| Comentarios sin etiqueta | `Sin_etiqueta.xlsx` | Clasificación con el modelo final (1.962) |
| TASS 2020 | `Task1-train-dev.zip` | Entrenamiento y comparación de modelos |

Se descargan y verifican con:

```bash
pip install gdown openpyxl pandas
python scripts/data_acquisition/main.py --data-dir data/raw --resumen
# solo TASS:
python scripts/data_acquisition/main.py --data-dir data/raw --solo tass_2020
```

Los archivos no se versionan en Git (`data/` está en `.gitignore`): se reconstruyen con ese script y cada descarga se valida contra un SHA-256 registrado. Así el repositorio no duplica datos de terceros ni comentarios de usuarios, y cualquier persona obtiene exactamente las mismas versiones.

## Reproducibilidad

Los datos se gestionan en versiones congeladas y se verifican con checksum SHA-256. El flujo completo se documenta en los notebooks y scripts del repositorio. No se incluyen datos personales ni credenciales; la clave de la YouTube Data API no se versiona.
