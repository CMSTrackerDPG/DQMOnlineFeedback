from dqmjson_online import *


class DQMInterface():
    def __init__(self, serverurl, RunNumber = 0) :
        self.RunNumber = RunNumber
        self.serverurl = serverurl
        self.runinfo = {"run": 0, "lumi": 0, "beamMode": '', "run_type": ''}
        self.dead_value = 0
        self.data_EventInfo = {}
        self.data_LhcInfo = {}
        self.onlinePublishing = False
        self()

    def __call__(self):
        self.data_EventInfo = dqm_get_json(self.serverurl, self.RunNumber , "/Online/ALL", "/SiStrip/EventInfo", True)
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
        lumi = self.data_EventInfo['iLumiSection']['value']
        run  = self.data_EventInfo['iRun']['value']

        value_at_lumi = self.data_LhcInfo['beamMode']['rootobj'].GetBinContent(self.data_LhcInfo['beamMode']['rootobj'].FindBin(float(lumi)))
        beamMode = self.data_LhcInfo['beamMode']['rootobj'].GetYaxis().GetBinLabel(int(value_at_lumi+1))
        data = dqm_get_json(self.serverurl, self.RunNumber , "/Online/ALL", "/Info/Layouts", True)
        run_type = data['Run Type']['value']
        self.runinfo = {"run": run, "lumi": lumi, "beamMode": beamMode, "run_type": run_type}


    def getdeadRocTrendLayer_1(self):
        data = dqm_get_json(self.serverurl, self.RunNumber , "/Online/ALL", "/PixelPhase1", True)
        self.dead_value = data['deadRocTrendLayer_1']['rootobj'].GetBinContent(data['deadRocTrendLayer_1']['rootobj'].FindBin(float(self.runinfo['lumi'])))
