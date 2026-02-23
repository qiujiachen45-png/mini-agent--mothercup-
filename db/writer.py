# db/writer.py
import json
import psycopg

DB_CONFIG = dict(
    host="localhost",
    dbname="mydb",
    user="myuser",
    password="123456"
)

#插入日志内容
#结构如下
#batch_id	agent_version	created_at	status
#100	v2.0.9	2024-01-01	active
def create_audit_batch(agent_version: str):
    conn = psycopg.connect(**DB_CONFIG)

    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO audit_batch (agent_version)
            VALUES (%s)
            RETURNING batch_id
            """,
            (agent_version,)
        )
        batch_id = cur.fetchone()[0]

    conn.commit()
    conn.close()
    return batch_id


def finish_audit_batch(batch_id: int):
    conn = psycopg.connect(**DB_CONFIG)

    with conn.cursor() as cur:
        cur.execute(
            """
            UPDATE audit_batch
            SET finished_at = CURRENT_TIMESTAMP
            WHERE batch_id = %s
            """,
            (batch_id,)

        )

    conn.commit()
    conn.close()


def write_abnormal_records(batch_id: int, rule: dict, rows: list):
    conn = psycopg.connect(**DB_CONFIG)

    sql = """
        INSERT INTO audit_abnormal_records
        (
            batch_id,
            rule_id,
            rule_desc,
            shipment_id,
            metric_name,
            metric_value
        )
        VALUES (%s, %s, %s, %s, %s, %s)
    """

    with conn.cursor() as cur:
        for row in rows:
            cur.execute(
                sql,
                (
                    batch_id,
                    rule["rule_id"],
                    rule["description"],
                    row[0],
                    rule["metric"],
                    row[1]
                )
            )


# 在原文件末尾追加即可

def update_risk_score(batch_id, shipment_id, risk_score):
    conn = psycopg.connect(**DB_CONFIG)

    with conn.cursor() as cur:
        cur.execute(
            """
            UPDATE audit_abnormal_records
            SET risk_score = %s
            WHERE batch_id = %s AND shipment_id = %s
            """,
            (risk_score, batch_id, shipment_id)
        )

def write_causal_result(batch_id, rule_id, shipment_id, cause, confidence):
    conn = psycopg.connect(**DB_CONFIG)

    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO audit_causal_result
            (batch_id, shipment_id, rule_id, inferred_cause, confidence)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (batch_id, shipment_id, rule_id, cause, confidence)
        )


def write_problem_cluster(batch_id, rule_id, cluster_key, count):
    conn = psycopg.connect(**DB_CONFIG)

    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO audit_problem_cluster
            (batch_id, rule_id, cluster_key, shipment_count)
            VALUES (%s, %s, %s, %s)
            """,
            (batch_id, rule_id, cluster_key, count)
        )

def write_decision_log(batch_id: int, decision: dict):
        conn = psycopg.connect(**DB_CONFIG)

        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO audit_decision_log
                (batch_id, decision, reason, signal)
                VALUES (%s, %s, %s, %s)
                """,
                (
                    batch_id,
                    decision["decision"],
                    decision["reason"],
                    json.dumps(decision["signal"], ensure_ascii=False)
                )
            )

        conn.commit()
        conn.close()

