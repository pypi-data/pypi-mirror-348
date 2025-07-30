import random
import time


def random_wait(seconds: int) -> None:
    wait_secs = random.randint(0, seconds)
    print(f"Going to wait for {wait_secs} seconds")
    time.sleep(wait_secs)
