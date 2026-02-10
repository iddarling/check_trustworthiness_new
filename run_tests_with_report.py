#!/usr/bin/env python3
"""
Скрипт для запуска тестов и генерации полного отчета о результатах.
Результаты сохраняются в results.txt и allure-report/
"""
import subprocess
import sys
import os
from datetime import datetime
import shutil
import re

def main():
    print("🚀 Запуск тестов API реестров...")
    print("=" * 80)
    
    # Запускаем тесты с сохранением результатов для Allure и HTML отчета
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/test_registry_api_only.py", "-v", "--tb=line",
         "--alluredir=allure-results", "--html=test_report.html", "--self-contained-html"],
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace',
        env={**os.environ, "PYTHONIOENCODING": "utf-8"}
    )
    
    # Исправляем кодировки в выводе
    result.stdout = fix_cyrillic_encoding(result.stdout)
    result.stderr = fix_cyrillic_encoding(result.stderr)
    
    # Формируем полный отчет
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report_lines = []
    
    report_lines.append("=" * 80)
    report_lines.append("📊 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ РЕЕСТРОВ")
    report_lines.append("=" * 80)
    report_lines.append(f"Дата/время: {timestamp}")
    report_lines.append(f"Статус: {'✅ УСПЕШНО' if result.returncode == 0 else '❌ ОШИБКА'}")
    report_lines.append("=" * 80)
    report_lines.append("")
    
    # Добавляем вывод тестов
    report_lines.append("📋 ВЫВОД ТЕСТОВ:")
    report_lines.append("-" * 80)
    
    # Обрабатываем вывод: скрываем детали ошибок с проблемами кодировки, оставляем только summary
    output_lines = result.stdout.split('\n')
    summary_started = False
    skip_errors_section = False
    
    for line in output_lines:
        # Пропускаем секцию FAILURES полностью (там проблемы с кодировкой)
        if '=== FAILURES ===' in line:
            skip_errors_section = True
            report_lines.append("-" * 80)
            report_lines.append("⚠️  ОШИБКИ ТЕСТОВ:")
            report_lines.append("-" * 80)
            continue
        
        # Заканчиваем пропускать когда видим summary
        if 'short test summary' in line or '= short test summary' in line:
            skip_errors_section = False
            summary_started = True
            report_lines.append("-" * 80)
            report_lines.append("📌 КРАТКАЯ СВОДКА:")
            report_lines.append("-" * 80)
            continue
        
        # Пропускаем строки если мы в секции ошибок
        if skip_errors_section and line.startswith('_'):
            continue
        if skip_errors_section and line.startswith('E  '):
            continue
        if skip_errors_section and 'tests/test_registry_api_only.py' in line and 'in ' in line:
            continue
        if skip_errors_section and ('AssertionError' in line or 'ÐÑÑÑ' in line):
            continue
        
        # Добавляем все остальные строки
        if not skip_errors_section or summary_started:
            report_lines.append(line)
    
    report_lines.append("")
    
    # Добавляем ошибки если они были
    if result.stderr:
        report_lines.append("⚠️  ОШИБКИ:")
        report_lines.append("-" * 80)
        report_lines.append(result.stderr)
        report_lines.append("")
    
    # Проверяем наличие файла об устаревших реестрах
    if os.path.exists("outdated_registries_report.txt"):
        try:
            with open("outdated_registries_report.txt", "r", encoding="utf-8") as f:
                outdated_report = f.read()
                report_lines.append("📌 УСТАРЕВШИЕ РЕЕСТРЫ:")
                report_lines.append("-" * 80)
                report_lines.append(outdated_report)
        except Exception as e:
            report_lines.append(f"Ошибка чтения отчета об устаревших реестрах: {e}")
    
    report_lines.append("=" * 80)
    report = "\n".join(report_lines)
    
    # Выводим в консоль
    print(report)
    
    # Сохраняем в файл
    output_file = "results.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"\n✅ Полный отчет сохранен в: {output_file}\n")
    
    # Генерируем Allure отчет и HTML отчет
    print("📊 Отчеты успешно созданы:")
    print("-" * 80)
    
    if os.path.exists("test_report.html"):
        print("✅ HTML отчет: test_report.html")
        print("   Откройте в браузере: file://$(pwd)/test_report.html")
    
    if os.path.exists("allure-results"):
        print("✅ Allure результаты сохранены: allure-results/")
        
        # Отправляем результаты на Allure Docker Service
        print("\n📤 Отправка результатов на Allure Docker Service...")
        print("-" * 80)
        
        if send_to_allure(allure_server="http://10.10.22.211:5050", project_id="test-trustworthiness-reestrs"):
            # Удаляем локальные результаты после успешной отправки
            print("\n🗑️  Удаление локальных результатов...")
            try:
                shutil.rmtree("allure-results")
                print("✅ Папка allure-results удалена")
            except Exception as e:
                print(f"⚠️  Ошибка удаления allure-results: {e}")
            
    print("=" * 80)
    
    return result.returncode


