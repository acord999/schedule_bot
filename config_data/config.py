from dataclasses import dataclass
from environs import Env


@dataclass
class DatabaseConfig:
    database: str  # Название базы данных
    db_host: str  # URL-адрес базы данных
    db_user: str  # Username пользователя базы данных
    db_password: str  # Пароль к базе данных


@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм-боту
    admin_ids: list[int]  # Список id администраторов бота
    orders_chanel: [int]  # Группа, в которую будут приходить заказы


@dataclass
class RedisConfig:
    host: str


@dataclass
class Parser:
    cfsrtoken: str


@dataclass
class GoogleCalendar:
    scopes: str
    filepath: str
    calendar_id: str


@dataclass
class Config:
    tg_bot: TgBot
    db: DatabaseConfig
    redis_config: RedisConfig
    parser: Parser
    google_calendar: GoogleCalendar


# Создаем экземпляр класса Env
env: Env = Env()

# Добавляем в переменные окружения данные, прочитанные из файла .env
env.read_env()

# Создаем экземпляр класса Config и наполняем его данными из переменных окружения
config = Config(
    tg_bot=TgBot(
        token=env('BOT_TOKEN'),
        admin_ids=list(map(int, env.list('ADMIN_IDS'))),
        orders_chanel=int(env('ORDERS_CHANEL'))
    ),
    db=DatabaseConfig(
        database=env('DATABASE'),
        db_host=env('DB_HOST'),
        db_user=env('DB_USER'),
        db_password=env('DB_PASSWORD')

    ),
    redis_config=RedisConfig(
        host=env("REDIS_HOST")
    ),
    parser=Parser(
        cfsrtoken=env('CSRFTOKEN')
    ),
    google_calendar=GoogleCalendar(
        scopes=env("SCOPES"),
        filepath=env("FILEPATH"),
        calendar_id=env("CALENDAR_ID")
    )
)


def load_config(path: str = ".env") -> Config:
    env: Env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN'),
            admin_ids=list(map(int, env.list('ADMIN_IDS'))),
            orders_chanel=int(env('ORDERS_CHANEL'))
        ),
        db=DatabaseConfig(
            database=env('DATABASE'),
            db_host=env('DB_HOST'),
            db_user=env('DB_USER'),
            db_password=env('DB_PASSWORD')
        ),
        redis_config=RedisConfig(
            host=env("REDIS_HOST")
        ),

        parser=Parser(
            cfsrtoken=env('CSRFTOKEN')
        ),
        google_calendar=GoogleCalendar(
            scopes=env("SCOPES"),
            filepath=env("FILEPATH"),
            calendar_id=env("CALENDAR_ID")
        )
    )


def DATABASE_URL_asyncpg(config_data: Config = load_config()) -> str:
    # postgresql+asyncpg://postgres:postgres@localhost:5432/sa
    db = config_data.db
    return f"postgresql+asyncpg://" \
           f"{db.db_user}:{db.db_password}@{db.db_host}/{db.database}"


def DATABASE_URL_psycopg(config_data: Config = load_config()) -> str:
    # DSN
    # postgresql+psycopg://postgres:postgres@localhost:5432/sa
    db = config_data.db
    return f"postgresql+psycopg://" \
           f"{db.db_user}:{db.db_password}@{db.db_host}/{db.database}"
