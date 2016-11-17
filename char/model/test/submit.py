#encoding: utf-8

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

def gsubmit(finput,ftar,frs):
	with open(frs,"w") as fwrt:
		with open(finput) as frdi:
			with open(ftar) as frdt:
				for line in frdi:
					tmp=line.strip()
					tsi=tmp.decode("utf-8")
					tsi=tsi.replace("  ","")
					tmp=frdt.readline()
					tmp=tmp.strip()
					tsd=tmp.decode("utf-8")
					tsd=tsd.split(" ")
					tsd="".join(tsd)
					tsd=tsd[1:len(tsi)]
					rsl=[]
					stid=0
					cid=1
					for tsu in tsd:
						if tsu=="B":
							rsl.append(tsi[stid:cid])
							stid=cid
						cid+=1
					rsl.append(tsi[stid:])
					tmp="  ".join(rsl)+"\n"
					fwrt.write(tmp.encode("utf-8"))

if __name__=="__main__":
	gsubmit("msr_testsort.txt","tpres.txt","msr_trs.txt")