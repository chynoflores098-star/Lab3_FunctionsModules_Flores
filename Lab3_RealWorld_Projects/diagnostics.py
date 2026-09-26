"""Module 2: processing, anomaly tracing, and reporting."""
import functools
from telemetry import telemetry_stream, is_abnormal, normalize, NORMAL_LIMIT

execution_log = []


def monitor(func):
    """Decorator that monitors a major processing function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        execution_log.append(f"START {func.__name__}")
        result = func(*args, **kwargs)
        execution_log.append(f"END {func.__name__}")
        return result
    return wrapper


def validate(value):
    if not isinstance(value, (int, float)):
        raise TypeError(f"non-numeric reading: {value!r}")
    if value < 0 or value > 200:
        raise ValueError(f"out-of-range reading: {value}")
    return value


def trace_abnormal(value, level=1, trail=None):
    """Recursively cool an abnormal value until it reaches the base condition."""
    if trail is None:
        trail = []
    if value <= NORMAL_LIMIT:                         # base condition
        trail.append(f"Level {level}: {value} <= {NORMAL_LIMIT} -> STABLE")
        return trail
    trail.append(f"Level {level}: {value} > {NORMAL_LIMIT} -> reduce 5%")
    return trace_abnormal(round(value * 0.95, 1), level + 1, trail)


@monitor
def process_stream(last_name, seed_num, artist):
    processed = valid = invalid = 0
    abnormal = []
    errors = []
    for raw in telemetry_stream(last_name, seed_num, artist):
        processed += 1
        try:
            value = normalize(validate(raw))
        except (TypeError, ValueError) as err:        # program keeps running
            invalid += 1
            errors.append(str(err))
            continue
        valid += 1
        if is_abnormal(value):
            abnormal.append((processed, value, trace_abnormal(value)))
    return {"processed": processed, "valid": valid, "invalid": invalid,
            "abnormal": abnormal, "errors": errors}


def overall_status(results):
    if not results["abnormal"]:
        return "NORMAL"
    ratio = len(results["abnormal"]) / max(results["valid"], 1)
    return "WARNING" if ratio <= 0.2 else "CRITICAL"


def build_report(results):
    return {
        "Processed readings": results["processed"],
        "Valid readings": results["valid"],
        "Invalid readings": results["invalid"],
        "Abnormal conditions": len(results["abnormal"]),
        "Overall status": overall_status(results),
    }