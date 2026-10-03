# Claude Code — Wildfire Paper Review

Este directorio contiene las instrucciones de trabajo para utilizar Claude Code durante la revisión de un paper científico sobre inteligencia artificial en el edge y despliegue de CNN cuantizadas en FPGA.

## Objetivo general

El objetivo final es corregir de forma sistemática todos los defectos, dudas y solicitudes identificados por los revisores del paper, preservando la reproducibilidad científica y la trazabilidad entre:

- el manuscrito;
- los comentarios de los revisores;
- el código;
- los notebooks;
- los experimentos históricos;
- los checkpoints;
- los resultados;
- las figuras y tablas;
- y las versiones de Git que pudieron producir los resultados publicados.

## Repositorios

Hay dos repositorios con roles diferentes:

### Repositorio activo

`~/wildfire_paper_review`

Es el repositorio de trabajo actual. Contiene solamente una parte seleccionada del código del proyecto original para reducir complejidad y facilitar el trabajo durante la revisión.

Claude puede modificar este repositorio cuando la tarea lo requiera, siguiendo las reglas definidas en estos documentos.

### Repositorio histórico

`~/uav`

Es el repositorio antiguo. Contiene los experimentos históricos y su historial Git. Debe tratarse como **READ-ONLY** salvo instrucción explícita en sentido contrario.

Su función principal es servir como evidencia histórica para averiguar qué código, configuración, notebook, checkpoint o commit produjo un resultado determinado del paper.

Su estructura de carpetas es esta:
`~/uav/code`: código fundamental del proyecto con todos los experimentos destinados a crear, entrenar, optimizar y cuantificar modelos.
`~/uav/finn`: repositorio de finn, con el código descargado directamente de xilinx/amd. Nunca se debe tocar ningún archivo de esta carpeta, a excepción de los notebooks que se describen en la línea siguiente.
`~/uav/finn/notebooks/uav_finn/classification_review`: aquí dejaremos los nuevos notebooks cuyo objetivo es resolver las objeciones de los revisores al paper. Esta es la única carpeta dentro de `~/uav/finn` que está permitido modificar.
`~/uav/finn/notebooks/uav_finn/classification`: notebooks antiguos, cuyos resultados se han utilizado en el paper. Esta carpeta tampoco se debe modificar nunca.
`~/uav/datasets`: estas carpetas contienen los diferentes datasets utilizados durante la investigación.


## Orden recomendado de trabajo

1. Leer estas instrucciones.
2. Verificar las rutas reales de ambos repositorios.
3. Convertir el PDF original del paper a Markdown fiel.
4. Incorporar los comentarios de los revisores como fuente de requisitos.
5. Reconstruir la relación entre paper, código y experimentos históricos.
6. Crear una matriz de trazabilidad/provenance.
7. Identificar qué observaciones de los revisores requieren:
   - cambios de redacción;
   - análisis adicional;
   - modificación de código;
   - repetición de experimentos;
   - nuevos experimentos;
   - nuevas figuras o tablas.
8. Ejecutar los cambios de forma incremental.
9. Mantener Git limpio y revisar cada diff antes de consolidarlo.

## Documentos de instrucciones

- `01_paper_pdf_to_markdown.md`: conversión fiel del paper a Markdown.
- `02_review_objective.md`: objetivo de la revisión y tratamiento de los comentarios de reviewers.
- `03_domain_and_tooling.md`: conocimiento técnico y herramientas del proyecto.
- `04_claude_agent_spec.md`: especificación del agente/protocolo de trabajo de Claude.
- `05_experimental_provenance.md`: trazabilidad entre resultados del paper y experimentos históricos.
- `06_reproducibility_and_git.md`: reglas para reproducibilidad, cambios de código y Git.

Estos documentos pueden integrarse después en un `CLAUDE.md` raíz, o mantenerse como documentación separada y referenciarse desde él.
