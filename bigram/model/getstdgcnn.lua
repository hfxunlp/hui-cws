function containergcnn(ncomb,vecsize,batchmode)
	local ldim=1
	local rdim=2
	if batchmode then
		ldim=2
		rdim=3
	end
	local rgate=nn.Sequential()
		:add(nn.Linear(ncomb*vecsize,ncomb*vecsize))
		:add(nn.Sigmoid())
	local argate=nn.ConcatTable()
		:add(nn.Identity())
		:add(rgate)
	local comm=nn.Sequential()
		:add(argate)
		:add(nn.CMulTable())
		:add(nn.Linear(ncomb*vecsize,vecsize))
		:add(nn.Tanh())
	local wholevec=nn.ConcatTable()
		:add(nn.Identity())
		:add(comm)
	local ugate=nn.Sequential()
		:add(nn.Linear((ncomb+1)*vecsize,(ncomb+1)*vecsize))
		:add(nn.Reshape(ncomb+1,vecsize,batchmode))
		:add(nn.Transpose({ldim,rdim}))
		:add(nn.SoftMax())
		:add(nn.Transpose({ldim,rdim}))
		:add(nn.Reshape((ncomb+1)*vecsize,batchmode))
	local augate=nn.ConcatTable()
		:add(ugate)
		:add(nn.Identity())
	local nnmodcore=nn.Sequential()
		:add(wholevec)
		:add(nn.JoinTable(2,2))
		:add(augate)
		:add(nn.CMulTable())
		:add(nn.Reshape(vecsize,(ncomb+1),true))
		:add(nn.SplitTable(3,3))
		:add(nn.CAddTable())
	return nnmodcore
end

function graphgcnn(ncomb,vecsize,batchmode)
	local ldim=1
	local rdim=2
	if batchmode then
		ldim=2
		rdim=3
	end
	local input=nn.Identity()():annotate{name="input",description="input"}
	local rgate=nn.Sigmoid()(nn.Linear(ncomb*vecsize,ncomb*vecsize)(input)):annotate{name="reset gate",description="Get reset gate"}
	local wcommonp=nn.CMulTable()({rgate,input}):annotate{name="reset char",description="use reset gate to get reset char"}
	local wcommon=nn.Tanh()(nn.Linear(ncomb*vecsize,vecsize)(wcommonp)):annotate{name="common vector",description="Common environment vector"}
	local wc=nn.JoinTable(2,2)({wcommon,input}):annotate{name="env&char vector",description="Common environment vector and char vector"}
	local ugate=nn.Reshape((ncomb+1)*vecsize,batchmode)(nn.Transpose({ldim,rdim})(nn.SoftMax()(nn.Transpose({ldim,rdim})(nn.Reshape(ncomb+1,vecsize,batchmode)(nn.Linear((ncomb+1)*vecsize,(ncomb+1)*vecsize)(wc)))))):annotate{name="update gate",description="update gates"}
	local www=nn.CMulTable()({ugate,wc}):annotate{name="www",description="apply update gates"}
	local wrs=nn.CAddTable()(nn.SplitTable(3,3)(nn.Reshape(vecsize,(ncomb+1),true)(www))):annotate{name="word vector",description="get word vector"}
	return nn.gModule({input},{wrs})
end

function getgcnn(ncomb,vecsize,inputdim,usegraph)
	local nnmod=nil
	local batchmod=nil
	if inputdim>=2 then
		batchmod=true
	end 
	if usegraph then
		nncoremod=graphgcnn(ncomb,vecsize,batchmod)
	else
		nncoremod=containergcnn(ncomb,vecsize,batchmod)
	end
	if inputdim>2 then
		return nn.Bottle(nncoremod)
	else
		return nncoremod
	end
end
