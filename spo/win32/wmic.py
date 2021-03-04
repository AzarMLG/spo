import subprocess


def strip(string):
    string = string.split("\n", 1)[1]
    string = string.replace("\n", "")
    return string


def get_wmic(device, par) -> str:
    command = "wmic " + device + " get " + par
    stdout = str(subprocess.check_output(command, text=True))
    return strip(stdout)


def win32_gpu(par) -> str:
    device = "path win32_VideoController"
    return get_wmic(device, par)


def win32_bios(par) -> str:
    device = "BIOS"
    return get_wmic(device, par)


def win32_cpu(par) -> str:
    device = "CPU"
    return get_wmic(device, par)


def win32_disk(par) -> str:
    device = "DISKDRIVE"
    return get_wmic(device, par)


def win32_mb(par) -> str:
    device = "BASEBOARD"
    return get_wmic(device, par)


def win32_mon(par) -> str:
    device = "DESKTOPMONITOR"
    return get_wmic(device, par)
