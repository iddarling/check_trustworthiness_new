import pdfplumber
import re
import os
from openpyxl import load_workbook

# === Настройки ===
iin_bin_pattern = re.compile(r"\b\d{12}\b")
bin_list = []

input_dir = "."  # Папка, где искать файлы (можно указать путь)
output_path = "../tests/bin_list.txt"

# === Проход по всем PDF и XLSX ===
for filename in os.listdir(input_dir):
    filepath = os.path.join(input_dir, filename)

    # --- Если PDF ---
    if filename.lower().endswith(".pdf"):
        try:
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        matches = iin_bin_pattern.findall(text)
                        bin_list.extend(matches)
            print(f"Извлекли ИИН/БИН из {filename}")
        except Exception as e:
            print(f"Ошибка при обработке {filename}: {e}")

    # --- Если XLSX ---
    elif filename.lower().endswith(".xlsx"):
        try:
            wb = load_workbook(filepath, data_only=True)
            for sheet in wb.worksheets:
                for row in sheet.iter_rows(values_only=True):
                    for cell in row:
                        if cell is not None:
                            matches = iin_bin_pattern.findall(str(cell))
                            bin_list.extend(matches)
            print(f"Извлекли ИИН/БИН из {filename}")
        except Exception as e:
            print(f"Ошибка при обработке {filename}: {e}")

# === Обработка и сохранение ===
bin_list = sorted(set(bin_list))[:50]  # уникальные, максимум 50

# создаём директорию для сохранения
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Сохраняем в .txt
with open(output_path, "w", encoding="utf-8") as f:
    for item in bin_list:
        f.write(item + "\n")

print(f"\nИзвлечено {len(bin_list)} ИИН/БИН (лимит 50).")
print(f"Сохранили в: {output_path}")

# === Удаляем все обработанные файлы ===
for filename in os.listdir(input_dir):
    if filename.lower().endswith((".pdf", ".xlsx")):
        filepath = os.path.join(input_dir, filename)
        try:
            os.remove(filepath)
            print(f"Файл {filename} успешно удалён.")
        except OSError as e:
            print(f"Ошибка при удалении {filename}: {e}")
