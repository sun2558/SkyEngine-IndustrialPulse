from pyModbusTCP.server import DataBank, ModbusServer
import random

class MyDataBank(DataBank):
    def read_holding_registers(self, address, count, srv_info):
        # 保持寄存器（40001）返回模拟温度值
        if address == 0:
            return [int(random.uniform(20, 35) * 10)]
        return [0] * count
    
    def read_coils(self, address, count, srv_info):
        # 线圈地址0返回布尔值1，让网关能读到数据
        if address == 0:
            return [1] * count
        return [0] * count

if __name__ == '__main__':
    server = ModbusServer(host="0.0.0.0", port=502, data_bank=MyDataBank())
    print("Modbus服务端已启动,监听端口502,模拟数据...")
    server.start()