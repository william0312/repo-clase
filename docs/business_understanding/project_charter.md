# Project Charter — Entendimiento del Negocio

## Nombre del Proyecto

Análisis comparativo de la recepción digital de Rock al Parque (2023–2025) mediante análisis de sentimiento sobre comentarios públicos de YouTube.

## Contexto y problema de negocio

Rock al Parque es un festival público de Bogotá declarado evento de interés cultural de la ciudad mediante el Acuerdo 120 de 2004 del Concejo de Bogotá, que establece entre sus propósitos integrar a la población joven a los programas institucionales de cultura y estimular los procesos democráticos y de cultura ciudadana. El evento trasciende su carácter musical y se configura como una apuesta institucional ligada a la cultura, la participación ciudadana y la apropiación del espacio público.

El beneficiario potencial es **IDARTES (Instituto Distrital de las Artes)**, en el dominio de sector público y gestión cultural. Hoy la evaluación del festival se apoya principalmente en indicadores cuantitativos —asistencia, alcance, visualizaciones—, que no permiten observar de manera estructurada cómo varía la recepción expresada por las audiencias en canales digitales entre ediciones. Los comentarios públicos de YouTube constituyen datos observacionales generados espontáneamente por los usuarios, pero permanecen sin explotar como fuente de evidencia.

**Pregunta de negocio:** ¿cambia la distribución del sentimiento expresado en los comentarios públicos de YouTube entre las ediciones 2023, 2024 y 2025 de Rock al Parque?

**Problema analítico asociado:** clasificar automáticamente un corpus de comentarios en español en tres categorías de polaridad (Positivo, Neutro, Negativo) y comparar estadísticamente su distribución entre las tres ediciones.

## Objetivo del Proyecto

Comparar la recepción digital de las ediciones 2023, 2024 y 2025 de Rock al Parque mediante un modelo de análisis de sentimiento basado en Procesamiento de Lenguaje Natural, aplicado a una muestra delimitada de comentarios públicos de YouTube, para aportar a IDARTES una fuente complementaria de evidencia sobre la valoración del festival por parte de sus audiencias digitales.

### Objetivos específicos

1. Construir un corpus de comentarios públicos de YouTube de las ediciones 2023, 2024 y 2025, aplicando criterios homogéneos de búsqueda, selección de videos y extracción.
2. Entrenar y comparar modelos de clasificación de sentimiento en español (TF-IDF + SVM lineal, RoBERTa-base-BNE y RoBERTuito) sobre el corpus TASS 2020 y una muestra etiquetada manualmente del dominio.
3. Clasificar el corpus completo con el modelo seleccionado y estimar la distribución de polaridad por edición, conservando las probabilidades por clase.
4. Evaluar estadísticamente si existen diferencias en la distribución del sentimiento entre las tres ediciones y documentar los resultados para su interpretación por parte del cliente.

## Alcance del Proyecto

### Incluye

- **Fuente de datos:** YouTube Data API. Para cada año se consultan hasta 50 videos ordenados por número de visualizaciones y se conservan los que referencian explícitamente Rock al Parque y el año; se recuperan hasta 100 comentarios públicos por video. Ediciones 2023, 2024 y 2025.
- **Corpus:** 2.706 comentarios recolectados (814 de 2023, 1.212 de 2024 y 680 de 2025); tras la depuración descrita en el análisis exploratorio, el corpus analítico queda en 2.530 comentarios.
- **Muestra etiquetada:** 586 comentarios anotados manualmente (169 de 2023, 196 de 2024 y 221 de 2025) con las categorías P, NEU y N.
- **Corpus de entrenamiento:** TASS 2020 (conjuntos train y dev), con etiquetas de polaridad P, NEU y N.
- **Modelado:** TF-IDF + SVM lineal como línea base; RoBERTa-base-BNE y RoBERTuito con fine-tuning; búsqueda de hiperparámetros y evaluación sobre conjunto de prueba independiente.
- **Análisis:** distribución del sentimiento por edición, prueba chi-cuadrado de independencia, V de Cramér y comparaciones por pares con corrección de Holm.
- **Entregables:** notebook reproducible con el flujo completo, corpus anonimizado, modelo entrenado, informe de resultados y material de sustentación.

### Excluye

- Representar la totalidad de la audiencia del festival: el corpus solo cubre comentarios públicos de YouTube y no es una muestra probabilística de asistentes ni de la ciudadanía.
- Otras plataformas (X, Instagram, TikTok, foros) y comentarios privados o eliminados.
- Datos personales o análisis de perfiles de usuarios; solo se conservan identificadores seudonimizados.
- Inferencia causal: el sentimiento observado no se atribuye a decisiones de programación, sonido, logística u organización.
- Ediciones anteriores a 2023 o posteriores a 2025.
- Despliegue en producción dentro de los sistemas de IDARTES; el producto es un prototipo analítico y un conjunto de indicadores.

### Criterios de éxito

**Técnicos**
- El modelo final supera la línea base TF-IDF + SVM en F1 macro sobre el conjunto de prueba.
- F1 macro del modelo final igual o superior a 0,70 en el conjunto de prueba no visto.
- Resultados reproducibles: semillas fijas, versiones de datos congeladas y verificación por checksum SHA-256.

**De negocio**
- Se obtiene una distribución de sentimiento comparable entre las tres ediciones, con indicadores y visualizaciones interpretables.
- La comparación estadística entre ediciones se reporta con su tamaño de efecto y sus limitaciones.
- IDARTES recibe un insumo documentado que puede usar como evidencia complementaria en la evaluación del festival.

