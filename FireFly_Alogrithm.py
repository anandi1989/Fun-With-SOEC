'''
@uthor : Amit Nandi
Date : 10/11/2016

Firefly Alogrithm 
'''

#Rosenbrock function
def f(x,a=1,b=100):
        return (a-x[0])**2+b*(x[1]-x[0]**2)**2

#Function to compute Intensity
def intensity(trialSolution,f):
	import numpy as n
	I = n.empty(trialSolution.shape[0])
	for i in range(trialSolution.shape[0]):
		I[i] = f(trialSolution[i])
	return I

#Function to compute Euclidean distance
def dist(x,y):
	import numpy as n
	tmp = 0
	for i in range(x.shape[0]):
		tmp = tmp + (x[i]-y[i])**2
	return n.sqrt(tmp)

#Firefly algorithm function
def FA(f,minRange,maxRange,maxItr=1000,nFireflies=25,gamma=1,beta0=2,alpha=0.2,delta=0.1,m=2):
	import numpy as n
	trialSolution = n.empty([nFireflies,len(minRange)])

	for i in range(nFireflies):
		for j in range(len(minRange)):
			trialSolution[i][j] = n.random.uniform(minRange[j],maxRange[j])

	itr = 0
	I = intensity(trialSolution,f)
	while itr!=maxItr:
		for i in range(nFireflies):
			for j in range(i+1):
				if I[j]<I[i]:
					r = dist(trialSolution[i],trialSolution[j])
					beta = beta0*n.exp(-gamma*r**m)
					e = delta*n.random.uniform(-1,1,size=len(minRange))
					tmp = beta*n.dot(n.random.uniform(-1,1,size=(len(minRange),len(minRange))),trialSolution[i]-trialSolution[j])

					trialSolution[i] = trialSolution[i] + alpha*e + tmp
					I = intensity(trialSolution,f)				
		itr = itr + 1

	bstValue = min(I)
	bstSol = trialSolution[n.where(I==min(I))]
	return list((bstValue,bstSol))

#Main
minRange = [0.5,0.5]
maxRange = [1.5,1.5]
a = FA(f,minRange,maxRange)
