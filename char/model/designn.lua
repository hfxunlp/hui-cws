require "rnn"
require "SeqBGRU"
require "SeqDropout"
--require "nngraph"
--require "getmaxout"
--require "getgcnn"
require "dpnn"
require "vecLookup"
require "maskZerovecLookup"
require "ASequencerCriterion"

function getnn()
	--return getonn()
	return getnnn()
end

function getonn()
	wvec = nil
	--local lmod = loadObject("modrs/nnmod.asc").module
	local lmod = torch.load("modrs/nnmod.asc").module
	return lmod
end

function getnnn()
	local id2vec=nn.maskZerovecLookup(wvec);
	wvec=nil

	local coremod=nn.SeqBGRU(sizvec,sizvec,nil,nn.JoinTable(2,2));
	coremod.maskzero=true
	--coremod.batchfirst=true	

	local clsmod=nn.Bottle(nn.MaskZero(nn.Linear(sizvec*2,nclass),1));

	--local nnmod=nn.Sequential():add(id2vec):add(nn.SeqDropout(0.2)):add(coremod):add(clsmod):add(nn.SplitTable(1));

	--local nnmod=nn.Sequential():add(id2vec):add(coremod):add(clsmod):add(nn.SplitTable(1));

	local nnmod=nn.Sequential():add(id2vec):add(nn.SeqDropout(0.2)):add(coremod):add(nn.Sequencer(nn.NormStabilizer())):add(clsmod):add(nn.SplitTable(1));

	return nnmod
end

function getcrit()
	return nn.ASequencerCriterion(nn.MaskZeroCriterion(nn.MultiMarginCriterion(),1));
end

function setupvec(modin,value)
	modin:get(1).updatevec = value
end

function dupvec(modin)
	setupvec(modin,false)
end

function upvec(modin)
	setupvec(modin,true)
end

function setnormvec(modin,value)
	modin:get(1).usenorm = value
end

function dnormvec(modin)
	setnormvec(modin,false)
end

function normvec(modin)
	setnormvec(modin,true)
end