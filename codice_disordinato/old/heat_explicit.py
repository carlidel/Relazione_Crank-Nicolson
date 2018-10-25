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

    h = L / (M-1)   # delta x
    r = D * k / (h*h)

    A = np.zeros((M-2,M-2))
    b = np.zeros((M-2))

    for i in range(M-2):
        if i==0:
            A[i,:] = [1 - 2 * r if j == 0 else r if j == 1 else 0 for j in range(M - 2)]
            b[i] = 0. # Condizione al contorno i=1
        elif i == M - 3:
            A[i,:] = [r if j == M - 4 else 1 - 2 * r if j == M - 3 else 0 for j in range(M - 2)]
            b[i] = 0. # Condizione al contorno i=M
        else:
            A[i,:] = [r if j == i - 1 else 1 - 2 * r if j == i else r if j == i + 1 else 0 for j in range(M - 2)]

    # Inizializzare grid

    x = np.linspace(0, L, M)
    t = np.linspace(0, k * (nsteps), nsteps+1)

    # Condizioni iniziali

    u = np.zeros((nsteps + 1,M))
    u[0] = np.asarray([np.sin(np.pi * j) for j in x])

    for j in range(nsteps):
        print(j)
        u[j+1][1:-1] = A.dot(u[j][1:-1]) + b
    
    number = (file.replace(".","_")).split("_")[1]
    np.save("graphics\\heat_explicit" + "_" + number, u)