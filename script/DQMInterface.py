from dqmjson_online import *
import math
from utils import WriteOut


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
        try:
            ##Monitor (lumi - 1) -- Ensures that the plots are filled
            lumi = float(self.data_EventInfo['iLumiSection']['value']) - 1
            run  = self.data_EventInfo['iRun']['value']
            value_at_lumi = self.data_LhcInfo['beamMode']['rootobj'].GetBinContent(self.data_LhcInfo['beamMode']['rootobj'].FindBin(float(lumi)))
            beamMode = self.data_LhcInfo['beamMode']['rootobj'].GetYaxis().GetBinLabel(int(value_at_lumi))
            run_type = self.data_InfoLayouts['Run Type']['value']
            self.runinfo = {"run": run, "lumi": lumi, "beamMode": beamMode, "run_type": run_type}
        except KeyError, e:
            WriteOut("getRunInfo KeyError "+str(e))

    def getdeadRocTrendLayer_1(self):
        try:
            if(self.runinfo['lumi']>40):
                bin_at_lumi = self.data_PixelPh1['deadRocTrendLayer_1']['rootobj'].FindBin(float(self.runinfo['lumi'])) - 1
                self.dead_value = self.data_PixelPh1['deadRocTrendLayer_1']['rootobj'].GetBinContent(bin_at_lumi)
            else:
                self.dead_value = 0
        except KeyError, e:
            WriteOut ("getdeadRocTrendLayer_1 KeyError "+str(e))
            self.dead_value = 0

    def getIsDataPresent(self):
        try:
            ndigis = self.data_PixelPh1MV['num_digis_per_Lumisection_PXBarrel']['rootobj'].GetBinContent(self.data_PixelPh1MV['num_digis_per_Lumisection_PXBarrel']['rootobj'].FindBin(float(self.runinfo['lumi'])))
            ndigism1 = 0
            ndigism2 = 0
            ndigism3 = 0
            ndigism4 = 0

            ##Tools start monitoring at LS=4, + 2 LS for digimon
            ##Check if 3 consecutive LS are empty. Avoid false alarms.
            if(self.runinfo['lumi']>=10):
                ndigism1 = self.data_PixelPh1MV['num_digis_per_Lumisection_PXBarrel']['rootobj'].GetBinContent(self.data_PixelPh1MV['num_digis_per_Lumisection_PXBarrel']['rootobj'].FindBin(float(self.runinfo['lumi'])-1))
                ndigism2 = self.data_PixelPh1MV['num_digis_per_Lumisection_PXBarrel']['rootobj'].GetBinContent(self.data_PixelPh1MV['num_digis_per_Lumisection_PXBarrel']['rootobj'].FindBin(float(self.runinfo['lumi'])-2))
                ndigism3 = self.data_PixelPh1MV['num_digis_per_Lumisection_PXBarrel']['rootobj'].GetBinContent(self.data_PixelPh1MV['num_digis_per_Lumisection_PXBarrel']['rootobj'].FindBin(float(self.runinfo['lumi'])-3))
                ndigism4 = self.data_PixelPh1MV['num_digis_per_Lumisection_PXBarrel']['rootobj'].GetBinContent(self.data_PixelPh1MV['num_digis_per_Lumisection_PXBarrel']['rootobj'].FindBin(float(self.runinfo['lumi'])-4))

            if(ndigis==0 and ndigism1==0 and ndigism2==0 and ndigism3==0 and ndigism4==0):
                self.isDataPresent = False
            else:
                self.isDataPresent = True
        except KeyError, e:
            WriteOut("getIsDataPresent KeyError "+str(e))
