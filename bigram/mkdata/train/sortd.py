#encoding: utf-8

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

def sortf(fsrc,frsi,frst,freqf):
	l=[]
	storage={}
	with open(fsrc) as frd:
		for line in frd:
			tmp=line.strip()
			if tmp:
				tmp=tmp.decode("utf-8")
				lgth=len("".join(tmp.split("  ")))
				if lgth>1:
					if lgth in storage:
						storage[lgth].append(tmp)
					else:
						l.append(lgth)
						storage[lgth]=[tmp]
	l.sort(reverse=True)
	with open(frsi,"w") as fwrti:
		with open(frst,"w") as fwrtt:
			with open(freqf,"w") as fwrtf:
				for lu in l:
					cwrtl=storage[lu]
					for lind in cwrtl:
						tmp=lind.split("  ")
						cl="".join(tmp)
						tl=[]
						for tmpu in tmp:
							tl.extend(["N" for i in xrange(len(tmpu)-1)])
							tl.append("S")
						del tl[-1]
						tmp=cl+"\n"
						fwrti.write(tmp.encode("utf-8"))
						tmp=" ".join(tl)+"\n"
						fwrtt.write(tmp.encode("utf-8"))
					tmp=str(lu)+"	"+str(len(cwrtl))+"\n"
					fwrtf.write(tmp.encode("utf-8"))

def sortfl(srcfl,rsfli,rsflt,frqfl):
	for i in xrange(len(srcfl)):
		sortf(srcfl[i],rsfli[i],rsflt[i],frqfl[i])

if __name__=="__main__":
	#fd=["addtag"]
	sortf("pku_training.txt","addtagsi.txt","addtagst.txt","addtagf.txt")
