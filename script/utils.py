import sys

def WriteOut(instring):
  #saveout = sys.stdout
  fileout = open('monoutput.log', 'a')
  #sys.stdout = fileout
  fileout.write(str(instring)+'\n')
  #sys.stdout = saveout
  fileout.close()
