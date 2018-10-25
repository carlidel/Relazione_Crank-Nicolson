import numpy as np
import matplotlib.pyplot as plt
import os, sys
import matplotlib

L = float(1)
M = 101
h = L / (M-1)	# delta x
k = 5.e-5		# delta t

nsteps = 10000
nplot = 100

D = 1.
r = D * k / (h*h)

A = np.zeros((M-2,M-2))

b = np.zeros((M-2))

for i in range(M-2):
    if i==0:
        A[i,:] = [- 2  if j == 0 else 1 if j == 1 else 0 for j in range(M - 2)]
        b[i] = 0. # Condizione al contorno i=1
    elif i == M - 3:
        A[i,:] = [2 if j == M - 4 else - 2 if j == M - 3 else 0 for j in range(M - 2)]
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
    
#%%

c = 0

for j in range(nsteps):
    if(j%nplot==0): # Stampa ogni nplot timesteps
        plt.plot(x,u[j],linewidth=2)
        plt.ylim([0,1])
        filename = 'foo' + str(c+1).zfill(3) + '.jpg';
        plt.xlabel("x")
        plt.ylabel("u")
        plt.title("t = %2.2f"%(k*(j+1)))
        plt.savefig(filename)
        plt.clf()
        c += 1
        print(j)


os.system("ffmpeg -y -i \"foo%03d.jpg\" calore_implicito.m4v")
os.system("bash -c \"rm -f *.jpg\"")