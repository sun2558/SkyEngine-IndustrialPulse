from pyModbusTCP.server import DataBank, ModbusServer
import random

class MyDataBank(DataBank):
    def get_holding_registers(self, address, number, srv_info):
        # 保持寄存器（40001）返回模拟温度值
        if address == 0:
            return [int(random.uniform(20, 35) * 10)]
        return [0] * number

    def get_coils(self, address, number, srv_info):
        # 线圈地址0返回布尔值1
        if address == 0:
            return [1]
        return [0] * number

if __name__ == '__main__':
    server = ModbusServer(host="0.0.0.0", port=502, data_bank=MyDataBank())
    print("Modbus服务端已启动,监听端口502,模拟温度数据...")
    server.start()