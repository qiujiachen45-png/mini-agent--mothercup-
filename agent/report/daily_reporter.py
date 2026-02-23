# agent/report/daily_reporter.py

def generate_daily_report(stats: dict) -> str:
    """
    只负责把统计结果翻译成人能读懂的日报
    不做任何数据库访问
    """

    return f"""
📊 数据库健康简报

- 异常订单总数：{stats['total_abnormal']}
- 高风险订单数：{stats['high_risk']}
- 最频繁问题：{stats['top_rule']}（{stats['top_rule_count']} 单）
- 主要推断原因：{stats['main_cause']}（{stats['cause_count']} 次）

系统建议：
{"⚠️ 建议人工介入排查" if stats['high_risk'] > 0 else "✅ 当前系统状态稳定"}
""".strip()
