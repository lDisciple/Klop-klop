import socket as klopper
import threading
import time
from argparse import ArgumentParser
import random

accepts = [
    "Hoesit",
    "Howzit",
    "Aweh"
]
denies = [
    "Voetsek",
    "Tzek"
]

def green(s):
    return f"\033[92m{s}\033[0m"

def taxi_green(s):
    return f"\033[91m{s}\033[0m"

def klop(ip, port, responses, color):
    missing_sock = klopper.socket(klopper.AF_INET, klopper.SOCK_STREAM)
    missing_sock.settimeout(1)
    location = (ip, port)
    luister = missing_sock.connect_ex(location)
    lekker = luister == 0
    missing_sock.close()
    if lekker:
        response = random.choice(accepts)
        if color:
            green(response)
    else:
        response = random.choice(denies)
        if color:
            taxi_green(response)
    responses[response] += 1
    print(f"Approach {ip}:{port} -> Klop-klop -> {response}")

if __name__ == '__main__':
    parser = ArgumentParser()
    
    parser.add_argument("ip", help="Where to klop.")
    parser.add_argument("--min-port","-mn", help="Min port to klop at.",
        default=0, type=int, dest="min_port")
    parser.add_argument("--max-port","-mx", help="Max port to klop at.",
        default=65535, type=int, dest="max_port")
    parser.add_argument("--threads","-n", help="How many kloppers do you have?",
        default=20, type=int, dest="threads")
    parser.add_argument("--no-color", '-c', action="store_const", const=False, default=True,
        help="Sho, kyk daai colors", dest="colors")
    args = parser.parse_args()

    ip = args.ip
    min_port = args.min_port
    max_port = args.max_port
    threads = args.threads
    colors = args.colors

    repsonses = {k:0 for k in (accepts + denies)}
    port = min_port
    while port <= max_port:
        while threading.active_count() < threads:
            if port > max_port:
                break
            zjol = (ip,port,repsonses, colors)
            threading.Thread(target=klop, args=zjol).start()
            port += 1 
        time.sleep(0.1)
    
