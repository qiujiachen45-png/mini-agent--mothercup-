# safety/config.py

FORBIDDEN_KEYWORDS = [
    "delete",
    "update",
    "insert",
    "drop",
    "alter",
    "truncate"
]


def check_sql_safe(sql: str):
    lower = sql.lower()
    for kw in FORBIDDEN_KEYWORDS:
        if kw in lower:
            raise ValueError(f"Forbidden SQL keyword detected: {kw}")
