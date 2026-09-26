LAST_NAME = "FLORES"          # surname in uppercase
SEED_NUM = 6                  # last digit of student ID
FAVORITE_ARTIST = "ONE DIRECTION"     # change to your favorite singer/band

execution_log = []


def validate(name, seed, artist):
    if not name.isalpha() or not artist.replace(" ", "").isalpha():
        raise ValueError("Surname and artist must contain letters only")
    if not isinstance(seed, int) or not 0 <= seed <= 9:
        raise ValueError("SEED_NUM must be a single digit (0-9)")
    execution_log.append("validate: inputs accepted")


def generate_fault_code(name, seed, artist):
    name_sum = sum(ord(c) for c in name.upper())
    artist_sum = sum(ord(c) for c in artist.upper().replace(" ", ""))
    code = name_sum * (seed + 1) + artist_sum
    execution_log.append(f"generate_fault_code: {name_sum} x {seed + 1} + {artist_sum} = {code}")
    return code


def trace_fault(code, call=1, trace=None):
    """Recursively reduce the fault code by summing its digits."""
    if trace is None:
        trace = []
    if code < 10:                                   # base condition
        trace.append(f"Call {call}: code {code} < 10 -> ROOT FAULT")
        execution_log.append(f"trace_fault: base case reached at call {call}")
        return code, trace, call
    next_code = sum(int(d) for d in str(code))
    trace.append(f"Call {call}: code {code} -> digit sum {next_code}")
    execution_log.append(f"trace_fault: call {call} processed {code}")
    return trace_fault(next_code, call + 1, trace)   # recursive call


def main():
    try:
        validate(LAST_NAME, SEED_NUM, FAVORITE_ARTIST)
        fault_code = generate_fault_code(LAST_NAME, SEED_NUM, FAVORITE_ARTIST)
        root, trace, calls = trace_fault(fault_code)
    except (ValueError, RecursionError) as err:
        print("Trace stopped:", err)
        return

    print("=== Generated Fault Data ===")
    print("Surname:", LAST_NAME)
    print("SEED_NUM:", SEED_NUM)
    print("Favorite Artist:", FAVORITE_ARTIST)
    print("Fault Code:", fault_code)

    print("\n=== Recursive Trace ===")
    for step in trace:
        print(step)

    print("\n=== Number of Recursive Calls ===")
    print(calls)

    print("\n=== Execution Log ===")
    for entry in execution_log:
        print(entry)

    print("\n=== Final Result ===")
    print(f"Fault code {fault_code} traced to root fault {root} in {calls} calls")


main()