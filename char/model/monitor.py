import subprocess
import os

cfgf="aconf.lua"
logf="alog.txt"
bestmodelf="devnnmod.asc"

maincmd="th adatrain.lua | tee "
testcmd="./fulltest.sh"

detectwd="new minimal dev error found"
testwd="=== F MEASURE:	"

savedir=""
bestscore=0.0

def ldsavedir(fname):
	rs="modrs/"
	with open(fname) as frd:
		for line in frd:
			tmp=line.strip()
			if tmp:
				tmp=tmp.decode("utf-8")
				if tmp.startswith("runid"):
					tmp=tmp[len("runid=\""):len(tmp)-1]
					rs+=tmp+"/"
					break
	return rs

def tarf():
	global savedir,bestmodelf
	rs=""
	ntime=0
	fi=os.listdir(savedir)
	for fu in fi:
		if fu.startswith("devnnmod") and fu!=bestmodelf:
			ctime=os.path.getmtime(savedir+fu)
			if ctime>ntime:
				ntime=ctime
				rs=fu
	return rs

def writetmod(modf):
	twrt="modtest=\""+modf+"\"\n"
	with open("modtest.lua","w") as fwrt:
		fwrt.write(twrt.encode("utf-8"))

def calltest():
	global testwd,testcmd
	p=subprocess.Popen(testcmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	rs=""
	while True:
		line=p.stdout.readline()
		if line:
			tmp=line.strip()
			if tmp.startswith(testwd):
				rs=tmp[len(testwd)+1:]
				break
		else:
			break
	p.terminate()
	return float(rs)

def mvmodule(modm):
	global savedir,bestmodelf
	os.rename(savedir+modm,savedir+bestmodelf)

def runtest():
	global bestscore
	tmod=tarf()
	if tmod:
		writetmod(savedir+tmod)
		score=calltest()
		if score>bestscore:
			bestscore=score
			mvmodule(tmod)
			print("\nnew best score:"+str(score)+"\n")

def oneprocess(logf):
	global maincmd,detectwd
	p=subprocess.Popen(maincmd+logf,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	while True:
		line=p.stdout.readline()
		if line:
			tmp=line[:-1]
			print tmp
			if tmp.startswith(detectwd):
				runtest()
		else:
			break
	p.terminate()

if __name__=="__main__":
	savedir=ldsavedir(cfgf)
	oneprocess(logf)

