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
