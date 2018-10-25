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

    r = D * k / (h*h)

    A = np.zeros((M-2,M-2))
    b = np.zeros((M-2))

    for i in range(M-2):
        if i==0:
            A[i,:] = [- 2  if j == 0 else 1 if j == 1 else 0 for j in range(M - 2)]
            b[i] = 0. # Condizione al contorno i=1
        elif i == M - 3:
            A[i,:] = [1 if j == M - 4 else - 2 if j == M - 3 else 0 for j in range(M - 2)]
            b[i] = 0. # Condizione al contorno i=M
        else:
            A[i,:] = [1 if j == i - 1 else - 2 if j == i else 1 if j == i + 1 else 0 for j in range(M - 2)]

    # Inizializzare grid

    x = np.linspace(0,L,M)

    LHS = (np.identity(M-2) - (r * 0.5) * A)
    RHS = (np.identity(M-2) + (r * 0.5) * A)

    # Condizioni iniziali

    u = np.zeros((nsteps + 1,M))
    u[0] = np.asarray([np.sin(np.pi * j) for j in x])

    # Calcolo rhs in t=0

    bb = RHS.dot(u[0][1:-1]) + b

    for j in range(nsteps):
        print(j)
        # Trova soluzione dentro il dominio
        u[j+1][1:-1] = np.linalg.solve(LHS,bb)
        # Aggiorna rhs
        bb = RHS.dot(u[j+1][1:-1]) + b
        
    number = (file.replace(".","_")).split("_")[1]
    np.save("graphics\\heat_implicit" + "_" + number, u)