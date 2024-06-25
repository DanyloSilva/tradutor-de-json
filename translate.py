import json
import time
from googletrans import Translator

input_json_file = '_SELECT_mrq_qa_FROM_master_room_question_mrq_JOIN_question_alter_202406171859.json'
output_json_file = 'translated_questions.json'

with open(input_json_file, 'r', encoding='utf-8') as file:
    raw_data = json.load(file)

data_key = next(iter(raw_data))
data = raw_data[data_key]

translator = Translator()
def translate_text(text, src='pt', dest='es', retries=5, initial_delay=5):
    delay = initial_delay
    for i in range(retries):
        try:
            return translator.translate(text, src=src, dest=dest).text
        except Exception as e:  # Captura qualquer exceção genérica
            print(f"Erro na tradução: {e}. Tentativa {i+1} de {retries}. Retentando após {delay} segundos.")
            time.sleep(delay)
            delay *= 2  # 
    print(f"Falha ao traduzir: {text}")
    return text  

def translate_items(items):
    translated_items = []
    for item in items:
        translated_item = item.copy()
        if 'statement' in item:
            translated_item['statement'] = translate_text(item['statement'])
        if 'description' in item:
            translated_item['description'] = translate_text(item['description'])
        if 'tip' in item:
            translated_item['tip'] = translate_text(item['tip'])
        translated_items.append(translated_item)
    return translated_items

chunk_size = 50  
chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]

translated_chunks = []
for i, chunk in enumerate(chunks):
    print(f"Traduzindo parte {i+1} de {len(chunks)}...")
    translated_chunk = translate_items(chunk)
    translated_chunks.extend(translated_chunk)

    time.sleep(10)

translated_data = {data_key: translated_chunks}

with open(output_json_file, 'w', encoding='utf-8') as file:
    json.dump(translated_data, file, ensure_ascii=False, indent=4)

print(f"Tradução completa. O novo arquivo JSON foi salvo como '{output_json_file}'.")
