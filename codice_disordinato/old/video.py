import matplotlib.pyplot as plt
import numpy as np
import os

nframes = 1000

names = os.listdir("graphics")

#for name in names:

 #   print(name)
    
u = np.load("graphics\\" + "heat_explicit_8.npy")

c = 0

for j in (range(len(u)) if len(u) <= nframes else np.linspace(0, len(u)-1, nframes, dtype=int)):
    plt.plot(np.linspace(0,1,len(u[j])),u[j],linewidth=2)
    filename = 'foo' + str(c+1).zfill(5) + '.jpg';
    plt.ylim([0,1])
    plt.xlabel("x")
    plt.ylabel("u")
    plt.title("t = k * %2.2f"%((j+1)))
    plt.savefig("video\\" + filename)
    plt.clf()
    c += 1
    print(j)

filename = "heat_explicit_8_bis.npy"
os.system("ffmpeg\\bin\\ffmpeg -y -i \"video\\foo%05d.jpg\" video\\" + filename + ".m4v")
os.system("del \"video\\*.jpg\"")
