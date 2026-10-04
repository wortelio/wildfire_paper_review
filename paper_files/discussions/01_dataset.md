# 01 — Dataset: validación, duplicados y semillas

Comentarios de los revisores que trata este documento: R3-1 (test usado para la selección del modelo), R2-M2 (duplicados entre train y test) y R2-M3 (semillas y variabilidad).

Problemas detectados por nosotros, no por los revisores. Su definición completa y su seguimiento están en `../reviewers/response_matrix.md`, sección "Author-identified issues":

| Código | Problema | Evidencia |
|---|---|---|
| A-3 | El `val.txt` oficial de FASDD se fusionó con el entrenamiento. La frase del paper "the original training and test assignments … are preserved" es inexacta | VERIFIED |
| A-7 | La lista de augmentations de §II-A está incompleta: faltan HorizontalFlip, CLAHE, RGBShift y el escalado. El blur 17×17 se aplica a resolución completa, y un `try/except` cambia las transformaciones en silencio | VERIFIED |
| A-8 | La búsqueda greedy de ratios de compresión de AIMET (BED) y la reconstrucción del channel pruning usaron 2048 imágenes de **test** | VERIFIED |
| A-9 | Las métricas de test se calcularon con `drop_last=True`: sobre 24,320 de las 24,371 imágenes de la Tabla 1 | VERIFIED |
| A-10 | Errata en la Tabla 1: en el test de FASDD CV, "Both" es 3358, no 3558 | VERIFIED |
Explicación general del problema: `00_discussion.md` → "Dataset".

## Contexto del autor y enfoque de la respuesta (2026-10-04)

**Reflexión del autor**, resumida fielmente:
- El paper se centra principalmente en optimizar modelos para su implementación en hardware de bajo consumo.
- La elección del caso de uso es uno de los "pecados originales" de la investigación, y la valoración es ambivalente:
  - por un lado, debería haberse elegido un caso de uso con un dataset estándar y bien establecido, para concentrar el esfuerzo en el hardware y no exponerse a los problemas actuales por la falta de un benchmark estándar de detección de incendios;
  - por otro lado, el caso de uso es interesante, motivador y de actualidad.
- El problema de fondo es que el caso de uso concreto no se trató con la rigurosidad necesaria. Fue por falta de experiencia: el autor hizo prácticamente toda la investigación solo, sin una guía científica adecuada, hace unos dos años, cuando la IA aún no estaba extendida.

**Implicación para la estrategia:**
- Las objeciones sobre el dataset se resuelven con una solución **robusta y honesta, proporcionada a lo que piden los revisores**, sin convertir el paper en un trabajo sobre datasets.
- El esfuerzo principal se reserva para las objeciones ligadas a la contribución de hardware (Tabla 9, potencia, comparación con trabajos FPGA, F1 en FPGA).

**Propuesta revisada para F1** (pendiente de confirmación del autor):
- Solo L0–L2, con hash exacto, hash de píxeles a 224 y hash perceptual (pHash/dHash, también sobre la imagen volteada), implementados con OpenCV y NumPy en los entornos existentes. Sin entorno nuevo y sin descarga de pesos, lo que resuelve D-F1a.
- Umbrales conservadores y una comprobación visual breve (30–50 pares).
- L3 con SSCD/DINOv2 se menciona como trabajo futuro, salvo que L0–L2 muestre una contaminación apreciable.
- Riesgo estimado de rechazo atribuible a no hacer L3: ≈ 1–3 % (INFERENCE).

Contenido:
1. Propuesta inicial de estrategias (usuario).
2. Comentarios de Claude (2026-10-03, secciones 1–8), trasladados sin cambios desde `00_discussion.md`.
3. **Plan detallado de detección de duplicados, evaluación de su impacto y estrategia de exclusión en test** (2026-10-04).

---

## Propuesta de estrategia
Se me ocurren 3 estrategias posibles:
1. Hacer un análisis de duplicados:
 - Qué resuelve? identifica si hay alguna imagen que contamine el conjunto de test.
 - Si hay duplicados, cómo se le podría dar solución? Habría que repetir gran cantidad de experimentos?
 - Problemas: sigue sin haber un conjunto de entrenamiento, uno de validación y uno de test.
    - Cómo se podría dar respuesta a esto? Cómo se podría justificar? Es defendible no utilizar un conjunto de validación, como de hecho sucede en DFire?

2. Eliminar DFire y utilizar solo FASDD, con sus 3 conjuntos: train/validation/test
 - Problema: cómo justificar a estas alturas a los revisores que se modifica el dataset. Crees que sería aceptable?

3. Hacer una combinación de 1 y 2: 
 - Se hace un análisis de duplicados
 - Se eliminan las imágenes duplicadas y se pasa a utilizar conjuntos de entrenamiento (DFire+FASDD), de validación (solo FASDD) y de test (DFire+FASDD)

## Claude comments

*(2026-10-03. Las estimaciones de horas son INFERENCE basadas en la estructura del código y en tiempos históricos. Los tiempos de GPU salen de las fechas de los ficheros de los runs históricos: ≈12 h Nano FP32 (100 épocas), ≈10 h Nano QAT, ≈14 h BED-FPGA QAT (150 épocas), en la RTX 4070 Ti compartida. Ver `reviewers/response_matrix.md`, filas R3-1, R2-M2, R2-M3, A-3.)*

### 1. Separar los dos problemas: tienen soluciones distintas

Las tres estrategias mezclan dos problemas independientes:

| | Problema | Revisor | Gravedad | Evidencia |
|---|---|---|---|---|
| **P1** | **El conjunto de test se usó para seleccionar el modelo.** ReduceLROnPlateau monitoriza la loss de test y el checkpoint elegido es el de mejor F1 en test | R3-1 (major) | **Crítico**: R3 lo cita para juzgar el paper como "technically sound: *partially*" | VERIFIED (`get_val_loader()` usa los splits de test en `train/mobilenet` y `train/bed`) |
| **P2** | Posibles duplicados o casi-duplicados entre train y test (internet, DFire ↔ FASDD) | R2-M2 | Moderado. R2 dice textualmente que el análisis *no es esencial*: pide aclarar si se hizo y, si no, reconocerlo | UNKNOWN (no consta ningún análisis) |

