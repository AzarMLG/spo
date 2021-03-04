from spo.win32.wmic import win32_cpu


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