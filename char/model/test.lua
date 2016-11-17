torch.setdefaulttensortype('torch.FloatTensor')

function loadObject(fname)
	--[[local file=torch.DiskFile(fname)
	local objRd=file:readObject()
	file:close()
	return objRd]]
	return torch.load(fname)
end

function loadTest(iprefix,ifafix,nfile)
	local id={}
	for i=1,nfile do
		table.insert(id,loadObject(iprefix..i..ifafix):cuda())
	end
	return id
end

function runtest(modin,x)
	local rs={}
	for _,v in ipairs(x) do
		local seqrs=modin:forward(v)
		local seqt={}
		for __,vrs in ipairs(seqrs) do
			local ___,mind=torch.max(vrs,2)
			table.insert(seqt,mind:float():resize(mind:size(1)):totable())
		end
		seqt=torch.LongTensor(seqt):t():totable()
		table.insert(rs,seqt)
	end
	return rs
end

function savers(fname,tb)
	local file=io.open(fname,"w")
	for _,bd in ipairs(tb) do
		for __,sentrs in ipairs(bd) do
			for ___,vwrt in ipairs(sentrs) do
				file:write(vwrt.." ")
			end
			file:write("\n")
		end
	end
	file:close()
end

require "cunn"
require "rnn"
require "SeqBGRU"
require "SeqDropout"
require "vecLookup"
require "maskZerovecLookup"

require "modtest"

print("load module")
nnmod=torch.load(modtest).module
nnmod:evaluate()
nnmod:cuda()
print("load data")
testin=loadTest('datasrc/thd/test','i.asc',101)
print("test")
rs=runtest(nnmod,testin)
print("save result")
savers("test/trs.txt",rs)
