# Dominio técnico y herramientas

Claude debe actuar como asistente experto en el dominio técnico del proyecto.

## Área científica

El trabajo se sitúa en:

- inteligencia artificial en el edge;
- deep learning eficiente;
- convolutional neural networks;
- quantization-aware training;
- redes neuronales cuantizadas;
- implementación de inferencia en FPGA;
- co-diseño software/hardware;
- análisis de precisión frente a recursos y rendimiento.

## Framework principal de entrenamiento

### PyTorch

PyTorch es la herramienta principal para:

- definición de redes;
- datasets y dataloaders;
- entrenamiento;
- validación;
- evaluación;
- checkpoints;
- análisis de accuracy y otras métricas.

Claude debe preservar el comportamiento experimental existente salvo que la revisión requiera cambios explícitos.

## Cuantización

### Brevitas

Brevitas se utiliza para construir y entrenar redes cuantizadas compatibles con el flujo posterior de implementación.

Claude debe prestar especial atención a:

- bit width de pesos;
- bit width de activaciones;
- tipos de cuantizadores;
- signed/unsigned;
- escalado;
- clipping;
- capas cuantizadas;
- compatibilidad de exportación;
- versiones de Brevitas;
- posibles diferencias de API entre versiones.

No asumir que una versión moderna de Brevitas reproduce el comportamiento de una versión histórica.

## Exportación e implementación

### QONNX / ONNX

Investigar cuando corresponda:

- exportación;
- transformaciones;
- operadores soportados;
- shapes;
- datatypes;
- compatibilidad entre Brevitas, QONNX y FINN.

## FPGA

### FINN (AMD/Xilinx)

FINN es la herramienta open-source fundamental para llevar las redes cuantizadas a una implementación FPGA.

Claude debe poder razonar sobre:

- FINN dataflow;
- transformaciones de modelo;
- folding;
- PE/SIMD;
- streaming;
- HLS;
- synthesis;
- resource utilization;
- LUT;
- FF;
- BRAM;
- URAM;
- DSP;
- latency;
- throughput;
- clock frequency;
- FPS;
- restricciones de dispositivo;
- generación de bitstream;
- estimaciones frente a resultados post-synthesis/post-implementation.

No confundir resultados estimados con resultados medidos o implementados.

## Entorno

El proyecto se ejecuta en Ubuntu, en un servidor universitario compartido.

El código se desarrolla principalmente en:

- Python;
- Jupyter notebooks;
- Conda.

Claude Code se ejecutará desde el servidor.

Antes de ejecutar experimentos, identificar el entorno Conda correcto.

No actualizar automáticamente:

- Python;
- PyTorch;
- Brevitas;
- FINN;
- QONNX;
- CUDA;
- dependencias relacionadas.

Los cambios de versiones pueden alterar reproducibilidad y deben ser deliberados.

## Notebooks

Gran parte del código histórico vive en `.ipynb`.

Claude debe tener en cuenta:

- estado implícito de celdas;
- orden de ejecución;
- variables persistentes;
- outputs guardados;
- código duplicado;
- configuración incrustada;
- paths relativos;
- checkpoints cargados;
- diferencias entre el notebook almacenado y el notebook que realmente se ejecutó históricamente.

No migrar masivamente notebooks a `.py` durante la primera fase.

Primero reconstruir y reproducir el comportamiento existente.

Después, si aporta valor, extraer a módulos Python únicamente lógica estable y repetida, preservando la reproducibilidad.
