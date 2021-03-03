import subprocess


def strip(string):
    string = string.split("\n", 1)[1]
    string = string.replace("\n", "")
    return string


def get_wmic(device, name):
    command = "wmic " + device + " get " + name
    stdout = str(subprocess.check_output(command, text=True))
    return strip(stdout)


def win32_gpu(name):
    device = "path win32_VideoController"
    return get_wmic(device, name)


def win32_bios(name):
    device = "BIOS"
    return get_wmic(device, name)