Hay además un tercer hecho relacionado: **el `val.txt` oficial de FASDD está fusionado en el entrenamiento** (VERIFIED: UAV 12550 + 8364 ≈ 20916 y CV 47660 + 31769 ≈ 79430 en la Tabla 1). Por tanto la frase del paper "the original training and test assignments … are preserved" es inexacta, y además FASDD *sí* tenía un conjunto de validación que no se usó como tal.

**Consecuencia clave: los duplicados (P2) se arreglan limpiando el test, no reentrenando.** Si hay imágenes de test con un duplicado en train, basta con quitarlas del test (o reportar test original y test limpio) y **re-evaluar los checkpoints existentes**. No hace falta reentrenar nada por P2. Lo que sí exige reentrenar es P1.

### 2. Respuestas a tus preguntas sobre la estrategia 1

- **¿Habría que repetir muchos experimentos si hay duplicados?** No por los duplicados en sí, como acabo de explicar: es re-evaluación. El reentrenamiento lo exige P1.
- **¿Es defendible no tener validación porque DFire no la tiene?** **No**, mientras el test se use para el scheduler y para elegir el checkpoint. Es práctica estándar separar un conjunto de validación del de entrenamiento cuando el dataset no lo trae, y los tres revisores lo saben. Solo sería defendible no tener validación con un protocolo sin ninguna selección: calendario fijo, sin scheduler dependiente de métricas y reportando la última época. No fue el caso.
- Ahora mismo el paper dice "held-out evaluation loss". Un revisor lo lee como un conjunto de validación separado y no lo es. **En la respuesta hay que decirlo claramente**: intentar maquillarlo es el mayor riesgo reputacional de todo este punto.

### 3. Valoración de las estrategias propuestas

Escala de impacto reputacional: ++ muy positivo / + positivo / 0 neutro / − negativo / −− muy negativo (riesgo alto de rechazo, o de dar imagen de poca rigurosidad).

| Estrategia | ¿Resuelve P1? | ¿Resuelve P2? | Puesta en marcha | Ejecución (GPU) | Impacto reputacional |
|---|---|---|---|---|---|
| 0. Solo reconocerlo como limitación | No | No | 2–3 h (texto) | — | **−−**: se admite un sesgo de selección sin corregirlo; R3 casi seguro mantiene su objeción, y solo hay un reenvío |
| 1. Solo análisis de duplicados | No | Sí | 10–14 h | 1–3 h | **−**: contenta a R2, pero deja abierto lo más grave (R3-1) |
| 2. Quitar DFire y usar solo FASDD (train/val/test) | Sí | Parcialmente | 30–40 h + reescritura casi total de resultados | Rehacer prácticamente todo: trayectorias BED y Nano, referencias y builds FINN. Del orden de 4–6 semanas de GPU, más síntesis | **−/−−**: cambia el dataset y todos los números en una revisión; puede leerse como "cambiar el dataset hasta que salga". No elimina el problema de las imágenes de internet (FASDD también las tiene) y pierde la parte de vigilancia de DFire. **No recomendado** |
| 3. Duplicados + train (DFire+FASDD) / val (solo FASDD oficial) / test | Sí | Sí | ≈ 45–60 h | 6–11 días | **+**: metodológicamente correcta y "oficial" para FASDD. Pero el entrenamiento pierde ~40k imágenes (−34 %) y la validación no contiene DFire. Los nuevos números dejan de ser comparables con los del paper, que es justo lo que queremos confirmar |
| **4. Recomendada: estrategia 3 refinada** (ver §4) | Sí | Sí | ≈ 50–75 h | 6–11 días (núcleo) + 4–5 días (ampliación opcional) | **++**: "detectamos un problema de protocolo, lo corregimos y confirmamos los resultados con media ± desviación". Responde a la vez R3-1, R2-M2, R2-M3 y A-3 |

### 4. Propuesta: estrategia 3 refinada, por fases

**F0 — Diagnóstico inmediato sin reentrenar** (útil para decidir cuánto invertir después).
- Para cada run clave (Nano FP32 `test_v04`, Nano QAT `test_v05`, BED-FPGA QAT `71_…`, BED Simplified `11_…`, MobileNetV2 de referencia), comparar el F1 de test del checkpoint `best_mean_F1` (elegido con test) con el del checkpoint `last_*.pt` (última época, sin selección por F1). He comprobado que existen ambos.
- La diferencia es una cota del sesgo de selección. Si es del orden de 0.1–0.3 pp, es una primera evidencia (parcial) de que los resultados son robustos. Ojo: el scheduler seguía mirando el test, así que no elimina toda la fuga.
- Puesta en marcha: **4–6 h** (copiar el código de evaluación al repo activo, rutas de solo lectura a los checkpoints de `uav`, salidas en `results/review_2026/`). Ejecución: **2–3 h** (≈15 evaluaciones de 24k imágenes).
- Impacto: **+** como evidencia complementaria. Por sí solo no basta.

**F1 — Análisis de duplicados.**
- Se combinan tres métodos:
  1. hash exacto (md5);
  2. hash perceptual (pHash/dHash), para recompresiones y redimensionados;
  3. vecinos más próximos con embeddings de una CNN preentrenada, para casi-duplicados (recortes, frames consecutivos).
- Se analiza train ↔ test (lo crítico), DFire ↔ FASDD, y también dentro de train, lo que sirve para F2.
- Los umbrales se calibran revisando a mano unas 100–200 parejas candidatas.
- Puesta en marcha: **10–14 h**, incluido crear un entorno conda nuevo (no tocar los existentes) y la revisión manual. Ejecución: **1–3 h**; el cuello de botella es leer y decodificar ~142k imágenes (≈42 GB).
- Resultado: test original + **test deduplicado**. Los checkpoints existentes (incluidos los desplegados) se re-evalúan en ambos: **+1 h** de ejecución sobre F0.
- Impacto: **+**. R2 solo pedía aclararlo; hacerlo es claramente mejor que admitir que no se hizo. Si sale contaminación relevante (más del ~1–2 % del test), el test limpio pasa a ser la cifra principal. Habría que actualizar las tablas, pero sin reentrenar.

