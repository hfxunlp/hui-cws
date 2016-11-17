#encoding: utf-8

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

def restore(tsi,tsd):
	rsl=[]
	stid=0
	cid=1
	for tsu in tsd:
		if tsu=="B":
			rsl.append(tsi[stid:cid])
			stid=cid
		cid+=1
	rsl.append(tsi[stid:])
	return "  ".join(rsl)

def backsrc(fsrc,frs):
	with open(frs,"w") as fwrt:
		with open(fsrc) as frd:
			for line in frd:
				tmp=line.strip()
				if tmp:
					tmp=tmp.decode("utf-8")
					tmp=tmp.split("  ")
					cl=[]
					tl=[]
					for tmpu in tmp:
						cid=tmpu.rfind("/")
						cl.append(tmpu[:cid])
						tl.append(tmpu[cid+1:])
					cl="".join(cl)
					tl="".join(tl)
					tl=tl[1:len(cl)]
					tmp=restore(cl,tl)+"\n"
					fwrt.write(tmp.encode("utf-8"))

if __name__=="__main__":
	backsrc("msr_tests.txt","msr_testsort.txt")