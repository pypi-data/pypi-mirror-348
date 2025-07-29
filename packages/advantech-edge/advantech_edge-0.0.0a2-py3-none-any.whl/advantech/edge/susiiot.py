import ctypes
import json
import sys
import os
import platform
from .iplatforminformation import IPlatformInformation
from .ionboardsensors import IOnboardSensors
from .igpio import IGpio, GpioDirectionType, GpioLevelType
from .imemory import IMemory
from .idisk import IDisk
from typing import List
import threading


class SusiIot(IPlatformInformation, IOnboardSensors, IGpio, IMemory, IDisk):
    _instance = None
    _lock = threading.Lock()

    susi_iot_library = None  
    json_library = None  #

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls.susi_iot_library = None
                cls.check_root_authorization()
                cls.import_library()
                cls.initialize_library()
                cls.susi_iot_library.SusiIoTInitialize()
                cls._instance = super().__new__(cls)
            return cls._instance

    def __init__(self):
        self.susi_iot_library = SusiIot.susi_iot_library
        self.json_library = SusiIot.json_library
        self.susi_information = None
        self.device_id_list = None
        self.gpio_table = None
        self.memory_sdram_table = None
        self.voltage_source_table = None
        self.temperature_source_table = None
        self.fan_source_table = None

        susiiot_information = self.get_susi_information_string()
        self.set_susiiot_information(susiiot_information)
        self.set_device_id_list()
        self.set_gpio_list()
        self.set_voltage_sources()
        self.set_memory_list()
        self.set_temperature_sources()

    def __del__(self):
        self.susi_iot_library.SusiIoTUninitialize()

    @staticmethod
    def check_root_authorization():
        if os.geteuid() != 0:
            sys.exit("Error: Please run this program as root (use sudo).")
        else:
            return True

    @staticmethod
    def initialize_library():

        SusiIot.susi_iot_library.SusiIoTInitialize.restype = ctypes.c_int

        SusiIot.susi_iot_library.SusiIoTSetValue.argtypes = [
            ctypes.c_uint32, ctypes.POINTER(JsonT)]
        SusiIot.susi_iot_library.SusiIoTSetValue.restype = ctypes.c_uint32

        SusiIot.susi_iot_library.SusiIoTGetLoggerPath.restype = ctypes.c_char_p

        SusiIot.susi_iot_library.SusiIoTGetPFDataString.restype = ctypes.c_char_p
        SusiIot.susi_iot_library.SusiIoTGetPFDataString.argtypes = [
            ctypes.c_uint32]

        SusiIot.susi_iot_library.SusiIoTGetPFDataStringByUri.restype = ctypes.c_char_p
        SusiIot.susi_iot_library.SusiIoTGetPFDataStringByUri.argtypes = [
            ctypes.c_char_p]

        SusiIot.json_library.json_dumps.restype = ctypes.c_char_p
        SusiIot.json_library.json_integer.restype = ctypes.POINTER(JsonT)

        SusiIot.json_library.json_real.restype = ctypes.POINTER(JsonT)
        SusiIot.json_library.json_string.restype = ctypes.POINTER(JsonT)
        prototype = ctypes.CFUNCTYPE(
            ctypes.c_char_p
        )
        SusiIot.SusiIoTGetPFCapabilityString = prototype(
            ("SusiIoTGetPFCapabilityString", SusiIot.susi_iot_library))

        SusiIot.susi_iot_library.SusiIoTUninitialize.restype = ctypes.c_int

    def get_json_indent(self, n):
        json_max_indent = 0x1F
        return n & json_max_indent

    def get_json_real_precision(self, n):
        return ((n & 0x1F) << 11)

    def turn_byte_to_json(self, json_bytes):
        json_str = json_bytes.decode('utf-8')
        data = json.loads(json_str)
        return data

    def get_data_by_id(self, device_id):
        result = self.susi_iot_library.SusiIoTGetPFDataString(device_id)
        return self.turn_byte_to_json(result)

    def set_value(self, device_id, value):
        result_ptr = self.json_library.json_integer(value)
        result = result_ptr.contents
        return self.susi_iot_library.SusiIoTSetValue(device_id, result)

    def get_susi_information_string(self):
        capability_string = self.SusiIoTGetPFCapabilityString()
        capability_string = capability_string.decode('utf-8')
        try:
            susi_information = json.loads(capability_string)
        except json.JSONDecodeError as e:
            print("Failed to parse JSON.:", e)
        return susi_information

    def set_susiiot_information(self, information):
        self.susi_information = information

    def get_susi_information_object(self):
        json_max_indent = 0x1F
        jsonObject = self.json_library.json_object()
        if self.susi_iot_library.SusiIoTGetPFCapability(jsonObject) != 0:
            self.susi_information = "SusiIoTGetPFCapability failed."
            exit(1)
        else:
            self.susi_json_t = self.json_library.json_dumps(jsonObject, self.get_json_indent(
                4) | json_max_indent | self.get_json_real_precision(10))
            self.susi_information = self.turn_byte_to_json(self.susi_json_t)

        return self.susi_information

    @property
    def susi_iot_information(self):
        return self.susi_information

    def extract_ids(self, obj, result=None):
        if result is None:
            result = []

        if isinstance(obj, dict):
            if "id" in obj:
                result.append(obj["id"])
            for value in obj.values():
                self.extract_ids(value, result)

        elif isinstance(obj, list):
            for item in obj:
                self.extract_ids(item, result)

        return result

    def set_device_id_list(self):
        self.device_id_list = self.extract_ids(self.susi_information)

    def set_gpio_list(self):
        self.gpio_table = {}
        initial = 17039617
        for i in range(64):
            register = initial+i
            if register in self.device_id_list:
                name = self.get_data_by_id(register)['bn']
                self.gpio_table.update({name: register})

    @property
    def pins(self) -> List[str]:
        if self.gpio_table == None:
            self.set_gpio_list()
        return self.gpio_table.keys()

    def set_voltage_sources(self):
        self.voltage_source_table = {}
        initial = 16908801
        for i in range(64):
            register = initial+i
            if register in self.device_id_list:
                name = self.get_data_by_id(register)['n']
                self.voltage_source_table.update({name: register})

    @property
    def voltage_sources(self) -> List[str]:
        if self.voltage_source_table == None:
            self.set_voltage_sources()
        return self.voltage_source_table.keys()

    def get_voltage(self, voltage_source):
        id_namuber = self.voltage_source_table[voltage_source]
        return self.get_data_by_id(id_namuber)['v']

    def set_temperature_sources(self):
        self.temperature_source_table = {}
        # system temperature
        initial = 16908545
        for i in range(20):
            register = initial+i
            if register in self.device_id_list:
                name = self.get_data_by_id(register)['n']
                self.temperature_source_table.update({name: register})

        # memory temperature
        initial = 337119489
        for i in range(20):
            register = initial+i
            if register in self.device_id_list:
                name = self.get_data_by_id(register)['n']
                self.temperature_source_table.update({name: register})

    @property
    def temperature_sources(self) -> List[str]:
        if self.temperature_source_table == None:
            self.set_temperature_sources()
        return self.temperature_source_table.keys()

    @staticmethod
    def import_library():
        architecture = platform.machine()
        os_name = platform.system()
        susi_iot_library_path = ""
        json_library_path = ""

        if os_name == "Linux" and 'x86' in architecture.lower():
            susi_iot_library_path = "/usr/lib/libSusiIoT.so"
            json_library_path = "/usr/lib/x86_64-linux-gnu/libjansson.so.4"

        elif os_name == "Linux" and 'aarch64' in architecture.lower():
            susi_iot_library_path = "/lib/libSusiIoT.so"
            json_library_path = "/lib/aarch64-linux-gnu/libjansson.so.4"

        elif os_name == "Windows" and 'x86' in architecture.lower():
            pass

        elif os_name == "Windows" and 'aarch64' in architecture.lower():
            pass

        else:
            print(
                f"disable to import library, architechture:{architecture.lower()}, os:{os_name}")
        try:
            pass
        except Exception as e:
            print("SUSI Iot is not installed, please install proper Advantech Library. ",e)

        if not os.path.exists(json_library_path):
            message=f"file {json_library_path} is not exist, please reference README and install proper suit."
            sys.exit(message)
        
        if not os.path.exists(susi_iot_library_path):
            message=f"file {json_library_path} is not exist, please reference README and install proper suit."
            sys.exit(message)

        SusiIot.json_library = ctypes.CDLL(
                json_library_path, mode=ctypes.RTLD_GLOBAL)
        SusiIot.susi_iot_library = ctypes.CDLL(
            susi_iot_library_path, mode=ctypes.RTLD_GLOBAL)

    @property
    def manufacturer(self):
        id_number = 16843777
        result = self.get_data_by_id(id_number)
        if not result:
            return None
        return result["sv"]

    @property
    def boot_up_times(self):
        id_number = 16843010
        result = self.get_data_by_id(id_number)
        if not result:
            return None
        return result["v"]

    @property
    def running_time_in_hours(self):
        id_number = 16843011
        result = self.get_data_by_id(id_number)
        if not result:
            return None
        return result["v"]

    @property
    def motherboard_name(self):
        id_number = 16843778
        result = self.get_data_by_id(id_number)
        if not result:
            return None
        return result["sv"]

    @property
    def bios_revision(self):
        id_number = 16843781
        result = self.get_data_by_id(id_number)
        if not result:
            return None
        return result["sv"]

    @property
    def firmware_name(self):
        id_number = 16843784
        result = self.get_data_by_id(id_number)
        if not result:
            return None
        return result["sv"]

    @property
    def library_version(self):
        id_number = 16843266
        result = self.get_data_by_id(id_number)
        if not result:
            return None
        return result["sv"]

    @property
    def driver_version(self):
        id_number = 16843265
        result = self.get_data_by_id(id_number)
        if not result:
            return None
        return result["sv"]

    @property
    def firmware_version(self):
        id_number = 16843267
        result = self.get_data_by_id(id_number)
        if not result:
            return None
        return result["sv"]

    @property
    def voltage_vcore(self):
        id_number = 16908801
        result = self.get_data_by_id(id_number)
        if not result:
            return None
        return result["v"]

    @property
    def voltage_3p3v(self):
        id_number = 16908804
        result = self.get_data_by_id(id_number)
        if not result:
            return None
        return result["v"]

    @property
    def voltage_5v(self):
        id_number = 16908805
        result = self.get_data_by_id(id_number)
        if not result:
            return None
        return result["v"]

    @property
    def voltage_12v(self):
        id_number = 16908806
        result = self.get_data_by_id(id_number)
        if not result:
            return None
        return result["v"]

    @property
    def voltage_5v_standby(self):
        id_number = 16908807
        result = self.get_data_by_id(id_number)
        if not result:
            return None
        return result["v"]

    @property
    def voltage_cmos_battery(self):
        id_number = 16908809
        result = self.get_data_by_id(id_number)
        if not result:
            return None
        return result["v"]

    @property
    def dc_power(self):
        id_number = 16908814
        result = self.get_data_by_id(id_number)
        if not result:
            return None
        return result["v"]

    @property
    def voltage_3v(self):
        id_number = 16908817
        result = self.get_data_by_id(id_number)
        if not result:
            return None
        return result["v"]

    @property
    def cpu_temperature(self):
        id_number = 16908545
        result = self.get_data_by_id(id_number)
        if not result:
            return None
        return result["v"]

    @property
    def system_temperature_in_celsius(self):
        id_number = 16908547
        result = self.get_data_by_id(id_number)
        if not result:
            return None
        return result["v"]

    def set_memory_list(self):
        self.memory_sdram_table = {}
        initial = 337117185
        for i in range(64):
            register = initial+i
            if register in self.device_id_list:
                name = self.get_data_by_id(register)['bn']
                self.memory_sdram_table.update({name: register})

    @property
    def memory_list(self) -> List[str]:
        if self.memory_sdram_table == None:
            self.set_memory_list()
        return self.memory_sdram_table.keys()

    @property
    def memory_count(self) -> List[str]:
        return len(self.memory_sdram_table)

    def get_memory_type(self, memory_number=0):
        id_number = 337117441
        result = self.get_data_by_id(id_number+memory_number)
        if not result:
            return None
        return result["sv"]

    def get_module_type(self, memory_number=0):
        id_number = 337117697
        result = self.get_data_by_id(id_number+memory_number)
        if not result:
            return None
        return result["sv"]

    def get_memory_size_in_GB(self, memory_number=0):
        id_number = 337117953
        result = self.get_data_by_id(id_number+memory_number)
        if not result:
            return None
        return result["v"]

    def get_memory_speed(self, memory_number=0):
        id_number = 337118209
        result = self.get_data_by_id(id_number+memory_number)
        if not result:
            return None
        return result["sv"]

    def get_memory_rank(self, memory_number=0):
        id_number = 337118465
        result = self.get_data_by_id(id_number+memory_number)
        if not result:
            return None
        return result["v"]

    def get_memory_voltage(self, memory_number=0):
        id_number = 337118721
        result = self.get_data_by_id(id_number+memory_number)
        if not result:
            return None
        return result["v"]

    def get_memory_bank(self, memory_number=0):
        id_number = 337118977
        result = self.get_data_by_id(id_number+memory_number)
        if not result:
            return None
        return result["sv"]

    def get_memory_manufacturing_date_code(self, memory_number=0):
        id_number = 337119233
        result = self.get_data_by_id(id_number+memory_number)
        if not result:
            return None
        return result["sv"]

    def get_memory_temperature(self, memory_number=0):
        id_number = 337119489
        result = self.get_data_by_id(id_number+memory_number)
        if not result:
            return None
        return result["v"]

    def get_memory_write_protection(self, memory_number=0):
        id_number = 337119745
        result = self.get_data_by_id(id_number+memory_number)
        if not result:
            return None
        return result["sv"]

    def get_memory_module_manufacture(self, memory_number=0):
        id_number = 337120001
        result = self.get_data_by_id(id_number+memory_number)
        if not result:
            return None
        return result["sv"]

    def get_memory_manufacture(self, memory_number=0):
        id_number = 337120257
        result = self.get_data_by_id(id_number+memory_number)
        if not result:
            return None
        return result["sv"]

    def get_memory_part_number(self, memory_number=0):
        id_number = 337121537
        result = self.get_data_by_id(id_number+memory_number)
        if not result:
            return None
        return result["sv"]

    def get_memory_specific(self, memory_number=0):
        id_number = 337125633
        result = self.get_data_by_id(id_number+memory_number)
        if not result:
            return None
        return result["sv"]

    @property
    def total_disk_space(self):
        # susi iot bug, there are two item with same id=353697792
        id_number = 353697792
        result = self.get_data_by_id(id_number)
        if not result:
            return None
        if type(result)==type(dict()):
            result = result['e'][0]
            return result["v"]
        return result["v"]

    @property
    def free_disk_space(self):
        id_number = 353697793
        result = self.get_data_by_id(id_number)
        if not result:
            return None
        return result["v"]

    @property
    def susiiot_version(self):
        id_number = 257
        result = self.get_data_by_id(id_number)
        if not result:
            return None
        return result["sv"]

    def get_temperature(self, temperature_source) -> float:
        try:
            id_number = self.temperature_source_table[temperature_source]
            result = self.get_data_by_id(id_number)
            return float(result["v"])
        except:
            pass

    def set_fan_source_table(self):
        self.fan_source_table = {}
        initial = 16909057
        for i in range(64):
            register = initial+i
            if register in self.device_id_list:
                name = self.get_data_by_id(register)['n']
                self.voltage_source_table.update({name: register})

    @property
    def fan_sources(self) -> List[str]:
        if self.fan_source_table == None:
            self.set_fan_source_table()
        return self.fan_source_table

    def get_direction(self, pin: str) -> None:
        gpio_number_initial = 17039617
        gpio_target_initial = 17039873  # first gpio dir id
        gpio_id_number = self.gpio_table[pin]
        diff_number = gpio_id_number-gpio_number_initial
        return self.get_data_by_id(gpio_target_initial+diff_number)['bv']

    def set_direction(self, pin: str, direction: GpioDirectionType) -> None:
        gpio_number_initial = 17039617
        gpio_target_initial = 17039873  # first gpio level id
        gpio_id_number = self.gpio_table[pin]
        diff_number = gpio_id_number-gpio_number_initial
        self.set_value(gpio_target_initial+diff_number, direction.value)

    def get_level(self, pin: str) -> None:
        gpio_number_initial = 17039617
        gpio_target_initial = 17040129  # first gpio level id
        gpio_id_number = self.gpio_table[pin]
        diff_number = gpio_id_number-gpio_number_initial
        return self.get_data_by_id(gpio_target_initial+diff_number)['bv']

    def set_level(self, pin: str, level: GpioLevelType) -> None:
        gpio_number_initial = 17039617
        gpio_target_initial = 17039873  # first gpio dir id
        gpio_id_number = self.gpio_table[pin]
        diff_number = gpio_id_number-gpio_number_initial
        dir_value = self.get_data_by_id(gpio_target_initial+diff_number)['bv']
        if dir_value == 1:
            return "error: set gpio level must in output, the direction is input now"

        gpio_target_initial = 17040129  # first gpio level id
        self.set_value(gpio_target_initial+diff_number, level.value)
        dir_value = self.get_data_by_id(gpio_target_initial+diff_number)['bv']
        if dir_value == level.value:
            return True
        else:
            return False


class JsonType:
    JSON_OBJECT = 0
    JSON_ARRAY = 1
    JSON_STRING = 2
    JSON_INTEGER = 3
    JSON_REAL = 4
    JSON_TRUE = 5
    JSON_FALSE = 6
    JSON_NULL = 7


class JsonT(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_int),
        ("refcount", ctypes.c_size_t)
    ]
