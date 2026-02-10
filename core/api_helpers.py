"""
Общие хелперы для API-тестирования без Selenium.
Поддерживает аутентификацию через JWT токены.
"""
import json
import os
import urllib.request
import urllib.parse
from http.cookiejar import CookieJar
from urllib.error import HTTPError, URLError
from datetime import datetime
from typing import Any, Dict, Optional


API_BASE_URL = os.getenv("API_BASE_URL", "https://pk-api.adata.kz")
AUTH_BASE_URL = os.getenv("AUTH_BASE_URL", "https://auth.adata.kz")

# Headers для API запросов
DEFAULT_HEADERS = {
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
    "Content-Type": "application/json",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "Origin": "https://pk.adata.kz",
    "Referer": "https://pk.adata.kz/",
}

# Глобальный cookie jar и access token
_cookie_jar = CookieJar()
_access_token: Optional[str] = None


def _get_opener():
    """Возвращает opener с cookie jar для сохранения cookies между запросами."""
    return urllib.request.build_opener(urllib.request.HTTPCookieProcessor(_cookie_jar))


def authenticate(username: str, password: str) -> str:
    """
    Аутентифицирует пользователя и возвращает JWT токен.
    
    Args:
        username: Email пользователя
        password: Пароль пользователя
        
    Returns:
        str: JWT токен для использования в дальнейших запросах
        
    Raises:
        AssertionError: Если аутентификация не удалась
    """
    global _access_token
    
    auth_url = f"{AUTH_BASE_URL}/api/login"
    payload = json.dumps({
        "username": username,
        "password": password,
    }).encode('utf-8')
    
    headers = {
        **DEFAULT_HEADERS,
        "Content-Type": "application/json",
    }
    
    req = urllib.request.Request(
        auth_url,
        data=payload,
        headers=headers,
        method="POST"
    )
    
    try:
        opener = _get_opener()
        with opener.open(req, timeout=20) as response:
            response_data = json.load(response)
    except HTTPError as exc:
        error_body = exc.read().decode() if hasattr(exc, 'read') else ""
        raise AssertionError(
            f"Ошибка аутентификации (HTTP {exc.code}): {exc.reason}\n{error_body}"
        ) from exc
    except URLError as exc:
        raise AssertionError(f"Ошибка аутентификации: {exc}") from exc
    
    # Проверяем поле 'success' вместо 'status'
    if not response_data.get("success"):
        raise AssertionError(f"Аутентификация не удалась: {response_data}")
    
    _access_token = response_data.get("data", {}).get("access_token")
    if not _access_token:
        raise AssertionError("Токен не получен в ответе аутентификации")
    
    return _access_token


def fetch_json(url: str, headers: Dict[str, str] = None, authenticated: bool = True) -> dict:
    """
    Выполняет GET запрос и возвращает JSON ответ.
    
    Args:
        url: Полный URL для запроса
        headers: Дополнительные headers (опционально)
        authenticated: Требуется ли аутентификация (добавляет Authorization header)
        
    Returns:
        dict: Распарсенный JSON ответ
        
    Raises:
        AssertionError: Если запрос не удался
    """
    request_headers = {**DEFAULT_HEADERS}
    if headers:
        request_headers.update(headers)
    
    if authenticated and _access_token:
        request_headers["Authorization"] = f"Bearer {_access_token}"
    
    req = urllib.request.Request(url, headers=request_headers)
    
    try:
        opener = _get_opener()
        with opener.open(req, timeout=20) as response:
            return json.load(response)
    except HTTPError as exc:
        error_body = exc.read().decode() if hasattr(exc, 'read') else ""
        raise AssertionError(
            f"API запрос не удался (HTTP {exc.code}): {exc.reason}\n"
            f"URL: {url}\nОтвет: {error_body}"
        ) from exc
    except URLError as exc:
        raise AssertionError(f"API запрос не удался: {exc}") from exc


def build_api_url(endpoint: str, params: Dict[str, str]) -> str:
    """
    Конструирует URL для API запроса.
    
    Args:
        endpoint: Путь до эндпоинта (без домена)
        params: Словарь параметров запроса
        
    Returns:
        str: Полный URL
    """
    query_string = "&".join(
        f"{key}={value}" for key, value in params.items()
    )
    return f"{API_BASE_URL}{endpoint}?{query_string}"


def extract_field_from_response(
    payload: dict, field_path: str, required: bool = True
) -> Any:
    """
    Извлекает значение из вложенного поля ответа API.
    
    Args:
        payload: Ответ от API
        field_path: Путь до поля через точку (например: "data.meta.relevance")
        required: Требуется ли поле (если False, возвращает None вместо исключения)
        
    Returns:
        Any: Значение поля или None
        
    Raises:
        AssertionError: Если поле отсутствует и required=True, или status=false
    """
    if not payload.get("status"):
        raise AssertionError(f"API вернул status=false: {payload}")

    keys = field_path.split(".")
    value = payload
    
    for key in keys:
        if isinstance(value, dict):
            value = value.get(key)
        else:
            value = None
            break
    
    if value is None and required:
        raise AssertionError(
            f"Поле '{field_path}' отсутствует в ответе: {payload}"
        )
    
    return value if isinstance(value, str) else (value or "").strip()


def validate_date_format(date_str: str, expected_format: str = "%d-%m-%Y") -> datetime:
    """
    Проверяет формат даты и возвращает объект datetime.
    
    Args:
        date_str: Строка с датой
        expected_format: Ожидаемый формат даты (по умолчанию DD-MM-YYYY)
        
    Returns:
        datetime: Объект datetime
        
    Raises:
        AssertionError: Если формат даты неверный
    """
    try:
        return datetime.strptime(date_str, expected_format)
    except ValueError as exc:
        raise AssertionError(
            f"Неверный формат даты '{date_str}'. "
            f"Ожидается формат: {expected_format}"
        ) from exc


def validate_date_not_future(date_obj: datetime) -> None:
    """
    Проверяет, что дата не находится в будущем.
    
    Args:
        date_obj: Объект datetime для проверки
        
    Raises:
        AssertionError: Если дата в будущем
    """
    if date_obj > datetime.now():
        raise AssertionError(
            f"Дата актуальности в будущем: {date_obj.strftime('%d-%m-%Y')}"
        )
