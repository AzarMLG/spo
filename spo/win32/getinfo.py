from psutil._common import bytes2human
from tabulate import tabulate

from spo.lists import form_list, insert_name, clear_list
from spo.win32.wmic import win32_cpu, win32_bios, win32_disk, win32_mb, win32_gpu, win32_mon


def win32_print_cpu():
    # Use "wmic CPU get ***"
    # AddressWidth Architecture AssetTag Availability Caption Characteristics ConfigManagerErrorCode
    # ConfigManagerUserConfig CpuStatus CreationClassName CurrentClockSpeed CurrentVoltage DataWidth Description
    # DeviceID ErrorCleared ErrorDescription ExtClock Family InstallDate L2CacheSize L2CacheSpeed L3CacheSize
    # L3CacheSpeed LastErrorCode Level LoadPercentage Manufacturer MaxClockSpeed Name NumberOfCores
    # NumberOfEnabledCore NumberOfLogicalProcessors OtherFamilyDescription PartNumber PNPDeviceID
    # PowerManagementCapabilities PowerManagementSupported ProcessorId ProcessorType Revision Role
    # SecondLevelAddressTranslationExtensions SerialNumber SocketDesignation Status StatusInfo Stepping
    # SystemCreationClassName SystemName ThreadCount UniqueId UpgradeMethod Version VirtualizationFirmwareEnabled
    # VMMonitorModeExtensions  VoltageCaps
    print("Имя: ", win32_cpu("Name"),
          "\nОписание: ", win32_cpu("Caption"),
          "\nТекущая тактовая частота: ", win32_cpu("CurrentClockSpeed"),
          "\nНапряжение: ", win32_cpu("CurrentVoltage"),
          "\nID Устройства: ", win32_cpu("DeviceID"),
          "\nРазмер кэша L2: ", win32_cpu("L2CacheSize").replace(' ', ''), "KB",
          "\nРазмер кэша L3: ", win32_cpu("L3CacheSize").replace(' ', ''), "KB",
          "\nТекущая загрузка: ", win32_cpu("LoadPercentage").replace(' ', ''), "%",
          "\nИзготовитель: ", win32_cpu("Manufacturer"),
          "\nКол-во ядер: ", win32_cpu("NumberOfCores"),
          "\nКол-во активированных ядер: ", win32_cpu("NumberOfEnabledCore"),
          "\nКол-во потоков: ", win32_cpu("NumberOfLogicalProcessors"),
          "\nИдентификатор процессора: ", win32_cpu("ProcessorId"),
          "\nРевизия процессора: ", win32_cpu("Revision")
          )


def win32_print_bios():
    # Use "wmic BIOS get BIOSVersion"
    # BiosCharacteristics BIOSVersion BuildNumber Caption CodeSet CurrentLanguage Description
    # EmbeddedControllerMajorVersion  EmbeddedControllerMinorVersion  IdentificationCode  InstallableLanguages
    # InstallDate  LanguageEdition  ListOfLanguages  Manufacturer  Name OtherTargetOS  PrimaryBIOS  ReleaseDate
    # SerialNumber  SMBIOSBIOSVersion  SMBIOSMajorVersion  SMBIOSMinorVersion  SMBIOSPresent  SoftwareElementID
    # SoftwareElementState  Status  SystemBiosMajorVersion  SystemBiosMinorVersion  TargetOperatingSystem  Version
    controller_version = (win32_bios("EmbeddedControllerMajorVersion") + "." +
                          win32_bios("EmbeddedControllerMinorVersion")).replace(" ", "")
    print("Имя: ", win32_bios("Name"),
          "\nИзготовитель: ", win32_bios("Manufacturer"),
          "\nВерсия BIOS: ", win32_bios("BIOSVersion"),
          "\nВерсия интегрированного контроллера: ", controller_version,
          "\nСерийный номер: ", win32_bios("SerialNumber"),
          "\nВерсия SMBIOSBIOS: ", win32_bios("SMBIOSBIOSVersion"),
          )


def win32_print_disks():
    # Use "wmic DISKDRIVE get ***"
    # Availability BytesPerSector Capabilities CapabilityDescriptions Caption
    # CompressionMethod ConfigManagerErrorCode ConfigManagerUserConfig CreationClassName DefaultBlockSize
    # Description DeviceID ErrorCleared ErrorDescription ErrorMethodology FirmwareRevision Index InstallDate
    # InterfaceType LastErrorCode Manufacturer MaxBlockSize MaxMediaSize MediaLoaded MediaType MinBlockSize Model
    # Name NeedsCleaning NumberOfMediaSupported Partitions PNPDeviceID PowerManagementCapabilities
    # PowerManagementSupported SCSIBus SCSILogicalUnit SCSIPort SCSITargetId SectorsPerTrack SerialNumber
    # Signature Size Status StatusInfo SystemCreationClassName SystemName TotalCylinders TotalHeads TotalSectors
    # TotalTracks TracksPerCylinder
    caption = form_list(win32_disk("Caption"), "Имя: ")
    device_id = form_list(win32_disk("DeviceID"), "ID Устройства: ")
    bytes_ps = form_list(win32_disk("BytesPerSector"), "Байт в секторе: ")
    firmware = form_list(win32_disk("FirmwareRevision"), "Ревизия прошивки: ")
    index = form_list(win32_disk("Index"), "Индекс: ")
    partitions = form_list(win32_disk("Partitions"), "Разделы: ")
    serial = form_list(win32_disk("SerialNumber"), "Серийный номер: ")
    total_sectors = form_list(win32_disk("TotalSectors"), "Всего секторов: ")
    size = clear_list(win32_disk("Size"))
    for each in range(len(size)):
        size[each] = bytes2human(int(size[each]))
    insert_name(size, "Размер: ")
    print(tabulate([index, size, device_id, partitions, firmware, serial, bytes_ps, total_sectors],
                   headers=caption))


def win32_print_mb():
    # Use "wmic BASEBOARD get ***"
    # Caption ConfigOptions CreationClassName Depth Description Height HostingBoard HotSwappable InstallDate
    # Manufacturer Model Name OtherIdentifyingInfo PartNumber PoweredOn  Product Removable  Replaceable
    # Requirements Description RequiresDaughterBoard SerialNumber SKU SlotLayout SpecialRequirements Status Tag
    # Version Weight  Width
    manufacturer = win32_mb("Manufacturer")
    product = win32_mb("Product")
    sn = win32_mb("SerialNumber")
    print("Имя: ", product,
          "\nИзготовитель: ", manufacturer,
          "\nСерийный номер: ", sn)


def win32_print_gpu():
    print("Имя: ", win32_gpu("Name"),
          "\nПамять: ", bytes2human(int(win32_gpu("AdapterRAM"))),
          "\nТекущее разрешение: ", win32_get_resolution(),
          "\nТекущаяя частота обновления: ", win32_gpu("CurrentRefreshRate"), "Hz",
          "\nВерсия драйвера: ", win32_gpu("DriverVersion"),
          "\nУстановленные видеодрайверы: ", win32_gpu("InstalledDisplayDrivers")
          )


def win32_get_resolution() -> str:
    return (win32_gpu("CurrentHorizontalResolution") + "x" +
            win32_gpu("CurrentVerticalResolution")).replace(" ", "")


def win32_print_monitor():
    print("Имя: ", win32_mon("Caption"),
          "\nID Устройства: ", win32_mon("DeviceID"),
          "\nТекущее разрешение: ", win32_get_resolution(),
          "\nТекущая частота обновления: ", win32_gpu("CurrentRefreshRate"), "Hz",
          )