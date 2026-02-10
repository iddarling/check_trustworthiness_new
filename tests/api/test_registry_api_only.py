"""
API-only тесты для реестров без использования Selenium.
Проверяют актуальность данных, формат дат и корректность ответов API.
"""
import pytest  # type: ignore[reportMissingImports]
from datetime import datetime, timedelta
from core.api_helpers import (
    build_api_url,
    fetch_json,
    extract_field_from_response,
    validate_date_format,
    validate_date_not_future,
    authenticate,
)
from config_api import REGISTRIES, DEFAULT_PARAMS, DATE_FORMAT, API_USERNAME, API_PASSWORD

# Хранилище для старых дат (более 2 недель)
OUTDATED_REGISTRIES = []


@pytest.fixture(scope="session", autouse=True)
def authenticate_session():
   
    authenticate(API_USERNAME, API_PASSWORD)


@pytest.mark.parametrize(
    "registry_key",
    REGISTRIES.keys(),
    ids=[v["description"] for v in REGISTRIES.values()],
)
def test_registry_relevance_date_format_and_validity(registry_key):
    """
    Параметризованный тест для проверки дат актуальности разных реестров.
    
    Проверяет:
    - Дата актуальности присутствует в ответе API
    - Формат даты соответствует DD-MM-YYYY
    - Дата не находится в будущем
    - Дата не старше 2 недель (собирает устаревшие в отдельный список)
    
    Args:
        registry_key: Ключ реестра из REGISTRIES
    """
    registry = REGISTRIES[registry_key]
    
    # Конструируем URL
    params = {**DEFAULT_PARAMS, "id": registry["bin"]}
    url = build_api_url(registry["endpoint"], params)
    
    # Получаем ответ API
    payload = fetch_json(url, authenticated=True)
    
    # Извлекаем дату актуальности
    relevance_date = extract_field_from_response(
        payload,
        field_path=registry["relevance_field"],
        required=True,
    )
    
    # Проверяем формат даты
    date_obj = validate_date_format(relevance_date, expected_format=DATE_FORMAT)
    
    # Проверяем, что дата не в будущем
    validate_date_not_future(date_obj)
    
    # Проверяем, что дата не старше 2 недель (14 дней)
    two_weeks_ago = datetime.now() - timedelta(days=14)
    if date_obj < two_weeks_ago:
        OUTDATED_REGISTRIES.append({
            "registry": registry["description"],
            "key": registry_key,
            "relevance_date": relevance_date,
            "days_old": (datetime.now() - date_obj).days,
        })


def test_bankruptcy_registry_kgd_relevance_date_api_only():
    """
    Простой тест для проверки реестра банкротства (КГД).
    Можно использовать как пример или для специфичных проверок одного реестра.
    """
    registry = REGISTRIES["bankruptcy_kgd"]
    
    params = {**DEFAULT_PARAMS, "id": registry["bin"]}
    url = build_api_url(registry["endpoint"], params)
    
    payload = fetch_json(url, authenticated=True)
    relevance_date = extract_field_from_response(
        payload,
        field_path=registry["relevance_field"],
        required=True,
    )
    
    date_obj = validate_date_format(relevance_date, expected_format=DATE_FORMAT)
    validate_date_not_future(date_obj)


def test_print_outdated_registries_report():
    """
    Выводит отчет об устаревших реестрах (более 2 недель) в консоль и сохраняет в файл.
    """
    if OUTDATED_REGISTRIES:
        sorted_outdated = sorted(OUTDATED_REGISTRIES, key=lambda x: x["days_old"], reverse=True)
        
        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append("⚠️  УСТАРЕВШИЕ РЕЕСТРЫ (дата актуальности > 2 недель назад)")
        report_lines.append("=" * 80)
        report_lines.append("")
        
        # Категоризируем по приоритету
        critical = [x for x in sorted_outdated if x["days_old"] > 90]
        important = [x for x in sorted_outdated if 30 < x["days_old"] <= 90]
        warning = [x for x in sorted_outdated if 14 <= x["days_old"] <= 30]
        
        if critical:
            report_lines.append("🔴 КРИТИЧНЫЕ (> 90 дней):")
            report_lines.append("-" * 80)
            for item in critical:
                report_lines.append(f"  📋 {item['registry']}")
                report_lines.append(f"     Ключ: {item['key']}")
                report_lines.append(f"     Дата актуальности: {item['relevance_date']}")
                report_lines.append(f"     Возраст: {item['days_old']} дней")
                report_lines.append("")
        
        if important:
            report_lines.append("🟠 ВАЖНЫЕ (30-90 дней):")
            report_lines.append("-" * 80)
            for item in important:
                report_lines.append(f"  📋 {item['registry']}")
                report_lines.append(f"     Ключ: {item['key']}")
                report_lines.append(f"     Дата актуальности: {item['relevance_date']}")
                report_lines.append(f"     Возраст: {item['days_old']} дней")
                report_lines.append("")
        
        if warning:
            report_lines.append("🟡 ВНИМАНИЕ (14-30 дней):")
            report_lines.append("-" * 80)
            for item in warning:
                report_lines.append(f"  📋 {item['registry']}")
                report_lines.append(f"     Ключ: {item['key']}")
                report_lines.append(f"     Дата актуальности: {item['relevance_date']}")
                report_lines.append(f"     Возраст: {item['days_old']} дней")
                report_lines.append("")
        
        report_lines.append("=" * 80)
        report_lines.append(f"📊 Статистика:")
        report_lines.append(f"  Всего устаревших: {len(sorted_outdated)}")
        report_lines.append(f"    - Критичные (>90): {len(critical)}")
        report_lines.append(f"    - Важные (30-90): {len(important)}")
        report_lines.append(f"    - Внимание (14-30): {len(warning)}")
        report_lines.append(f"  Дата генерации: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("=" * 80)
        
        report = "\n".join(report_lines)
        
        # Выводим в консоль
        print("\n" + report)
        
        # Сохраняем в файл
        import os
        output_path = os.path.join(os.path.dirname(__file__), "..", "outdated_registries_report.txt")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report)
        
        print(f"\n✅ Отчет сохранен в: {output_path}\n")
    else:
        msg = "\n✅ Все реестры актуальны (дата актуальности ≤ 2 недель)\n"
        print(msg)
