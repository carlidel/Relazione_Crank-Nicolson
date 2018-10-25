import numpy as np
import matplotlib.pyplot as plt
import os, sys
import matplotlib

L = float(1)
M = 21
k = 5.e-6
D = 1.

t_target = 0.5

nsteps = int(round(t_target/k))

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
t = np.asarray([k * j for j in range(nsteps+1)])

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

# Analitic

analitic_solution = lambda x, t: np.sin(np.pi * x / L) * np.exp(- D * np.pi * np.pi * t / (L * L))

analitic = np.zeros((nsteps + 1, M))
for i in range(len(analitic)):
    analitic[i] = analitic_solution(x,t[i])
    print(i)

#%%
# Print_graphs

os.system("bash -c \"rm -f *fooB*.png\"")

nplot = 1000000
c = 0
error = (u-analitic)**2

for j in range(nsteps):
    if(j%nplot==0): # Stampa ogni nplot timesteps
        plt.subplot(1,2,1)
        plt.plot(x,u[j],linewidth=0, marker='o', label="Euler-Explicit")
        plt.plot(x,analitic[j], linewidth=2, label="Analytic")
        plt.legend()
        plt.ylim([0,1.2])
        filename = 'fooB' + str(c+1).zfill(6) + '.png';
        plt.xlabel("x")
        plt.ylabel("u")
        plt.title("t = %2.2f"%(k*(j+1)))
        plt.subplot(1,2,2)
        plt.plot(x,error[j], label="Error^2")
        plt.legend()
        plt.title("t = %2.2f"%(k*(j+1)))
        plt.xlabel("x")
        plt.ylabel("u")
        plt.ylim((0,np.amax(error[j:])))
        plt.tight_layout()
        plt.savefig(filename)
        plt.clf()
        c += 1
        print(j)

plt.clf()
error_sum = np.sqrt(np.asarray([np.sum(error[j]) for j in range(len(error))]))
plt.plot(t,error_sum, marker='o')
plt.xlabel("t")
plt.ylabel("Somma quadratica errore")
plt.title("Somma quadratica dell'errore rispetto al tempo")
plt.tight_layout()
plt.savefig("het_cn_M"+str(M)+"_N"+str(nsteps)+".jpg")

os.system("ffmpeg -y -i \"fooB%06d.png\" het_cn_M"+str(M)+"_N"+str(nsteps)+".m4v")