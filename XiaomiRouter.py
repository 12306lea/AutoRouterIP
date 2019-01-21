import copy
import random
import re
import time

from Crypto.Hash import SHA

from BaseRouter import baseRouter
from config import RouterConfig
from config.urlConf import urls


class xiaomiRouter(baseRouter):
    def __init__(self):
        super().__init__()
        self.stok = None

    def getDeviceId(self):
        """
        获取设备唯一表示
        :return:
        """
        homeRsp = self.httpClient.send(urls=urls.get("xiaomiHome"))
        deviceId = re.findall(r'deviceId = \'(.*)\';', homeRsp)[0]
        return deviceId

    def secretJs(self, password):
        """
        TPLINK加密登录密码
        :return:
        """
        key = 'a2ffa5c9be07488bbb04a3a47d3c5f6a'
        mac = self.getDeviceId()
        nonce = "0_" + mac + "_" + str(int(time.time())) + "_" + str(random.randint(1000, 10000))
        pwd = SHA.new()
        pwd.update(password.encode("utf8") + key.encode("utf8"))
        hexpwd1 = pwd.hexdigest()

        pwd2 = SHA.new()
        pwd2.update(nonce.encode("utf8") + hexpwd1.encode("utf8"))
        hexpwd2 = pwd2.hexdigest()
        return hexpwd2, nonce

    def login(self, RouterPwd):
        """
        登录
        :param RouterPwd:
        :return:
        """
        secretRouterPwd, nonce = self.secretJs(RouterPwd)
        TPLinkRouterUrls = urls.get("xiaomi")
        data = {
            "username":	"admin",
            "password":	secretRouterPwd,
            "logtype": 2,
            "nonce": nonce,
        }
        loginRsp = self.httpClient.send(urls=TPLinkRouterUrls, data=data)
        if loginRsp.get("code") is 0:
            print("路由器登录成功")
            self.stok = loginRsp.get("url").split("web/")[0]
        else:
            print("小米路由器登录失败：{}".format(loginRsp))

    def disconnect(self):
        if self.stok:
            disconnectUrl = copy.deepcopy(urls["xiaomi"])
            disconnectUrl["req_url"] = self.stok + "api/xqnetwork/pppoe_stop"
            disconnectRsp = self.httpClient.send(urls=disconnectUrl)
            if disconnectRsp.get("code") is 0:
                print("断开连接成功")
            else:
                print("断开路由器失败: {}".format(disconnectRsp))

    def connect(self, broadbandUserName=None, broadbandPwd=None):
        connectUrl = copy.deepcopy(urls["xiaomi"])
        connectUrl["req_url"] = self.stok + "/api/xqnetwork/pppoe_start"
        connectRsp = self.httpClient.send(connectUrl)
        if connectRsp.get("code") is 0:
            statusUrl = copy.deepcopy(urls["xiaomi"])
            statusUrl["req_url"] = self.stok + "/api/xqnetwork/pppoe_status"
            statusRsp = ""
            for i in range(10):
                statusRsp = self.httpClient.send(statusUrl)
                address = statusRsp.get("ip", {}).get("address")
                if statusRsp.get("code") is 0 and address:
                    print("路由器重新拨号成功, iP地址为: {}".format(address))
                    break
                else:
                    time.sleep(0.5)
            else:
                print("路由器拨号失败: {}".format(statusRsp))
        else:
            print("拨号失败: {}".format(connectRsp))

    def main(self):
        while True:
            self.login(RouterConfig.routerPwd)
            self.disconnect()
            self.connect(RouterConfig.broadbandUserName, RouterConfig.broadbandPwd)
            time.sleep(RouterConfig.routerTime * 60)


if __name__ == '__main__':
    xm = xiaomiRouter()
    xm.login("")
    xm.disconnect()
    xm.connect()