**F2 — Nuevo protocolo de particiones.** Puesta en marcha **3–4 h**; ejecución de minutos. Dos variantes; la decisión es tuya:

| Variante | Validación | Entrenamiento | Ventaja | Inconveniente |
|---|---|---|---|---|
| V-A (tu estrategia 3) | FASDD val oficial (40k) | DFire train + FASDD train (~77k) | Splits oficiales de FASDD, muy fácil de defender | −34 % de datos de entrenamiento. Confunde "corregir el protocolo" con "cambiar el dataset". La validación no incluye DFire |
| **V-B (recomendada)** | ~10 % estratificado (por dataset y combinación de etiquetas) del pool de entrenamiento actual, **por grupos**: los clústeres de duplicados de F1 caen enteros en un solo lado | El 90 % restante (~106k) | El entrenamiento es casi idéntico al del paper, así que **los nuevos runs confirman o refutan los resultados originales**. La validación representa los tres orígenes | No usa la partición oficial de val de FASDD (hay que explicarlo en una frase) |

En ambas variantes el **test no se toca** (salvo la limpieza de F1). Las listas de ficheros de cada partición se versionan en el repo, lo que mejora mucho la reproducibilidad y responde de paso al Data Availability Statement.

**F3 — Reentrenamiento con protocolo riguroso.**
- Selección y scheduler solo sobre validación; test evaluado una única vez al final.
- Semillas fijas y determinismo de cuDNN; registro de entorno, commit y configuración en cada run.
- **No se repite todo**:
  - *Núcleo* (3 semillas cada uno): Nano FP32, Nano QAT, BED-FPGA QAT y MobileNetV2 de referencia. La referencia hace falta porque la cifra central del paper ("−2.33 pp respecto a FP32 de referencia", "< 2.5 pp") depende de ella. Son 12 runs ≈ **144 GPU-h ≈ 6 días**. Si caben dos entrenamientos simultáneos en la GPU (modelos de ~70k parámetros; el cuello de botella probable es la CPU por Albumentations), ≈ 4 días (HYPOTHESIS: hay que medirlo en la puesta en marcha).
  - *Ampliación opcional* (1 semilla cada uno): BED Original y Simplified, Nano ReLU6, 4-bit input, 160 y 112, MobileNetV3 y ShuffleNetV2. Son ≈ 8–10 runs ≈ **+4–5 días**. Permite poner el nuevo protocolo en todas las filas de las Tablas 2, 3, 5 y 10.
- Puesta en marcha: **20–30 h**. Incluye:
  - pasar el notebook a un script ejecutable en segundo plano, sin reescribir la lógica (papermill o extracción mínima);
  - configuración por fichero, en lugar de editar `config.py`, que además hace `mkdir` al importarse;
  - una cola de jobs que lance el siguiente experimento al terminar el anterior, con reanudación si algo falla;
  - pruebas cortas (1–2 épocas) que comprueben que el modelo y el número de parámetros coinciden con los históricos.
- Seguimiento durante la ejecución: ≈ **1 h/día**.
- Análisis y redacción (tablas media ± desviación, texto de metodología, respuesta a R3-1, R2-M2 y R2-M3): **8–12 h**.
- Impacto: **++**, siempre que se reporte con honestidad aunque los números bajen algo. Si la media del Nano queda por debajo del valor publicado, hay que revisar las afirmaciones ("< 2.5 pp", "95.32 %"), y aun así la imagen es mucho mejor que si lo detecta un revisor.

**F4 — Coherencia con el hardware.** Opcional; depende de D2 (disponibilidad de la placa).
- **Los diseños FPGA desplegados se mantienen.** Recursos, potencia y throughput dependen del folding y de la arquitectura, no del valor de los pesos. Los nuevos modelos QAT se validan en simulación funcional QONNX/FINN, que es bit-exacta respecto al acelerador, para mostrar que la caída software→FPGA (~0.13–0.16 pp) se mantiene.
- Puesta en marcha **4–8 h**; ejecución **2–6 h**.
- Bitstream nuevo con los pesos reentrenados y el mismo folding: +3 h de puesta en marcha y 3–6 h de síntesis por diseño. Medida en placa: requiere el PYNQ-Z1.
- Impacto: **+**. Evita la objeción de que el hardware usa un modelo distinto del que ahora se reporta.

### 5. Resumen de esfuerzo de la estrategia recomendada (F0–F3, más F4 sin bitstream)

| | Puesta en marcha (humano) | Ejecución (máquina, en segundo plano) |
|---|---|---|
| F0 diagnóstico | 4–6 h | 2–3 h |
| F1 duplicados | 10–14 h | 1–3 h (+1 h re-evaluación) |
| F2 particiones | 3–4 h | minutos |
| F3 reentrenamiento (núcleo) | 20–30 h, más ~1 h/día de seguimiento | ≈ 6 días (≈ 4 si caben 2 en paralelo) |
| F3 ampliación (opcional) | +2 h | +4–5 días |
| F4 simulación funcional | 4–8 h | 2–6 h |
| Análisis y redacción | 8–12 h | — |
| **Total** | **≈ 50–75 h** | **≈ 6–11 días de reloj** |

Orden propuesto: F0 → F1 → F2 → lanzar F3 → mientras corre F3, avanzar con el resto de la revisión (Tabla 9, potencia, related work). Cada fase sirve para decidir si la siguiente merece la pena. Por ejemplo, si F0 y F1 muestran sesgos despreciables, la ampliación de F3 se puede omitir.

### 6. Lo que necesito que decidas

