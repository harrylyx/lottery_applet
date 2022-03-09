import re
import random
import requests
from bs4 import BeautifulSoup
from itertools import combinations


def get_by_randomorg():
    r = requests.get("https://www.random.org/quick-pick/?tickets=1&lottery=6x33.1x16")
    soup = BeautifulSoup(r.text, features="lxml")

    ssq_random = soup.pre.text.strip()
    ssq_random = ssq_random.split("\n")

    ssq_random = [re.split("-| / ", line) for line in ssq_random][0]
    return ssq_random


def get_by_system():
    ssq_system = []
    for _ in range(6):
        ssq_system.append(f"{random.randint(1, 33):02d}")
    ssq_system = sorted(ssq_system)
    ssq_system.append(f"{random.randint(1, 16):02d}")
    return ssq_system


def get_combinations(ball_list):
    key_list = []
    # 一等奖
    key_list.append("".join(ball_list))
    # 二等奖
    key_list.append("".join(ball_list[:6]))
    # 三等奖
    key_list.extend(
        ["".join(x) + f"{ball_list[-1]}" for x in combinations(ball_list[:6], 5)]
    )
    # 四等奖
    key_list.extend(["".join(x) for x in combinations(ball_list[:6], 5)])
    key_list.extend(
        ["".join(x) + f"{ball_list[-1]}" for x in combinations(ball_list[:6], 4)]
    )
    # 五等奖
    key_list.extend(["".join(x) for x in combinations(ball_list[:6], 4)])
    key_list.extend(
        ["".join(x) + f"{ball_list[-1]}" for x in combinations(ball_list[:6], 3)]
    )
    return key_list


if __name__ == "__main__":
    # ssq_random = get_by_randomorg()
    # print(ssq_random)

    ssq_system = get_by_system()
    print(ssq_system)
