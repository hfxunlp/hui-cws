#encoding: utf-8

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

def euni(fsrc,frs):
	with open(frs,"w") as fwrt:
		with open(fsrc) as frd:
			for line in frd:
				tmp=line.strip()
				if tmp:
					tmp=tmp.decode("utf-8")
					if len(tmp)==1:
						tmp+="\n"
						fwrt.write(tmp)

if __name__=="__main__":
	euni("pku_test.txt","uni.txt")