1. ¿V-A (validación oficial de FASDD) o V-B (validación separada por grupos del pool actual)? Yo recomiendo V-B.
2. Presentación en el paper:
   - (a) sustituir las cifras software por las del nuevo protocolo (media ± desviación) y mantener las cifras FPGA de los diseños desplegados; o
   - (b) mantener las originales y añadir una tabla de "sensibilidad al protocolo".
   - Creo que (a) es más limpio ante R3, pero exige reescribir más tablas.
3. ¿Está libre la GPU del servidor durante ~1–2 semanas? ¿Puedo lanzar dos entrenamientos en paralelo?
4. ¿Empiezo por F0 (≈ medio día y sin riesgo), para tener datos reales antes de comprometer el resto?

### 7. Semillas: estado real y criticidad (añadido 2026-10-03, tras revisar el código)

**Estado real de la aleatoriedad** (VERIFIED en el código; el repo activo es idéntico al histórico):

| Fuente de aleatoriedad | ¿Controlada? | Detalle |
|---|---|---|
| Inicialización de pesos (PyTorch) | **No** | No hay `torch.manual_seed` en ningún sitio |
| Orden de batches (`DataLoader(shuffle=True)`, 8 workers) | **No** | No hay `generator` ni `worker_init_fn` |
| Augmentation (Albumentations: flip, blur, CLAHE, shift/scale/rotate…) | **No** | No hay semilla de `random` ni de `numpy` en entrenamiento |
| cuDNN | **No** | No se fija `deterministic` ni `benchmark` |
| Subconjuntos (`ds_len`: runs de depuración de 128 imágenes y subconjunto de 2048 de AIMET) | **Sí** | `random.seed(123)` en `dataset_*.py`, **solo** cuando `ds_len` no es `None`. Con el dataset completo no se ejecuta |
| AIMET spatial SVD | Determinista | Una SVD es determinista para unos pesos dados; la búsqueda greedy de ratios también lo es para unos pesos y datos fijos |
| AIMET channel pruning | **Probablemente no** | La reconstrucción por mínimos cuadrados con `num_reconstruction_samples=500` muestrea posiciones de los mapas de activación (HYPOTHESIS: sin semilla dentro de AIMET) |
| Fine-tuning tras SVD y pruning | **No** | Usa el mismo bucle de entrenamiento sin semillas |

Así que tu recuerdo es correcto: con el dataset completo no se fijó ninguna semilla, y en AIMET solo es determinista la parte de SVD. **Consecuencia importante: los runs históricos no se pueden reproducir bit a bit, se haga lo que se haga.** La respuesta a R2-M3 no puede ser "reproducimos el resultado", sino "**cuantificamos la variabilidad y comprobamos que las conclusiones se mantienen**".

**Hallazgo nuevo que agrava R3-1** (VERIFIED en `aimet_spatial_svd_then_pruning_fasdd.ipynb`):
- La búsqueda greedy de AIMET, que decide cuánto se comprime cada capa de BED, evalúa el F1 sobre `aimet_val_loader = get_val_loader(val_ds_len=2048)`, es decir, **2048 imágenes del test**.
- La reconstrucción del channel pruning también usa ese loader.
- Por tanto, el test influyó también en la elección de la arquitectura comprimida de BED, no solo en el checkpoint. Esto se debe declarar.
- Atenuante: la arquitectura BED FPGA final se ajustó después a mano (canales múltiplos de 4/8, eliminación del padding, 230×230), así que la salida de AIMET fue una guía, no la arquitectura final.

**Otro hallazgo menor** (VERIFIED, `get_train_loader()`):
- La augmentation real incluye HorizontalFlip, CLAHE, RGBShift y escalado, que el paper no menciona.
- El Blur 17×17 se aplica **a resolución completa** (imágenes de hasta 3072×2048) antes del `Resize`.
- Hay un `try/except` que, si falla la augmentation, sustituye silenciosamente las transformaciones por otras.

Hay que corregir el texto de §II-A. Lo anoto como A-7 y A-8 en la matriz.

**Criticidad de la objeción de semillas (R2-M3):**

| Aspecto | Valoración |
|---|---|
| Quién la plantea | Solo R2, que es el revisor favorable ("suitable for publication after appropriate revision"). R3 no menciona las semillas |
| Qué pide | Un compromiso explícito: *no* repetir todo; repetir baseline, Nano y las configuraciones donde diferencias < ~0.2 pp sostienen una conclusión, con varias semillas y media ± desviación |
| Criticidad | **Media-alta** (P1). Es fácil de satisfacer porque el propio revisor define el alcance. No atenderla con un revisor favorable que da la solución sería un error evitable |
| Conclusiones afectadas | Tabla 3 (BED): −0.08 (simplificación), −0.03 (SVD), −0.06 (pruning), −0.16 (adaptación FPGA). Tabla 5: ECA −0.10. Con una desviación típica plausible de 0.1–0.3 pp (INFERENCE, a medir), **estas diferencias probablemente no son significativas**. Las caídas de cuantización (≈1.1–1.3 pp), ReLU6 (−1.26) y 4-bit input (−1.01) probablemente sí lo son |
| No afectadas | La caída software→FPGA (−0.13/−0.16 pp, Tabla 7): mismos pesos, es determinista y no depende de semillas. Recursos, throughput y potencia: dependen de la arquitectura y del folding, no de la semilla |

**Lo que propongo para las semillas:**
1. **No hace falta tener semillas en cada etapa.** Basta con medir σ para cada familia (BED y Nano) en FP32 y en QAT, y reformular el texto: diferencias menores que σ se presentan como "comparables" y no como mejoras o pérdidas.
   - Impacto **+**: hace el paper más honesto y R2 lo valorará. El coste es que algunas frases de la trayectoria BED pierden fuerza, pero esa trayectoria es narrativa y no la conclusión principal.
