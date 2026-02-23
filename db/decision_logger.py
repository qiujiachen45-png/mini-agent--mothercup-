import psycopg

DB_CONFIG = dict(
    host="localhost",
    dbname="mydb",
    user="myuser",
    password="123456"
)


def write_decision_log(
    batch_id: int,
    decision_type: str,
    content: str,
    rule_id: str = None,
    related_key: str = None,
    confidence: float = None,
    agent_version: str = None
):
    conn = psycopg.connect(**DB_CONFIG)

    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO agent_decision_log
            (
                batch_id,
                decision_type,
                rule_id,
                related_key,
                content,
                confidence,
                agent_version
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                batch_id,
                decision_type,
                rule_id,
                related_key,
                content,
                confidence,
                agent_version
            )
        )

    conn.commit()
    conn.close()
