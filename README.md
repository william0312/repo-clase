# Recepción digital de Rock al Parque (2023–2025)

Proyecto de ciencia de datos para comparar la recepción digital de las ediciones 2023, 2024 y 2025 del festival Rock al Parque, a partir del análisis de sentimiento sobre comentarios públicos de YouTube.

**Beneficiario potencial:** IDARTES (Instituto Distrital de las Artes).
**Dominio:** sector público / gestión cultural.

## Problema

La evaluación del festival se apoya en indicadores cuantitativos (asistencia, alcance, visualizaciones), que no muestran de forma estructurada cómo varía la recepción expresada por las audiencias en canales digitales. El proyecto clasifica los comentarios en Positivo (P), Neutro (NEU) y Negativo (N), y compara estadísticamente la distribución del sentimiento entre ediciones.

## Enfoque

- **Datos:** comentarios públicos de YouTube (2023, 2024, 2025) recuperados con criterios homogéneos; muestra etiquetada manualmente de 580 comentarios; corpus TASS 2020 para entrenamiento.
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
scripts/                    Scripts ejecutables por etapa
src/                        Código fuente del proyecto (paquete Python)
```

## Estado

| Fase TDSP | Estado |
|---|---|
| Entendimiento del negocio | En curso — semana 1 |
| Entendimiento y preparación de datos | Pendiente |
| Modelado | Pendiente |
| Despliegue | Pendiente |
| Aceptación | Pendiente |

## Equipo

- William Mora
- Jorge Esau Tierradentro

Curso: Proyecto Aplicado — Universidad Nacional de Colombia.

## Reproducibilidad

Los datos se gestionan en versiones congeladas y se verifican con checksum SHA-256. El flujo completo se documenta en los notebooks y scripts del repositorio. No se incluyen datos personales ni credenciales; la clave de la YouTube Data API no se versiona.
