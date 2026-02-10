"""
Конфигурация pytest для API-тестов.
Добавляет хук для вывода финального отчета об устаревших реестрах.
"""
import pytest # type: ignore[reportMissingImports]
from datetime import datetime


def pytest_sessionfinish(session, exitstatus):
    """
    Хук, который запускается в конце тестовой сессии.
    Выводит дополнительный отчет об устаревших реестрах.
    """
    # Импортируем после того, как тесты завершены
    try:
        from test_registry_api_only import OUTDATED_REGISTRIES
        
        if OUTDATED_REGISTRIES:
            sorted_outdated = sorted(OUTDATED_REGISTRIES, key=lambda x: x["days_old"], reverse=True)
            
            # Создаем отчет
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            report = f"\n{'='*80}\n"
            report += f"📊 ОТЧЕТ ОБ АКТУАЛЬНОСТИ РЕЕСТРОВ\n"
            report += f"Дата/время: {timestamp}\n"
            report += f"{'='*80}\n\n"
            
            report += f"⚠️  КРИТИЧНЫЕ: Дата актуальности старше 2 недель (14 дней)\n"
            report += f"Всего устаревших: {len(sorted_outdated)} реестров\n\n"
            
            for i, item in enumerate(sorted_outdated, 1):
                days = item["days_old"]
                # Визуальный индикатор срочности
                if days > 90:
                    priority = "🔴 КРИТИЧНО"
                elif days > 30:
                    priority = "🟠 ВАЖНО"
                else:
                    priority = "🟡 ВНИМАНИЕ"
                
                report += f"{i}. {priority} - {item['registry']}\n"
                report += f"   Дата: {item['relevance_date']} ({days} дней назад)\n"
                report += f"   Ключ: {item['key']}\n\n"
            
            report += f"{'='*80}\n"
            report += f"Сохраните эти реестры для ручной проверки или обновления источников данных.\n"
            report += f"{'='*80}\n"
            
            # Выводим в консоль
            print(report)
            
            # Сохраняем в файл
            with open("outdated_registries_report.txt", "w", encoding="utf-8") as f:
                f.write(report)
            
            print(f"✅ Отчет сохранен в outdated_registries_report.txt\n")
    except ImportError:
        pass
