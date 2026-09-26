"""Module 1: generates the student-specific telemetry stream."""

NORMAL_LIMIT = 100                      # readings above this are abnormal
is_abnormal = lambda v: v > NORMAL_LIMIT          # lambda filter
normalize = lambda v: round(v, 1)                 # lambda transform


def build_seed(last_name, seed_num, artist):
    name_sum = sum(ord(c) for c in last_name.upper())
    artist_sum = sum(ord(c) for c in artist.upper().replace(" ", ""))
    return name_sum * (seed_num + 1) + artist_sum


def telemetry_stream(last_name, seed_num, artist, count=30):
    """Generator: yields one raw reading at a time (nothing is stored)."""
    state = build_seed(last_name, seed_num, artist)
    for i in range(1, count + 1):
        state = (state * 1103515245 + 12345) % (2 ** 31)
        value = 50 + (state % 700) / 10          # 50.0 to 119.9
        if i % 9 == 0:
            yield None                            # missing sensor data
        elif i % 13 == 0:
            yield -999                            # sensor fault
        else:
            yield value