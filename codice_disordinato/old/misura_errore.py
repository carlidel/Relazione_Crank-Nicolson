import matplotlib.pyplot as plt
import numpy as np
import os

files = os.listdir("parameters")
n = range(0,len(files))

u_analitic = [np.load("graphics\\heat_analitic_" + str(i) +".npy") for i in n]
u_explicit = [np.load("graphics\\heat_explicit_" + str(i) +".npy") for i in n]
u_implicit = [np.load("graphics\\heat_implicit_" + str(i) +".npy") for i in n]

for i in n:
	np.linalg.norm(np.absolute(u_analitic[i][-1] - u_explicit[i][-1])
