#encoding: utf-8

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

def splitf(fsrci,fsrct,freq,rsp):
	cursave=1
	minib=16
	maxdl=16
	mab=1024#64:2G,128:4G,256:8G
	ib=mab/2
	with open(freq) as frd:
		with open(fsrci) as fsrdi:
			with open(fsrct) as fsrdt:
				cache=[]
				for line in frd:
					tmp=line.strip()
					if tmp:
						tmp=tmp.decode("utf-8")
						lgth,freq=tmp.split("	")
						lgth=int(lgth)
						freq=int(freq)
						if freq>minib:
							if cache:
								nstore=0
								for cu in cache:
									nstore+=cu[-1]
								with open(rsp+str(cursave)+"i.txt","w") as fwrt:
									for i in xrange(nstore):
										lind=fsrdi.readline()
										lind=lind.strip()
										lind=lind.decode("utf-8")
										lind+="\n"
										fwrt.write(lind.encode("utf-8"))
								with open(rsp+str(cursave)+"t.txt","w") as fwrt:
									for i in xrange(nstore):
										lind=fsrdt.readline()
										lind=lind.strip()
										lind=lind.decode("utf-8")
										lind+="\n"
										fwrt.write(lind.encode("utf-8"))
								cursave+=1
								cache=[]
							if freq>mab:
								while freq>mab:
									with open(rsp+str(cursave)+"i.txt","w") as fwrt:
										for i in xrange(ib):
											lind=fsrdi.readline()
											lind=lind.strip()
											lind=lind.decode("utf-8")
											lind+="\n"
											fwrt.write(lind.encode("utf-8"))
									with open(rsp+str(cursave)+"t.txt","w") as fwrt:
										for i in xrange(ib):
											lind=fsrdt.readline()
											lind=lind.strip()
											lind=lind.decode("utf-8")
											lind+="\n"
											fwrt.write(lind.encode("utf-8"))
									cursave+=1
									freq-=ib
							with open(rsp+str(cursave)+"i.txt","w") as fwrt:
								for i in xrange(freq):
									lind=fsrdi.readline()
									lind=lind.strip()
									lind=lind.decode("utf-8")
									lind+="\n"
									fwrt.write(lind.encode("utf-8"))
							with open(rsp+str(cursave)+"t.txt","w") as fwrt:
								for i in xrange(freq):
									lind=fsrdt.readline()
									lind=lind.strip()
									lind=lind.decode("utf-8")
									lind+="\n"
									fwrt.write(lind.encode("utf-8"))
							cursave+=1
						else:
							if cache:
								if cache[0][0]-lgth<maxdl:
									cache.append([lgth,freq])
									nstore=0
									for cu in cache:
										nstore+=cu[-1]
									if nstore>minib:
										with open(rsp+str(cursave)+"i.txt","w") as fwrt:
											for i in xrange(nstore):
												lind=fsrdi.readline()
												lind=lind.strip()
												lind=lind.decode("utf-8")
												lind+="\n"
												fwrt.write(lind.encode("utf-8"))
										with open(rsp+str(cursave)+"t.txt","w") as fwrt:
											for i in xrange(nstore):
												lind=fsrdt.readline()
												lind=lind.strip()
												lind=lind.decode("utf-8")
												lind+="\n"
												fwrt.write(lind.encode("utf-8"))
										cursave+=1
										cache=[]
								else:
									nstore=0
									for cu in cache:
										nstore+=cu[-1]
									with open(rsp+str(cursave)+"i.txt","w") as fwrt:
										for i in xrange(nstore):
											lind=fsrdi.readline()
											lind=lind.strip()
											lind=lind.decode("utf-8")
											lind+="\n"
											fwrt.write(lind.encode("utf-8"))
									with open(rsp+str(cursave)+"t.txt","w") as fwrt:
										for i in xrange(nstore):
											lind=fsrdt.readline()
											lind=lind.strip()
											lind=lind.decode("utf-8")
											lind+="\n"
											fwrt.write(lind.encode("utf-8"))
									cursave+=1
									cache=[[lgth,freq]]
							else:
								cache=[[lgth,freq]]
				if cache:
					nstore=0
					for cu in cache:
						nstore+=cu[-1]
					with open(rsp+str(cursave)+"i.txt","w") as fwrt:
						for i in xrange(nstore):
							lind=fsrdi.readline()
							lind=lind.strip()
							lind=lind.decode("utf-8")
							lind+="\n"
							fwrt.write(lind.encode("utf-8"))
					with open(rsp+str(cursave)+"t.txt","w") as fwrt:
						for i in xrange(nstore):
							lind=fsrdt.readline()
							lind=lind.strip()
							lind=lind.decode("utf-8")
							lind+="\n"
							fwrt.write(lind.encode("utf-8"))
					cache=[]
					cursave+=1
	print cursave-1

def splitfl(srcfli,srcflt,frqfl,rsflp):
	for i in xrange(len(srcfli)):
		splitf(srcfli[i],srcflt[i],frqfl[i],rsflp[i])

if __name__=="__main__":
	fd=["addtag"]
	splitfl([i+"si.txt" for i in fd],[i+"st.txt" for i in fd],[i+"f.txt" for i in fd],["rs\\"+i for i in fd])
