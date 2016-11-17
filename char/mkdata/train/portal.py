#encoding: utf-8

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

def portal(fsrc,frs):
	with open(frs,"w") as fwrt:
		with open(fsrc) as frd:
			for line in frd:
				tmp=line.strip()
				if tmp:
					tmp=tmp.decode("utf-8")
					tmp=tmp.split("  ")
					cl=[tmpu for tmpu in "".join(tmp)]
					tl=[]
					for tmpu in tmp:
						tl.append("B")
						tl.extend(["M" for i in xrange(len(tmpu)-1)])
					tmp=zip(cl,tl)
					tmp=["/".join(tmpu) for tmpu in tmp]
					tmp="  ".join(tmp)+"\n"
					fwrt.write(tmp.encode("utf-8"))

if __name__=="__main__":
	portal("msr_training.txt","addtag.txt")