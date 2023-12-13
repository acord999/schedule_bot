from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.redis import RedisStorage, Redis
from config_data.config import load_config

redis = Redis(host=load_config().redis_config.host)
storage = RedisStorage(redis=redis)



