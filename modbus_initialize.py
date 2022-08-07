from pymodbus.client.sync import ModbusSerialClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian


def decode_float_from_holding_register(holding_register_response):
    decoder = BinaryPayloadDecoder.fromRegisters(holding_register_response.registers, Endian.Big,
                                                 wordorder=Endian.Big
                                                 )
    return decoder.decode_32bit_float()


def decode_double_word_from_holding_register(holding_register_response):
    val_list = holding_register_response.registers
    return val_list[0] * (2 ** 16) + val_list[1]


class SlaveAcuvim2:
    def __init__(self, master: ModbusSerialClient, slave_id: int):
        self.master = master
        self.slave_id = slave_id

        response = master.read_holding_registers(4101, 2, unit=slave_id)
        self.pt1 = decode_double_word_from_holding_register(response)
        self.pt2 = master.read_holding_registers(4103, 1, unit=slave_id).registers[0]

        self.ct1 = master.read_holding_registers(4104, 1, unit=slave_id).registers[0]
        self.ct2 = master.read_holding_registers(4105, 1, unit=slave_id).registers[0]

    def get_frequency(self):
        response = self.master.read_holding_registers(16384, 2, unit=self.slave_id).registers
        primary_reading = decode_float_from_holding_register(response)
        return primary_reading

    def get_voltage_LL_average(self):
        response = self.master.read_holding_registers(16400, 2, unit=self.slave_id).registers
        primary_reading = decode_float_from_holding_register(response)
        return primary_reading * (self.pt1 / self.pt2)

    def get_current_a(self):
        # Line current of phase a
        response = self.master.read_holding_registers(16402, 2, unit=self.slave_id).registers
        primary_reading = decode_float_from_holding_register(response)
        return primary_reading * (self.ct1 / self.ct2)

    def get_current_b(self):
        # Line current of phase b
        response = self.master.read_holding_registers(16404, 2, unit=self.slave_id).registers
        primary_reading = decode_float_from_holding_register(response)
        return primary_reading * (self.ct1 / self.ct2)

    def get_current_c(self):
        # Line current of phase c
        response = self.master.read_holding_registers(16406, 2, unit=self.slave_id).registers
        primary_reading = decode_float_from_holding_register(response)
        return primary_reading * (self.ct1 / self.ct2)

    def get_current_neutral(self):
        # Line current of neutral
        response = self.master.read_holding_registers(16410, 2, unit=self.slave_id).registers
        primary_reading = decode_float_from_holding_register(response)
        return primary_reading * (self.ct1 / self.ct2)

    def get_real_power_total(self):
        # Total System Power
        response = self.master.read_holding_registers(16402, 2, unit=self.slave_id).registers
        primary_reading = decode_float_from_holding_register(response)
        return primary_reading * (self.pt1 / self.pt2) * (self.ct1 / self.ct2) / 1000

    def get_reactive_power_total(self):
        # Total System Power
        response = self.master.read_holding_registers(16426, 2, unit=self.slave_id).registers
        primary_reading = decode_float_from_holding_register(response)
        return primary_reading * (self.pt1 / self.pt2) * (self.ct1 / self.ct2) / 1000

    def get_import_real_energy_total(self):
        # Total System Power
        response = self.master.read_holding_registers(16456, 2, unit=self.slave_id).registers
        primary_reading = decode_double_word_from_holding_register(response)
        return primary_reading / 1000

    def get_import_reactive_energy_total(self):
        # Total System Power
        response = self.master.read_holding_registers(16460, 2, unit=self.slave_id).registers
        primary_reading = decode_double_word_from_holding_register(response)
        return primary_reading / 1000

    def get_export_real_energy_total(self):
        # Total System Power
        response = self.master.read_holding_registers(16458, 2, unit=self.slave_id).registers
        primary_reading = decode_double_word_from_holding_register(response)
        return primary_reading / 1000

    def get_export_reactive_energy_total(self):
        # Total System Power
        response = self.master.read_holding_registers(16462, 2, unit=self.slave_id).registers
        primary_reading = decode_double_word_from_holding_register(response)
        return primary_reading / 1000


