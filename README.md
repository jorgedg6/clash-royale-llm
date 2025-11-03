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

## Estructura del directorio

```bash
├── README.md
├── app_run.log
├── baseline/
│   ├── 06_lightfm.ipynb
│   ├── 07_deepfm.ipynb
│   ├── deepfm.ipynb
│   └── lightfm.ipynb
├── card_utils.py
├── consts.py
├── data/
│   ├── dataset.ipynb
│   ├── game_cards.csv
│   ├── player_cards.csv
│   ├── player_stats.csv
│   ├── player_tags.csv
│   └── top_decks_per_card.json
├── data_analytics.ipynb
├── deck_rate_fetcher.py
├── final_prompts/
│   ├── final_prompts_lite/
│   └── grafico_mazos_mejorados.png
├── grafico_validez.png
├── logs/
├── main.ipynb
├── prompts/
│   ├── human_prompt_context.txt
│   ├── human_prompt_no_context.txt
│   └── system_prompt.txt
├── results/
│   ├── a_raw_results_run_150_players.jsonl
│   ├── a_valid_results_run_150_players.jsonl
│   ├── raw_results_20251103_141716.jsonl
│   └── valid_results_20251103_141716.jsonl
├── top_deck_fetcher.py
└── users.json

```
9 directories, 414 files
