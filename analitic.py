import numpy as np
import matplotlib.pyplot as plt
import os, sys
import matplotlib

L = float(1)
M = 101
h = L / (M-1)	# delta x
k = 5.e-6		# delta t

nsteps = 10000
nplot = 100

D = 1.

x = np.linspace(0, L, M)
t = np.linspace(0, k * (nsteps), nsteps+1)

analitic_solution = lambda x, t: np.sin(np.pi * x / L) * np.exp(- D * np.pi * np.pi * t / (L * L))

u = np.zeros((nsteps + 1, M))
for i in range (0, nsteps + 1):
    u[i] = np.asarray([analitic_solution(j,t[i]) for j in x])
    print(i)
    
# %%

c = 0

for j in range(nsteps):
    if(j%nplot==0): # Stampa ogni nplot timesteps
        plt.plot(x,u[j],linewidth=2)
        filename = 'foo' + str(c+1).zfill(3) + '.jpg';
        plt.ylim([0,1])
        plt.xlabel("x")
        plt.ylabel("u")
        plt.title("t = %2.2f"%(k*(j+1)))
        plt.savefig(filename)
        plt.clf()
        c += 1
        print(j)

os.system("ffmpeg -y -i \"foo%03d.jpg\" calore_analitico.m4v")
os.system("bash -c \"rm -f *.jpg\"")

