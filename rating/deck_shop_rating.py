import os
import json
import asyncio
import pandas as pd
import logging
import time
import sys
from deck_shop_fetcher import fetch_deck_rating

os.makedirs("../logs", exist_ok=True)
os.makedirs("../results", exist_ok=True)

LOG_LEVEL = logging.INFO 

logging.basicConfig(
    level=LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("../logs/app_run{}.log".format(time.strftime('%Y%m%d_%H%M%S'))), 
        logging.StreamHandler(sys.stdout) 
    ],
    force=True 
)

logging.info("Logger configurado exitosamente.")

score_mapping = {
    "RIP": 0, "Bad": 1, "Mediocre": 2, "Good": 3, "Great!": 4, "Godly!": 5,
}

CACHE_FILE = "deck_shop_cache.json"

def load_deck_cache():
    """Carga el caché de ratings existente."""
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Error cargando caché: {e}")
            return {}
    return {}

def save_deck_cache(cache_data):
    """Guarda el caché actualizado en disco."""
    try:
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logging.error(f"Error guardando caché: {e}")

def get_deck_key(cards_list):
    """
    Genera una clave única para un mazo, independiente del orden.
    Ejemplo: ['Zap', 'Miner'] -> "Miner,Zap"
    """
    if not isinstance(cards_list, list):
        return ""
    # Ordenamos y unimos para que el orden no importe
    return ",".join(sorted([c.strip() for c in cards_list]))

def process_deck_rating(rating: str) -> dict:
    if not rating: return {}
    parts = rating.strip().split(" ")
    try:
        return {
            "Attack": score_mapping.get(parts[1], 0),
            "Defense": score_mapping.get(parts[3], 0),
            "Synergy": score_mapping.get(parts[5], 0),
            "Versatility": score_mapping.get(parts[7], 0),
            "F2P score": score_mapping.get(parts[10], 0),
        }
    except:
        return {}

# --- Pipeline de Evaluación Actualizado ---

