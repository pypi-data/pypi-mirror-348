from collections import defaultdict

_grouped = defaultdict(lambda: {
    "type": "aggregated_request",
    "service": None,
    "path": None,
    "method": None,
    "request_count": 0,
    "error_count": 0,
    "total_duration": 0.0,
    "max_duration": 0.0
})

def record(metric):
    if metric.get("type") != "request":
        return

    key = f"{metric.get('service')}|{metric.get('path')}|{metric.get('method')}"
    group = _grouped[key]
    group["service"] = metric.get("service")
    group["path"] = metric.get("path")
    group["method"] = metric.get("method")
    group["request_count"] += 1

    if metric.get("statusCode", 0) >= 500:
        group["error_count"] += 1

    duration = float(metric.get("duration", 0))
    group["total_duration"] += duration
    group["max_duration"] = max(group["max_duration"], duration)

def flush():
    results = []
    for group in _grouped.values():
        count = group["request_count"]
        results.append({
            "type": group["type"],
            "service": group["service"],
            "path": group["path"],
            "method": group["method"],
            "request_count": count,
            "error_count": group["error_count"],
            "avg_duration": round(group["total_duration"] / count, 2),
            "max_duration": round(group["max_duration"], 2)
        })
    _grouped.clear()
    return results
