# Discusión entre Claude y Yo acerca de las decisiones/estrategias para superar la revisión

## Decisiones a lo largo de la investigación para comprender los motivos

Este proyecto no comenzó como un trabajo de investigación, sino que tuvo una orientación más cercana a la elaboración de un producto de ingeniería. Por tanto, muchas decisiones no se tomaron siguiendo una metodología científica, sino con el objetivo de construir un producto.

### Dataset
Al comienzo de este trabajo solo estaba disponible el dataset DFire. Posteriormente, apareció FASDD y se incorporó. La realidad es que ambos datasets incorporan imágenes de internet y no hay traza de que imágenes que estén en entrenamiento de uno no estén en validación o test de otro, lo que falsearía los resultados, al utilizarse imágenes con las que se ha entrenado el modelo para verificarlo.

No se hizo un conjunto separado de validación porque DFire no cuenta con ese conjunto, sino que solo tiene train y test.

#### Propuesta de estrategia
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

#### Claude comments

*(2026-10-03. Las estimaciones de horas son INFERENCE basadas en la estructura del código y en tiempos históricos. Los tiempos de GPU salen de las fechas de los ficheros de los runs históricos: ≈12 h Nano FP32 (100 épocas), ≈10 h Nano QAT, ≈14 h BED-FPGA QAT (150 épocas), en la RTX 4070 Ti compartida. Ver `reviewers/response_matrix.md`, filas R3-1, R2-M2, R2-M3, A-3.)*

##### 1. Separar los dos problemas: tienen soluciones distintas

Las tres estrategias mezclan dos problemas independientes:

| | Problema | Revisor | Gravedad | Evidencia |
|---|---|---|---|---|
| **P1** | **El conjunto de test se usó para seleccionar el modelo.** ReduceLROnPlateau monitoriza la loss de test y el checkpoint elegido es el de mejor F1 en test | R3-1 (major) | **Crítico**: R3 lo cita para juzgar el paper como "technically sound: *partially*" | VERIFIED (`get_val_loader()` usa los splits de test en `train/mobilenet` y `train/bed`) |
| **P2** | Posibles duplicados o casi-duplicados entre train y test (internet, DFire ↔ FASDD) | R2-M2 | Moderado. R2 dice textualmente que el análisis *no es esencial*: pide aclarar si se hizo y, si no, reconocerlo | UNKNOWN (no consta ningún análisis) |

Hay además un tercer hecho relacionado: **el `val.txt` oficial de FASDD está fusionado en el entrenamiento** (VERIFIED: UAV 12550 + 8364 ≈ 20916 y CV 47660 + 31769 ≈ 79430 en la Tabla 1). Por tanto la frase del paper "the original training and test assignments … are preserved" es inexacta, y además FASDD *sí* tenía un conjunto de validación que no se usó como tal.

**Consecuencia clave: los duplicados (P2) se arreglan limpiando el test, no reentrenando.** Si hay imágenes de test con un duplicado en train, basta con quitarlas del test (o reportar test original y test limpio) y **re-evaluar los checkpoints existentes**. No hace falta reentrenar nada por P2. Lo que sí exige reentrenar es P1.

##### 2. Respuestas a tus preguntas sobre la estrategia 1

- **¿Habría que repetir muchos experimentos si hay duplicados?** No por los duplicados en sí, como acabo de explicar: es re-evaluación. El reentrenamiento lo exige P1.
- **¿Es defendible no tener validación porque DFire no la tiene?** **No**, mientras el test se use para el scheduler y para elegir el checkpoint. Es práctica estándar separar un conjunto de validación del de entrenamiento cuando el dataset no lo trae, y los tres revisores lo saben. Solo sería defendible no tener validación con un protocolo sin ninguna selección: calendario fijo, sin scheduler dependiente de métricas y reportando la última época. No fue el caso.
- Ahora mismo el paper dice "held-out evaluation loss". Un revisor lo lee como un conjunto de validación separado y no lo es. **En la respuesta hay que decirlo claramente**: intentar maquillarlo es el mayor riesgo reputacional de todo este punto.

##### 3. Valoración de las estrategias propuestas

Escala de impacto reputacional: ++ muy positivo / + positivo / 0 neutro / − negativo / −− muy negativo (riesgo alto de rechazo, o de dar imagen de poca rigurosidad).

| Estrategia | ¿Resuelve P1? | ¿Resuelve P2? | Puesta en marcha | Ejecución (GPU) | Impacto reputacional |
|---|---|---|---|---|---|
| 0. Solo reconocerlo como limitación | No | No | 2–3 h (texto) | — | **−−**: se admite un sesgo de selección sin corregirlo; R3 casi seguro mantiene su objeción, y solo hay un reenvío |
| 1. Solo análisis de duplicados | No | Sí | 10–14 h | 1–3 h | **−**: contenta a R2, pero deja abierto lo más grave (R3-1) |
| 2. Quitar DFire y usar solo FASDD (train/val/test) | Sí | Parcialmente | 30–40 h + reescritura casi total de resultados | Rehacer prácticamente todo: trayectorias BED y Nano, referencias y builds FINN. Del orden de 4–6 semanas de GPU, más síntesis | **−/−−**: cambia el dataset y todos los números en una revisión; puede leerse como "cambiar el dataset hasta que salga". No elimina el problema de las imágenes de internet (FASDD también las tiene) y pierde la parte de vigilancia de DFire. **No recomendado** |
| 3. Duplicados + train (DFire+FASDD) / val (solo FASDD oficial) / test | Sí | Sí | ≈ 45–60 h | 6–11 días | **+**: metodológicamente correcta y "oficial" para FASDD. Pero el entrenamiento pierde ~40k imágenes (−34 %) y la validación no contiene DFire. Los nuevos números dejan de ser comparables con los del paper, que es justo lo que queremos confirmar |
| **4. Recomendada: estrategia 3 refinada** (ver §4) | Sí | Sí | ≈ 50–75 h | 6–11 días (núcleo) + 4–5 días (ampliación opcional) | **++**: "detectamos un problema de protocolo, lo corregimos y confirmamos los resultados con media ± desviación". Responde a la vez R3-1, R2-M2, R2-M3 y A-3 |

##### 4. Propuesta: estrategia 3 refinada, por fases

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

##### 5. Resumen de esfuerzo de la estrategia recomendada (F0–F3, más F4 sin bitstream)

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

##### 6. Lo que necesito que decidas

1. ¿V-A (validación oficial de FASDD) o V-B (validación separada por grupos del pool actual)? Yo recomiendo V-B.
2. Presentación en el paper:
   - (a) sustituir las cifras software por las del nuevo protocolo (media ± desviación) y mantener las cifras FPGA de los diseños desplegados; o
   - (b) mantener las originales y añadir una tabla de "sensibilidad al protocolo".
   - Creo que (a) es más limpio ante R3, pero exige reescribir más tablas.
3. ¿Está libre la GPU del servidor durante ~1–2 semanas? ¿Puedo lanzar dos entrenamientos en paralelo?
4. ¿Empiezo por F0 (≈ medio día y sin riesgo), para tener datos reales antes de comprometer el resto?

##### 7. Semillas: estado real y criticidad (añadido 2026-10-03, tras revisar el código)

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

##### 8. Estrategia inicial recomendada (revisada con lo anterior)

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


