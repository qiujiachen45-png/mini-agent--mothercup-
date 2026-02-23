from collections import defaultdict


def cluster_by_route(records: list):
    clusters = defaultdict(list)

    for r in records:
        key = r.get("route_type", "unknown")
        clusters[key].append(r)

    return clusters
