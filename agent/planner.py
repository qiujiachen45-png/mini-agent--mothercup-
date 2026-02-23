# agent/planner.py

def plan_audit():
    """
    定义需要执行的审计规则列表
    """
    return [
        {
            "rule_id": "delay_extreme",
            "description": "极端延误订单（P95 延误）",
            "metric": "delay_hours"
        },
        {
            "rule_id": "fresh_without_coldchain",
            "description": "生鲜未冷链履约订单",
            "metric": "coldchain_flag"
        }
    ]
