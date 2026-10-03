# Especificación del agente Claude para la revisión

## Misión

Ayudar a completar la revisión científica del paper utilizando como fuentes:

- el PDF original;
- su representación Markdown;
- los comentarios de los revisores;
- el repositorio activo;
- el repositorio histórico;
- el historial Git;
- notebooks;
- scripts;
- logs;
- checkpoints;
- resultados experimentales.

El agente debe maximizar trazabilidad y reproducibilidad.

## Repositorio activo

Directorio esperado:

```text
~/wildfire_paper_review
```

Este es el repositorio en el que se realizan los cambios de la revisión.

Antes de asumir la ruta, comprobarla con:

```bash
pwd
git rev-parse --show-toplevel
```

## Repositorio histórico

Existe un repositorio antiguo denominado `uav`.

Su ruta exacta debe verificarse.

Contiene:

- experimentos históricos;
- notebooks;
- scripts;
- resultados;
- posiblemente instalaciones/artefactos FINN;
- historial `.git`.

Debe considerarse **READ-ONLY**.

Claude puede inspeccionarlo para recuperar evidencia histórica, pero no debe:

- modificar archivos;
- eliminar archivos;
- mover archivos;
- renombrar archivos;
- hacer commits;
- ejecutar procesos destructivos.

Si Claude Code se inicia desde el repo activo, incorporar el histórico como directorio adicional únicamente después de verificar su ruta.

Ejemplo conceptual:

```bash
cd ~/wildfire_paper_review
claude --add-dir /RUTA/REAL/uav
```

## Fuentes de verdad

Jerarquía general:

### Manuscrito
1. PDF original.
2. Markdown verificado.

### Requisitos de revisión
1. Texto original de los reviewers.
2. Matriz de respuesta derivada de esos comentarios.

### Resultados experimentales
La fuente de verdad puede requerir combinar:

- output histórico;
- logs;
- CSV;
- TensorBoard;
- checkpoints;
- notebooks;
- configs;
- Git;
- archivos generados;
- resultados FINN.

No asumir que el código actualmente presente en el repo activo produjo los resultados del paper.

## Reglas de razonamiento

Claude debe distinguir explícitamente:

- VERIFIED: existe evidencia directa;
- STRONG EVIDENCE: múltiples evidencias consistentes;
- INFERENCE: conclusión razonable pero no demostrada;
- HYPOTHESIS: posibilidad que necesita validación;
- UNKNOWN: evidencia insuficiente.

No presentar inferencias como hechos.

## Antes de modificar código

Para cualquier cambio experimental importante:

1. identificar qué comentario del reviewer lo motiva;
2. identificar sección/tabla/figura afectada;
3. localizar el código actual;
4. investigar el histórico si existe incertidumbre;
5. comprobar Git cuando sea relevante;
6. explicar qué se propone cambiar;
7. aplicar el cambio mínimo;
8. ejecutar validación;
9. mostrar `git diff`;
10. documentar el resultado.

## Seguridad experimental

No sobrescribir por defecto:

- checkpoints históricos;
- logs históricos;
- CSV originales;
- notebooks originales del repositorio histórico;
- resultados FINN;
- bitstreams;
- outputs que puedan servir como evidencia.

Crear nuevos resultados en ubicaciones claramente diferenciadas.

## Estilo de colaboración

Ante incertidumbre científica o experimental:

- investigar primero;
- mostrar evidencia;
- explicar alternativas;
- evitar hacer cambios irreversibles.

Preferir cambios pequeños, verificables y versionados frente a grandes refactors.

## Primera tarea recomendada

Antes de modificar código:

1. analizar la estructura del repo activo;
2. localizar paper y reviewers;
3. verificar la ruta del repo histórico;
4. reconstruir los principales pipelines;
5. producir un mapa:
   - paper → resultado → experimento → código → artefactos → commit;
6. identificar lagunas de reproducibilidad.

No modificar todavía los experimentos durante esta fase inicial.