2. **AIMET: no repetir la compresión con semillas** (nadie lo pide y la parte SVD es determinista). Sí propongo un **chequeo barato**: repetir solo la búsqueda greedy de ratios evaluando sobre la nueva validación (no sobre test) y comparar los ratios por capa con los históricos.
   - Si salen iguales o muy parecidos, la fuga del test en AIMET queda neutralizada con evidencia.
   - Puesta en marcha **4–6 h** (entorno `pytorch_aimet`; he comprobado que torch 2.1.2+cu121 ve la GPU). Ejecución **2–4 h**.
   - Impacto **+**. Sin el chequeo, la fuga hay que declararla como limitación: **−**.
3. **Las semillas y el nuevo protocolo se resuelven en la misma campaña.** Cada run nuevo (validación separada y semilla fija s ∈ {0, 1, 2}) responde a la vez a R3-1 y R2-M3. No son dos campañas.

### 8. Estrategia inicial recomendada (revisada con lo anterior)

**Comprobaciones de viabilidad hechas hoy:**
- Los entornos funcionan: driver 555 / CUDA 12.5, torch cu121 en `pytorch_brevitas`, `pytorch_23` y `pytorch_aimet`, con `cuda.is_available() = True` y la RTX 4070 Ti visible. El riesgo de CUDA que menciona el apartado *Legacy* no se materializa (VERIFIED).
- Servidor: 20 núcleos, 125 GB de RAM y GPU de 12 GB.
- **El cuello de botella probable no es la GPU sino la CPU** (HYPOTHESIS, a medir en la puesta en marcha):
  - los modelos son de ~70k parámetros;
  - cada imagen se decodifica a resolución completa (1–6 MP) y se aumenta antes del `Resize`;
  - no se puede acelerar redimensionando antes, porque cambiaría el efecto del blur y del resto de transformaciones, y dejaríamos de estar confirmando los experimentos originales.
- Por tanto, la "GPU exclusiva" solo acelera si **también la CPU está libre**. En esos periodos se podrían lanzar 2 runs en paralelo (12 GB de VRAM sobran). Lo verificaré midiendo la utilización de la GPU durante una época de prueba.

**Campaña única C1**, en el orden de la §4:

| Bloque | Contenido | Responde a | Puesta en marcha | Ejecución |
|---|---|---|---|---|
| F0 | Diagnóstico sin reentrenar: `best_mean_F1` vs `last_*.pt` | R3-1 (evidencia preliminar) | 4–6 h | 2–3 h |
| F1 | Duplicados train↔test → test deduplicado; re-evaluar los checkpoints existentes | R2-M2 | 10–14 h | 2–4 h |
| F2 | Validación separada por grupos (V-B), listas de ficheros versionadas | R3-1, A-3 | 3–4 h | minutos |
| F-AIMET | Búsqueda greedy de ratios usando la validación; comparar con los ratios históricos | R3-1 (fuga en AIMET), A-8 | 4–6 h | 2–4 h |
| F3 Tier 1 | 3 semillas × {Nano FP32, Nano QAT, BED-FPGA QAT, MobileNetV2 ref} = 12 runs | R3-1, R2-M3 | 20–30 h (incl. cola reanudable con checkpoint por época, para aprovechar las ventanas de GPU exclusiva: +2–3 h) | ≈ 6 días secuencial / ≈ 3–4 días con 2 en paralelo |
| F3 Tier 2 | 3 semillas × {BED Original FP32, BED Simplified FP32} = 6 runs (valida o matiza las diferencias pequeñas de la Tabla 3) | R2-M3 | +1 h | ≈ +3 días / ≈ +1.5–2 días |
| F3 Tier 3 (opcional) | 1 semilla con el nuevo protocolo para el resto de filas (ReLU6, 4b-input, 160, 112, ECA, MobileNetV3, ShuffleNetV2, MobileViT) ≈ 8–10 runs | Coherencia de todas las tablas | +1 h | ≈ +4–5 días / ≈ +2–3 días |
| F4 | Simulación funcional QONNX/FINN de los nuevos modelos QAT | Coherencia con el hardware | 4–8 h | 2–6 h |
| Redacción | Tablas media ± σ, reformulación de las diferencias pequeñas, respuesta a R3-1, R2-M2 y R2-M3 | — | 10–14 h | — |

**Totales:**
- **Tier 1 + Tier 2** (recomendado): puesta en marcha **≈ 60–85 h** de trabajo humano, más ~1 h/día de seguimiento. Ejecución **≈ 9 días** de GPU secuencial, o **≈ 5–6 días** con GPU y CPU exclusivas y 2 runs en paralelo.
- **Con Tier 3:** +4–5 días de ejecución (o +2–3 en paralelo), y casi nada de trabajo humano adicional.

**Impacto reputacional del conjunto: ++.** El mensaje a los revisores sería:
- "Reconocemos que el conjunto descrito como held-out era el test."
- "Rehicimos los experimentos clave con un protocolo train/val/test por grupos, semillas fijas y test deduplicado."
- "Las conclusiones se mantienen (o se matizan) con media ± σ."
- "Los diseños FPGA desplegados no cambian."

Esto responde de una vez a la objeción más grave de R3 y a la petición explícita de R2. Además, el paper queda reproducible con las listas de particiones, las semillas y el entorno publicados.

**Siguiente paso propuesto:** empezar con F0 y la medida de la utilización de CPU y GPU en una época de prueba (≈ 1 día de trabajo, sin riesgo, en una copia de trabajo dentro del repo activo con salidas en `results/review_2026/`). Así sabremos cuánto sesgo hubo y cuánto dura realmente un run, antes de comprometer la campaña completa.

---

## Plan detallado: detección de duplicados, impacto y exclusión en test (2026-10-04)

Responde a R2-M2. También prepara las particiones por grupos de F2 (R3-1). Se implementa en `code_review/train/02_audit/f1_duplicates/`. Reglas: `~/uav` es de solo lectura, los datasets no se modifican nunca y todo filtrado se hace con **listas de ficheros versionadas**.

### P0. Datos de partida (VERIFIED, 2026-10-04)

