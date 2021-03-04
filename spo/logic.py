import sys

from spo.multiplatform.getinfo import print_partitions, print_network, print_ps, print_uptime, print_who
from spo.linux.getinfo import linux_print_cpu, linux_print_bios, linux_print_disks, linux_print_mb, linux_print_gpu, \
    linux_print_monitor
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
    print_network()


def info_ps():
    print_ps()


def info_uptime():
    print_uptime()


def info_who():
    print_who()
