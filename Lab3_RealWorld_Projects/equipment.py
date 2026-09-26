import functools

LAST_NAME = "FLORES"          
SEED_NUM = 6                 
FAVORITE_ARTIST = "ONE DIRECTION"     

execution_log = []


def record(func):
    """Decorator that records each diagnostic step."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            execution_log.append(f"{func.__name__}: SUCCESS")
            return result
        except Exception as e:
            execution_log.append(f"{func.__name__}: FAILED ({e})")
            raise
    return wrapper


@record
def generate_readings(last_name, seed, artist):
    name_sum = sum(ord(c) for c in last_name)
    artist_sum = sum(ord(c) for c in artist.upper())
    return {
        "Temperature (C)": 40 + (name_sum % 50) + seed,
        "Pressure (psi)": 20 + (artist_sum % 60) + seed,
        "Vibration (mm/s)": round(1 + ((name_sum + artist_sum) % 100) / 10 + seed / 10, 1),
        "Voltage (V)": 200 + ((name_sum * seed) % 40),
    }


@record
def validate(readings):
    limits = {
        "Temperature (C)": (0, 150),
        "Pressure (psi)": (0, 150),
        "Vibration (mm/s)": (0, 20),
        "Voltage (V)": (100, 300),
    }
    results = {}
    for key, value in readings.items():
        if not isinstance(value, (int, float)):
            raise TypeError(f"{key} must be numeric")
        low, high = limits[key]
        if not low <= value <= high:
            raise ValueError(f"{key} out of range: {value}")
        results[key] = "VALID"
    return results


@record
def calculate(readings):
    values = list(readings.values())
    return {
        "Total": round(sum(values), 2),
        "Average": round(sum(values) / len(values), 2),
        "Highest": max(values),
        "Lowest": min(values),
    }


@record
def classify(stats):
    avg = stats["Average"]
    if avg < 70:
        return "NORMAL"
    elif avg < 120:
        return "WARNING"
    return "CRITICAL"


def main():
    try:
        readings = generate_readings(LAST_NAME, SEED_NUM, FAVORITE_ARTIST)
        validation = validate(readings)
        stats = calculate(readings)
        status = classify(stats)
    except (ValueError, TypeError) as err:
        print("Diagnostic stopped:", err)
        return

    print("=== Generated Equipment Data ===")
    for k, v in readings.items():
        print(f"{k}: {v}")

    print("\n=== Validation Results ===")
    for k, v in validation.items():
        print(f"{k}: {v}")

    print("\n=== Diagnostic Results ===")
    for k, v in stats.items():
        print(f"{k}: {v}")
    print("Status:", status)

    print("\n=== Summary ===")
    print(f"{len(execution_log)} steps completed for {LAST_NAME} (seed {SEED_NUM}, "
          f"artist {FAVORITE_ARTIST}): equipment status is {status} "
          f"with an average reading of {stats['Average']}")


main()