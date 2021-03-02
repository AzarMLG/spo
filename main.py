from info_ import info_cpu, info_bios, info_partitions, info_disks, info_keyboard, info_motherboard, info_mouse, \
    info_gpu, info_monitor, info_network, info_ps, info_uptime, info_who
from print_ import print_welcome, print_menu


def menu():
    print_menu()
    while True:
        x = int(input("Введите ваш выбор: "))
        if x == 1:
            info_cpu()
        elif x == 2:
            info_bios()
        elif x == 3:
            info_partitions()
        elif x == 4:
            info_disks()
        elif x == 5:
            info_keyboard()
        elif x == 6:
            info_motherboard()
        elif x == 7:
            info_mouse()
        elif x == 8:
            info_gpu()
        elif x == 9:
            info_monitor()
        elif x == 10:
            info_network()
        elif x == 11:
            info_ps()
        elif x == 13:
            info_uptime()
        elif x == 14:
            info_who()
        elif x == 0:
            break
        else:
            print("ERROR")


print_welcome()
menu()
