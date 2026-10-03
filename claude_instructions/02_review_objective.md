# Objetivo de la revisión del paper

## Objetivo final

Claude debe ayudar a corregir de manera sistemática todos los defectos, dudas, objeciones y solicitudes identificados por los revisores durante el proceso de evaluación del paper para publicación.

El objetivo no es simplemente "mejorar el código", sino producir una revisión científicamente defendible y trazable del trabajo.

Los comentarios de los revisores están en el email paper_review_email.md.

## Los comentarios de los revisores son requisitos de trabajo

Los informes de revisión deben incorporarse al repositorio, preferiblemente en un formato textual como:

```paper_files/reviewers/
├── reviewer_1.md
├── reviewer_2.md
├── reviewer_3.md
└── response_matrix.md
```

Para incorporarlos, lee todos el email de paper_review_email.md, localiza los comentarios que pertenecen a cada revisor y trasládalos a su correspondiente reviewer_<num>.md.

No reinterpretar silenciosamente una petición del reviewer.

Para cada comentario, identificar:

- texto original del comentario;
- problema señalado;
- sección afectada del paper;
- evidencia existente;
- código relacionado;
- experimento relacionado;
- si el resultado histórico puede reproducirse;
- acción requerida;
- estado;
- evidencia que demuestra que el comentario ha sido resuelto.

## Clasificación útil de cada comentario

Cada observación puede requerir una o varias de estas acciones:

- cambio exclusivamente editorial;
- aclaración metodológica;
- ampliación de discusión;
- explicación de una decisión de diseño;
- corrección de una inconsistencia;
- verificación de un resultado;
- recuperación de un experimento histórico;
- repetición de un experimento;
- nuevo experimento;
- nuevo baseline;
- análisis estadístico adicional;
- modificación de una figura;
- modificación de una tabla;
- modificación de código;
- cambio del pipeline FINN;
- nueva síntesis FPGA;
- nueva medición de recursos, rendimiento, latencia o throughput.

## No cambiar resultados

Nunca modificar código por el momento.

Si existe una discrepancia:

1. documentarla;
2. investigar su procedencia;
3. buscar el experimento histórico;
4. inspeccionar Git;
5. identificar la causa probable;
6. proponer cómo resolverla a alto nivel. Esta sección la utilizaremos en el futuro para discutir las estrategias para resolver las objeciones declaradas por los revisores.

Distinguir siempre entre:

- hecho verificado;
- evidencia parcial;
- inferencia razonable;
- hipótesis;
- información desconocida.

## Matriz de respuesta

Mantener una matriz de seguimiento con una fila por comentario relevante:

| Reviewer | Comentario | Paper | Código/experimento | Acción | Evidencia | Estado |
|---|---|---|---|---|---|---|

La matriz debe permitir responder, al final del proceso:

- qué cambió;
- por qué cambió;
- qué experimento lo justifica;
- dónde está el resultado;
- qué commit contiene el cambio;
- y cómo responder al reviewer.

## Estrategia

Antes de realizar cambios extensos:

1. comprender el comentario;
2. localizar su relación con el paper;
3. localizar el código pertinente;
4. comprobar la procedencia de los resultados afectados;
5. proponer la mínima intervención necesaria;
6. hacer una estimación del tiempo que habría que invertir para resolver la objeción con garantías.

La prioridad es una revisión científicamente sólida.