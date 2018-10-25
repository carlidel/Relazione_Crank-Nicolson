import matplotlib.pyplot as plt
import numpy as np
import os

files = os.listdir("parameters")
n = range(0,len(files))

u_analitic = [np.load("graphics\\heat_analitic_" + str(i) +".npy") for i in n]
u_explicit = [np.load("graphics\\heat_explicit_" + str(i) +".npy") for i in n]
u_implicit = [np.load("graphics\\heat_implicit_" + str(i) +".npy") for i in n]

parameters = [open("parameters\\parameters_" + str(i) + ".txt") for i in n]

# Analisi Errori Tempo (7 casi)

err_explicit_t = []
err_implicit_t = []
err_info_t = []

for i in range(0,7):

	lines = [line for line in parameters[i]]
	L = float(lines[0].split()[1])
	M = int(lines[1].split()[1])
	k = float(lines[2].split()[1])
	D = float(lines[3].split()[1])
	nsteps = int(lines[4].split()[1])
	nplot = int(lines[5].split()[1])

	h = L / (M-1)

	err_explicit_t.append(np.linalg.norm(np.absolute(u_analitic[i][-1] - u_explicit[i][-1])))
	err_implicit_t.append(np.linalg.norm(np.absolute(u_analitic[i][-1] - u_implicit[i][-1])))
	err_info_t.append(k)
	print(u_analitic[i][-1] - u_explicit[i][-1])

plt.figure(1)
plt.scatter(err_info_t, err_explicit_t)
plt.scatter(err_info_t, err_implicit_t)
plt.show()
plt.savefig("troncamento_t.jpg")

# Analisi Errori Spazio (7 casi)

err_explicit_x = []
err_implicit_x = []
err_info_x = []

for i in range(7,14):

	lines = [line for line in parameters[i]]

	L = float(lines[0].split()[1])
	M = int(lines[1].split()[1])
	k = float(lines[2].split()[1])
	D = float(lines[3].split()[1])
	nsteps = int(lines[4].split()[1])
	nplot = int(lines[5].split()[1])

	h = L / (M-1)

	err_explicit_x.append(np.linalg.norm(np.absolute(u_analitic[i][-1] - u_explicit[i][-1])))
	err_implicit_x.append(np.linalg.norm(np.absolute(u_analitic[i][-1] - u_implicit[i][-1])))
	err_info_x.append(h)

plt.figure(2)
plt.scatter(err_info_x, err_explicit_x)
plt.scatter(err_info_x, err_implicit_x)
plt.savefig("troncamento_x.jpg")
