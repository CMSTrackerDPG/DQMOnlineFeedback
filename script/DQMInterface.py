from dqmjson_online import *
import math

class DQMInterface():
    def __init__(self, serverurl, RunNumber = 0) :
        self.RunNumber = RunNumber
        self.serverurl = serverurl
        self.runinfo = {"run": 0, "lumi": 0, "beamMode": '', "run_type": ''}
        self.dead_value = 0
        self.isDataPresent = 0
        self.data_InfoLayouts = {}
        self.data_PixelPh1 = {}
        self.data_PixelPh1MV = {}
        self.data_EventInfo = {}
        self.data_LhcInfo = {}
        self.onlinePublishing = False
        self()

    def __call__(self):
        self.data_EventInfo = dqm_get_json(self.serverurl, self.RunNumber , "/Online/ALL", "/SiStrip/EventInfo", False)
        self.data_InfoLayouts = dqm_get_json(self.serverurl, self.RunNumber , "/Online/ALL", "/Info/Layouts", False)
        self.data_PixelPh1 = dqm_get_json(self.serverurl, self.RunNumber , "/Online/ALL", "/PixelPhase1", True)
        self.data_PixelPh1MV = dqm_get_json(self.serverurl, self.RunNumber , "/Online/ALL", "/PixelPhase1/Phase1_MechanicalView", True)
        self.data_LhcInfo = dqm_get_json(self.serverurl, self.RunNumber , "/Online/ALL", "/Info/LhcInfo", True)
        self.onlinePublishing = self.isOnlinePublishing()

    def refresh(self):
        self()

    def isOnlinePublishing(self):
        status = True
        if str(self.data_EventInfo) == "{}":
            status = False
        return status

    def getRunInfo(self):
        ##Monitor (lumi - 1) -- Ensures that the plots are filled
        try:
            lumi = float(self.data_EventInfo['iLumiSection']['value']) - 1
            run  = self.data_EventInfo['iRun']['value']
            value_at_lumi = self.data_LhcInfo['beamMode']['rootobj'].GetBinContent(self.data_LhcInfo['beamMode']['rootobj'].FindBin(float(lumi)))
            beamMode = self.data_LhcInfo['beamMode']['rootobj'].GetYaxis().GetBinLabel(int(value_at_lumi))
                    #data = dqm_get_json(self.serverurl, self.RunNumber , "/Online/ALL", "/Info/Layouts", True)
            run_type = self.data_InfoLayouts['Run Type']['value']
            self.runinfo = {"run": run, "lumi": lumi, "beamMode": beamMode, "run_type": run_type}
        except KeyError, e:
            print("getRunInfo KeyError "+str(e))

    def getdeadRocTrendLayer_1(self):
        #data = dqm_get_json(self.serverurl, self.RunNumber , "/Online/ALL", "/PixelPhase1", True)
        ##Round lumisection to the nearest ten due to binning of the deadROC histogram
        #print(self.runinfo['lumi'])
        try:
            lumi_round10 = int(math.floor(self.runinfo['lumi']/10.)*10)
            bin_at_lumi = self.data_PixelPh1['deadRocTrendLayer_1']['rootobj'].FindBin(float(lumi_round10)) - 1
            self.dead_value = self.data_PixelPh1['deadRocTrendLayer_1']['rootobj'].GetBinContent(bin_at_lumi)
        except KeyError, e:
            print ("getdeadRocTrendLayer_1 KeyError "+str(e))
            self.dead_value = 0

    def getIsDataPresent(self):
        try:
            #data = dqm_get_json(self.serverurl, self.RunNumber , "/Online/ALL", "/PixelPhase1/Phase1_MechanicalView", True)
            ndigis = self.data_PixelPh1MV['num_digis_per_Lumisection_PXBarrel']['rootobj'].GetBinContent(self.data_PixelPh1MV['num_digis_per_Lumisection_PXBarrel']['rootobj'].FindBin(float(self.runinfo['lumi'])))
            ndigism1 = 0
            ndigism2 = 0
            if(self.runinfo['lumi']>7):
                ndigism1 = self.data_PixelPh1MV['num_digis_per_Lumisection_PXBarrel']['rootobj'].GetBinContent(self.data_PixelPh1MV['num_digis_per_Lumisection_PXBarrel']['rootobj'].FindBin(float(self.runinfo['lumi'])-1))
                ndigism2 = self.data_PixelPh1MV['num_digis_per_Lumisection_PXBarrel']['rootobj'].GetBinContent(self.data_PixelPh1MV['num_digis_per_Lumisection_PXBarrel']['rootobj'].FindBin(float(self.runinfo['lumi'])-2))

            if(ndigis==0 and ndigism1==0 and ndigism2==0):
                self.isDataPresent = False
            else:
                self.isDataPresent = True
        except KeyError, e:
            print("getIsDataPresent KeyError "+str(e))
