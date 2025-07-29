import unittest

import advantech

class TestPlatformInformation(unittest.TestCase):
    
    def test_platfomr_information(self):
        
        print("\n---------------------------------------")
        
        device = advantech.edge.Device()
        print(f"Motherboard Manufacturer : {device.platform_information.manufacturer}")
        print(f"Motherboard Name : {device.platform_information.motherboard_name}")
        print(f"BIOS Revision : {device.platform_information.bios_revision}")
        print(f"Library Version : {device.platform_information.library_version}")

class TestOnboardSensors(unittest.TestCase):
    
    def test_onboard_sensors_temperature(self):
        
        print("\n---------------------------------------")
        
        device = advantech.edge.Device() 
        for src in device.onboard_sensors.temperature_sources:
            print(f"{src}: {device.onboard_sensors.get_temperature(src)} degrees Celsius")
    
    def test_onboard_sensors_voltage(self):
        
        print("\n---------------------------------------")
        
        device = advantech.edge.Device()
        for src in device.onboard_sensors.voltage_sources:
            print(src, device.onboard_sensors.get_voltage(src))
            
    def test_onboard_sensors_fan_speed(self):
        
        print("\n---------------------------------------")
        
        device = advantech.edge.Device()
        for src in device.onboard_sensors.fan_sources:
            print(src)

class TestGpio(unittest.TestCase):
    
    def test_get_pin_states(self):
        
        print("\n---------------------------------------")
        
        device = advantech.edge.Device()
        for pin in device.gpio.pins:
            dir = device.gpio.get_direction(pin)
            level = device.gpio.get_level(pin)
            print(f"Pin {pin} : direction : {dir}, level : {level}")

    def test_set_gpio_direction(self):
        
        print("\n---------------------------------------")
        
        device = advantech.edge.Device()
        original_dir = 0
        updated_dir = 0
        print()
        for pin in device.gpio.pins:
            device.gpio.set_direction(pin, advantech.edge.igpio.GpioDirectionType.INPUT)
            print(f"{pin}, direction:{device.gpio.get_direction(pin)}")
            device.gpio.set_direction(pin, advantech.edge.igpio.GpioDirectionType.OUTPUT)
            print(f"{pin}, direction:{device.gpio.get_direction(pin)}")

    def test_set_gpio_level(self):
        
        print("\n---------------------------------------")
        
        device = advantech.edge.Device()
        for pin in device.gpio.pins:
            device.gpio.set_direction(pin, advantech.edge.igpio.GpioDirectionType.INPUT)  # must in input model
            result = device.gpio.set_level(pin, advantech.edge.igpio.GpioLevelType.HIGH)
            print(f"set {pin} level result: {result}")
            result = device.gpio.set_level(pin, advantech.edge.igpio.GpioLevelType.LOW)
            print(f"set {pin} level result: {result}")

class TestSDRAM(unittest.TestCase):
    
    def test_sdram(self):
        
        print("\n---------------------------------------")
        
        device = advantech.edge.Device()
        print(f"memory count: {device.memory.memory_count}")
        for i in range(device.memory.memory_count):
            print(f"Memory {i} :")
            print(f"-\tType : {device.memory.get_memory_type(i)}")
            print(f"-\tModule type : {device.memory.get_module_type(i)}")
            print(f"-\tSize in GB : {device.memory.get_memory_size_in_GB(i)}")
            print(f"-\tSpeed : {device.memory.get_memory_speed(i)} MT/s")
            print(f"-\tRank : {device.memory.get_memory_rank(i)}")
            print(f"-\tVoltage : {device.memory.get_memory_voltage(i)} v")
            print(f"-\tBank : {device.memory.get_memory_bank(i)}")
            print(f"-\tManufacturing date code week/year : {device.memory.get_memory_manufacturing_date_code(i)}")
            print(f"-\tTemperature : {device.memory.get_memory_temperature(i)} degrees Celsius")
            print(f"-\tWrite protection : {device.memory.get_memory_write_protection(i)}")
            print(f"-\tModule manufacturer : {device.memory.get_memory_module_manufacture(i)}")
            print(f"-\tManufacture : {device.memory.get_memory_manufacture(i)}")
            print(f"-\tPart number : {device.memory.get_memory_part_number(i)}")
            print(f"-\tSpecific : {device.memory.get_memory_specific(i)}")

class TestDiskInfo(unittest.TestCase):
    
    def test_disk_info(self):
        
        print("\n---------------------------------------")
        
        device = advantech.edge.Device()
        print(f"Total Disk Space: {device.disk.total_disk_space} MB")
        print(f"Free Disk Space: {device.disk.free_disk_space} MB")

class TestListAndCount(unittest.TestCase):
    
    def test_memory_list(self):
        
        print("\n---------------------------------------")
        
        device = advantech.edge.Device()
        for src in device.memory.memory_list:
            print(src)

if __name__ == '__main__':
    unittest.main()
