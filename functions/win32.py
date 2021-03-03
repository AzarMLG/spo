import subprocess


def get_wmic(device, name):
    command = "wmic " + device + " get " + name
    result = str(subprocess.check_output(command, text=True))
    result = result.split("\n", 1)[1]
    result = result.replace("\n", "")
    return result


def win32_gpu(name):
    device = "path win32_VideoController"
    result = get_wmic(device, name)
    return result
