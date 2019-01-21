import copy
import json
import time
import execjs
from BaseRouter import baseRouter
from config import RouterConfig
from config.urlConf import urls


class tpLinkRouter(baseRouter):
    def __init__(self):
        super().__init__()
        self.stok = None

    def secretJs(self, pwd):
        """
        TPLINK加密登录密码
        :return:
        """
        jsStr = """
        function a() {
            a = '""" + pwd + """';
            c = 'RDpbLfCPsJZ7fiv';
            b = 'yLwVl0zKqws7LgKPRQ84Mdt708T1qQ3Ha7xv3H7NyU84p21BriUWBU43odz3iP4rBL3cD02KZciXTysVXiV8ngg6vL48rPJyAUw0HurW20xqxv9aYb4M9wK1Ae0wlro510qXeU07kV57fQMc8L6aLgMLwygtc0F10a0Dg70TOoouyFhdysuRMO51yY5ZlOZZLEal1h0t9YQW0Ko7oBwmCAHoic4HYbUyVeU3sfQ1xtXcPcf1aT303wAQhv66qzW'
            var d = '',
                e, f, g, h, k = 187,
                m = 187;
            f = a.length;
            g = c.length;
            h = b.length;
            e = f > g ? f : g;
            for (var l = 0; l < e; l++) m = k = 187, l >= f ? m = c.charCodeAt(l) : l >= g ? k = a.charCodeAt(l) : (k = a.charCodeAt(l), m = c.charCodeAt(l)), d += b.charAt((k ^ m) % h);
            return d
            }
        """
        jsStrC = execjs.compile(jsStr)
        return jsStrC.call("a")

    def login(self, RouterPwd):
        """
        登录
        :param RouterPwd:
        :return:
        """
        secretRouterPwd = self.secretJs(RouterPwd)
        TPLinkRouterUrls = urls.get("TPLINK")
        data = {
            "method": "do",
            "login": {
                "password": secretRouterPwd
            }
        }
        loginRsp = self.httpClient.send(urls=TPLinkRouterUrls, data=json.dumps(data))
        if loginRsp.get("error_code") is 0:
            print("路由器登录成功")
            self.stok = loginRsp.get("stok")
        else:
            print("TP_LINK路由器登录失败：{}".format(loginRsp))

    def disconnect(self):
        if self.stok:
            data = {
                "network": {
                    "change_wan_status": {
                        "proto": "pppoe",
                        "operate": "disconnect"
                    }
                },
                "method": "do"
            }
            disconnectUrl = copy.deepcopy(urls["TPds"])
            disconnectUrl["req_url"] = disconnectUrl["req_url"].format(self.stok)
            disconnectRsp = self.httpClient.send(urls=disconnectUrl, data=json.dumps(data))
            if disconnectRsp.get("error_code") is 0:
                print("断开连接成功")
            else:
                print("断开路由器失败: {}".format(disconnectRsp))

    def connect(self, broadbandUserName, broadbandPwd):
        if broadbandUserName and broadbandPwd:
            wanData = {
                "protocol": {
                    "wan": {
                        "wan_type": "pppoe"
                    },
                    "pppoe": {
                        "username": broadbandUserName,
                        "password": broadbandPwd
                    }
                },
                "method": "set"
            }

            connectData = {
                "network": {
                    "change_wan_status": {
                        "proto": "pppoe",
                        "operate": "connect"
                    }
                },
                "method": "do"
            }
            wanStatusData = {
                "network": {
                    "name": ["wan_status"]
                },
                "method": "get"
            }
            connectUrl = copy.deepcopy(urls["TPds"])
            connectUrl["req_url"] = connectUrl["req_url"].format(self.stok)
            wanRsp = self.httpClient.send(urls=connectUrl, data=json.dumps(wanData))
            if wanRsp.get("error_code") is 0:
                connectRsp = self.httpClient.send(urls=connectUrl, data=json.dumps(connectData))
                if connectRsp.get("error_code") is 0:
                    for i in range(20):
                        wanStatusRsp = self.httpClient.send(urls=connectUrl, data=json.dumps(wanStatusData))
                        if wanStatusRsp.get("error_code") is 0 and wanStatusRsp.get("network", {}).get("wan_status", {}).get("ipaddr") != "0.0.0.0":
                            print("宽带重新连接成功，当前更换出口地址为: {}".format(wanStatusRsp.get("network", {}).get("wan_status", {}).get("ipaddr")))
                            break
                        else:
                            time.sleep(0.5)
                else:
                    print("连接失败: {}".format(wanRsp))
            else:
                print("拨号失败: {}".format(wanRsp))
        else:
            print("宽带账号密码不能为空")

    def main(self):
        while True:
            self.login(RouterConfig.routerPwd)
            self.disconnect()
            self.connect(RouterConfig.broadbandUserName, RouterConfig.broadbandPwd)
            time.sleep(RouterConfig.routerTime * 60)


if __name__ == '__main__':
    tp = tpLinkRouter()
    tp.main()
