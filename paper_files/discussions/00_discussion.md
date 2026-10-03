# Discusión entre Claude y Yo acerca de las decisiones/estrategias para superar la revisión

## Decisiones a lo largo de la investigación para comprender los motivos

Este proyecto no comenzó como un trabajo de investigación, sino que tuvo una orientación más cercana a la elaboración de un producto de ingeniería. Por tanto, muchas decisiones no se tomaron siguiendo una metodología científica, sino con el objetivo de construir un producto.

### Dataset
Al comienzo de este trabajo solo estaba disponible el dataset DFire. Posteriormente, apareció FASDD y se incorporó. La realidad es que ambos datasets incorporan imágenes de internet y no hay traza de que imágenes que estén en entrenamiento de uno no estén en validación o test de otro, lo que falsearía los resultados, al utilizarse imágenes con las que se ha entrenado el modelo para verificarlo.

No se hizo un conjunto separado de validación porque DFire no cuenta con ese conjunto, sino que solo tiene train y test.

#### Resumen del problema

El protocolo de evaluación del paper tiene tres problemas relacionados con los datos. Todos se han verificado en el código y en los datos históricos.

1. **El test se usó como conjunto de validación (R3-1, crítico).** ReduceLROnPlateau monitoriza la loss de test y se reporta el checkpoint con mejor F1 en test. Además, AIMET eligió los ratios de compresión de BED evaluando sobre 2048 imágenes de test (A-8).
2. **Posibles duplicados o casi-duplicados entre train y test (R2-M2).** Ambos datasets contienen imágenes de internet, y DFire probablemente frames de vídeo. Nunca se comprobó.
3. **Las particiones no son exactamente las "oficiales"** (A-3). El `val.txt` de FASDD se fusionó con el entrenamiento. Además, todas las métricas de test se calcularon con `drop_last=True` (A-9).

A esto se suma la falta de semillas (R2-M3), que se resuelve en la misma campaña de reentrenamiento.

Base de partida verificada: los modelos MobileNetV2 Nano FP32 y QAT del paper se reproducen exactamente con su código y sus pesos históricos (`results_audit/mobilenet_paper_replica`).

**Detalle, análisis de estrategias, plan de detección de duplicados y evaluación de su impacto:** `01_dataset.md`.
