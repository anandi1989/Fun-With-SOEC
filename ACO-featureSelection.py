'''
@uthor : Amit Nandi
Date : 01/10/2016

Feature Selection using - Ant-Colony Optimization 
'''

#Fitness function
def fitnessFunc(data,subset,k=5):
        import numpy as n
        x = data.data[:,subset]
        y = data.target
        from sklearn import svm
        from sklearn.cross_validation import cross_val_score
        clf = svm.SVC(kernel='linear', C=1)
        acc = cross_val_score(clf, x, y, cv=k)
        return acc.mean()

#ACO feature selection function
def ACO_featureSelection(data,nSubset,nAnts=100,maxItr=1000,q0=0.8):
	nFeatures = len(data.feature_names)
	pheromoneMatrix = n.empty([len(data.feature_names), len(data.feature_names)])
	pheromoneMatrix.fill(1)
	minAcc = 0
	for ants in range(nAnts):
		features = range(nFeatures)
		subset = [n.random.random_integers(nFeatures)-1]
		features.remove(subset[len(subset)-1])
		for subsets in range(nSubset-1):
			if n.random.uniform(0,1,size=1) < q0:	
				tmp = n.where(pheromoneMatrix[subset[len(subset)-1]][features]==min(pheromoneMatrix[subset[len(subset)-1]][features]))
				subset.append(features[tmp[0][0]])
				features.remove(features[tmp[0][0]])
			else:
				prob = pheromoneMatrix[subset[len(subset)-1]][features]/sum(pheromoneMatrix[subset[len(subset)-1]][features])
				tmp = n.random.choice(features,p=prob)
				subset.append(tmp)
				features.remove(tmp)
		if fitnessFunc(data,subset) >= minAcc:
			optAcc = fitnessFunc(data,subset)
			optSubset = subset
	return list((optSubset,optAcc))

#Maain
import numpy as n
from sklearn import datasets as s
data = s.load_iris()
a = ACO_featureSelection(data,3,nAnts=100,maxItr=1000,q0=0.8)
print a
