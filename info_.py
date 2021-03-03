import json
import os
import sys
import socket
import cpuinfo
import psutil
import time
import subprocess
from print_ import print_unavailable
from datetime import datetime, date
from psutil._common import bytes2human
from psutil._compat import get_terminal_size

af_map = {
    socket.AF_INET: 'IPv4',
    socket.AF_INET6: 'IPv6',
    psutil.AF_LINK: 'MAC',
}
duplex_map = {
    psutil.NIC_DUPLEX_FULL: "full",
    psutil.NIC_DUPLEX_HALF: "half",
    psutil.NIC_DUPLEX_UNKNOWN: "?",
}


def info_cpu():
    print("Собираю информацию...")
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


# TODO:BIOS
def info_bios():
    if sys.platform == 'win32':
        print_unavailable('win')
    else:
        if os.getuid() != 0:
            print_unavailable('root')
        else:
            bios = dict()
            parameters = ["bios-vendor", "bios-release-date", "bios-version",
                          "bios-revision", "baseboard-manufacturer", "baseboard-product-name"]
            for parameter in parameters:
                string = str("dmidecode -s " + parameter)
                bios[parameter] = subprocess.check_output(string,
                                                          universal_newlines=True,
                                                          shell=True)

            print("Производитель: ", bios['vendor'],
                  "Версия: ", bios['version'],
                  "Дата: ", bios['release_date'])


def info_partitions():
    temp_line = "%-16s %10s %10s %10s %5s%% %9s  %s"
    print(temp_line % ("Раздел", "Всего", "Исп", "Свободно", "Исп ", "ФС", "Путь"))
    for part in psutil.disk_partitions():
        if sys.platform == 'win32':
            if 'cdrom' in part.opts or part.fstype == '':
                # skip cd-rom drives with no disk in it; they may raise
                # ENOENT, pop-up a Windows GUI error for a non-ready
                # partition or just hang.
                continue
        usage = psutil.disk_usage(part.mountpoint)
        print(temp_line % (
            part.device,
            bytes2human(usage.total),
            bytes2human(usage.used),
            bytes2human(usage.free),
            int(usage.percent),
            part.fstype,
            part.mountpoint))


# TODO: Disks
def info_disks():
    pass


# TODO: Keyboard(WTF is even supposed to be here?)
def info_keyboard():
    pass


# TODO: Motherboard
def info_motherboard():
    pass


# TODO Mouse
def info_mouse():
    pass


# TODO GPU
def info_gpu():
    pass


# TODO monitor(probably resolution, input type, etc)
def info_monitor():
    pass


def info_network():
    stats = psutil.net_if_stats()
    io_counters = psutil.net_io_counters(pernic=True)
    for nic, addresses in psutil.net_if_addrs().items():
        print("%s:" % nic)
        if nic in stats:
            st = stats[nic]
            print("    Параметры      : ", end='')
            print("скорость=%sMB, дуплекс=%s, mtu=%s, up=%s" % (
                st.speed, duplex_map[st.duplex], st.mtu,
                "yes" if st.isup else "no"))
        if nic in io_counters:
            io = io_counters[nic]
            print("    Входящие       : ", end='')
            print("байт=%s, пакет=%s, ошиб=%s, отброш=%s" % (
                bytes2human(io.bytes_recv), io.packets_recv, io.errin,
                io.dropin))
            print("    Исходящие      : ", end='')
            print("байт=%s, пакет=%s, ошиб=%s, отброш=%s" % (
                bytes2human(io.bytes_sent), io.packets_sent, io.errout,
                io.dropout))
        for address in addresses:
            print("    %-4s" % af_map.get(address.family, address.family), end="")
            print(" Адрес     : %s" % address.address)
            if address.broadcast:
                print("         Трансляция: %s" % address.broadcast)
            if address.netmask:
                print("    Маска подсети  : %s" % address.netmask)
            if address.ptp:
                print("      p2p       : %s" % address.ptp)
        print("")


def info_ps():
    today_day = date.today()
    temp_line = "%-10s %9s %9s %9s %9s %9s  %s"
    attrs = ['pid', 'memory_percent', 'name', 'cmdline', 'cpu_times',
             'create_time', 'memory_info', 'status', 'nice', 'username']
    print(temp_line % ("Пользователь", "PID", "%Память",
                       "Состояние", "Запущен", "Время", "Комманда"))
    for p in psutil.process_iter(attrs, ad_value=None):
        if p.info['create_time']:
            create_time = datetime.fromtimestamp(p.info['create_time'])
            if create_time.date() == today_day:
                create_time = create_time.strftime("%H:%M")
            else:
                create_time = create_time.strftime("%b%d")
        else:
            create_time = ''
        if p.info['cpu_times']:
            cpu_time = time.strftime("%M:%S",
                                     time.localtime(sum(p.info['cpu_times'])))
        else:
            cpu_time = ''

        user = p.info['username']
        if not user and psutil.POSIX:
            try:
                user = p.uids()[0]
            except psutil.Error:
                pass
        if user and psutil.WINDOWS and '\\' in user:
            user = user.split('\\')[1]
        if not user:
            user = ''
        user = user[:9]
        memp = round(p.info['memory_percent'], 1) if \
            p.info['memory_percent'] is not None else ''
        if p.info['cmdline']:
            cmdline = ' '.join(p.info['cmdline'])
        else:
            cmdline = p.info['name']
        status = p.info['status'][:5] if p.info['status'] else ''

        line = temp_line % (
            user,
            p.info['pid'],
            memp,
            status,
            create_time,
            cpu_time,
            cmdline)
        print(line[:get_terminal_size()[0]])


def info_uptime():
    print("ПК был запущен:",
          datetime.fromtimestamp(psutil.boot_time()).strftime("%d.%m.%Y %H:%M:%S"))


def info_who():
    users = psutil.users()
    for user in users:
        proc_name = psutil.Process(user.pid).name() if user.pid else ""
        print("%-12s %-10s %-10s %-14s %s" % (
            user.name,
            user.terminal or '-',
            datetime.fromtimestamp(user.started).strftime("%Y-%m-%d %H:%M"),
            "(%s)" % user.host if user.host else "",
            proc_name
        ))
