import redis
from fastapi import Depends, FastAPI
from fastapi import FastAPI
from pydantic import BaseModel

from utils.ssq import get_by_randomorg, get_by_system, get_combinations

app = FastAPI()
rdb = redis.Redis(host="localhost", port="6379", db=0, decode_responses=True)


class Ssq(BaseModel):
    code: int
    data: dict


@app.post("/ssq", summary="获取随机双色球", response_model=Ssq)
async def get_random_ssq(method: str = "system") -> dict:
    """_summary_: 获取随机双色球

    Args:
        method (str, optional): 随机方法. 默认system,假随机; randomorg,真随机.

    Returns:
        {code: int, data: object},code=0,成功; code=1,失败.
        data: {list: 双色球，date: 日期，bouns：奖金，peopleNum：同期中奖人数}
    """
    model = Ssq(code=0, data=[], bounes=[])
    if method == "randomorg":
        sdata = get_by_randomorg()
    elif method == "system":
        sdata = get_by_system()
    else:
        sdata = []
        model.code = 1
    model.data["list"] = sdata
    key_list = get_combinations(sdata)
    bouns = []
    for key in key_list:
        bouns = rdb.lrange(key, 0, -1)
        if len(bouns) > 0:
            break
    if bouns:
        model.data["date"] = bouns[0]
        model.data["bouns"] = bouns[1]
        model.data["peopleNum"] = bouns[2]
    else:
        model.data["date"] = ""
        model.data["bouns"] = ""
        model.data["peopleNum"] = ""
    return model
