import json

import cpuinfo
import psutil
from psutil._common import bytes2human


def linux_print_cpu():
    # TODO: Use non retarded way of getting this
    # Apparently this just stopped working
    j = json.loads(cpuinfo.get_cpu_info_json())
    print(j["brand_raw"])
    print("Производитель: ", j["vendor_id_raw"])
    print("Архитектура: ", j["arch"])
    print("Частота: ", j["hz_advertised_friendly"])
    print("Нагрузка: ", psutil.cpu_percent(), "%")
    print("Логические процессоры: ", psutil.cpu_count())
    print("Ядер: ", psutil.cpu_count(logical=False))
    # print("Кэш L1: ", j["l1_data_cache_size"])
    try:
        print("Кэш L2: ", bytes2human(j["l2_cache_size"]))
        print("Кэш L3: ", bytes2human(j["l3_cache_size"]))
    except TypeError:
        pass
    print("Поддерживаемые инструкции: ", j["flags"])