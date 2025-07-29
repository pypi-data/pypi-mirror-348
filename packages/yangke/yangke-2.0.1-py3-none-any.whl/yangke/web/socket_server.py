#!/usr/bin/python3
# 文件名：server.py

# 导入 socket、sys 模块
import socket
import sys
import time

from yangke.base import start_threads, execute_function_by_interval
from yangke.common.config import logger
from queue import Queue  # Queue是线程安全的，因此可以替代我们对操作进行加锁
import uuid

from yangke.web.flaskserver import start_server_app


def deal(msg):
    print(f"Server: 回调函数收到消息{msg}")


class YkSocketServer:
    def __init__(self, port=9990, host='localhost', callback=None):
        """
        创建并初始化一个服务器监听端口。使用示例：
sock = YkSocketServer(callback=deal) # deal为回调函数，该类会自动将端口接收到的消息传递给deal的第一个参数，参考本模块的deal方法
sock.start_server(damon=False)
# 等待连接后，可以调用send方法发送消息
sock.send('服务器消息')

        Parameters
        ----------
        port
        host
        callback: 服务器接收到客户端消息时的回调函数
        """
        self.host = "0.0.0.0" if host == "localhost" else host  # socket.gethostname()在linux上可能报错：socket.gaierror: [Errno -2] Name or service not known
        self.port = port
        # 创建 socket 对象
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 绑定端口号
        self.server_socket.bind((self.host, self.port))
        print(f"监听{self.host}:{self.port}...")

        # 设置最大连接数，超过后排队
        self.server_socket.listen(5)  # 只能连接一个客户端

        self.connected_sockets = None
        self.callback = callback  # 当端口上接收到客户端发送的消息时，会回调该方法
        self.answers = Queue()  # Queue是线程安全的，在多线程中，会自动对资源进行锁的获取与释放

    def forward(self, msg):
        """
        当服务器接收到客户端消息时，会自动执行该方法
        Parameters
        ----------
        msg

        Returns
        -------

        """
        msg = eval(msg)  # 将返回的msg字符串转换为dict对象
        self.answers.put(msg)
        if self.answers.qsize() > 100:  # 保证Queue对象中的消息不超过100个
            for i in range(50):
                self.answers.get()  # 只保留最后50条消息
        if self.callback is None:
            self.callback = deal
        self.callback(msg)

    def start_server(self, damon=True):
        """
        开启socket服务监听，等待客户端连接
        Parameters
        ----------
        damon： 是否守护线程，如果不守护，将在新进程里开启监听，该方法不会阻塞，否则该方法阻塞监听端口连接

        Returns
        -------

        """
        start_threads(self.on_msg_received)  # 开启新线程，持续检测端口是否接收到新的数据，并执行deal函数对收到的数据进行处理
        self.send("服务器发送的消息！！YK")
        logger.debug("等待[计算服务器]连接，连接后才可以处理http请求")
        if damon:
            while True:
                # 建立客户端连接
                client_socket, addr = self.server_socket.accept()  # 会阻塞，如果连接进来，则clientsocket会返回一个可通信的对象
                self.connected_sockets = client_socket
                logger.debug("[计算服务器]已连接，连接地址: %s" % str(addr))
                msg = 'connect done'
                client_socket.send(msg.encode('utf-8'))
        else:
            def _start_server():
                while True:
                    # 建立客户端连接
                    client_socket, addr = self.server_socket.accept()  # 会阻塞，如果连接进来，则clientsocket会返回一个可通信的对象
                    self.connected_sockets = client_socket
                    logger.debug("[计算服务器]已连接，连接地址: %s" % str(addr))
                    client_socket.send('connect done！'.encode('utf-8'))

            start_threads(_start_server)

    def on_msg_received(self):
        print(f"开始监听端口，并接收消息，如收到消息，会回调{self.callback}")
        while True:
            # 接收小于 1024 字节的数据
            if self.connected_sockets is not None:
                msg = self.connected_sockets.recv(1024)
                self.forward(msg.decode('utf8'))

    def send(self, msg):
        msg = str(msg).encode('utf8')
        if self.connected_sockets is not None:
            self.connected_sockets.send(msg)

    def get_answer_by_id(self, aid):
        answers = list(self.answers.queue)
        for a in answers:  # 因为on_message_received线程在修改self.answers，因此可能需要对资源加锁
            if a.get("mid") == aid:
                return a
        return None

    def get_answer_of_send(self, msg: dict):
        """
        向客户端发送消息，并获取客户端的回复，调用该方法时，不能设置callback参数，必须callback==None

        Parameters
        ----------
        msg        http请求里的参数的字典

        Returns
        -------

        """
        message_id = uuid.uuid1().hex
        msg.update({"mid": message_id})
        msg = str(msg)  # 将int/float/dict等类型统一转换为字符串
        if self.connected_sockets is None:
            logger.warning(f"公网ipv4服务器已经接收到客户端的请求，但尚未收到真正的内网服务器的连接请求，因此无法与内网服务器建立连接！")
            logger.warning(f"请先启动【内网服务器】上的socket客户端，以完成http请求的最终处理！")
            return {"Error": "请先启动【内网服务器】上的socket客户端，以完成http请求的最终处理！"}
        self.send(msg)
        # 循环扫描接收到的消息，找出与本次发送相对应的，并返回
        while self.get_answer_by_id(message_id) is None:  # 此处虽然在查询self.answers，但是并不占用锁
            time.sleep(1)
        answer = self.get_answer_by_id(message_id)
        return answer


def socket_communication_server(port=9990, call_back=None):
    """
    开启websocket通信，监听本机9990端口，如果本机接受到请求，可以通过该接口将请求转发至另一台电脑。
    转发请求时。使用socket.send(msg)即可，本方法不会阻塞主进程

    Returns
    -------

    """
    socket1 = YkSocketServer(port=port, callback=call_back)
    socket1.start_server(damon=False)  # 启动后持续监听本机指定端口，不阻塞
    return socket1


if __name__ == "__main__":
    sock = socket_communication_server(call_back=deal, port=9990)  #
    while True:
        sock.send("server 1")
        time.sleep(5)
