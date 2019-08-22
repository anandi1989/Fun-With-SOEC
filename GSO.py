'''
@uthor : Amit Nandi
Date : 20/11/2016

Glowworm swarm optimization Algorithm
'''

#Rosenbrock function
def f(x,a=1,b=100):
        return (a-x[0])**2+b*(x[1]-x[0]**2)**2

#Distance function
def dist(x,y):
	import numpy as n
	d = 0
	for i in range(x.shape[0]):
		d = d + (x[i]-y[i])**2
	return n.sqrt(d)

#GSO function
def GSO(f,minRange,maxRange,nGlowWorms=1000,maxItr=100,s=0.03,rho=0.4,gamma=0.6,beta=0.08,l0=5,n1=5,r0=3):
	import numpy as n
	trialSolution = n.empty([nGlowWorms,len(minRange)])
	for i in range(nGlowWorms):
		for j in range(len(minRange)):
			trialSolution[i,j] = n.random.uniform(minRange[j],maxRange[j])

	l = n.empty(nGlowWorms)
	l.fill(l0)

	r = n.empty(nGlowWorms)
	r.fill(r0)

	itr = 0
	while itr!=maxItr:
		for i in range(nGlowWorms):
			l[i] = (1-rho)*l[i] + gamma*f(trialSolution[i])

		for i in range(nGlowWorms):
			neighbours = []
			p = []
			for j in range(nGlowWorms):
				if i!=j:
					d = dist(trialSolution[i],trialSolution[j])	
					if d < r[i] and l[i] < l[j]:
						neighbours.append(j)		
			tmp = 0
			if len(neighbours) != 0:
				for k in range(len(neighbours)):
					tmp = tmp + (l[neighbours[k]] - l[i])
					p.append((l[neighbours[k]]-l[i])/tmp)
				j = neighbours[n.where(p==max(p))[0][0]]
				tmp = dist(trialSolution[i],trialSolution[j])
				tmp1 = (s/tmp)*n.subtract(trialSolution[j],trialSolution[i])
				trialSolution[i] = n.add(trialSolution[i],tmp1)
				r[i] = 	min(r0,max(0,r[i]+beta*(n1-len(neighbours))))
		itr = itr+1
	funValues = n.empty(nGlowWorms)
	for i in range(nGlowWorms):
		funValues[i] = f(trialSolution[i])
	bstValue = min(funValues)
	bstSolution = trialSolution[n.where(funValues==min(funValues))[0][0]]

	return list((bstValue,bstSolution))

#Main
minRange = [0.5,0.5]
maxRange = [1.5,1.5]
a = GSO(f,minRange,maxRange,nGlowWorms=1000,maxItr=100,s=0.03,rho=0.4,gamma=0.6,beta=0.08,l0=5,n1=5,r0=3) 
