# -*- coding: utf-8 -*-
import thostmduserapi as mdapi  

class CFtdcMdSpi(mdapi.CThostFtdcMdSpi):
    tapi=''

    def __init__(self,tapi):
        mdapi.CThostFtdcMdSpi.__init__(self)
        self.tapi=tapi

    def OnFrontConnected(self):
        print ("OnFrontConnected")
        loginfield = mdapi.CThostFtdcReqUserLoginField()
        loginfield.BrokerID="4900"
        loginfield.UserID="000005"
        loginfield.Password="123456"
        loginfield.UserProductInfo="python dll"
        self.tapi.ReqUserLogin(loginfield,0)

    def OnRspUserLogin(self, *args):
        print ("OnRspUserLogin")
        rsploginfield=args[0]
        rspinfofield=args[1]
        print ("SessionID=",rsploginfield.SessionID)
        errorCode= rspinfofield.ErrorID;
        if 0 != errorCode :
            print ("ErrorID=",errorCode)
            print ("ErrorMsg=",rspinfofield.ErrorMsg)
        else:
            print("建立连接成功")
        #ret=self.tapi.SubscribeMarketData([b"ru1909",b"rb1909"],2)
        ret = self.tapi.SubscribeMarketData([ b"rb1909"],1)
    def OnRtnDepthMarketData(self, *args):
        print ("OnRtnDepthMarketData")
        field=args[0]
        print ("合约 InstrumentID=",field.InstrumentID," : LastPrice=",field.LastPrice )


    def OnRspSubMarketData(self, *args):
        print ("OnRspSubMarketData")
        field=args[0]
        print ("InstrumentID=",field.InstrumentID)
        rspinfofield=args[1]
        print ("ErrorID=",rspinfofield.ErrorID)
        print ("ErrorMsg=",rspinfofield.ErrorMsg)

def main():
    mduserapi=mdapi.CThostFtdcMdApi_CreateFtdcMdApi()
    mduserspi=CFtdcMdSpi(mduserapi)

    ## 测试地址
    ##mduserapi.RegisterFront("tcp://180.168.146.187:10010")
    """mduserapi.RegisterFront("tcp://180.168.146.187:10031")"""

    ##东吴期货生产地址前置
    mduserapi.RegisterFront("tcp://180.169.116.99:41213")


    mduserapi.RegisterSpi(mduserspi)
    mduserapi.Init()    
    mduserapi.Join()

if __name__ == '__main__':
    main()