from flask import Flask, request, make_response
import hashlib
import xml.etree.ElementTree as ET
from yangke.common.config import logger, add_file_logger
from yangke.web.flaskserver import start_server_app
from yangke.web.socket_server import socket_communication_server, YkSocketServer

socket: YkSocketServer | None = None


# app = Flask(__name__)


# @app.route('/', methods=['GET', 'POST'])
# def wechat_auth():
#     logger.debug(f"receive request")
#     if request.method == 'GET':
#         logger.debug("接收到GET请求")
#         token = '5d9d54c798119aab5dfc126ea45432a2'  # 替换为自己在公众号设置中的Token
#         data = request.args
#         signature = data.get('signature', '')
#         timestamp = data.get('timestamp', '')
#         nonce = data.get('nonce', '')
#         echostr = data.get('echostr', '')
#         list = [token, timestamp, nonce]
#         list.sort()
#         s = ''.join(list).encode('utf-8')
#         if (hashlib.sha1(s).hexdigest() == signature):
#             return make_response(echostr)
#         else:
#             return 'Invalid Signature'
#     else:
#         logger.debug("接收到POST请求")
#         xml_data = request.stream.read()
#         xml_tree = ET.fromstring(xml_data)
#         msg_type = xml_tree.find('MsgType').text
#         if msg_type == 'text':
#             content = xml_tree.find('Content').text
#             response_content = chat_with_gpt(content)
#             response = generate_text_response(xml_tree, response_content)
#             return make_response(response)
#         else:
#             response_content = '暂不支持该类型消息的回复。'
#             response = generate_text_response(xml_tree, response_content)
#             return make_response(response)

def on_receive_msg(msg):
    """
    接收到服务器的消息时，执行该方法，如果是转发请求，需要在该方法中将msg发送给需要转发的对象计算机

    Parameters
    ----------
    msg

    Returns
    -------

    """
    # todo 将msg转发给发送请求的计算机
    logger.debug(f"接收到客户端的消息：{msg}")


def deal(text: dict):
    """
    将请求参数发送给远程服务器，由远程服务器处理，本机只做数据转发
    Parameters
    ----------
    text

    Returns
    -------

    """
    global socket
    if socket is not None:
        res = socket.get_answer_of_send(text)  # 当访问http://{ipv4}:{port_of_ipv4}/时，text为空字典{}
        return res
    socket.send(text)
    return {"error": "未知结果"}


def http_transfer_server(http_listen_port=80, transfer_listen_port=9990):
    """
    http请求转发方法，默认将请求到本机80端口的数据转发给远程服务器9990端口，无需指定远程服务器ip，但需要本机具有公网ipv4地址，远程服务器和
    http请求发送者都会通过本机ipv4地址建立连接

    Parameters
    ----------
    http_listen_port: 接受http请求的端口号
    transfer_listen_port: websocket转发请求信息的端口号，本端口与另一台真正提供服务的服务器通信

    Returns
    -------

    """
    global socket
    # 初始化socket，在本机建立websocket通讯，使用9990端口与真正的服务器进行通讯，后续可以使用socket.send方法转发数据
    socket = socket_communication_server(call_back=on_receive_msg, port=transfer_listen_port)

    logger.debug(
        f"http请求转发方法，将请求到本机{http_listen_port}端口的数据转发给远程服务器{transfer_listen_port}端口，无需指定远程服务器ip，但需要本机具有公网ipv4地址，远程服务器和http请求发送者都会通过本机ipv4地址建立连接\n")
    logger.debug(f"正在监听0.0.0.0:{http_listen_port}")

    # 在本机80端口启动服务，使互联网上的计算机可以请求该服务，在接收到请求后，在deal方法中将请求转发给真正的服务器
    start_server_app(deal=deal, host="0.0.0.0", port=http_listen_port, use_action=False)


if __name__ == "__main__":
    add_file_logger('log.txt')
    http_transfer_server(http_listen_port=8080)
    # 测试url: http://localhost:80/?Action=ChatGPT&Question=核电站给水流量孔板的精度是多少？
