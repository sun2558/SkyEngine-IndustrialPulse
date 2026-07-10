from pyModbusTCP.server import DataBank, ModbusServer
import random
import time

class MyDataBank(DataBank):
    def get_holding_registers(self, address, number, srv_info):
        # 模拟温度数据，在寄存器40001返回随机值
        if address == 0:  # 40001对应的内部地址是0
            return [int(random.uniform(20, 35) * 10)]  # 20~35℃
        return [0] * number

if __name__ == '__main__':
    server = ModbusServer(host="0.0.0.0", port=502, data_bank=MyDataBank())
    print("Modbus服务端已启动,监听端口502,模拟温度数据...")
    server.start()