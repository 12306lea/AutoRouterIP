from httpUtils import HTTPClient


class baseRouter:
    def __init__(self):
        self.httpClient = HTTPClient(0)

    def login(self, RouterPwd):
        """
        登录
        :param RouterPwd:
        :return:
        """
        pass

    def disconnect(self):
        """
        断开路由
        :return:
        """
        pass

    def connect(self, broadbandUserName, broadbandPwd):
        """
        启动路由
        :return:
        """
        pass
