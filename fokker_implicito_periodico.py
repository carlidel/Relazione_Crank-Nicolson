from scipy.linalg import solve_banded
import numpy as np
import matplotlib.pyplot as plt
import os, sys
import matplotlib

L = float(1)
M = 101
h = L / (M-1)   # delta x
k = 5.e-6       # delta t


nsteps = 100000

A_coefficent = 10.
B_coefficent = 0.5
t0 = 0.001

alpha = A_coefficent * k / (4 * h)
beta = B_coefficent * k / (2 * h * h)

A = np.zeros((M-2,M-2))
b = np.zeros((M-2))

for i in range(M-2):
    if i==0:
        A[i,:] = [- 2 * beta  if j == 0 else - alpha + beta if j == 1 else alpha + beta if j == (M - 3) else 0 for j in range(M - 2)]
        b[i] = 0. # Condizione al contorno i=1
    elif i == M - 3:
        A[i,:] = [- alpha + beta if j == 0 else alpha + beta if j == M - 4 else - 2 * beta if j == M - 3 else 0 for j in range(M - 2)]
        b[i] = 0. # Condizione al contorno i=M
    else:
        A[i,:] = [alpha + beta if j == i - 1 else - 2 * beta if j == i else - alpha + beta if j == i + 1 else 0 for j in range(M - 2)]

# Inizializzare grid

x = np.linspace(0,L,M)

LHS = (np.identity(M-2) - A)
RHS = (np.identity(M-2) + A)

# Condizioni iniziali

u = np.zeros((nsteps + 1,M))
u[0] = np.asarray([1/(2*np.sqrt(np.pi*B_coefficent*t0)) * np.exp(-((j-0.5) + A_coefficent * t0)**2 / (4*B_coefficent*t0)) for j in x])

# Calcolo rhs in t=0

bb = RHS.dot(u[0][1:-1])

for j in range(nsteps):
    print(j)
    # Trova soluzione dentro il dominio
    u[j+1][1:-1] = np.linalg.solve(LHS,bb)
    # Aggiorna rhs
    bb = RHS.dot(u[j+1][1:-1])
    
#%%

nplot = 100
c = 0

for j in range(nsteps):
    if(j%nplot==0): # Stampa ogni nplot timesteps
        plt.plot(x[1:-1],u[j][1:-1],linewidth=2)
        plt.ylim([0,2])
        filename = 'foo' + str(c+1).zfill(6) + '.jpg';
        plt.xlabel("x")
        plt.ylabel("u")
        plt.title("DE-SPA-CITO! t = %2.2f"%(k*(j+1)))
        plt.savefig(filename)
        plt.clf()
        c += 1
        print(j)


os.system("ffmpeg -y -i \"foo%06d.jpg\" fokker_implicito_periodico.m4v")
os.system("bash -c \"rm -f *.jpg\"")