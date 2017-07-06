from x509auth import *
from ROOT import TBufferFile, TH1F, TProfile, TH2F, TCanvas, TProfile2D
import re
import pickle

X509CertAuth.ssl_key_file, X509CertAuth.ssl_cert_file = x509_params()

def dqm_get_json(server, run, dataset, folder, rootContent=False):
#    postfix = "?rootcontent=1" if rootContent else ""
#    datareq = urllib2.Request(('%s/data/json/archive/%s/Global/%s%s') % (server, run, dataset, folder, postfix))
#    datareq = urllib2.Request(('%s/data/json/archive/%s/%s/%s?rootcontent=1') % (server, run, dataset, folder)) #- offline?
#    datareq = urllib2.Request(('%s/data/json/live/%s/Global/%s/%s?rootcontent=1') % (server, run, dataset, folder))
    datareq = urllib2.Request(('%s/data/json/archive/%s/Global/%s/%s?rootcontent=1') % (server, run, dataset, folder))
#    print '%s/data/json/archive/%s/%s/%s%s' % (server, run, dataset, folder, postfix)
    datareq.add_header('User-agent', ident)
    # Get data
    data = eval(re.sub(r"\bnan\b", "0", urllib2.build_opener(X509CertOpen()).open(datareq).read()),
              { "__builtins__": None }, {})
    #dump/read data in pickle for tests
    #pickle.dump(data, open('data.json', 'wb'))
    #data = pickle.load(open('data.json', 'rb'))
    if rootContent:
        # Now convert into real ROOT histograms
        for idx,item in enumerate(data['contents']):
            if 'obj' in item.keys():
                if 'rootobj' in item.keys():
                    a = array('B')
                    a.fromstring(item['rootobj'].decode('hex'))
                    t = TBufferFile(TBufferFile.kRead, len(a), a, False)
                    rootType = item['properties']['type']
                    if rootType == 'TPROF': rootType = 'TProfile'
                    if rootType == 'TPROF2D': rootType = 'TProfile2D'
                    data['contents'][idx]['rootobj'] = t.ReadObject(eval(rootType+'.Class()'))
    return dict( [ (x['obj'], x) for x in data['contents'][1:] if 'obj' in x] )

def dqm_get_samples(server, match, type="offline_data"):
    datareq = urllib2.Request(('%s/data/json/samples?match=%s') % (server, match))
    datareq.add_header('User-agent', ident)
    # Get data
    data = eval(re.sub(r"\bnan\b", "0", urllib2.build_opener(X509CertOpen()).open(datareq).read()),
               { "__builtins__": None }, {})
    ret = []
    for l in data['samples']:
        if l['type'] == type:
            ret += [ (int(x['run']), x['dataset']) for x in l['items'] ]
    return ret


###Examples
# Values
# data = dqm_get_json('https://cmsweb.cern.ch/dqm/online', 297726 , "/Online/ALL", "/SiStrip/EventInfo", True)
# print(data['iRun']['value'])
# print(data['iLumiSection']['value'])
# ROOT object
# data = dqm_get_json('https://cmsweb.cern.ch/dqm/online', 297726 , "/Online/ALL", "/PixelPhase1", True)
# c1 = TCanvas("c1", "C1", 800, 600)
# c1.cd()
# data['deadRocTrendLayer_1']['rootobj'].Draw()
# c1.SaveAs("dead.png")