| Origen | Train (pool del paper) | Test | Disco | Observaciones |
|---|---|---|---|---|
| DFire | 17,221 | 4,306 | 3.0 GB | Prefijos: `WEB` (9443 / 2364), `AoF` (6723 / 1661), `PublicDataset` (1055 / 281). La numeración consecutiva de `AoF` sugiere **frames de vídeo** (HYPOTHESIS), el caso más probable de casi-duplicados entre train y test |
| FASDD UAV | 20,916 (= train 12,550 + val 8,364) | 4,181 | 15 GB | Prefijos por clase (`bothFireAndSmoke_UAV…`). Imágenes de dron y de vigilancia de alta resolución |
| FASDD CV | 79,430 (= train 47,660 + val 31,769) | 15,884 | 12 GB | Imágenes web y sintéticas, tal como describe el propio paper |
| **Total** | **117,567** | **24,371** | ≈ 30 GB | — |

- **Errata detectada en la Tabla 1 (VERIFIED):** el test de FASDD CV tiene **3358** imágenes "Both", no 3558. Con 3558 la fila suma 16,084 en lugar de 15,884, y la fila Total (Both 5556 = 895 + 1303 + 3358) solo cuadra con 3358. Se anota en `paper_comments.md`.
- **Ventaja de partida:** para los dos modelos Nano ya existen las predicciones por imagen sobre las 24,371 imágenes de test (`code_review/train/01_replicas/mobilenet_paper/results/predictions__*.csv`). Para ellos, el impacto de los duplicados se calcula sin volver a ejecutar inferencia.

### P1. Qué es un "duplicado": niveles y alcance

Se definen cuatro niveles, de más a menos estricto. Se informa de cada uno por separado para que el revisor pueda juzgar:

| Nivel | Definición | Ejemplos | Detector principal |
|---|---|---|---|
| **L0 Exacto** | Mismo fichero byte a byte | La misma imagen descargada dos veces | md5 / sha256 |
| **L1 Mismo contenido** | Mismos píxeles tras decodificar, o tras el `Resize` a 224×224 que ve el modelo | Distinta compresión JPEG o metadatos; distinta resolución original | Hash de los píxeles a 224×224 |
| **L2 Casi-duplicado** | La misma foto editada | Recompresión fuerte, recorte pequeño, marca de agua, cambio de color o brillo, volteo | Hash perceptual (pHash/dHash, también sobre la imagen volteada) + descriptor de copy detection |
| **L3 Mismo evento / casi la misma escena** | Distinta foto o frame de la misma escena con cambios pequeños | Frames consecutivos de un vídeo (DFire `AoF`), ráfagas de dron | Embedding semántico + SSIM, con umbral calibrado a mano |

Fuera de alcance, por no ser duplicado: escenas *parecidas* de eventos distintos (otro incendio, otro bosque).

Comparaciones, por orden de importancia:
1. **Test ↔ pool de entrenamiento.** Es la que determina la contaminación del test.
2. **Entre datasets** (DFire ↔ FASDD UAV ↔ FASDD CV), en las cuatro combinaciones de split.
3. **Dentro del pool de entrenamiento.** Sirve para que en F2 la validación se forme por grupos.
4. **Dentro del test.** No es fuga, pero sobrepondera algunas escenas y se informa como estadística.

### P2. Pipeline de detección (scripts en `code_review/train/02_audit/f1_duplicates/`)

**S0 — Inventario (manifest).**
- Se construye la lista exacta de imágenes que usan los dataloaders del paper, reutilizando las clases `DFireDataset` y `FASDDDataset` de la réplica. Así se aplica el mismo filtrado ("Removed wrong images") y el mismo orden.
- Por imagen: id, ruta relativa, origen, split original (DFire train/test; FASDD train/val/test), split del paper (pool / test), etiquetas smoke/fire, resolución, tamaño, md5 y posición en el loader de test (para cruzar con los CSV de predicciones).
- Salida: `artifacts/manifest.parquet` (no versionado) y un resumen versionado en `results/`. Comprobación: los recuentos coinciden con la Tabla 1 corregida.
- Puesta en marcha 2–3 h; ejecución 20–40 min (lectura de ~30 GB).

**S1 — L0 y L1.**
- Se agrupa por md5 (L0).
- Se decodifica cada imagen, se aplica `cv2.resize` a 224×224 como en `get_val_loader()` y se calcula el hash del array resultante (L1, igualdad exacta).
- Ejecución 30–60 min (decodificación de 142k imágenes a resolución completa con 16 procesos).

**S2 — Hashes perceptuales (L2 "barato").**
- pHash y dHash de 64 bits sobre la imagen original y sobre la volteada horizontalmente, porque el entrenamiento usa `HorizontalFlip`.
- Candidatos con distancia de Hamming ≤ 12, buscados con un índice multi-índice o un BK-tree.
- Sin GPU; se puede ejecutar en la misma pasada que S1.

**S3 — Embeddings (L2 robusto y L3).**
- **Descriptor de copy detection: SSCD** (Pizzi et al., CVPR 2022, entrenado específicamente para detectar copias editadas). Cubre L2 con recortes y ediciones que el pHash no detecta.
- **Descriptor semántico: DINOv2 ViT-S/14.** Cubre L3 (frames consecutivos, misma escena).
- Ambos sobre imágenes a 224 normalizadas en L2; búsqueda exacta de los k = 10 vecinos por producto interno en GPU.
  - test ↔ pool: 24k × 118k;
  - pool ↔ pool: por bloques, para la agrupación de F2.
- Ejecución: 1–2 h de GPU, limitada otra vez por la decodificación.
- **Requiere decisión (D-F1a):** un entorno conda nuevo, `dedup_audit` (torch, faiss, imagehash, scikit-image), y descargar de internet los pesos de SSCD y DINOv2. No se toca ningún entorno existente.

**S4 — Verificación de candidatos.**
- A cada pareja candidata de S2/S3 se le calculan SSIM y MSE a 224, la similitud de cada descriptor y la relación de las etiquetas (iguales o distintas).

