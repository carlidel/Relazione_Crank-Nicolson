import numpy as np
import matplotlib.pyplot as plt
import os, sys
import matplotlib

L = float(1)
M = 101
h = L / (M-1)	# delta x
k = 5.e-6		# delta t

nsteps = 100000
nplot = 100

D = 1.
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
 
#%%

analitic_solution = lambda x, t: np.sin(np.pi * x / L) * np.exp(- D * np.pi * np.pi * t / (L * L))

analitic = np.zeros((nsteps + 1, M))
for i in range (0, nsteps + 1):
    analitic[i] = np.asarray([analitic_solution(j,t[i]) for j in x])
    print(i)
    
#%%
    
errors = np.absolute(analitic - u)

error = np.asarray([np.amax(errors[i]) for i in range(0,nsteps + 1)])
highest = np.asarray([np.amax(u[i]) for i in range(0,nsteps + 1)])

plt.plot(error)
plt.savefig("error_esplicito.jpg")

#%%

c = 0

for j in range(nsteps):
    if(j%nplot==0): # Stampa ogni nplot timesteps
        plt.plot(x,u[j],linewidth=2)
        filename = 'foo' + str(c+1).zfill(4) + '.jpg';
        plt.ylim([0,1])
        plt.xlabel("x")
        plt.ylabel("u")
        plt.title("t = %2.2f"%(k*(j+1)))
        plt.savefig(filename)
        plt.clf()
        c += 1
        print(j)

os.system("ffmpeg -y -i \"foo%04d.jpg\" calore_esplicito.m4v")
os.system("bash -c \"rm -f *.jpg\"")
