from pyModbusTCP.server import DataBank, ModbusServer
import random

class MyDataBank(DataBank):
    def read_holding_registers(self, address, count, srv_info):
        print(f"收到读保持寄存器请求: address={address}, count={count}")
        if address == 0:
            return [int(random.uniform(20, 35) * 10)]
        return [0] * count
    
    def read_coils(self, address, count, srv_info):
        print(f"收到读线圈请求: address={address}, count={count}")
        if address == 0:
            return [1] * count
        return [0] * count

if __name__ == '__main__':
    server = ModbusServer(host="0.0.0.0", port=502, data_bank=MyDataBank())
    print("Modbus服务端已启动,监听端口502,模拟数据...")
    server.start()