**S5 — Calibración de umbrales con revisión humana (punto de supervisión).**
- Se genera una página HTML de pares lado a lado: una muestra estratificada por bin de similitud, unos 20 pares por bin en ~10 bins, por descriptor, en total 200–300 pares.
- Etiquetas: *duplicado L1/L2*, *misma escena L3*, *distinto*.
- Con ellas se estima la precisión por bin y se fijan los umbrales:
  - **L2:** alta precisión (≥ 95 % de pares realmente duplicados);
  - **L3:** se informa de la curva completa y se fija un umbral "conservador" (alta cobertura), más otro "estricto".
- Se registra un ejemplo de cada caso límite.
- **Supervisión humana: 2–3 h.**

**S6 — Agrupación.**
- Se construye el grafo de imágenes conectadas por aristas L0–L2 (y, por separado, L0–L3) y se obtienen los clústeres de duplicados con union-find.
- Por clúster: tamaño, orígenes, splits y etiquetas.
- **Clústeres con etiquetas contradictorias** (la misma imagen con etiquetas distintas): se informa del ruido de etiquetado. Es un hallazgo útil en sí mismo y se reporta por separado.

**S7 — Informe de contaminación** (`results/contamination_report.md` + JSON):
- % del test con al menos un duplicado en el pool, por nivel (L0, L1, L2, L3-estricto, L3-conservador), por origen del test, por combinación de etiquetas y por par de orígenes (p. ej. test DFire ↔ train FASDD CV);
- duplicados entre datasets distintos (DFire ↔ FASDD);
- duplicados dentro del test;
- una figura con ejemplos.

### P3. Evaluación del impacto (sin reentrenar)

**Reglas de decisión fijadas antes de ver los resultados**, para que el análisis no se ajuste a posteriori:
- **R-a. Impacto despreciable:** contaminación (L0–L2) < 1 % del test y |ΔF1-Macro| ≤ 0.2 pp en todos los modelos del paper. Las tablas se mantienen y se añaden una frase y una tabla de robustez con el test limpio.
- **R-b. Impacto relevante:** contaminación ≥ 1 % o |ΔF1-Macro| > 0.2 pp en algún modelo. **Todas las tablas pasan al test limpio** y el test original se da solo como referencia.
- **R-c.** Si en el test limpio cambia el orden de algún par de modelos o configuraciones que el paper usa para una conclusión, esa conclusión se reformula.

Pasos:
1. **I1 — Re-evaluación en tres subconjuntos:**
   - (a) test completo (24,371);
   - (b) **test limpio** = test sin las imágenes contaminadas, para cada nivel;
   - (c) solo las imágenes contaminadas.

   Métricas: P/R/F1 por clase y F1-Macro.
   - Nano FP32 y Nano QAT: directamente desde los CSV de predicciones (minutos).
   - Resto de modelos de las Tablas 2, 3, 5 y 10: inferencia sobre el test completo una sola vez por checkpoint (≈ 4–8 min cada uno; unos 15 checkpoints ≈ 1.5–2 h), guardando predicciones por imagen. Antes hay que replicar cada modelo como se hizo con el Nano.
2. **I2 — Control por composición.** Quitar imágenes cambia por sí solo el reparto de clases y la dificultad del test. Por eso se compara el Δ real con el Δ obtenido al quitar 1000 subconjuntos **aleatorios del mismo tamaño y con la misma distribución de origen y etiquetas**. El efecto de la contaminación es la diferencia con esa distribución nula; se da el p-valor empírico.
3. **I3 — Señal de memorización.**
   - Se compara la tasa de error en imágenes contaminadas y en no contaminadas, dentro de los mismos estratos de origen y etiqueta (test de permutación o de Fisher estratificado).
   - Si el modelo acierta claramente más en las contaminadas, hay evidencia de que la fuga infla las cifras. Si no, es una evidencia fuerte de que no hay impacto.
   - También se compara la confianza media (probabilidad sigmoide) en ambos grupos.
4. **I4 — Intervalos de confianza.** Bootstrap pareado (2000 réplicas) del F1-Macro en el test completo y en el limpio, y de la diferencia entre modelos (p. ej. FP32 − QAT) en ambos. Esto ayuda además con R2-M3: muestra qué diferencias del paper superan el ruido de muestreo del test.
5. **I5 — Hardware.**
   - La columna FPGA de la Tabla 7 (94.38 / 95.32) no se puede recalcular sobre el test limpio mientras no se sepa cómo se obtuvo (R3-2, UNKNOWN).
   - Si se recuperan las predicciones por imagen de la FPGA, o se reproduce con simulación funcional QONNX/FINN, se aplica el mismo análisis.
   - Si no, se argumenta con la concordancia entre software y FPGA medida sobre el test completo.

### P4. Estrategia de manejo de duplicados: que no se usen en la evaluación

1. **E1 — Test limpio canónico.**
   - Se versionan `code_review/dataset_review_split/test_clean.txt` (rutas relativas) y `test_contaminated.csv` (ruta, nivel, motivo, imagen del pool con la que coincide y similitud).
   - Criterio por defecto (propuesta): quitar del test toda imagen de un clúster L0–L2 que incluya alguna imagen del pool, más las L3 por encima del **umbral estricto** calibrado en S5.
   - Las L3 entre el umbral estricto y el conservador se informan como análisis de sensibilidad.
2. **E2 — Filtrado en el dataloader.**
   - Copia del `dataloaders.py` de la réplica (copy-on-write, con el diff documentado) que acepta una lista de ficheros permitidos y comprueba con `assert` los recuentos esperados.
   - El dataset en disco no se toca.
   - Se elimina también `drop_last` en evaluación (A-9).
3. **E3 — Modelos históricos (los del paper).** Se evalúan sobre el test limpio sin reentrenar (P3). Es la única opción que conserva los pesos y los diseños FPGA desplegados.
4. **E4 — Modelos nuevos (F3, protocolo riguroso).**
   - **Se limpia también el entrenamiento:** de la lista de entrenamiento se quitan los miembros del pool de los clústeres que tocan el test.
   - La validación de F2 se forma **por clústeres** (cada clúster cae entero en train o en val).
   - Así, los modelos nuevos se pueden evaluar sobre el test completo y sobre el limpio sin ninguna fuga posible, y la comparación con los históricos es directa.
