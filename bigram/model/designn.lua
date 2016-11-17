require "rnn"
require "SeqBGRU"
require "SeqDropout"
--require "nngraph"
--require "getmaxout"
require "getgcnn"
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

	--local premod=nn.Sequential():add(nn.ConcatTable():add(nn.Narrow(1,1,-2)):add(nn.Narrow(1,2,-1))):add(nn.JoinTable(3,3)):add(nn.ConcatTable():add(getgcnn(2,sizvec,3)):add(nn.Bottle(nn.Linear(sizvec*2,sizvec)))):add(nn.CAddTable())
	--local premod=nn.Sequential():add(nn.ConcatTable():add(nn.Narrow(1,1,-2)):add(nn.Narrow(1,2,-1))):add(nn.JoinTable(3,3)):add(getgcnn(2,sizvec,3))

	local coremod=nn.SeqBGRU(sizvec,sizvec,nil,nn.JoinTable(2,2));
	coremod.maskzero=true
	--coremod.batchfirst=true	

	local npiece=8

	--local clsmod=nn.Sequencer(nn.MaskZero(nn.Sequential():add(nn.ConcatTable():add(nn.Sequential():add(nn.Linear(sizvec*2,sizvec)):add(nn.Tanh()):add(nn.Linear(sizvec,nclass))):add(nn.Linear(sizvec*2,nclass))):add(nn.CAddTable()),1));
	clsmod=nn.Sequencer(nn.MaskZero(nn.Sequential():add(nn.NormStabilizer()):add(nn.Linear(sizvec*2,nclass*npiece)):add(nn.Reshape(npiece,nclass,true)):add(nn.Max(2)),1));
	--clsmod=nn.Sequencer(nn.MaskZero(nn.Sequential():add(nn.NormStabilizer()):add(nn.Linear(sizvec*2,nclass)),1));

	local nnmod=nn.Sequential():add(id2vec):add(nn.ConcatTable():add(nn.Narrow(1,1,-2)):add(nn.Narrow(1,2,-1))):add(nn.JoinTable(3,3)):add(getgcnn(2,sizvec,3)):add(nn.SeqDropout(0.2)):add(coremod):add(clsmod):add(nn.SplitTable(1));

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