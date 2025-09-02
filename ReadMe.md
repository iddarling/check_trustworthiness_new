# Trustworthiness BIN Checker

## 🔧 Как сделать проверку универсальной (для всех вкладок)

Скрипт сейчас собирает только данные с вкладки **"Надёжность"**.  
Чтобы сделать его универсальным и собирать данные со всех вкладок:
1. Для начала работы нужно установить venv и активировать его:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

2. Не забудьте установить зависимости из `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
3. Убедитесь, что у вы ввели свои логин и пароль в `.env` файл:
   ```python
    LOGIN=1234@adata.kz
    PASSWORD=1234
   
4. Как проверить нужный таб просто замените и разкомментируйте нужные строки в списке `buttons_and_labels`в `test_customs_status.py`:
   ```python
   buttons_and_labels = [
            ("Enterprise", 'In the list of "Preventive Control and Supervision for the 2nd half of 2025 year"'),
            # ("Finances", "In the list of taxpayers whose transactions were made without actual performance of work, provision of services, or shipment of goods"),
            # ("Purchases", "In the list of TOP 100 suppliers of state purchases"),
            # ("CEO", "Tax and Customs Payment Debt"),
            # ("Founder", "In the list of legal entities with offshore participation"),
        ]   
    ``` 
5. Чтобы запустить проверку в терминале введите:
   ```bash
   pytest -v tests/test_customs_status.py
   ```
6. Результаты проверки появятся в терминале и в файле `result.txt`.