def fix_cyrillic_encoding(text):
    """Исправляет проблемы с кодировкой кириллицы из pytest вывода"""
    if not text:
        return text
    
    try:
        # Попытка 1: исправить двойное кодирование (UTF-8 как Latin-1)
        # Это происходит когда UTF-8 байты неправильно интерпретированы как Latin-1
        fixed = text.encode('latin-1').decode('utf-8', errors='ignore')
        # Проверяем что получилось валидное
        if 'Ð²' not in fixed:  # Если нет испорченных символов
            return fixed
    except:
        pass
    
    try:
        # Попытка 2: unicode_escape декодирование
        return text.encode('utf-8').decode('unicode_escape')
    except:
        pass
    
    try:
        # Попытка 3: raw_unicode_escape
        return text.encode('raw_unicode_escape').decode('utf-8')
    except:
        pass
    
    # Если ничего не помогло, возвращаем исходный
    return text


def decode_unicode_escapes(text):
    """Преобразует unicode escape sequences (\\uXXXX) обратно в кириллицу"""
    if not text:
        return text
    try:
        # Используем кодирование raw_unicode_escape для декодирования
        return text.encode('utf-8').decode('unicode_escape')
    except:
        # Если что-то пошло не так, возвращаем исходный текст
        return text


def send_to_allure(allure_server, project_id):
    """Отправляет результаты тестов в Allure Docker Service"""
    import glob
    
    # Получаем список всех файлов в allure-results
    result_files = glob.glob("allure-results/*")
    
    if not result_files:
        print("⚠️  Нет файлов результатов для отправки")
        return False
    
    # Строим команду curl с опциями -F для каждого файла
    curl_cmd = [
        "curl", "-X", "POST",
        f"{allure_server}/allure-docker-service/send-results?project_id={project_id}"
    ]
    
    # Добавляем каждый файл с опцией -F
    for file_path in result_files:
        curl_cmd.extend(["-F", f"files[]=@{file_path}"])
    
    try:
        response = subprocess.run(curl_cmd, capture_output=True, text=True, timeout=60)
        
        if response.returncode == 0:
            print(f"✅ Результаты успешно отправлены на {allure_server}")
            print(f"   Проект: {project_id}")
            print(f"   Файлов отправлено: {len(result_files)}")
            if response.stdout:
                # Проверяем наличие успешного ответа сервера
                if "data" in response.stdout or "success" in response.stdout.lower():
                    print(f"   Ответ сервера: ✓ Принято")
                    return True
                else:
                    print(f"   Ответ: {response.stdout[:200]}")
                    return True
            return True
        else:
            print(f"❌ Ошибка отправки результатов:")
            print(f"   Status code: {response.returncode}")
            if response.stderr:
                print(f"   Ошибка: {response.stderr[:300]}")
            return False
            
    except Exception as e:
        print(f"❌ Исключение при отправке результатов: {str(e)[:200]}")
        return False

if __name__ == "__main__":
    sys.exit(main())
