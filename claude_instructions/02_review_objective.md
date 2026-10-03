# Objetivo de la revisión del paper

## Objetivo final

Claude debe ayudar a corregir de manera sistemática todos los defectos, dudas, objeciones y solicitudes identificados por los revisores durante el proceso de evaluación del paper para publicación.

El objetivo no es simplemente "mejorar el código", sino producir una revisión científicamente defendible y trazable del trabajo.

## Los comentarios de los revisores son requisitos de trabajo

Los informes de revisión deben incorporarse al repositorio, preferiblemente en un formato textual como:

```text
reviewers/
├── reviewer_1.md
├── reviewer_2.md
└── response_matrix.md
```

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

## No cambiar resultados para hacerlos encajar

Nunca modificar código, tablas o texto con el objetivo de hacer que un experimento "coincida" con el paper sin evidencia.

Si existe una discrepancia:

1. documentarla;
2. investigar su procedencia;
3. buscar el experimento histórico;
4. inspeccionar Git;
5. identificar la causa probable;
6. proponer cómo resolverla.

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
6. ejecutar;
7. validar;
8. documentar.

La prioridad es una revisión científicamente sólida, no maximizar la cantidad de cambios.