async def run_rating_pipeline(input_filename: str, output_filename: str):
    logging.info(f"Iniciando evaluación de decks desde {input_filename}...")
    
    # 1. Cargar caché y registros previos
    deck_cache = load_deck_cache()
    logging.info(f"Caché cargado con {len(deck_cache)} mazos únicos.")
    
    records = []
    try:
        with open(input_filename, 'r', encoding='utf-8') as f:
            for line in f:
                records.append(json.loads(line))
    except FileNotFoundError:
        logging.error("No existe el archivo de generación.")
        return

    # 2. Verificar procesados
    processed_ids = set()
    try:
        with open(output_filename, 'r', encoding='utf-8') as f:
             for line in f:
                processed_ids.add(json.loads(line).get("execution_id"))
    except FileNotFoundError:
        pass

    # Semáforo para DeckShop (limitamos llamadas simultáneas reales)
    sem = asyncio.Semaphore(5) 
    
    # Variable para saber si necesitamos guardar caché al final
    cache_updated = False

    async def get_rating_data(deck_list):
        nonlocal cache_updated
        if not deck_list or len(deck_list) != 8:
            return None, {}
        
        # Generar clave ordenada (independiente del orden)
        deck_key = get_deck_key(deck_list)
        
        # A. Intentar leer del caché
        if deck_key in deck_cache:
            return deck_cache[deck_key], True # True indica que vino de caché
            
        # B. Si no está, llamar a fetch_deck_rating
        async with sem:
            loop = asyncio.get_running_loop()
            try:
                raw_rating = await loop.run_in_executor(None, fetch_deck_rating, deck_list)
                scores = process_deck_rating(raw_rating)
                
                # Guardar en memoria caché
                deck_cache[deck_key] = scores
                cache_updated = True
                
                return scores, False
            except Exception as e:
                logging.error(f"Error obteniendo rating para {deck_key}: {e}")
                return {}, False

    async def rate_entry(record):
        eid = record["execution_id"]
        if eid in processed_ids: return

        result = {"execution_id": eid, "was_improved": False}
        
        # --- BLOQUE CORREGIDO ---
        parsed_data = record.get("parsed_selection")
        selection_part = []

        if isinstance(parsed_data, list):
            # CASO A: Es directamente una lista (como en tu ejemplo del log)
            selection_part = parsed_data
        elif isinstance(parsed_data, dict):
            # CASO B: Es un diccionario {"selection": [...]}
            selection_part = parsed_data.get("selection", [])
        
        # Limpieza final: asegurar que sea una lista válida
        if not isinstance(selection_part, list):
            selection_part = []
        # ------------------------

        if record.get("is_parsed") and selection_part:
            try:
                # Aseguramos que sean listas antes de sumar
                original_base = record["original_deck"] if isinstance(record["original_deck"], list) else []
                deleted_part = record["deleted_cards"] if isinstance(record["deleted_cards"], list) else []
                
                # Mazo Original Completo (Base + Lo que se borró)
                original_full = original_base + deleted_part
                
                # Mazo Nuevo Completo (Base + Lo que eligió el LLM)
                new_full = original_base + selection_part

                if len(new_full) == 8:
                    scores_orig, _ = await get_rating_data(original_full)
                    scores_new, used_cache = await get_rating_data(new_full)
                    
                    total_orig = sum(scores_orig.values())
                    total_new = sum(scores_new.values())
                    
                    result.update({
                        "rating_status": "success",
                        "scores_original": scores_orig,
                        "scores_new": scores_new,
                        "total_original": total_orig,
                        "total_new": total_new,
                        "was_improved": total_new >= total_orig,
                        "correct_selection_count": sum(1 for c in deleted_part if c in selection_part),
                        "used_cache": used_cache
                    })
                else:
                    result["rating_status"] = f"invalid_deck_len_({len(new_full)})"
            except Exception as e:
                result["rating_status"] = f"error: {str(e)}"
        else:
            result["rating_status"] = "skipped_no_parse"

        # Escribir resultado
        with open(output_filename, 'a', encoding='utf-8') as f_out:
            f_out.write(json.dumps(result, ensure_ascii=False) + '\n')

    # 4. Ejecutar por lotes
    tasks = [rate_entry(rec) for rec in records]
    chunk_size = 10
    total = len(tasks)
    
    for i in range(0, total, chunk_size):
        await asyncio.gather(*tasks[i:i+chunk_size])
        
        # Guardado parcial del caché cada cierto tiempo para evitar pérdidas
        if cache_updated:
            save_deck_cache(deck_cache)
            cache_updated = False
            
        logging.info(f"Evaluados {min(i+chunk_size, total)}/{total}")
        await asyncio.sleep(0.5)

    # Guardado final del caché
    save_deck_cache(deck_cache)
    logging.info("Evaluación finalizada y caché guardado.")

async def main():
    # --- Archivos de ENTRADA y SALIDA ---
    
    # Reemplaza con el nombre de tu archivo de generación existente
    # (El archivo que quieres evaluar)
    input_gen_file = "../results/generations_20251128_082528.jsonl" 
    
    # 1. Verifica si el archivo de generación existe
    if not os.path.exists(input_gen_file):
        logging.error(f"ERROR: No se encontró el archivo de generación: {input_gen_file}")
        return

    # 2. Genera un nombre de archivo de ratings único
    timestamp = time.strftime('%Y%m%d_%H%M%S')
    rating_file = f"deck_shop_ratings_{timestamp}.jsonl"

    logging.info(">>> INICIANDO FASE 2: EVALUACIÓN DECKSHOP")

    # Ejecuta la función de rating que has definido
    await run_rating_pipeline(
        input_filename=input_gen_file,
        output_filename=rating_file
    )

    logging.info(f"Proceso de rating completado. \nRatings guardados en: {rating_file}")

if __name__ == "__main__":
    # Asegúrate de que el directorio 'results' exista
    os.makedirs("../results", exist_ok=True)
    asyncio.run(main())