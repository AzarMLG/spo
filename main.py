import psutil
import cpuinfo
import json


def print_welcome():
    print("""Курсовой проект по дисциплине \"Системное программное обеспечение\"
Исполнитель студент группы АССЗ-21 Азаревич А.Я.
Разработка программного комплекса сбора информации о вычислительной системе""")


def print_menu():
    print(
        """    Главное меню:
1. Определение информации о центральном процессоре
2. Определение информации о BIOS
3. Определение информации о разделах дисков
4. Определение информации об дисковых накопителях
5. Определение информации о об использовании клавиатуры
6. Определение информации о системной плате
7. Определение информации об импользовании mouse
8. Определение информации о видеокарте
9. Определение информации о мониторе
10. Определение информации о сетевых адаптерах
11. Определение информации о запущенных приложениях
12. Сбор всех данных в один текстовый файл и трпнспортировка его на сервер в указанную папку
13. Сбор информации о дате и времени запуска и завершения ПК
14. Сбор информации о дате и времени входа и выхода из системы определенного пользователя""")


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
    print("Кэш L2: ", float(j["l2_cache_size"])/1000, "KiB")
    print("Кэш L3: ", float(j["l3_cache_size"])/1000, "KiB")
    print("Поддерживаемые инструкции: ", j["flags"])


def info_bios():
    pass


def info_partitions():
    pass


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
    pass


def info_ps():
    pass


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
        elif x == 0:
            break
        else:
            print("ERROR")


print_welcome()
menu()
