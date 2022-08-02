import time
import traceback
import serial
import modbus_tk.defines as tkCst
import modbus_tk.modbus_rtu as tkRtu

import minimalmodbus as mmRtu

from pymodbus.client.sync import ModbusSerialClient as pyRtu

slavesArr = [2]
reg_addr = 4101  # pt2
iteration_count = 10
register_count = 1
portNbr = 2
portName = 'com2'
baudrate = 9600

timeoutSp = 0.018 + register_count * 0
print("timeout: %s [s]" % timeoutSp)

mmc = mmRtu.Instrument(portName, 2)  # port name, slave address
mmc.serial.baudrate = baudrate
mmc.serial.timeout = timeoutSp

tb = None
errCnt = 0
startTs = time.time()
for i in range(iteration_count):
    for slaveId in slavesArr:
        mmc.address = slaveId
        try:
            mmc.read_registers(reg_addr, register_count)
        except:
            tb = traceback.format_exc()
            errCnt += 1
stopTs = time.time()
timeDiff = stopTs - startTs

mmc.serial.close()

print(mmc.serial)

print("mimalmodbus:\ttime to read %s x %s (x %s regs): %.3f [s] / %.3f [s/req]" % (
    len(slavesArr), iteration_count, register_count, timeDiff, timeDiff / iteration_count))
if errCnt > 0:
    print("   !mimalmodbus:\terrCnt: %s; last tb: %s" % (errCnt, tb))

pymc = pyRtu(method='rtu', port=portName, baudrate=baudrate, timeout=timeoutSp)

errCnt = 0
startTs = time.time()
for i in range(iteration_count):
    for slaveId in slavesArr:
        try:
            pymc.read_holding_registers(reg_addr, register_count, unit=slaveId)
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

tkmc = tkRtu.RtuMaster(serial.Serial(port=portName, baudrate=baudrate))
tkmc.set_timeout(timeoutSp)

errCnt = 0
startTs = time.time()
for i in range(iteration_count):
    for slaveId in slavesArr:
        try:
            tkmc.execute(slaveId, tkCst.READ_HOLDING_REGISTERS, reg_addr, register_count)
        except:
            errCnt += 1
            tb = traceback.format_exc()
stopTs = time.time()
timeDiff = stopTs - startTs
print("modbus-tk:\ttime to read %s x %s (x %s regs): %.3f [s] / %.3f [s/req]" % (
    len(slavesArr), iteration_count, register_count, timeDiff, timeDiff / iteration_count))
if errCnt > 0:
    print("!modbus-tk:\terrCnt: %s; last tb: %s" % (errCnt, tb))
tkmc.close()
