# Reproducibilidad, Git y disciplina de cambios

## Principio general

El proceso de revisión debe permitir explicar después:

- qué se cambió;
- por qué;
- qué comentario del reviewer motivó el cambio;
- qué código se ejecutó;
- con qué entorno;
- qué resultado produjo;
- y qué commit contiene el cambio.

## Estado inicial

Antes de modificaciones importantes:

```bash
git status
git log --oneline --decorate -n 20
```

Registrar la estructura y estado inicial del repo activo.

## Repo histórico

El repo `uav` debe permanecer read-only.

Nunca utilizar en él comandos que modifiquen su estado salvo autorización expresa.

Evitar:

```bash
git checkout ...
git reset ...
git clean ...
git commit ...
```

si pueden alterar evidencia histórica.

Para inspeccionar versiones históricas, preferir:

```bash
git show
git log
git diff
```

## Repo activo

Realizar cambios solamente en `wildfire_paper_review`.

Antes de una intervención grande, crear un commit base limpio.

Mantener commits pequeños y conceptualmente claros.

Ejemplos:

```text
Import original experiment provenance
Fix W4A4 training configuration
Add reviewer-requested latency experiment
Update Table III source data
```

## Diff

Después de cada modificación relevante:

```bash
git diff
```

Claude debe revisar el diff y explicar:

- archivos modificados;
- cambios funcionales;
- cambios puramente editoriales;
- posibles efectos experimentales.

## Entornos

Registrar el entorno utilizado.

Cuando sea relevante:

```bash
which python
python --version
conda env export
pip freeze
```

No reemplazar el entorno histórico por uno moderno sin antes entender el impacto.

## Seeds y determinismo

Cuando existan:

- registrar random seed;
- NumPy seed;
- PyTorch seed;
- CUDA determinism;
- dataset split;
- shuffle;
- workers;
- transformaciones aleatorias.

Si el experimento histórico no registra estas variables, marcarlo como limitación de reproducibilidad.

## Outputs nuevos

Separar claramente resultados históricos de resultados generados durante la revisión.

Ejemplo:

```text
results/
├── historical_reference/
└── review_2026/
```

Nunca sobrescribir un output que pueda servir como evidencia del trabajo original.

## Notebooks

Antes de ejecutar un notebook histórico:

- revisar paths;
- identificar dependencias;
- comprobar qué celdas producen efectos secundarios;
- comprobar si sobrescribe checkpoints o resultados.

Si existe riesgo de modificar evidencia histórica, trabajar sobre una copia en el repo activo.

## Reproducibilidad científica

Para cada resultado nuevo que vaya al paper, registrar como mínimo:

- commit;
- comando/notebook;
- entorno;
- config;
- dataset/split;
- checkpoint;
- métricas;
- fecha;
- hardware relevante;
- artefactos generados.

Para resultados FPGA, registrar también cuando proceda:

- board/device;
- FINN version;
- clock target;
- folding configuration;
- synthesis tool version;
- resource report;
- timing report;
- latency/throughput measurement method.
