from diagnostics import process_stream, build_report, execution_log

LAST_NAME = "FLORES"
SEED_NUM = 6
FAVORITE_ARTIST = "ONE DIRECTION"      # change to your favorite singer/band

results = process_stream(LAST_NAME, SEED_NUM, FAVORITE_ARTIST)
report = build_report(results)

print("=== Invalid Readings Handled ===")
for e in results["errors"]:
    print(e)

print("\n=== Abnormal Condition Traces ===")
for index, value, trail in results["abnormal"]:
    print(f"Reading #{index} = {value}")
    for step in trail:
        print("  ", step)

print("\n=== Execution Log ===")
for entry in execution_log:
    print(entry)

print("\n=== Final Diagnostic Report ===")
for key, val in report.items():
    print(f"{key}: {val}")