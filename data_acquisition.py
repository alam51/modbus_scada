from pymodbus.client.sync import ModbusSerialClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian
from modbus_initialize import SlaveAcuvim2
port_name = 'com4'
baud_rate = 9600
time_out_second = .2
modbus_rtu_master = ModbusSerialClient(method='rtu', port=port_name, baudrate=baud_rate, timeout=time_out_second)
a = 9

slave_list = []
slave_address_list = [1, 2, 3]
for i, slave_id in enumerate(slave_address_list):
    slave_list[i] = SlaveAcuvim2(modbus_rtu_master, slave_id=slave_id)
"""Initialization Complete"""

for slave in slave_list:
    f = slave.get_frequency()
    v = slave.get_voltage_LL_average()
    ia = slave.get_current_a()
    ib = slave.get_current_b()
    ic = slave.get_current_c()
    i_n = slave.get_current_neutral()
    p = slave.get_real_power_total()
    q = slave.get_reactive_power_total()
    p_import = slave.get_import_active_power_total()
    q_import = slave.get_import_

