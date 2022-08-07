from pymodbus.client.sync import ModbusSerialClient
import pymodbus
slave_id_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


class Slave:
    def __init__(self, slave_id):
        modbus_conn = pymodbus