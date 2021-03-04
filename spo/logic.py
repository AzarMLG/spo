import sys

from spo.multiplatform.getinfo import print_partitions, print_network, print_ps, print_uptime, print_who
from spo.linux.getinfo import linux_print_cpu, linux_print_bios, linux_print_disks, linux_print_mb, linux_print_gpu, \
    linux_print_monitor
from spo.win32.getinfo import win32_print_cpu, win32_print_bios, win32_print_disks, win32_print_mb, win32_print_gpu, \
    win32_print_monitor


def info_cpu():
    print("Информация о центральном процессоре: \n")
    if sys.platform == 'win32':
        win32_print_cpu()
    else:
        linux_print_cpu()


def info_bios():
    print("Информация о BIOS:\n")
    if sys.platform == 'win32':
        win32_print_bios()
    else:
        linux_print_bios()


def info_partitions():
    print("Информация о разделах на дисковых накопителях: \n")
    print_partitions()


def info_disks():
    print("Информация о дисковых устройсвах: \n")
    if sys.platform == 'win32':
        win32_print_disks()
    else:
        linux_print_disks()


# TODO: Keyboard(WTF is even supposed to be here?)
def info_keyboard():
    print("Информация о клавиатуре: \n")
    print("Имя: ", "Standard PS/2 Keyboard")


def info_motherboard():
    print("Информация о системной плате: \n")
    if sys.platform == 'win32':
        win32_print_mb()
    else:
        linux_print_mb()


# TODO Mouse
def info_mouse():
    print("Информация о mouse: \n")
    print("HID-compliant mouse")


def info_gpu():
    print("Информация о графическом процессоре: \n")
    if sys.platform == "win32":
        win32_print_gpu()
    else:
        linux_print_gpu()


def info_monitor():
    print("Информация о мониторе: \n")
    if sys.platform == 'win32':
        win32_print_monitor()
    else:
        linux_print_monitor()


def info_network():
    print("Информация о сетевых адаптерах: \n")
    print_network()


def info_ps():
    print("Информация о запущенных процессах: \n")
    print_ps()


def info_uptime():
    print("Информация о дате и времени запуска операционной системы: \n")
    print_uptime()


def info_who():
    print("Информация о дате и времени входа в систему пользователей: \n")
    print_who()
