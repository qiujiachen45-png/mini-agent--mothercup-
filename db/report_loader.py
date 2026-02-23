from db.executor import execute_sql


def load_audit_summary(batch_id: int):
    sql = f"""
        SELECT
            COUNT(*) AS total_abnormal,
            COUNT(*) FILTER (WHERE risk_score >= 0.8) AS high_risk
        FROM audit_abnormal_records
        WHERE batch_id = {batch_id}
    """
    _, rows = execute_sql(sql)
    return rows[0][0], rows[0][1]


def load_top_problem(batch_id: int):
    sql = f"""
        SELECT rule_id, COUNT(*) AS cnt
        FROM audit_abnormal_records
        WHERE batch_id = {batch_id}
        GROUP BY rule_id
        ORDER BY cnt DESC
        LIMIT 1
    """
    _, rows = execute_sql(sql)
    if not rows:
        return "无", 0
    return rows[0][0], rows[0][1]


def load_main_cause(batch_id: int):
    sql = f"""
        SELECT cause, COUNT(*) AS cnt
        FROM audit_causal_results
        WHERE batch_id = {batch_id}
        GROUP BY cause
        ORDER BY cnt DESC
        LIMIT 1
    """
    _, rows = execute_sql(sql)
    if not rows:
        return "未推断", 0
    return rows[0][0], rows[0][1]

def load_daily_stats(batch_id: int):
    """
    汇总日报所需的全部统计信息
    """
    total_abnormal, high_risk = load_audit_summary(batch_id)
    top_rule, top_rule_count = load_top_problem(batch_id)
    main_cause, cause_count = load_main_cause(batch_id)

    return {
        "total_abnormal": total_abnormal,
        "high_risk": high_risk,
        "top_rule": top_rule,
        "top_rule_count": top_rule_count,
        "main_cause": main_cause,
        "cause_count": cause_count
    }
