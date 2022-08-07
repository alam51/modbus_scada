import time
import traceback
import numpy as np
import pandas as pd
import serial
# import modbus_tk.defines as tkCst
# import modbus_tk.modbus_rtu as tkRtu
#
# import minimalmodbus as mmRtu

from pymodbus.client.sync import ModbusSerialClient as pyRtu
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder

slavesArr = [1]
slave_addr = 1
reg_addr = 16394  # pt2
iteration_count = 200
register_count = 2
# portNbr = 4
portName = 'com4'
baudrate = 19200

timeoutSp = 0.018 + register_count * 0
print("timeout: %s [s]" % timeoutSp)

pymc = pyRtu(method='rtu', port=portName, baudrate=baudrate, timeout=timeoutSp)

errCnt = 0
startTs = time.time()

pt1 = pymc.read_holding_registers(4101, 2, unit=slave_addr)
pt2 = pymc.read_holding_registers(4103, 1, unit=slave_addr)

for i in range(iteration_count + 1):
    for slaveId in slavesArr:
        try:
            val = pymc.read_holding_registers(reg_addr, register_count, unit=slaveId)
            decoder = BinaryPayloadDecoder.fromRegisters(val.registers, Endian.Big,
                                                         wordorder=Endian.Big
                                                         )
            float_op = decoder.decode_32bit_float()
            print(f'Iteration: {i}; slave id: {slaveId}; value: {float_op:.2f}')
            time.sleep(.2)
        except:
            errCnt += 1
            tb = traceback.format_exc()
stopTs = time.time()
timeDiff = stopTs - startTs
print("pymodbus:\ttime to read %s x %s (x %s regs): %.3f [s] / %.3f [s/req]" % (
    len(slavesArr), iteration_count, register_count, timeDiff, timeDiff / iteration_count))
if errCnt > 0:
    print("   !pymodbus:\terrCnt: %s; last tb: %s" % (errCnt, tb))
pymc.close()
