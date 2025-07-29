
from .susiiot import SusiIot


class Device:
    def __init__(self):
        self.platform_information = None
        self.onboard_sensors = None
        self.gpio = None
        self.memory = None
        self.disk = None

        susiiot_object = SusiIot()

        self.platform_information = susiiot_object
        self.onboard_sensors = susiiot_object
        self.gpio = susiiot_object
        self.memory = susiiot_object
        self.disk = susiiot_object

    def is_support_susiiot(device_number):
        susiiot_support_list = [
            "EPC-T4286",
        ]
        if device_number in susiiot_support_list:
            return True
        return False

    def is_support_platform_sdk(device_number):
        platform_sdk_support_list = [
            "",
        ]
        if device_number in platform_sdk_support_list:
            return True
        return False
