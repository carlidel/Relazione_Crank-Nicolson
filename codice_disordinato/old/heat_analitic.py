import numpy as np
import matplotlib.pyplot as plt
import os, sys
import matplotlib
conditions = os.listdir("parameters")

for file in conditions:
    parameters = open("parameters\\" + file)
    lines = [line for line in parameters]

    L = float(lines[0].split()[1])
    M = int(lines[1].split()[1])
    k = float(lines[2].split()[1])
    D = float(lines[3].split()[1])
    nsteps = int(lines[4].split()[1])
    nplot = int(lines[5].split()[1])

    h = L / (M-1)	# delta x

    x = np.linspace(0, L, M)
    t = np.linspace(0, k * (nsteps), nsteps+1)

    analitic_solution = lambda x, t: np.sin(np.pi * x / L) * np.exp(- D * np.pi * np.pi * t / (L * L))

    u = np.zeros((nsteps + 1, M))
    for i in range (0, nsteps + 1):
        u[i] = np.asarray([analitic_solution(j,t[i]) for j in x])
        print(i)

    number = (file.replace(".","_")).split("_")[1]
    np.save("graphics\\heat_analitic" + "_" + number, u)