5. **E5 — Duplicados dentro del test.** No se eliminan del test principal. Se informa de cuántos hay y, como análisis secundario, se da el F1 con un representante por clúster.
6. **E6 — Paper y respuesta.**
   - Tabla 1 corregida (errata 3558 → 3358) con las columnas de contaminación.
   - Un párrafo en §II-A sobre el método de detección y el resultado.
   - Cifras en el test limpio según R-a / R-b.
   - Respuesta a R2-M2 y a R3-1 con los números.
   - Las listas `test_clean.txt` y de particiones se publican en el material de reproducción, lo que también mejora el Data Availability Statement.

### P5. Esfuerzo, cómputo y supervisión

| Paso | Puesta en marcha (Claude) | Ejecución (máquina) | Supervisión humana |
|---|---|---|---|
| Entorno `dedup_audit` + descarga de pesos SSCD/DINOv2 | 1–2 h | 15 min | **Sí: aprobar (D-F1a)** |
| S0 inventario | 2–3 h | 20–40 min | No |
| S1 + S2 hashes | 2–3 h | 30–60 min | No |
| S3 embeddings + kNN | 3–4 h | 1–2 h GPU | No |
| S4 verificación | 1–2 h | 15–30 min | No |
| S5 calibración (página de revisión) | 2 h | — | **Sí: 2–3 h de revisión de pares** |
| S6 + S7 clústeres e informe | 2–3 h | minutos | Revisar el informe (30 min) |
| P3 Nano (desde los CSV), I1–I4 | 3–4 h | minutos | **Sí: aplicar las reglas R-a/R-b** |
| P3 resto de modelos (replicar e inferir unos 15 checkpoints) | 6–10 h (depende de la procedencia de BED y de las referencias) | 1.5–2 h | Confirmar los runs de cada tabla |
| P4 E1–E2 (listas y dataloader filtrado) | 2–3 h | — | No |
| **Total** | **≈ 25–35 h** | **≈ 4–7 h** | **≈ 4–6 h** |

Orden: S0 → S1/S2 → S3 → S4 → **S5 (revisión humana)** → S6/S7 → P3 (Nano primero; es inmediato) → decisión R-a/R-b → P4 → resto de modelos.

Tras S1/S2 ya se tienen L0–L2 baratos. Si la contaminación exacta ya fuera alta, se informaría antes de seguir.

### P6. Riesgos y limitaciones

- **Recall imperfecto.** Ningún detector encuentra todos los casi-duplicados. Por eso se combinan tres familias de detectores y se informa de la sensibilidad a los umbrales. En la respuesta se dirá "hasta el nivel de detección descrito", no "sin duplicados".
- **L3 subjetivo.** La frontera entre "misma escena" y "escena parecida" depende del criterio. Se resuelve con la revisión humana documentada (S5) y reportando dos umbrales.
- **Contaminación propia de los datasets.** Si FASDD o DFire ya traen duplicados entre sus propios splits oficiales, no es un error nuestro, pero afecta igual a las cifras. Se informa por origen.
- **Ruido de etiquetas.** Los clústeres con etiquetas contradictorias pueden revelar errores de anotación en los datasets originales. Se informa sin corregir etiquetas, porque corregirlas cambiaría el benchmark.
- **Pesos externos.** SSCD y DINOv2 requieren descarga. Si no hay acceso a internet desde el servidor, se usarían pHash + SSIM + un ResNet de torchvision ya en caché, con menor recall en L2/L3.

### P7. Decisiones pendientes

- **D-F1a:** ¿crear el entorno `dedup_audit` y descargar los pesos de SSCD y DINOv2?
- **D-F1b:** ¿aceptas las reglas de decisión R-a/R-b/R-c (umbrales de 1 % de contaminación y 0.2 pp) antes de ver los datos?
- **D-F1c:** criterio por defecto del test limpio: L0–L2 + L3 estricto (propuesto), o solo L0–L2.
- **D-F1d:** ¿se limpia también el entrenamiento en F3 (E4)? Lo recomiendo.

---

## Resultado de F0 (2026-10-04) — sesgo de selección

Detalle: `code_review/train/02_audit/f0_selection_bias/README.md`.

- **Los logs reflejan fielmente los checkpoints (VERIFIED).** Los checkpoints `best_mean_F1`, `best_loss` y `last` de los dos Nano reproducen exactamente las métricas por época del log. Por eso el análisis basado en logs es válido para todos los runs del paper.
- **Los 18 runs del paper se recuperan desde sus logs.** Hay procedencia nueva para la Tabla 2 (MobileNetV2, ShuffleNetV2, MobileViTV3) y para MobilenetV3 Mini. La fila MobileNetV3 de la Tabla 2 mezcla dos modelos (A-11).
- **Efecto de elegir el checkpoint con el test** (frente a la media de las 10 últimas épocas):
  - +0.03 a +0.15 pp en las referencias con transfer learning;
  - +0.18 a +0.36 pp en los modelos FP32 entrenados desde cero;
  - +0.33 a +0.71 pp en los modelos QAT.
- **Consecuencia:** ninguna comparación del paper cambia de signo, pero las penalizaciones de cuantización, ReLU6 y 4-bit input son algo mayores. **La afirmación "< 2.5 pp" frente a la referencia deja de cumplirse** con aproximaciones sin selección (2.57–2.67 pp; A-13, INFERENCE). Esto refuerza la necesidad de F3.
- **Coste de F3, revisado con datos medidos:**
  - hoy un entrenamiento rinde unas 153 img/s, unas 21 h por 100 épocas, aproximadamente el doble de lo que tardaron en 2024;
  - 2 procesos en paralelo casi duplican el rendimiento total;
  - construir el dataset añade unos 45 min fijos por run.
  - **Tier 1 (12 runs): unos 9.5 días en secuencial, unos 5 días con 2 procesos en paralelo.**
