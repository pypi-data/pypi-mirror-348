import atexit
import requests
from requests.auth import HTTPBasicAuth
import RPi.GPIO as GPIO
import time
import json
import os


PID_FILE = "./watring_pid.txt"


def pid_exists(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    else:
        return True


def create_pid_file() -> None:
    if os.path.isfile(PID_FILE):
        with open(PID_FILE) as f:
            try:
                mypid = int(f.readline())
            except RuntimeError:
                print(f"Error: cannot read value from {PID_FILE}")
                remove_pid_file()
                exit(1)
        print(f"{PID_FILE} already exists with pid {mypid}")
        if pid_exists(mypid):
            print(f"and process with {mypid} is running - bye")
            exit(0)
        else:
            print(f"but there is no process with {mypid} - deleting {PID_FILE}")
            remove_pid_file()

    mypid = os.getpid()
    with open(PID_FILE, "w") as f:
        f.write(f"{mypid}")

    atexit.register(remove_pid_file)


def remove_pid_file() -> None:
    os.unlink(PID_FILE)


def close_entry(server: str, item: dict, user: str, password: str) -> None:
    url = f"{server}/api/watering_queue/update/{item['id']}/"
    headers = {"Content-type": "application/json", "Accept": "*/*"}
    data = {"status": 1}
    r = requests.patch(
        url, data=json.dumps(data), headers=headers, auth=HTTPBasicAuth(user, password)
    )
    print(r.text)


def do_watering(server: str, client_no: int, user: str, password: str) -> None:
    url = f"{server}/api/watering_queue/{client_no}/"
    headers = {"Content-type": "application/json", "Accept": "*/*"}
    r = requests.get(url, headers=headers, auth=HTTPBasicAuth(user, password))
    if r.status_code == 200:
        for p in r.json():
            print(p)
            print(
                f"Watering plant {p['plant']['name']} {p['topping_in_seconds']} s pin {p['plant']['gpio_pin']}"
            )

            close_entry(server, p, user, password)

            pin_no = p["plant"]["gpio_pin"]
            time_in_sec = p["topping_in_seconds"]

            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)

            GPIO.setup(pin_no, GPIO.OUT)

            GPIO.output(pin_no, GPIO.HIGH)
            time.sleep(time_in_sec)
            GPIO.output(pin_no, GPIO.LOW)
            time.sleep(1)
    else:
        print(f"Status code = {r.status_code}")


def main(args) -> None:
    create_pid_file()
    do_watering(args.server, args.client_number, args.user, args.password)
