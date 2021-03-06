import json
import random
from django.http import HttpResponse

from spoon_server.database.redis_config import RedisConfig
from spoon_server.main.manager import Manager

redis = RedisConfig("127.0.0.1", 21009)


def get_keys(request):
    m = Manager(database=redis)
    return HttpResponse(json.dumps(m.get_keys()))


def fetchone_from(request):
    m = Manager(database=redis)
    target_name = request.GET.get("target", "www.baidu.com")
    filter_num = int(request.GET.get("filter", 10))
    search_name = ":".join(["spoon", target_name, "useful_proxy"])

    px_kv = m.get_all_kv_from(search_name)
    res_list = random.sample([k.decode('utf-8') for (k, v) in px_kv.items() if int(v.decode('utf-8')) > filter_num], 1)

    return HttpResponse(res_list[0])


def fetchall_from(request):
    m = Manager(database=redis)
    target_name = request.GET.get("target", "www.baidu.com")
    filter_num = int(request.GET.get("filter", 10))
    search_name = ":".join(["spoon", target_name, "useful_proxy"])

    px_kv = m.get_all_kv_from(search_name)
    res_list = [k.decode('utf-8') for (k, v) in px_kv.items() if int(v) > filter_num]

    return HttpResponse("\r\n".join(res_list))
