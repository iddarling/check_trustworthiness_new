#!/usr/bin/env python3
"""
Скрипт для диагностики доступных API эндпоинтов.
Результаты сохраняются в ../diag_output.txt
"""
import sys
import os
from datetime import datetime
sys.path.insert(0, '/home/darling/testing_files/test_reestrs')

from core.api_helpers import fetch_json, build_api_url, authenticate
from config_api import REGISTRIES, DEFAULT_PARAMS, API_USERNAME, API_PASSWORD

# Путь для сохранения результатов
output_file = os.path.join(os.path.dirname(__file__), '..', 'diag_output.txt')
output_lines = []

def log_message(message):
    """Выводит сообщение в консоль и добавляет в список"""
    print(message)
    output_lines.append(message)

# Заголовок отчета
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
log_message("=" * 80)
log_message(f"🔍 ДИАГНОСТИКА API ЭНДПОИНТОВ - {timestamp}")
log_message("=" * 80)
log_message("")

log_message("🔑 Аутентификация...")
try:
    token = authenticate(API_USERNAME, API_PASSWORD)
    log_message("✅ Успешная аутентификация!\n")
except Exception as e:
    log_message(f"❌ Ошибка аутентификации: {e}\n")
    sys.exit(1)

test_bin = "200140023023"

log_message("🔍 Проверка доступных API эндпоинтов...\n")

# Проверка open-card эндпоинта перед основной диагностикой
log_message("=" * 80)
log_message("📌 ПРЕДВАРИТЕЛЬНАЯ ПРОВЕРКА: open-card эндпоинт")
log_message("=" * 80)
open_card_url = f"https://pk-api.adata.kz/api/v1/data/counterparty/company/open-card?id={test_bin}"
log_message(f"URL: {open_card_url}\n")

try:
    response = fetch_json(open_card_url, authenticated=True)
    if response.get("status"):
        log_message(f"✅ Успешно! Status: {response.get('status')}")
        if "data" in response and response["data"]:
            log_message(f"   Response structure:")
            data = response["data"]
            if isinstance(data, dict):
                for key, value in data.items():
                    if isinstance(value, dict):
                        log_message(f"   ├─ {key}: {list(value.keys())}")
                    elif isinstance(value, list):
                        log_message(f"   ├─ {key}: list[{len(value)}]")
                    else:
                        log_message(f"   ├─ {key}: {type(value).__name__}")
            else:
                log_message(f"   Data type: {type(data).__name__}")
        else:
            log_message(f"⚠️  Response data is empty or null")
    else:
        log_message(f"⚠️  Status: False. Message: {response.get('message')}")
except Exception as e:
    log_message(f"❌ Ошибка: {str(e)[:300]}")

log_message("\n" + "=" * 80)
log_message("📋 ПРОВЕРКА ДОСТУПНЫХ РЕЕСТРОВ")
log_message("=" * 80 + "\n")

for key, registry in REGISTRIES.items():
    log_message(f"📋 {registry['description']} ({key})")
    params = {**DEFAULT_PARAMS, "id": test_bin}
    url = build_api_url(registry["endpoint"], params)
    log_message(f"   URL: {url}")
    
    try:
        response = fetch_json(url, authenticated=True)
        if response.get("status"):
            log_message(f"   ✅ Успешно! Status: {response.get('status')}")
            if "data" in response:
                log_message(f"   Data keys: {list(response['data'].keys())}")
                if "meta" in response["data"]:
                    log_message(f"   Meta: {response['data']['meta']}")
        else:
            log_message(f"   ⚠️  Status: False. Response: {response}")
    except AssertionError as e:
        log_message(f"   ❌ Ошибка: {str(e)[:200]}")
    log_message("")

# Сохраняем результаты в файл
log_message("=" * 80)
log_message(f"📁 Результаты сохранены в: {output_file}")
log_message("=" * 80)

with open(output_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines))

print(f"\n✅ Диагностика завершена. Результаты сохранены в: {output_file}")
