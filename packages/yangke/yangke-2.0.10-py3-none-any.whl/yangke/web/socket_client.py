import json
import websocket

channels_ws = []


class Feed(object):
    def __init__(self):
        self.url = 'ws://192.168.3.9:9990'
        self.ws = None

    def on_open(self, ws):
        print('A new WebSocketApp is opened!')
        sub_param = {"op": "subscribe", "args": channels_ws}
        sub_str = json.dumps(sub_param)
        ws.send(sub_str)
        print("Following Channels are subscribed!")
        print(channels_ws)

    def on_data(self, ws, string, type, continue_flag):
        """

        Args:
            ws: this class object
            string: a utf8 string which we get from the server
            type: data type, ABNF.OPCODE_TEXT or ABNF.OPCODE_BINARY
            continue_flag:

        Returns:

        """
        ...

    def on_message(self, ws, message):
        """
        当接收到消息时的回调函数
        Args:
            ws: the WebSocketApp object
            message: 从服务器接收到的消息

        Returns:

        """
        result = message
        print(result)

    def on_error(self, ws, error):
        """
        当遇到错误时的回调函数
        Args:
            ws:
            error: exception object

        Returns:

        """
        print(error)

    def on_close(self, ws, close_status_code, close_msg):
        """
        连接关闭时的回调函数

        Args:
            ws:
            close_status_code:
            close_msg:

        Returns:

        """
        print("连接已经关闭")

    def start(self):
        self.ws = websocket.WebSocketApp(
            self.url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_data=self.on_data,
            on_error=self.on_error,
            on_close=self.on_close,

        )
        self.ws.run_forever()


if __name__ == "__main__":
    feed = Feed()
    feed.start()
