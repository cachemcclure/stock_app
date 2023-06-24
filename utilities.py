from ratelimit import limits, sleep_and_retry
from datetime import datetime


CALLS = 5
RATE_LIMIT = 61


@sleep_and_retry
@limits(calls=CALLS, period=RATE_LIMIT)
def check_limit():
    return


def log_handling(log_level: str = "ERROR", msg: str = "", log_file: str = "logs.txt"):
    out = f"{datetime.now()}: {log_level} - {msg}\n"
    with open(log_file, "a") as f:
        f.write(out)
    with open("master_logs.txt", "a") as f:
        f.write(out)
