from .hypothesis import CAUSAL_HYPOTHESES



def _match(record, conditions):
    for field, op, value in conditions:
        if op == ">" and not record[field] > value:
            return False
        if op == "==" and not record[field] == value:
            return False
    return True


def infer_cause(rule_id: str, record: dict):
    results = []

    for h in CAUSAL_HYPOTHESES.get(rule_id, []):
        if _match(record, h["conditions"]):
            results.append(h)

    if not results:
        return None

    return max(results, key=lambda x: x["confidence"])
