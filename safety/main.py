# safety/main.py

from safety.config import check_sql_safe

def safe_execute(sql: str, executor):
    check_sql_safe(sql)
    return executor(sql)