## Metodología

Se adopta el **Team Data Science Process (TDSP)** como marco de gestión del proyecto, con las fases de entendimiento del negocio, adquisición y entendimiento de datos, modelado, despliegue y aceptación. El trabajo técnico se organiza según una adaptación de **CRISP-DM**, coherente con TDSP, y con un flujo de PLN: adquisición → limpieza y normalización → análisis exploratorio → representación y modelado → evaluación → comunicación.

**Herramientas:** Python 3, pandas, NumPy, scikit-learn, PyTorch y Hugging Face Transformers, matplotlib y seaborn, Google Colab (GPU) y gdown para la gestión de versiones congeladas de los datos.

**Control de calidad:** corpus versionado con checksums; separación estricta entre entrenamiento, validación y prueba; la muestra etiquetada del dominio se usa para evaluar la generalización y no para ajustar el modelo base; todas las transformaciones se ajustan solo con datos de entrenamiento.

## Cronograma

Las fechas son de referencia y se ajustan al calendario oficial del curso.

| Etapa | Duración | Fechas | Entregable principal |
|---|---|---|---|
| Entendimiento del negocio y carga de datos | 2 semanas | 25 nov – 8 dic 2026 | `project_charter.md`, definición y diccionario de datos |
| Preprocesamiento y análisis exploratorio | 4 semanas | 9 dic 2026 – 5 ene 2027 | `data_summary.md`, notebooks de EDA y limpieza |
| Modelamiento y extracción de características | 4 semanas | 6 ene – 2 feb 2027 | `baseline_models.md`, `model_report.md` |
| Despliegue | 2 semanas | 3 – 16 feb 2027 | `deploymentdoc.md`, prototipo de inferencia |
| Evaluación y entrega final | 3 semanas | 17 feb – 9 mar 2027 | `exit_report.md`, informe y sustentación |

## Equipo del Proyecto

- **William Mora** — integrante del equipo; análisis de datos, modelado y documentación.
- **Jorge Esau Tierradentro** — integrante del equipo; adquisición de datos, modelado y documentación.
- **Felipe Restrepo Calle** — profesor del curso; orientación metodológica y evaluación.

## Presupuesto

| Rubro | Tratamiento | Observación |
|---|---|---|
| Horas del equipo | Aporte en especie | Dedicación semanal de los dos integrantes |
| Infraestructura de cómputo | Aporte en especie | Google Colab con GPU en su capa gratuita; equipo local para tareas livianas |
| Almacenamiento y versionado | Aporte en especie | Google Drive para versiones congeladas del corpus |
| YouTube Data API | Sin costo | Consumo dentro de la cuota gratuita |
| Licencias de software | Sin costo | Stack open source (Python, scikit-learn, PyTorch, Transformers) |
| Servicios de nube adicionales | No previstos | — |

**Costo monetario directo estimado: 0 COP.** El proyecto se financia con aporte en especie de los integrantes.

## Stakeholders

| Stakeholder | Rol | Expectativa |
|---|---|---|
| IDARTES | Beneficiario y cliente potencial | Evidencia complementaria sobre la recepción digital del festival y su evolución entre ediciones |
| Secretaría de Cultura, Recreación y Deporte / Concejo de Bogotá | Marco institucional del evento | Que el análisis aporte a la valoración de un evento de interés cultural |
| Audiencias y ciudadanía | Fuente de los datos y destinatarias del evento | Uso responsable de comentarios públicos, sin exposición de datos personales |
| Equipo del proyecto | Ejecución | Resultados técnicamente sólidos, reproducibles y entregados en los plazos |
| Universidad Nacional de Colombia (curso) | Evaluación académica | Rigor metodológico, trazabilidad y documentación de cada fase |

**Aprobador:** profesor del curso. **Fecha de aprobación:** pendiente de la revisión de la semana 1.

## Riesgos y supuestos

| Riesgo | Impacto | Mitigación |
|---|---|---|
| Sesgo de selección de YouTube: el corpus no representa a toda la audiencia | Conclusiones no generalizables | Declarar el alcance explícitamente y no extrapolar a asistentes ni a la ciudadanía |
| Comentarios muy breves, emojis y jerga | Pérdida de señal y errores de clasificación | Preprocesamiento diferenciado por modelo; conservar emojis en RoBERTuito |
| Clase neutra ambigua y minoritaria | Bajo F1 en NEU | Reportar F1 macro y por clase; analizar la matriz de confusión |
| Etiquetado manual subjetivo (586 comentarios) | Ruido en las etiquetas | Criterios de anotación documentados y revisión de casos dudosos |
| Cambios en la API o agotamiento de cuota | Interrupción de la recolección | Corpus congelado con checksums; recolección única documentada |
| Deriva de dominio entre ediciones | Comparaciones inválidas | Criterios homogéneos de búsqueda y extracción; verificación de la distribución |
| Fuga de información entre train y test | Métricas infladas | Partición estricta y ajuste de transformaciones solo con entrenamiento |

**Supuestos:** los comentarios son públicos y accesibles al momento de la recolección; no contienen datos personales sensibles; el corpus descrito en el notebook es la versión oficial del proyecto.

## Aprobaciones

| Nombre | Cargo | Firma | Fecha |
|---|---|---|---|
| Felipe Restrepo Calle | Profesor del curso | | |
| William Mora | Integrante del equipo | | |
| Jorge Esau Tierradentro | Integrante del equipo | | |
