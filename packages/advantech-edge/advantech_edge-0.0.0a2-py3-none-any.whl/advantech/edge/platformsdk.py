
import ctypes
import os
import platform


class PlatformSDK:
    def __init__(self):
        self.e_api_library = None
        self.board_information_string = None
        self.board_information_value = None
        self.board_information = {}
        self.EApiBoardGetStringA = None
        self.EApiBoardGetValue = None
        self.EApiLibInitialize = None
        self.EApiLibUnInitialize = None
        self.EApiGetMemoryAvailable = None
        self.EApiGetDiskInfo = None
        self.EApiETPReadDeviceData = None
        self.EApiETPReadUserData = None
        self.EApiGPIOGetLevel = None
        self.EApiExtFunctionGetStatus = None
        self.EApiExtFunctionSetStatus = None
        self.EApiGPIOGetCount = None
        self.EApiGPIOGetDirection = None
        self.EApiGPIOSetDirection = None
        self.EApiGPIOSetLevel = None
        self.EApiWDogGetCap = None
        self.EApiStorageCap = None

        self.led_id_list = []

        self.import_library()
        self.initialize()
        self.initial_constant()

    def import_library(self):
        library_path = "/usr/src/advantech/libEAPI/"
        architecture = platform.machine()
        os_name = platform.system()
        e_api_library_path = ""

        if os_name == "Linux" and 'x86' in architecture.lower():
            library_path += "libEAPI_linux-x86_64/"
            e_api_library_path = library_path+"libEAPI.so"

        elif os_name == "Linux" and 'aarch64' in architecture.lower():
            library_path += "libEAPI_linux-aarch64/"
            e_api_library_path = library_path+"libEAPI.so"

        elif os_name == "Windows" and 'x86' in architecture.lower():
            pass

        elif os_name == "Windows" and 'aarch64' in architecture.lower():
            pass

        else:
            print(
                f"disable to import library, architechture:{architecture.lower()}, os:{os_name}")

        self.e_api_library = ctypes.CDLL(e_api_library_path)

    def initial_constant(self):
        # LED ID 範圍的最小值和最大值
        EAPI_ID_EXT_FUNC_LED_MIN = 0x00000000
        EAPI_ID_EXT_FUNC_LED_MAX = 0x0000000F

        # 生成 LED ID 列表，範圍從 EAPI_ID_EXT_FUNC_LED_MIN 到 EAPI_ID_EXT_FUNC_LED_MAX
        self.led_id_list = [EAPI_ID_EXT_FUNC_LED_MIN + i for i in range(
            EAPI_ID_EXT_FUNC_LED_MAX - EAPI_ID_EXT_FUNC_LED_MIN + 1)]

        self.board_information_string = {
            "EAPI_ID_BOARD_MANUFACTURER_STR": 0x0,
            "EAPI_ID_BOARD_NAME_STR": 0x1,
            "EAPI_ID_BOARD_REVISION_STR": 0x2,
            "EAPI_ID_BOARD_SERIAL_STR": 0x3,
            "EAPI_ID_BOARD_BIOS_REVISION_STR": 0x4,
            "EAPI_ID_BOARD_HW_REVISION_STR": 0x5,
            "EAPI_ID_BOARD_PLATFORM_TYPE_STR": 0x6,
            "EAPI_ID_BOARD_EC_REVISION_STR": 0x101,
            "EAPI_ID_BOARD_OS_REVISION_STR": 0x102,
            "EAPI_ID_BOARD_CPU_MODEL_NAME_STR": 0x103,
        }
        self.board_information_value = {
            "EAPI_ID_HWMON_TEMP_CPU": 0x00050000,
            "EAPI_ID_HWMON_TEMP_SYSTEM": 0x00050002,
            "EAPI_ID_HWMON_VOLTAGE_VCORE": 0x00051000,
            "EAPI_ID_HWMON_VOLTAGE_3V3": 0x00051003,
            "EAPI_ID_HWMON_VOLTAGE_5V": 0x00051004,
            "EAPI_ID_HWMON_VOLTAGE_12V": 0x00051005,
            "EAPI_ID_HWMON_VOLTAGE_VBAT": 0x00051008,
            "EAPI_ID_HWMON_VOLTAGE_DC": 0x0005100D,
            "EAPI_ID_HWMON_VOLTAGE_3VSB": 0x00051007,
            "EAPI_ID_HWMON_VOLTAGE_5VSB": 0x00051006,
            "EAPI_ID_HWMON_VOLTAGE_VIN": 0x00051018,
            "EAPI_ID_HWMON_CURRENT_OEM1": 0x00053001,
            "EAPI_ID_GPIO_POE_PINNUM": 0x00070001,
            "EAPI_ID_HWMON_FAN_CPU": 0x00052000,
            "EAPI_ID_HWMON_FAN_SYSTEM": 0x00052001,
        }

        for i in self.board_information_string.keys():
            result = self.get_board_string_data(
                self.board_information_string[i])
            self.board_information.update({i: result})
        for i in self.board_information_value.keys():
            result = self.get_board_value_data(self.board_information_value[i])
            self.board_information.update({i: result})

    def initialize(self):
        EApiStatus_t = ctypes.c_int
        EApiId_t = ctypes.c_int

        prototype = ctypes.CFUNCTYPE(
            EApiStatus_t,           # 返回類型
            EApiId_t,               # 參數 1: EApiId_t
            ctypes.POINTER(ctypes.c_char),   # 參數 2: char *pValue
            ctypes.POINTER(ctypes.c_uint32)  # 參數 3: uint32_t *pBufLen
        )
        self.EApiBoardGetStringA = prototype(
            ("EApiBoardGetStringA", self.e_api_library))

        prototype = ctypes.CFUNCTYPE(
            EApiStatus_t,
            EApiId_t,
            ctypes.POINTER(ctypes.c_uint32),
        )
        self.EApiBoardGetValue = prototype(
            ("EApiBoardGetValue", self.e_api_library))

        prototype = ctypes.CFUNCTYPE(
            EApiStatus_t,
        )
        self.EApiLibInitialize = prototype(
            ("EApiLibInitialize", self.e_api_library))

        prototype = ctypes.CFUNCTYPE(
            EApiStatus_t,
        )
        self.EApiLibUnInitialize = prototype(
            ("EApiLibUnInitialize", self.e_api_library))

        prototype = ctypes.CFUNCTYPE(
            EApiStatus_t,
            ctypes.POINTER(ctypes.c_float)
        )
        self.EApiGetMemoryAvailable = prototype(
            ("EApiGetMemoryAvailable", self.e_api_library))

        prototype = ctypes.CFUNCTYPE(
            EApiStatus_t,
            ctypes.POINTER(DiskInfoC)  # 傳入 DISK_INFO 結構的指針
        )
        self.EApiGetDiskInfo = prototype(
            ("EApiGetDiskInfo", self.e_api_library))

        prototype = ctypes.CFUNCTYPE(
            EApiStatus_t,
            ctypes.POINTER(ctypes.POINTER(ETP_USER_DATA))  # 傳入 DISK_INFO 結構的指針
        )
        self.EApiETPReadDeviceData = prototype(
            ("EApiETPReadDeviceData", self.e_api_library))

        prototype = ctypes.CFUNCTYPE(
            EApiStatus_t,
            ctypes.POINTER(ctypes.POINTER(ETP_USER_DATA))  # 傳入 DISK_INFO 結構的指針
        )
        self.EApiETPReadUserData = prototype(
            ("EApiETPReadUserData", self.e_api_library))

        prototype = ctypes.CFUNCTYPE(
            EApiStatus_t,
            EApiId_t,
            ctypes.POINTER(ctypes.c_uint32)
        )
        self.EApiExtFunctionGetStatus = prototype(
            ("EApiExtFunctionGetStatus", self.e_api_library))

        prototype = ctypes.CFUNCTYPE(
            EApiStatus_t,
            EApiId_t,
            ctypes.c_uint32
        )
        self.EApiExtFunctionSetStatus = prototype(
            ("EApiExtFunctionSetStatus", self.e_api_library))

        prototype = ctypes.CFUNCTYPE(
            EApiStatus_t,
            ctypes.POINTER(ctypes.c_uint32)
        )
        self.EApiGPIOGetCount = prototype(
            ("EApiGPIOGetCount", self.e_api_library))

        prototype = ctypes.CFUNCTYPE(
            EApiStatus_t,
            EApiId_t,
            ctypes.c_uint32,
            ctypes.POINTER(ctypes.c_uint32),
        )
        self.EApiGPIOGetLevel = prototype(
            ("EApiGPIOGetLevel", self.e_api_library))

        prototype = ctypes.CFUNCTYPE(
            EApiStatus_t,
            EApiId_t,
            ctypes.c_uint32,
            ctypes.POINTER(ctypes.c_uint32)
        )
        self.EApiGPIOGetDirection = prototype(
            ("EApiGPIOGetDirection", self.e_api_library))

        prototype = ctypes.CFUNCTYPE(
            EApiStatus_t,
            EApiId_t,
            ctypes.POINTER(ctypes.c_uint32),
            ctypes.POINTER(ctypes.c_uint32)
        )
        self.EApiGPIOGetDirectionCaps = prototype(
            ("EApiGPIOGetDirectionCaps", self.e_api_library))

        prototype = ctypes.CFUNCTYPE(
            EApiStatus_t,
            EApiId_t,
            ctypes.c_uint32,
            ctypes.c_uint32
        )
        self.EApiGPIOSetDirection = prototype(
            ("EApiGPIOSetDirection", self.e_api_library))

        prototype = ctypes.CFUNCTYPE(
            EApiStatus_t,
            EApiId_t,
            ctypes.c_uint32,
            ctypes.c_uint32
        )
        self.EApiGPIOSetLevel = prototype(
            ("EApiGPIOSetLevel", self.e_api_library))

        prototype = ctypes.CFUNCTYPE(
            EApiStatus_t,
            ctypes.POINTER(ctypes.c_uint32),
            ctypes.POINTER(ctypes.c_uint32),
            ctypes.POINTER(ctypes.c_uint32)
        )
        self.EApiWDogGetCap = prototype(
            ("EApiWDogGetCap", self.e_api_library))

        # undefined symbol: EApiStorageCap
        # prototype = ctypes.CFUNCTYPE(
        #             EApiStatus_t,
        #             EApiId_t,
        #             ctypes.POINTER(ctypes.c_uint32),
        #             ctypes.POINTER(ctypes.c_uint32)
        #         )
        # self.EApiStorageCap = prototype(
        #     ("EApiStorageCap", self.e_api_library))

    def handle_error_code(self, n):
        n = int(n)
        if n < 0:
            n = (1 << 32) + n
        n = hex(n)
        if n == "0xfffff0ff":
            return "EAPI_STATUS_ERROR, Generic error"
        elif n == "0xfffffcff":
            return "EAPI_STATUS_UNSUPPORTED"

    def get_board_string_data(self, id_number):
        CMD_RETURN_BUF_SIZE = 4096
        pValue = ctypes.create_string_buffer(CMD_RETURN_BUF_SIZE)
        pBufLen = ctypes.c_uint32(CMD_RETURN_BUF_SIZE)

        status = self.EApiBoardGetStringA(
            id_number, pValue, ctypes.byref(pBufLen))

        if status == 0:
            return pValue.value.decode("utf-8")
        else:
            error_message = self.handle_error_code(status)
            return error_message

    def get_board_value_data(self, id_number):
        pValue = ctypes.c_uint32(0)

        status = self.EApiBoardGetValue(
            id_number, ctypes.byref(pValue))

        if status == 0:
            return pValue.value
        else:
            error_message = self.handle_error_code(status)
            return error_message

    def initial_EApiLibrary(self):

        status = self.EApiLibInitialize()
        if status == 0:
            print("run EApiLibInitialize successfully")
        else:
            error_message = self.handle_error_code(status)
            print(f"run EApiLibInitialize fail: {error_message}")

        # occurs Segmentation fault
        # status = self.EApiLibUnInitialize()
        # if status == 0:
        #     print("run EApiLibUnInitialize successfully")
        # else:
        #     error_message = self.handle_error_code(status)
        #     print(f"run EApiLibUnInitialize fail: {error_message}")

    def get_available_memory(self):
        try:
            available_memory = ctypes.c_float()
            status = self.EApiGetMemoryAvailable(
                ctypes.byref(available_memory))
            return available_memory.value
        except Exception as e:
            print("error: ", e)
            return None

    def get_disk_information(self):
        try:
            disk_info_c = DiskInfoC()
            status = self.EApiGetDiskInfo(ctypes.byref(disk_info_c))
            disk_info_obj = DiskInfo(disk_count=disk_info_c.disk_count,
                                     disk_part_info=[DiskPartInfo(
                                         partition_id=disk_info_c.disk_part_info[i].partition_id,
                                         partition_size=disk_info_c.disk_part_info[i].partition_size,
                                         partition_name=disk_info_c.disk_part_info[i].partition_name.decode(
                                             "utf-8")
                                     ) for i in range(disk_info_c.disk_count)])
            print(status)
            return disk_info_obj
        except Exception as e:
            print("error: ", e)
            return None

    def get_etp_device_data(self):
        device_data = ctypes.pointer(ctypes.pointer(ETP_DATA()))
        # device_data = ctypes.pointer(ctypes.pointer(ETP_USER_DATA()))
        status = self.EApiETPReadDeviceData(device_data)
        # argument 1: <class 'TypeError'>: expected LP_LP_ETP_USER_DATA instance instead of LP_LP_ETP_DATA
        etp_device_data = device_data.contents.contents
        device_order_text = bytes(
            etp_device_data.DeviceOrderText).decode('utf-8').strip('\x00')
        device_drder_number = bytes(
            etp_device_data.DeviceOrderNumber).decode('utf-8').strip('\x00')
        device_index = bytes(
            etp_device_data.DeviceIndex).decode('utf-8').strip('\x00')
        device_serial_umber = bytes(
            etp_device_data.DeviceSerialNumber).decode('utf-8').strip('\x00')
        device_operating_system = bytes(
            etp_device_data.OperatingSystem).decode('utf-8').strip('\x00')
        device_image = bytes(
            etp_device_data.Image).decode('utf-8').strip('\x00')
        reverse = bytes(
            etp_device_data.Reverse).decode('utf-8').strip('\x00')
        print("status ", status)
        print("device_order_text: ", device_order_text)
        print("device_drder_number: ", device_drder_number)
        print("DeviceIndex: ", device_index)
        print("DeviceSerialNumber: ", device_serial_umber)
        print("OperatingSystem: ", device_operating_system)
        print("Image: ", device_image)
        print("Reverse: ", reverse)

        if status == 0:
            return etp_user_data
        else:
            error_message = self.handle_error_code(status)
            return error_message

    def get_etp_user_data(self):
        user_data = ctypes.pointer(ctypes.pointer(ETP_USER_DATA()))
        status = self.EApiETPReadUserData(user_data)
        etp_user_data = user_data.contents.contents
        userspace_1 = bytes(etp_user_data.UserSpace1).decode(
            'utf-8').strip('\x00')
        userspace_2 = bytes(etp_user_data.UserSpace2).decode(
            'utf-8').strip('\x00')
        print("status ", status)
        print("userspace1: ", userspace_1)
        print("userspace2: ", userspace_2)
        if status == 0:
            return etp_user_data
        else:
            error_message = self.handle_error_code(status)
            return error_message

    def get_led_id_list(self):
        return self.led_id_list

    def get_led_status(self, id_number=0):
        id_number_int_type = ctypes.c_int(id_number)
        status = ctypes.c_uint32()
        result = self.EApiExtFunctionGetStatus(
            id_number_int_type, ctypes.byref(status))
        print(id_number_int_type, status, result)

        if result == 0:
            return status
        else:
            error_message = self.handle_error_code(result)
            return error_message

    def set_led_status(self, id_number=0):
        id_number_int_type = ctypes.c_int(id_number)
        status = ctypes.c_uint32()
        result = self.EApiExtFunctionSetStatus(id_number_int_type, status)
        print(id_number_int_type, status, result)

        if result == 0:
            return status
        else:
            error_message = self.handle_error_code(result)
            return error_message

    def get_gpio_count(self):
        buffer = 0
        count = ctypes.c_uint32(buffer)
        status = self.EApiGPIOGetCount(ctypes.byref(count))
        if status == 0:
            return status
        else:
            error_message = self.handle_error_code(status)
            return error_message

    def get_gpio_level(self, id_number=0):
        bitmask = ctypes.c_uint32(1)
        level = ctypes.c_uint32(0)
        status = self.EApiGPIOGetLevel(id_number, bitmask, ctypes.byref(level))
        if status == 0:
            return level
        else:
            error_message = self.handle_error_code(status)
            return error_message

    def get_gpio_direction(self, id_number=0):
        id_number_int_type = ctypes.c_int(id_number)
        direction = ctypes.c_uint32()
        bitmask = ctypes.c_uint32(1)
        status = self.EApiGPIOGetDirection(
            id_number_int_type, bitmask, ctypes.byref(direction))
        if status == 0:
            return direction
        else:
            error_message = self.handle_error_code(status)
            return error_message

    def get_gpio_capability(self, id_number=0):
        id_number_int_type = ctypes.c_int(id_number)
        gpio_input = ctypes.c_uint32(0)
        gpio_output = ctypes.c_uint32(0)
        status = self.EApiGPIOGetDirectionCaps(id_number_int_type,
                                               ctypes.byref(gpio_input),
                                               ctypes.byref(gpio_output))
        if status == 0:
            return direction
        else:
            error_message = self.handle_error_code(status)
            return error_message

    def set_gpio_direction(self, id_number=0, direction=0):
        id_number_int_type = ctypes.c_int(id_number)
        bitmask = ctypes.c_uint32(1)
        gpio_direction = ctypes.c_uint32(direction)
        status = self.EApiGPIOSetDirection(id_number_int_type,
                                           bitmask,
                                           gpio_direction)
        if status == 0:
            return True
        else:
            error_message = self.handle_error_code(status)
            return error_message

    def set_gpio_level(self, id_number=0, level=0):
        id_number_int_type = ctypes.c_int(id_number)
        bitmask = ctypes.c_uint32(1)
        gpio_level = ctypes.c_uint32(level)
        status = self.EApiGPIOSetLevel(id_number_int_type,
                                       bitmask,
                                       gpio_level)
        if status == 0:
            return True
        else:
            error_message = self.handle_error_code(status)
            return error_message

    def get_watchdog_capability(self):
        max_delay_in_milliseconds = ctypes.c_uint32(0)
        max_event_timeout_in_milliseconds = ctypes.c_uint32(0)
        max_reset_timeout_in_milliseconds = ctypes.c_uint32(0)
        status = self.EApiWDogGetCap(max_delay_in_milliseconds,
                                     max_event_timeout_in_milliseconds,
                                     max_reset_timeout_in_milliseconds)
        if status == 0:
            return max_delay_in_milliseconds.value, max_event_timeout_in_milliseconds.value, max_reset_timeout_in_milliseconds.value
        else:
            error_message = self.handle_error_code(status)
            return error_message

    def get_storage_capability(self, id_number=0):
        id_number_int_type = ctypes.c_int(id_number)
        storage_size = ctypes.c_uint32(0)
        block_length = ctypes.c_uint32(0)
        status = self.EApiStorageCap(id_number_int_type, ctypes.byref(
            storage_size), ctypes.byref(block_length))
        if status == 0:
            return storage_size.value, block_length.value
        else:
            error_message = self.handle_error_code(status)
            return error_message


