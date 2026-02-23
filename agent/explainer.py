# agent/explainer.py

def explain(rule: dict, rows: list) -> str:
    if not rows:
        return f"【{rule['rule_id']}】未发现异常。"

    return (
        f"【{rule['rule_id']}】命中异常\n"
        f"规则说明：{rule['description']}\n"
        f"异常订单数：{len(rows)}"
    )
