"""
Конфигурация API-тестов реестров (все рабочие эндпоинты, протестированные 19-01-2026).

Структура:
- Все эндпоинты протестированы и возвращают валидные даты в meta.relevance
- Организованы по категориям: Предприятие, Финансы, Закупки, Руководитель
- Всего: 54 эндпоинта (31 Company + 8 Finance + 11 Procurement + 4 Director)

Примечание: не все 117 "реестров" = 117 эндпоинтов. Один реестр часто = short + more + graph вариации.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Данные для аутентификации
API_USERNAME = os.getenv("API_USERNAME", "22773@adata.kz")
API_PASSWORD = os.getenv("API_PASSWORD", "Cntgfy555@")

# Рабочие реестры по категориям (только протестированные эндпоинты с валидными датами)
REGISTRIES = {
    # ========================= ПРЕДПРИЯТИЕ (30 эндпоинтов) =========================
    # Банкротство / ликвидация / реабилитация
    "bankruptcy_kgd": {
        "endpoint": "/api/v1/data/company/bankruptcy/kgd/short",
        "bin": "200140023023",
        "relevance_field": "data.meta.relevance",
        "description": "Предприятие | Реестр банкротства (КГД)",
    },
    "liquidating_taxpayer": {
        "endpoint": "/api/v1/data/company/liquidating-taxpayer",
        "bin": "200140023023",
        "relevance_field": "data.meta.relevance",
        "description": "Предприятие | Ликвидируемые налогоплательщики",
    },
    "announcement_cases": {
        "endpoint": "/api/v1/data/company/trustworthy/announcement-cases/short",
        "bin": "200140023023",
        "relevance_field": "data.meta.relevance",
        "description": "Предприятие | Объявления (банкротство/реабилитация/собрания кредиторов)",
    },
    
    # Проверки / надзор
    "custom_inspection": {
        "endpoint": "/api/v1/data/company/custom-inspection/short",
        "bin": "200140023023",
        "relevance_field": "data.meta.relevance",
        "description": "Предприятие | Таможенные проверки и выездные проверки",
    },
    "control_supervision": {
        "endpoint": "/api/v1/data/company/control-supervision/short",
        "bin": "200140023023",
        "relevance_field": "data.meta.relevance",
        "description": "Предприятие | Профилактический контроль и надзор",
    },
    "labor_inspection": {
        "endpoint": "/api/v1/data/company/labor-inspection/short",
        "bin": "200140023023",
        "relevance_field": "data.meta.relevance",
        "description": "Предприятие | Проверки по труду",
    },
    
    # Надёжность / риски / признаки
    "trustworthy_inactivity": {
        "endpoint": "/api/v1/data/company/trustworthy/inactivity",
        "bin": "200140023023",
        "relevance_field": "data.meta.relevance",
        "description": "Предприятие | Бездействующее предприятие",
    },
    "trustworthy_unreliability": {
        "endpoint": "/api/v1/data/company/trustworthy/unreliability",
        "bin": "200140023023",
        "relevance_field": "data.meta.relevance",
        "description": "Предприятие | Лжепредприятие / недостоверность / отсутствует по адресу",
    },
    
    # Аресты / запреты / обременения
    "share_arrest": {
        "endpoint": "/api/v1/data/company/share-arrest/short",
        "bin": "200140023023",
        "relevance_field": "data.meta.relevance",
        "description": "Предприятие | Обременение долей",
    },
    "arrest": {
        "endpoint": "/api/v1/data/company/arrest/short",
        "bin": "200140023023",
        "relevance_field": "data.meta.relevance",
        "description": "Предприятие | Аресты (счета, имущество, транспорт, запреты)",
    },
    
    # Санкции
    "sanction": {
        "endpoint": "/api/v1/data/company/sanction/short",
        "bin": "200140023023",
        "relevance_field": "data.meta.relevance",
        "description": "Предприятие | Санкции (основная информация)",
    },
    "sanction_graph": {
        "endpoint": "/api/v1/data/company/sanction/graph",
        "bin": "200140023023",
        "relevance_field": "data.meta.relevance",
        "description": "Предприятие | Санкции (график по времени)",
    },
    
    # Массовый адрес
    "mass_address": {
        "endpoint": "/api/v1/data/company/mass-address/short",
        "bin": "200140023023",
        "relevance_field": "data.meta.relevance",
        "description": "Предприятие | Массовый адрес",
    },
    
    # Административные штрафы
    "fine": {
        "endpoint": "/api/v1/data/company/fine/short",
        "bin": "200140023023",
        "relevance_field": "data.meta.relevance",
        "description": "Предприятие | Административные штрафы (основное)",
    },
    "fine_more": {
        "endpoint": "/api/v1/data/company/fine/more",
        "bin": "200140023023",
        "relevance_field": "data.meta.relevance",
        "description": "Предприятие | Административные штрафы (подробно)",
    },
    "fine_graph": {
        "endpoint": "/api/v1/data/company/fine/graph",
        "bin": "200140023023",
        "relevance_field": "data.meta.relevance",
        "description": "Предприятие | Административные штрафы (график)",
    },
    "fine_qualifications": {
        "endpoint": "/api/v1/data/company/fine/qualifications-list",
        "bin": "200140023023",
        "relevance_field": "data.meta.relevance",
        "description": "Предприятие | Классификация административных штрафов",
    },
    
    # История и статистика
    "history_graph": {
        "endpoint": "/api/v1/data/company/history/graph",
        "bin": "200140023023",
        "relevance_field": "data.meta.relevance",
        "description": "Предприятие | История (график по времени)",
    },
    "history_trustworthy_counts": {
        "endpoint": "/api/v1/data/company/history/trustworthy/counts",
        "bin": "200140023023",
        "relevance_field": "data.meta.relevance",
        "description": "Предприятие | История надежности (счёты событий)",
    },
    "history_trustworthy_details": {
        "endpoint": "/api/v1/data/company/history/trustworthy/details",
        "bin": "200140023023",
        "relevance_field": "data.meta.relevance",
        "description": "Предприятие | История надежности (детали событий)",
    },
    
    # Основные данные
    "company_short": {
        "endpoint": "/api/v1/data/company/short",
        "bin": "200140023023",
        "relevance_field": "data.meta.relevance",
        "description": "Предприятие | Информация о компании (краткая)",
    },
    "director_company": {
        "endpoint": "/api/v1/data/company/director-company/short",
        "bin": "200140023023",
        "relevance_field": "data.meta.relevance",
        "description": "Предприятие | Информация о директоре компании",
    },
    "founders_list": {
        "endpoint": "/api/v1/data/company/founders/list-info",
        "bin": "200140023023",
        "relevance_field": "data.meta.relevance",
        "description": "Предприятие | Список учредителей",
    },
    "same_counterparty": {
        "endpoint": "/api/v1/data/same-counterparty/unreliable-companies",
        "bin": "200140023023",
        "relevance_field": "data.meta.relevance",
        "description": "Предприятие | Контрагенты (проблемные компании рядом)",
    },
    
    # Риск и степень
    "risk_degree": {
        "endpoint": "/api/v1/data/company/risk-degree/short",
        "bin": "200140023023",
        "relevance_field": "data.meta.relevance",
        "description": "Предприятие | Степень риска налогоплательщика",
    },
    
    # Финансовая задолженность
    "enforcement_debt": {
        "endpoint": "/api/v1/data/company/enforcement-debt/short",
        "bin": "200140023023",
        "relevance_field": "data.meta.relevance",
        "description": "Предприятие | Долги по исполнительным производствам",
    },
    "tax_debt": {
        "endpoint": "/api/v1/data/company/tax-debt/short",
        "bin": "200140023023",
        "relevance_field": "data.meta.relevance",
        "description": "Предприятие | Налоговая задолженность",
    },
    "tax_debt_more": {
        "endpoint": "/api/v1/data/company/tax-debt/more",
        "bin": "200140023023",
        "relevance_field": "data.meta.relevance",
        "description": "Предприятие | Налоговая задолженность (подробно)",
    },
    
    # Специальные реестры
    "fin_pyramids": {
        "endpoint": "/api/v1/data/company/fin-pyramids/short",
        "bin": "200140023023",
        "relevance_field": "data.meta.relevance",
        "description": "Предприятие | Финансовые пирамиды (АФМ)",
    },
    "foreign_income": {
        "endpoint": "/api/v1/data/company/foreign-income/short",
        "bin": "200140023023",
        "relevance_field": "data.meta.relevance",
        "description": "Предприятие | Иностранные доходы",
    },
    
    # ========================= ФИНАНСЫ (8 эндпоинтов) =========================
    "director_enforcement_debt": {
        "endpoint": "/api/v1/data/director/enforcement-debt/short",
        "bin": "200140023023",
        "relevance_field": "data.meta.relevance",
        "description": "Финансы | Директор - исполнительные производства",
    },
    "director_tax_debt": {
        "endpoint": "/api/v1/data/director/tax-debt/short",
        "bin": "200140023023",
        "relevance_field": "data.meta.relevance",
        "description": "Финансы | Директор - налоговая задолженность",
    },
    "taxpayers_large": {
        "endpoint": "/api/v1/data/company/zakup/taxpayers-large/short",
        "bin": "200140023023",
        "relevance_field": "data.meta.relevance",
        "description": "Финансы | Крупные налогоплательщики, подлежащие мониторингу",
    },
    "taxpayers_workless": {
        "endpoint": "/api/v1/data/company/zakup/taxpayers-workless/short",
        "bin": "200140023023",
        "relevance_field": "data.meta.relevance",
        "description": "Финансы | Сделки без фактического выполнения работ",
    },
    "employee_count": {
        "endpoint": "/api/v1/data/company/employee/count/short",
        "bin": "200140023023",
        "relevance_field": "data.meta.relevance",
        "description": "Финансы | Количество сотрудников",
    },
    "employee_count_graph": {
        "endpoint": "/api/v1/data/company/employee/count/graph",
        "bin": "200140023023",
        "relevance_field": "data.meta.relevance",
        "description": "Финансы | Количество сотрудников (график)",
    },
    "company_founder_trustworthy": {
        "endpoint": "/api/v1/data/company/founder/trustworthy",
        "bin": "200140023023",
        "relevance_field": "data.meta.relevance",
        "description": "Финансы | Учредитель - флаги надежности",
    },
    "company_history_trustworthy_counts": {
        "endpoint": "/api/v1/data/company/history/trustworthy/counts",
        "bin": "200140023023",
        "relevance_field": "data.meta.relevance",
        "description": "Финансы | История счётов надежности компании",
    },
    
    # ========================= ЗАКУПКИ (11 эндпоинтов) =========================
    "zakup_unreliable_national_bank": {
        "endpoint": "/api/v1/data/company/zakup/unreliable-national-bank/short",
        "bin": "200140023023",
        "relevance_field": "data.meta.relevance",
        "description": "Закупки | Ненадежные поставщики (Национальный Банк)",
    },
    "zakup_unreliable_samruk": {
        "endpoint": "/api/v1/data/company/zakup/unreliable-samruk/short",
        "bin": "200140023023",
        "relevance_field": "data.meta.relevance",
        "description": "Закупки | Ненадежные поставщики (Самрук-Казына)",
    },
    "zakup_unreliable_mitwork": {
        "endpoint": "/api/v1/data/company/zakup/unreliable-mitwork/short",
        "bin": "200140023023",
        "relevance_field": "data.meta.relevance",
        "description": "Закупки | Ненадежные поставщики (MITWORK)",
    },
    "zakup_unreliable_nis": {
        "endpoint": "/api/v1/data/company/zakup/unreliable-nis/short",
        "bin": "200140023023",
        "relevance_field": "data.meta.relevance",
        "description": "Закупки | Ненадежные поставщики (НИС)",
    },
    "zakup_unreliable_nu": {
        "endpoint": "/api/v1/data/company/zakup/unreliable-nu/short",
        "bin": "200140023023",
        "relevance_field": "data.meta.relevance",
        "description": "Закупки | Ненадежные поставщики (НУ)",
    },
    "zakup_nadloc": {
        "endpoint": "/api/v1/data/company/zakup/nadloc/short",
        "bin": "200140023023",
        "relevance_field": "data.meta.relevance",
        "description": "Закупки | NADLoC (добросовестные участники)",
    },
    "zakup_fms": {
        "endpoint": "/api/v1/data/company/zakup/fms/short",
        "bin": "200140023023",
        "relevance_field": "data.meta.relevance",
        "description": "Закупки | ФМС",
    },
    "zakup_unreliable_goszakup": {
        "endpoint": "/api/v1/data/company/zakup/unreliable-goszakup/short",
        "bin": "200140023023",
        "relevance_field": "data.meta.relevance",
        "description": "Закупки | Ненадежные поставщики (Госзакупки РК)",
    },
    "zakup_samruk": {
        "endpoint": "/api/v1/data/company/zakup/samruk/short",
        "bin": "200140023023",
        "relevance_field": "data.meta.relevance",
        "description": "Закупки | Самрук-Казына (участник/добросовестный)",
    },
    "zakup_goszakup": {
        "endpoint": "/api/v1/data/company/zakup/goszakup/short",
        "bin": "200140023023",
        "relevance_field": "data.meta.relevance",
        "description": "Закупки | Государственные закупки РК (ТОП-100, участник)",
    },
    "zakup_samruk_software": {
        "endpoint": "/api/v1/data/company/zakup/samruk/software",
        "bin": "200140023023",
        "relevance_field": "data.meta.relevance",
        "description": "Закупки | Доверенное ПО и электропром (Самрук)",
    },
    
    # ========================= РУКОВОДИТЕЛЬ (4 эндпоинта) =========================
    "director_arrest": {
        "endpoint": "/api/v1/data/director/arrest/short",
        "bin": "200140023023",
        "relevance_field": "data.meta.relevance",
        "description": "Руководитель | Аресты",
    },
    "director_terrorism": {
        "endpoint": "/api/v1/data/director/terrorism/short",
        "bin": "200140023023",
        "relevance_field": "data.meta.relevance",
        "description": "Руководитель | Финансирование терроризма/экстремизма",
    },
    "director_wanted": {
        "endpoint": "/api/v1/data/director/wanted/short",
        "bin": "200140023023",
        "relevance_field": "data.meta.relevance",
        "description": "Руководитель | В розыске",
    },
    "director_court_case": {
        "endpoint": "/api/v1/data/director/court-case/short",
        "bin": "200140023023",
        "relevance_field": "data.meta.relevance",
        "description": "Руководитель | Судебные дела",
    },
}

# Параметры по умолчанию для запросов
DEFAULT_PARAMS = {
    "initial": "1",

}

# Формат даты актуальности в API
DATE_FORMAT = "%d-%m-%Y"

# Статистика:
# Всего эндпоинтов: 53
# - Предприятие: 30 (банкротство, проверки, надежность, аресты, санкции, штрафы, история, основные данные)
# - Финансы: 8 (директор-долги, крупные налогоплательщики, история)
# - Закупки: 11 (ненадежные/добросовестные на разных площадках)
# - Руководитель: 4 (аресты, терроризм, розыск, суд)
#
# Примечание: Учредитель (30 в UI) покрывается через:
# - /api/v1/data/company/founders/list-info (в Предприятие)
# - /api/v1/data/company/founder/trustworthy (в Финансы)
# - /api/v1/data/same-counterparty/unreliable-companies (в Предприятие)
