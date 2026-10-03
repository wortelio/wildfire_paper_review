# Discusión entre Claude y Yo acerca de las decisiones/estrategias para superar la revisión

## Decisiones a lo largo de la investigación para comprender los motivos

Este proyecto no comenzó como un trabajo de investigación, sino que tuvo una orientación más cercana a la elaboración de un producto de ingeniería. Por tanto, muchas decisiones no se tomaron siguiendo una metodología científica, sino con el objetivo de construir un producto.

### Dataset
Al comienzo de este trabajo solo estaba disponible el dataset DFire. Posteriormente, apareció FASDD y se incorporó. La realidad es que ambos datasets incorporan imágenes de internet y no hay traza de que imágenes que estén en entrenamiento de uno no estén en validación o test de otro, lo que falsearía los resultados, al utilizarse imágenes con las que se ha entrenado el modelo para verificarlo.

No se hizo un conjunto separado de validación porque DFire no cuenta con ese conjunto, sino que solo tiene train y test.

#### Propuesta de estrategia
Se me ocurren 3 estrategias posibles:
1. Hacer un análisis de duplicados:
 - Qué resuelve: identifica si hay alguna imagen que contamine el conjunto de test.
 - Si hay duplicados, cómo se le podría dar solución? Habría que repetir gran cantidad de experimentos?
 - Problemas: sigue sin haber un conjunto de entrenamiento, uno de validación y uno de test.
    - Cómo se podría dar respuesta a esto? Cómo se podría justificar?

2. Eliminar DFire y utilizar solo FASDD, con sus 3 conjuntos: train/validation/test
 - Problema: cómo justificar a estas alturas a los revisores que se modifica el dataset. Crees que sería aceptable?

3. Hacer una combinación de 1 y 2: 
 - Se hace un análisis de duplicados
 - Se eliminan las imágenes duplicadas y se pasa a utilizar conjuntos de entrenamiento (DFire+FASDD), de validación (solo FASDD) y de test (DFire+FASDD)

