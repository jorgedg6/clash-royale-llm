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

.
├── README.md
├── __pycache__
│   ├── card_utils.cpython-313.pyc
│   ├── consts.cpython-313.pyc
│   └── deck_rate_fetcher.cpython-313.pyc
├── app_run.log
├── baseline
│   ├── 06_lightfm.ipynb
│   ├── 07_deepfm.ipynb
│   ├── __pycache__
│   ├── deepfm.ipynb
│   └── lightfm.ipynb
├── card_utils.py
├── consts.py
├── content.txt
├── data
│   ├── dataset.ipynb
│   ├── game_cards.csv
│   ├── player_cards.csv
│   ├── player_stats.csv
│   ├── player_tags.csv
│   └── top_decks_per_card.json
├── data_analytics.ipynb
├── deck_rate_fetcher.py
├── eliminados.txt
├── final_prompts
│   ├── final_prompts_lite
│   ├── grafico_mazos_mejorados.png
├── grafico_validez.png
├── grapths.ipynb
├── hola.json
├── logs
├── main copy 2.ipynb
├── main copy 3.ipynb
├── main copy 4.ipynb
├── main copy.ipynb
├── main.ipynb
├── prompts
│   ├── human_prompt_context.txt
│   ├── human_prompt_context_lite.txt
│   ├── human_prompt_context_semi_lite.txt
│   ├── human_prompt_no_context.txt
│   ├── human_prompt_no_context_lite.txt
│   ├── human_prompt_no_context_semi_lite.txt
│   └── system_prompt.txt
├── results
│   ├── a_raw_results_run_150_players.jsonl
│   ├── a_valid_results_run_150_players.jsonl
│   ├── raw_results_20251102_182116.jsonl
│   ├── raw_results_20251102_221805.jsonl
│   ├── raw_results_20251102_222549.jsonl
│   ├── raw_results_20251102_223353.jsonl
│   ├── raw_results_20251102_224222.jsonl
│   ├── raw_results_20251102_225632.jsonl
│   ├── raw_results_20251102_231706.jsonl
│   ├── raw_results_20251102_231758.jsonl
│   ├── raw_results_20251102_232520.jsonl
│   ├── raw_results_20251103_114210.jsonl
│   ├── raw_results_20251103_115624.jsonl
│   ├── raw_results_20251103_141716.jsonl
│   ├── valid_results_20251102_182116.jsonl
│   ├── valid_results_20251102_221805.jsonl
│   ├── valid_results_20251102_222549.jsonl
│   ├── valid_results_20251102_223353.jsonl
│   ├── valid_results_20251102_224222.jsonl
│   ├── valid_results_20251102_225632.jsonl
│   ├── valid_results_20251102_231706.jsonl
│   ├── valid_results_20251102_231758.jsonl
│   ├── valid_results_20251102_232520.jsonl
│   ├── valid_results_20251103_114210.jsonl
│   ├── valid_results_20251103_115624.jsonl
│   └── valid_results_20251103_141716.jsonl
├── results.json
├── top_deck_fetcher.py
└── users.json

9 directories, 414 files
