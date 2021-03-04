import json
import os
import subprocess

import cpuinfo
import psutil
from psutil._common import bytes2human

from print_ import print_unavailable


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


def linux_print_bios():
    if os.getuid() != 0:
        print_unavailable('root')
    else:
        bios = dict()
        dmi_id = ["bios-vendor", "bios-release-date", "bios-version",
                  "bios-revision", "baseboard-manufacturer", "baseboard-product-name",
                  "baseboard-serial-number", "processor-manufacturer", "processor-version"]
        for dmi in dmi_id:
            string = str("dmidecode -s " + dmi)
            bios[dmi] = subprocess.check_output(string,
                                                universal_newlines=True,
                                                shell=True)
        print("Изготовитель: ", bios[dmi_id[4]],
              "Наименование продукта: ", bios[dmi_id[5]],
              "Поставщик BIOS: ", bios[dmi_id[0]],
              "Версия: ", bios[dmi_id[2]],
              "Дата: ", bios[dmi_id[1]],
              "Серийный номер: ", bios[dmi_id[6]],
              "Изготовитель процессора: ", bios[dmi_id[7]],
              "Версия процесссора: ", bios[dmi_id[8]])


def linux_print_disks():
    pass


def linux_print_mb():
    pass


def linux_print_gpu():
    # TODO: GPU info on Linux
    print_unavailable("linux")


def linux_print_monitor():
    pass