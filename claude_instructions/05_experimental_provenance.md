# Trazabilidad y procedencia de los resultados experimentales

## Problema

El repositorio activo contiene solamente una parte del código copiado desde el repositorio antiguo.

Existe incertidumbre sobre si el código copiado es exactamente el que produjo los resultados publicados.

El repositorio histórico `uav` contiene muchos experimentos y puede contener el experimento concreto que generó cada resultado.

Por tanto, antes de asumir que el código actual reproduce el paper, es necesario realizar una auditoría de procedencia experimental.

## Objetivo

Para cada resultado importante del paper, establecer la cadena:

```text
paper
→ tabla/figura/afirmación
→ valor numérico
→ experimento histórico
→ notebook/script
→ configuración
→ checkpoint
→ log/output
→ versión Git
→ código correspondiente en el repo activo
```

## Elementos prioritarios

Investigar especialmente:

- accuracies;
- precisiones por clase si existen;
- pérdidas;
- bit widths;
- comparaciones FP32 vs cuantizado;
- recursos FPGA;
- LUT;
- FF;
- BRAM;
- DSP;
- frecuencia;
- latency;
- throughput;
- FPS;
- power/energy si existen;
- resultados por dispositivo;
- tablas comparativas;
- figuras generadas a partir de experimentos.

## Estrategia de búsqueda

Cuando se quiera localizar el experimento que produjo un número concreto:

1. buscar el valor textual en:
   - notebooks;
   - outputs guardados;
   - logs;
   - CSV;
   - JSON;
   - YAML;
   - TXT;
   - scripts;
2. buscar configuraciones compatibles;
3. buscar checkpoints relacionados;
4. inspeccionar fechas;
5. comparar nombres de carpetas;
6. revisar historial Git;
7. comprobar si posteriores commits alteraron el experimento.

## Git histórico

Si un archivo parece corresponder a un experimento, investigar:

```bash
git -C <repo_uav> log -- <archivo>
```

y, cuando sea necesario:

```bash
git -C <repo_uav> show <commit>:<archivo>
git -C <repo_uav> diff <commit1> <commit2> -- <archivo>
```

El estado actual de un notebook no demuestra que esa versión fuera la utilizada para el paper.

## Matriz de provenance

Crear una tabla como:

| Paper result | Value | Historical experiment | Code | Config | Checkpoint | Output | Git commit | Active repo match | Evidence |
|---|---:|---|---|---|---|---|---|---|---|

## Comparación con el repo activo

Cuando se encuentre el experimento histórico probable:

- comparar el código con el equivalente copiado en `wildfire_paper_review`;
- identificar diferencias;
- determinar si pueden afectar resultados;
- no corregir automáticamente las diferencias;
- documentar qué versión tiene mejor evidencia de ser la original.

## Regla crítica

Encontrar un experimento con un resultado parecido NO demuestra que sea el experimento original.

Para elevar la confianza, buscar evidencia adicional:

- mismo valor;
- misma arquitectura;
- mismos bit widths;
- mismos hiperparámetros;
- mismo dataset split;
- misma semilla;
- checkpoint;
- timestamp;
- nombre de experimento;
- referencias desde otros archivos;
- commits;
- outputs FINN compatibles.

## Resultado esperado

Antes de realizar cambios científicos importantes, debería existir una lista explícita de:

- resultados con procedencia confirmada;
- resultados con procedencia probable;
- resultados ambiguos;
- resultados para los que no existe evidencia suficiente.

Esta lista determinará qué experimentos deben reproducirse o repetirse durante la revisión.
