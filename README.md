# Clash Royale LLM

Proyecto desarrollado en el contexto del curso IIC3633 (RecSys) @ PUC Chile.

## Desarrolladores

* @emolaba
* @jorgedg6
* @vjimenezs

## Directorios relevantes

* `data`: Contiene el archivo `dataset.ipynb` que se utilizó para realizar las llamadas a la *API* de *Clash Royale* y obtener los datos, junto a los archivos *csv* resultantes del proceso.
* `baseline`: Contiene los archivos `lightfm.ipynb` y `deepfm.ipynb`, dentro de los cuales se entrenador los modelos para luego medir su *precision* y *recall* como punto de comparación.
* `prompts`: Contiene los **prompts** que fueron utilizados para realizar las consultas a los *LLM*.
* `results`: Resultados enriquecidos de la respuesta de los *LLM* a las consultas realizadas.