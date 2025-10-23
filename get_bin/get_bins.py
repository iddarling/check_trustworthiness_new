import pdfplumber
import re

iin_bin_pattern = re.compile(r"\b\d{12}\b")
bin_list = []

with pdfplumber.open("1.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            matches = iin_bin_pattern.findall(text)
            bin_list.extend(matches)

# убираем дубликаты
bin_list = sorted(set(bin_list))

# ограничиваем 50 штук
bin_list = bin_list[:50]

# сохраняем в файл
with open("bin_list.txt", "w", encoding="utf-8") as f:
    for item in bin_list:
        f.write(item + "\n")

print(f"Извлечено {len(bin_list)} ИИН/БИН (лимит 50). Сохранили в bin_list.txt")
