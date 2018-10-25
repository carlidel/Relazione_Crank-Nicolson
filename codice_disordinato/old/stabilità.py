import matplotlib.pyplot as plt
import numpy as np
import os

nsamples = 5

files = os.listdir("parameters")
n = range(0,len(files))

u_analitic = [np.load("graphics\\heat_analitic_" + str(i) +".npy") for i in n]
u_explicit = [np.load("graphics\\heat_explicit_" + str(i) +".npy") for i in n]
u_implicit = [np.load("graphics\\heat_implicit_" + str(i) +".npy") for i in n]

parameters = [open("parameters\\parameters_" + str(i) + ".txt") for i in n]

#%%

# explicit

for i in n:

	lines = [line for line in parameters[i]]

	L = float(lines[0].split()[1])
	M = int(lines[1].split()[1])
	k = float(lines[2].split()[1])
	D = float(lines[3].split()[1])
	nsteps = int(lines[4].split()[1])
	nplot = int(lines[5].split()[1])

	x = np.linspace(0, L, M)
	t = np.linspace(0, k * (nsteps), nsteps+1)

	h = L / (M-1)

	samples = np.linspace(0, len(u_explicit[i]), nsamples, dtype = int)

	for j in samples:
		plt.plot(x, u_analitic[i][j])
		plt.scatter(x, u_explicit[i][j])

	plt.show()
	plt.savefig(str(i) + "_" + str(j) + "_stability.jpg")
	plt.clf()

# implicit

for i in n:

	lines = [line for line in parameters[i]]

	L = float(lines[0].split()[1])
	M = int(lines[1].split()[1])
	k = float(lines[2].split()[1])
	D = float(lines[3].split()[1])
	nsteps = int(lines[4].split()[1])
	nplot = int(lines[5].split()[1])

	x = np.linspace(0, L, M)
	t = np.linspace(0, k * (nsteps), nsteps+1)

	h = L / (M-1)

	samples = np.linspace(0, len(u_implicit[i]), nsamples, dtype = int)

	for j in samples:

		plt.plot(x, u_analitic[i][j])
		plt.scatter(x, u_implicit[i][j])

	plt.savefig(str(i) + "_" + str(j) + "_stability.jpg")
	plt.clf()