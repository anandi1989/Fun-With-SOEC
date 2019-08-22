'''
@uthor : Amit Nandi
Date : 05/10/2016

Classifier using - Ant-Colony Optimization 

'''

from sklearn import datasets
import numpy as n

nAnts = 100
minObjects = 2
q0 = 0.8
rho = 0.9
data = datasets.load_iris()
x = data.data
y = data.target
classes = n.unique(y)
bins = 3
maxItr = 10

def fitnessFun(x,y,rule):
	a=[]
	for i in range(x.shape[0]):
		if x[i,0]==rule[0] and x[i,1]==rule[1] and x[i,2]==rule[2] and x[i,3]==rule[3]:	
			a.append(i)
	from scipy import stats
	if len(a)!=0:
		tmp = stats.mode(a)
		return (float(len(n.where(y[a]==tmp[0])[0]))-float(len(n.where(y[a]!=tmp[0])[0]))) / float(len(y))
	else:
		return 0			

for i in range(x.shape[1]):
        for j in range(x.shape[0]):
                tmp = n.histogram(x[:,i],bins=bins)
                if x[j,0]>=tmp[1][0] and x[j,0]<=tmp[1][1]:
                        x[j,0] = 1
                elif x[j,0]>tmp[1][1] and x[j,0]<=tmp[1][2]:
                        x[j,0] = 2
                elif x[j,0]>tmp[1][2] and x[j,0]<=tmp[1][3]:
                        x[j,0] = 3
                if x[j,1]>=tmp[1][0] and x[j,1]<=tmp[1][1]:
                        x[j,1] = 4
                elif x[j,1]>tmp[1][1] and x[j,1]<=tmp[1][2]:
                        x[j,1] = 5
                elif x[j,1]>tmp[1][2] and x[j,1]<=tmp[1][3]:
                        x[j,1] = 6
                if x[j,2]>=tmp[1][0] and x[j,2]<=tmp[1][1]:
                        x[j,2] = 7
                elif x[j,2]>tmp[1][1] and x[j,2]<=tmp[1][2]:
                        x[j,2] = 8
                elif x[j,2]>tmp[1][2] and x[j,2]<=tmp[1][3]:
                        x[j,2] = 9
                if x[j,3]>=tmp[1][0] and x[j,3]<=tmp[1][1]:
                        x[j,3] = 10
                elif x[j,3]>tmp[1][1] and x[j,3]<=tmp[1][2]:
                        x[j,3] = 11
                elif x[j,3]>tmp[1][2] and x[j,3]<=tmp[1][3]:
                        x[j,3] = 12

bstRuleStack = n.empty((0,x.shape[1]))
itr=0
while itr<maxItr or x.shape[1]<bins:
	ruleMatrix = range(x.shape[1]*bins)
	ruleMatrix = n.add(ruleMatrix,1)
	ruleMatrix.resize((x.shape[1],bins))
	ruleMatrix = ruleMatrix.transpose()

	infoT = n.empty((bins,x.shape[1]))

	for i in range(bins):
		for j in range(x.shape[1]):
			tmp = 0
			for c in range(len(classes)):
				tmp1 = n.where(x[:,j]==ruleMatrix[i,j])
				tmp2 = n.where(y[tmp1[0]]==c)
				tmp = tmp + float(len(tmp2[0]))/float(len(y))*n.log2((float(len(tmp2[0]))/float(len(y)))+1)
			infoT[i,j] = -tmp
		
	heuristicInfo = infoT/sum(sum(infoT))

	pheromoneMatrix = n.empty((bins,x.shape[1]))
	pheromoneMatrix.fill(1)

	probFun = pheromoneMatrix*infoT
	probFun = probFun/sum(sum(probFun))
	fitnessValues = []
	ruleStack = n.empty((0,x.shape[1]))
	for ants in range(nAnts):
		counter = 0
		tprobFun = probFun
		truleMatrix = ruleMatrix
		rule = n.zeros(x.shape[1])
		arr = []
		tmp = n.random.random_integers(x.shape[1]-1)
		arr.append(tmp)
		tmp1 = n.random.random_integers(bins-1)
		a = ruleMatrix[tmp1,tmp]
		rule[n.where(ruleMatrix==a)[1]]=a
		while counter!=x.shape[1]-1:
			truleMatrix = n.delete(truleMatrix,arr[len(arr)-1],1)
			tprobFun = n.delete(tprobFun,arr[len(arr)-1],1)
			a = truleMatrix[n.where(tprobFun==tprobFun.max())][0]
			if len(n.where(a==x[:,i]))<minObjects:
				rule[n.where(ruleMatrix==a)[1]]=a
				arr.append(n.where(ruleMatrix==ruleMatrix[n.where(tprobFun==tprobFun.max())][0])[1][0])
				counter = counter+1
		ruleStack = n.vstack((ruleStack,rule))
		fitnessValues.append(fitnessFun(x,y,rule))	
	fitnessValues = n.asarray(fitnessValues)
	index = n.where(fitnessValues==fitnessValues.max())
	bstRuleStack = n.vstack((bstRuleStack,ruleStack[index[0][0]]))
	for i in range(bstRuleStack.shape[0]):
		for j in range(bstRuleStack.shape[1]):
			tmp = n.where(ruleMatrix==bstRuleStack[i,j])
			pheromoneMatrix[tmp] = (1-rho)*pheromoneMatrix[tmp] + rho*pheromoneMatrix[tmp]
	a=[]
	for i in range(x.shape[0]):
		for j in range(bstRuleStack.shape[0]):
			if x[i,0]==bstRuleStack[j,0] and x[i,1]==bstRuleStack[j,1] and x[i,2]==bstRuleStack[j,2] and x[i,3]==bstRuleStack[j,3]:
				a.append(i)
	x = n.delete(x,a,0)
	y = n.delete(y,a,0)
	print bstRuleStack
	print itr
	itr = itr+1