class DiskPartInfo:
    def __init__(self, partition_id, partition_size, partition_name):
        self.partition_id = partition_id
        self.partition_size = partition_size
        self.partition_name = partition_name


class DiskInfo:
    def __init__(self, disk_count, disk_part_info):
        self.disk_count = disk_count
        self.disk_part_info = disk_part_info


class DiskPartInfoC(ctypes.Structure):
    _fields_ = [("partition_id", ctypes.c_int),
                ("partition_size", ctypes.c_int),
                ("partition_name", ctypes.c_char_p)]


class DiskInfoC(ctypes.Structure):
    _fields_ = [("disk_count", ctypes.c_int),
                ("disk_part_info", DiskPartInfoC * 8)]  # 最多支持 8 個分區


class ETP_USER_DATA(ctypes.Structure):
    _fields_ = [
        ("UserSpace1", ctypes.c_ubyte * 128),  # A6, offset 0
        ("UserSpace2", ctypes.c_ubyte * 128)   # A6, offset 128
    ]


class ETP_DATA(ctypes.Structure):
    _fields_ = [
        ("DeviceOrderText", ctypes.c_ubyte * 40),
        ("DeviceOrderNumber", ctypes.c_ubyte * 10),
        ("DeviceIndex", ctypes.c_ubyte * 3),
        ("DeviceSerialNumber", ctypes.c_ubyte * 15),
        ("OperatingSystem", ctypes.c_ubyte * 40),
        ("Image", ctypes.c_ubyte * 40),
        ("Reverse", ctypes.c_ubyte * 92)
    ]
