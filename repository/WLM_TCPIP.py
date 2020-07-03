from artiq.experiment import *
import socket
import time

class TCPIP_LaserFrequency(EnvExperiment):
    """TCPIP_LaserFrequency"""

    def build(self):
        pass
    
    def prepare(self):
        pass
        
    def run(self):
        sk = socket.socket()

        # 绑定一个ip和端口
        # Bind an IP
        sk.bind(("192.168.0.76",8888))

        # 服务器端一直监听是否有客户端进行连接
        # listening for the Client
        sk.listen(5)
        conn,addr = sk.accept()
        
        # 设置光速
        # Define the speed of the light
        C_Chamber=299792.458
        
        # 设置397与866的失谐量标定值
        Standard_397=755.222800
        Standard_866=346.000280

        while 1:
            
            #从客户端接收数据
            # Recieve the data from the Client
            rev_data = conn.recv(1024).decode('GB2312')
            
            #数据类型为：X Y, X 为激光的参数， Y 为激光的波长
            #The data should be like: X Y,X is the number of the laser,Y is nanometer.
            rev_array = rev_data.split()
            
            # 根据收集到的信息来对特定的激光频率赋值
            # brodcast the frequency of lasers according to the number of the laser
            
            # NA
            if rev_array[0]=="1":
                data_nm = float(rev_array[1])
                data_frequency = C_Chamber/data_nm
                self.set_dataset("Laser1", float(format(data_frequency, '.6f')), broadcast=True)
                
            # 866
            elif rev_array[0]=="2":
                data_nm = float(rev_array[1])
                data_frequency = C_Chamber/data_nm
                data_deturning = (data_frequency-Standard_866)*10**6
                
                self.set_dataset("Laser2", float(format(data_frequency, '.6f')), broadcast=True)
                self.set_dataset("Deturning866", float(format(data_deturning, '.0f')), broadcast=True)
                
            # 729
            elif rev_array[0]=="3":
                data_nm = float(rev_array[1])
                data_frequency = C_Chamber/data_nm
                self.set_dataset("Laser3", float(format(data_frequency, '.6f')), broadcast=True)
                
            # 423
            elif rev_array[0]=="4":
                data_nm = float(rev_array[1])
                data_frequency = C_Chamber/data_nm
                self.set_dataset("Laser4", float(format(data_frequency, '.6f')), broadcast=True)
            
            # 397
            elif rev_array[0]=="5":
                data_nm = float(rev_array[1])
                data_frequency = C_Chamber/data_nm
                data_deturning = (data_frequency-Standard_397)*10**6
                
                self.set_dataset("Laser5", float(format(data_frequency, '.6f')), broadcast=True)
                self.set_dataset("Deturning397", float(format(data_deturning, '.0f')), broadcast=True)
                
            # 854
            elif rev_array[0]=="6":
                data_nm = float(rev_array[1])
                data_frequency = C_Chamber/data_nm
                self.set_dataset("Laser6", float(format(data_frequency, '.6f')), broadcast=True)
            
            # NA
            elif rev_array[0]=="7":
                data_nm = float(rev_array[1])
                data_frequency = C_Chamber/data_nm
                self.set_dataset("Laser7", float(format(data_frequency, '.6f')), broadcast=True)
            
            # NA
            elif rev_array[0]=="8":
                data_nm = float(rev_array[1])
                data_frequency = C_Chamber/data_nm
                self.set_dataset("Laser8", float(format(data_frequency, '.6f')), broadcast=True)
                
            # 设置每个数据的刷新时间
            # Set the period for updating
            time.sleep(0.1)
            
            # 服务端给客户端回消息
            # Send the message back to the Client
            to_be_sent_data="1"
            conn.send(to_be_sent_data.encode('GB2312'))

        # 关闭socket对象
        # Close the socket
        conn.close()