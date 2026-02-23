# agent/decision/decider.py

def make_decision(stats: dict) -> dict:
    """
    根据统计结果做最终决策
    """
    signals = []

    if stats["high_risk"] >= 5:
        signals.append("高风险订单数量过多")

    if stats["top_rule_count"] >= 10:
        signals.append("单一异常规则集中爆发")

    if stats["main_cause"] != "未推断" and stats["cause_count"] >= 5:
        signals.append("存在稳定重复的异常原因")

    if signals:
        return {
            "decision": "YES",
            "reason": "；".join(signals),
            "signal": stats
        }

    return {
        "decision": "NO",
        "reason": "系统整体风险可控，未触发人工介入阈值",
        "signal": stats
    }
