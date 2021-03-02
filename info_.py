import datetime
import json
import os
import socket
import cpuinfo
import psutil
from psutil._common import bytes2human

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
    print("Кэш L2: ", bytes2human(j["l2_cache_size"]))
    print("Кэш L3: ", bytes2human(j["l3_cache_size"]))
    print("Поддерживаемые инструкции: ", j["flags"])


def info_bios():
    pass


def info_partitions():
    templ = "%-16s %10s %10s %10s %5s%% %9s  %s"
    print(templ % ("Раздел", "Всего", "Исп", "Свободно", "Исп ", "ФС", "Путь"))
    for part in psutil.disk_partitions():
        if os.name == 'nt':
            if 'cdrom' in part.opts or part.fstype == '':
                # skip cd-rom drives with no disk in it; they may raise
                # ENOENT, pop-up a Windows GUI error for a non-ready
                # partition or just hang.
                continue
        usage = psutil.disk_usage(part.mountpoint)
        print(templ % (
            part.device,
            bytes2human(usage.total),
            bytes2human(usage.used),
            bytes2human(usage.free),
            int(usage.percent),
            part.fstype,
            part.mountpoint))


def info_disks():
    pass


def info_keyboard():
    pass


def info_motherboard():
    pass


def info_mouse():
    pass


def info_gpu():
    pass


def info_monitor():
    pass


def info_network():
    stats = psutil.net_if_stats()
    io_counters = psutil.net_io_counters(pernic=True)
    for nic, addrs in psutil.net_if_addrs().items():
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
        for addr in addrs:
            print("    %-4s" % af_map.get(addr.family, addr.family), end="")
            print(" Адрес     : %s" % addr.address)
            if addr.broadcast:
                print("         Трансляция: %s" % addr.broadcast)
            if addr.netmask:
                print("    Маска подсети  : %s" % addr.netmask)
            if addr.ptp:
                print("      p2p       : %s" % addr.ptp)
        print("")


def info_ps():
    pass


def info_uptime():
    date = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%d.%m.%Y %H:%M:%S")
    print("ПК был запущен:", date)


def info_who():
    users = psutil.users()
    for user in users:
        proc_name = psutil.Process(user.pid).name() if user.pid else ""
        print("%-12s %-10s %-10s %-14s %s" % (
            user.name,
            user.terminal or '-',
            datetime.datetime.fromtimestamp(user.started).strftime("%Y-%m-%d %H:%M"),
            "(%s)" % user.host if user.host else "",
            proc_name
        ))