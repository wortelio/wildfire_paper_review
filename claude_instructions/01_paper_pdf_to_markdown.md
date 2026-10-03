# Conversión del paper científico de PDF a Markdown

## Propósito

El PDF original del paper es la fuente primaria del manuscrito, pero no es el formato más cómodo para realizar búsqueda, comparación, edición controlada y análisis automatizado durante la revisión.

Debe generarse una representación Markdown fiel del PDF que pueda utilizarse como **fuente de verdad manejable** durante el trabajo con Claude.

El PDF original debe conservarse intacto.

## Archivos recomendados

Dentro del repositorio activo:

```text
paper_files/
├── original.pdf
└── paper.md
```

## Regla fundamental

La conversión PDF → Markdown **NO es una reescritura**.

Durante la conversión:

- no resumir;
- no mejorar la redacción;
- no corregir gramática;
- no actualizar terminología;
- no corregir errores científicos;
- no reinterpretar afirmaciones;
- no modificar resultados;
- no cambiar valores numéricos;
- no cambiar unidades;
- no cambiar nombres de modelos;
- no cambiar referencias;
- no añadir contenido que no esté en el PDF.

El objetivo es producir una representación textual estructurada lo más fiel posible al original.

## Elementos que deben conservarse

Mantener, siempre que sea posible:

- título;
- autores;
- afiliaciones;
- abstract;
- keywords;
- títulos de secciones y subsecciones;
- texto completo;
- listas;
- ecuaciones;
- símbolos matemáticos;
- subíndices y superíndices;
- tablas;
- valores de tablas;
- unidades;
- captions de figuras;
- numeración de figuras;
- numeración de tablas;
- referencias cruzadas;
- citas bibliográficas;
- bibliografía;
- notas al pie;
- nombres de datasets;
- nombres de arquitecturas;
- configuraciones experimentales;
- métricas;
- resultados cuantitativos.

Usar Markdown para estructura textual y LaTeX para ecuaciones cuando sea adecuado.

## Figuras

No inventar una descripción de una figura.

Conservar como mínimo:

- número de figura;
- caption;
- referencias a la figura desde el texto.

Si el contenido visual de una figura es necesario para interpretar resultados y no puede representarse de forma segura en Markdown, marcarlo explícitamente como pendiente de inspección del PDF.

Ejemplo:

```text
[FIGURE 4: consultar original.pdf; el contenido visual no se ha transcrito]
```

## Incertidumbre

Si algún elemento no puede convertirse con seguridad, **no adivinar**.

Marcarlo claramente, por ejemplo:

```text
[UNCERTAIN TRANSCRIPTION: verificar contra original.pdf]
```

## Segunda pasada obligatoria

Tras generar `paper.md`, comparar de nuevo el Markdown con `original.pdf`.

Revisar específicamente:

- números;
- porcentajes;
- decimales;
- signos;
- unidades;
- ecuaciones;
- símbolos;
- tablas;
- captions;
- referencias cruzadas;
- bibliografía.

Corregir el Markdown solamente cuando el contenido pueda verificarse contra el PDF.

## Jerarquía de fuentes

Para cuestiones relativas al contenido publicado:

1. `original.pdf` = fuente primaria e inmutable.
2. `paper.md` = representación de trabajo.
3. Interpretaciones de Claude = análisis auxiliar, nunca fuente primaria.

Si existe discrepancia entre `paper.md` y `original.pdf`, prevalece el PDF.
