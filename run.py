from TPLinkRouter import tpLinkRouter
from XiaomiRouter import xiaomiRouter
from config import RouterConfig

if __name__ == '__main__':
    if RouterConfig.routerType == "TPLINK":
        tp = tpLinkRouter()
        tp.main()
    elif RouterConfig.routerType == "小米":
        xiaomi = xiaomiRouter()
        xiaomi.main()