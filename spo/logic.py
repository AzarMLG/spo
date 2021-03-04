import sys
import time
import socket
import psutil

from datetime import datetime, date
from psutil._common import bytes2human
from psutil._compat import get_terminal_size

from spo.linux.getinfo import linux_print_cpu, linux_print_bios, linux_print_disks, linux_print_mb, linux_print_gpu, \
    linux_print_monitor
from spo.multiplatform.getinfo import print_partitions
from spo.win32.getinfo import win32_print_cpu, win32_print_bios, win32_print_disks, win32_print_mb, win32_print_gpu, \
    win32_print_monitor


def info_cpu():
    if sys.platform == 'win32':
        win32_print_cpu()
    else:
        linux_print_cpu()


def info_bios():
    if sys.platform == 'win32':
        win32_print_bios()
    else:
        linux_print_bios()


def info_partitions():
    print_partitions()


def info_disks():
    if sys.platform == 'win32':
        win32_print_disks()
    else:
        linux_print_disks()


# TODO: Keyboard(WTF is even supposed to be here?)
def info_keyboard():
    print("Standard PS/2 Keyboard")


def info_motherboard():
    if sys.platform == 'win32':
        win32_print_mb()
    else:
        linux_print_mb()


# TODO Mouse
def info_mouse():
    print("HID-compliant mouse")


def info_gpu():
    if sys.platform == "win32":
        win32_print_gpu()
    else:
        linux_print_gpu()


def info_monitor():
    if sys.platform == 'win32':
        win32_print_monitor()
    else:
        linux_print_monitor()


def info_network():
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
