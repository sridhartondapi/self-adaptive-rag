from langchain_community.cache import SQLiteCache
from langchain_core.globals import set_llm_cache
from retrieval.agents.config.settings import CACHE_DB_PATH

def init_llm_cache():
    path = CACHE_DB_PATH
    set_llm_cache(SQLiteCache(database_path=path))