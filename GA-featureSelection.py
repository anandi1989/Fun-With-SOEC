'''
@uthor : Amit Nandi
Date : 10/11/2016

Feature Selection using - Genetic Algorithm 
'''

def fitnessValues(data,trialSolution,k=5,c=1):
	import numpy as n
	scoreValues = n.empty(trialSolution.shape[0])
	for i in range(trialSolution.shape[0]):
		tmp = n.where(trialSolution[i]==1)
		x = data.data[:,tmp[0]]
		y = data.target
		from sklearn import svm
		from sklearn.cross_validation import cross_val_score
		clf = svm.SVC(kernel='linear', C=1)
		scores = cross_val_score(clf, x, y, cv=k)
		scoreValues[i] = scores.mean()*c*sum(trialSolution[i])/len(trialSolution[i])
	return scoreValues

def GAFeatureSelection(data,fitnessValues,population=50,generation=100,crossoverProb=0.8,mutationProb=0.03,c=1):

	import numpy as n
	byte = len(data.feature_names)
	trialSolution = n.empty([population,byte])
	for i in range(population):
		trialSolution[i] = n.random.choice([0,1],size=byte)

	for generations in range(generation):

		#Natural Selection using tournament selection
		naturalSelection = []
		funValues = fitnessValues(data,trialSolution)
		while len(naturalSelection)!=population:
			tmp = n.random.random_integers(population,size=2)-1
			if funValues[tmp[0]] > funValues[tmp[1]]:
				naturalSelection.append(tmp[0])
			else:
				naturalSelection.append(tmp[1])
		trialSolution = trialSolution[naturalSelection]

		#Crossover using one point
		tmp = n.random.random_integers(population,size=2)-1
		tmp1 = n.random.random_integers(byte)-1
		if n.random.uniform(0,1) < crossoverProb:
			a = trialSolution[tmp[0]][range(tmp1)]
			b = trialSolution[tmp[1]][range(tmp1,byte,1)]
			c = trialSolution[tmp[1]][range(tmp1)]
			d = trialSolution[tmp[0]][range(tmp1,byte,1)]
			trialSolution[tmp[0]] = n.append(a,b)
			trialSolution[tmp[1]] = n.append(c,d)

		#Mutation using bit-flip
		tmp = n.random.random_integers(population)-1
		tmp1 = n.random.random_integers(byte)-1
		if n.random.uniform(0,1) < mutationProb:
			if trialSolution[tmp][tmp1] == 0:
				trialSolution[tmp][tmp1] = 1
			else:
				trialSolution[tmp][tmp1] = 0

	funValues = fitnessValues(data,trialSolution)
	bstValue = funValues.max()
	bstIndex = n.where(funValues==funValues.max())	
	bstSolution = trialSolution[bstIndex[0][0]]
	return list((bstSolution,bstValue))

from sklearn import datasets as d
data = d.load_iris()
a = GAFeatureSelection(data,fitnessValues)

